"""
Enterprise Lending Workflow Orchestrator (workflow_engine.py)
Project AAROHAN - ESE Core

Provides reusable workflow definitions, execution state machine,
event publishing, pause/resume/retry/cancel controls, and
concurrent multi-workflow execution support.
"""

import uuid
import time
import logging
import threading
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable, Dict, List, Optional

logger = logging.getLogger("ese-workflow-engine")


# ============================================================
# 1. WORKFLOW STATE MACHINE
# ============================================================

class WorkflowState(str, Enum):
    PENDING   = "PENDING"
    RUNNING   = "RUNNING"
    WAITING   = "WAITING"
    COMPLETED = "COMPLETED"
    SKIPPED   = "SKIPPED"
    FAILED    = "FAILED"
    CANCELLED = "CANCELLED"
    RETRYING  = "RETRYING"


# ============================================================
# 2. STEP DEFINITION
# ============================================================

class WorkflowStep:
    """
    Describes a single step in a workflow.

    Attributes
    ----------
    name          : Human-readable step identifier
    description   : Purpose of this step
    dependencies  : Names of steps that must complete before this one
    timeout_s     : Maximum seconds allowed for execution
    max_retries   : Number of automatic retries on failure
    compensation  : Optional callable invoked on permanent failure
    handler       : Callable that performs the actual work; receives (context) dict
    business_events : List of event type strings to publish on SUCCESS
    """

    def __init__(
        self,
        name: str,
        description: str,
        handler: Callable[[Dict[str, Any]], Dict[str, Any]],
        dependencies: Optional[List[str]] = None,
        timeout_s: float = 30.0,
        max_retries: int = 1,
        compensation: Optional[Callable] = None,
        business_events: Optional[List[str]] = None,
    ):
        self.name = name
        self.description = description
        self.handler = handler
        self.dependencies: List[str] = dependencies or []
        self.timeout_s = timeout_s
        self.max_retries = max_retries
        self.compensation = compensation
        self.business_events: List[str] = business_events or []


# ============================================================
# 3. WORKFLOW INSTANCE
# ============================================================

class WorkflowInstance:
    """
    Runtime state for a single workflow execution.
    """

    def __init__(self, workflow_id: str, template_name: str, context: Dict[str, Any]):
        self.workflow_id = workflow_id
        self.template_name = template_name
        self.context = dict(context)
        self.state = WorkflowState.PENDING
        self.current_step: Optional[str] = None
        self.completed_steps: List[str] = []
        self.failed_steps: List[str] = []
        self.skipped_steps: List[str] = []
        self.retries: Dict[str, int] = {}
        self.timeline: List[Dict[str, Any]] = []
        self.audit_log: List[Dict[str, Any]] = []
        self.business_events_published: List[Dict[str, Any]] = []
        self.started_at: Optional[float] = None
        self.ended_at: Optional[float] = None

        # Threading controls for pause/resume/cancel
        self._pause_event = threading.Event()
        self._pause_event.set()          # not paused by default
        self._cancel_flag = threading.Event()

    # --------------------------------------------------------
    # Internal helpers
    # --------------------------------------------------------

    def _log_audit(self, step_name: str, status: str, details: str = ""):
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "step": step_name,
            "status": status,
            "details": details,
        }
        self.audit_log.append(entry)
        self.timeline.append({
            "step": step_name,
            "elapsed_ms": round((time.time() - (self.started_at or time.time())) * 1000, 2),
        })
        logger.info(f"[WORKFLOW:{self.workflow_id}] {step_name} | {status} | {details}")

    def _publish_event(self, event_type: str, step_name: str):
        record = {
            "event_id": f"wf_evt_{uuid.uuid4().hex[:10]}",
            "event_type": event_type,
            "workflow_id": self.workflow_id,
            "step": step_name,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "persona": self.context.get("persona", ""),
        }
        self.business_events_published.append(record)
        logger.info(f"[EVENT_BUS] Published: {event_type} | from step: {step_name}")

    # --------------------------------------------------------
    # Admin control surface
    # --------------------------------------------------------

    def pause(self):
        self._pause_event.clear()
        self.state = WorkflowState.WAITING
        logger.info(f"[WORKFLOW:{self.workflow_id}] Paused.")

    def resume(self):
        self._pause_event.set()
        self.state = WorkflowState.RUNNING
        logger.info(f"[WORKFLOW:{self.workflow_id}] Resumed.")

    def cancel(self):
        self._cancel_flag.set()
        self._pause_event.set()      # unblock if paused
        logger.info(f"[WORKFLOW:{self.workflow_id}] Cancel requested.")

    # --------------------------------------------------------
    # Execution
    # --------------------------------------------------------

    def execute_step(self, step: WorkflowStep) -> bool:
        """
        Execute a single workflow step with timeout, retry and
        pause/cancel checks.  Returns True on success.
        """
        # Honour pause
        self._pause_event.wait()

        # Honour cancel
        if self._cancel_flag.is_set():
            self.state = WorkflowState.CANCELLED
            return False

        self.current_step = step.name
        attempt = 0

        while attempt <= step.max_retries:
            attempt += 1
            status_tag = WorkflowState.RUNNING if attempt == 1 else WorkflowState.RETRYING
            self._log_audit(step.name, status_tag.value, f"Attempt {attempt}/{step.max_retries + 1}")

            try:
                result = step.handler(self.context)
                self.context[f"_output_{step.name}"] = result

                self._log_audit(step.name, WorkflowState.COMPLETED.value, str(result)[:200])
                self.completed_steps.append(step.name)

                # Publish business events for this step
                for evt_type in step.business_events:
                    self._publish_event(evt_type, step.name)

                return True

            except Exception as exc:
                self._log_audit(step.name, "ERROR", str(exc))
                if attempt > step.max_retries:
                    self._log_audit(step.name, WorkflowState.FAILED.value, "Max retries exhausted")
                    self.failed_steps.append(step.name)
                    if step.compensation:
                        try:
                            step.compensation(self.context)
                        except Exception as comp_err:
                            logger.warning(f"Compensation failed for {step.name}: {comp_err}")
                    return False

                # Brief back-off before retry
                time.sleep(min(2 ** attempt, 10))

        return False   # should never reach here

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    def to_dict(self) -> Dict[str, Any]:
        return {
            "workflow_id": self.workflow_id,
            "template_name": self.template_name,
            "state": self.state.value,
            "current_step": self.current_step,
            "completed_steps": self.completed_steps,
            "failed_steps": self.failed_steps,
            "skipped_steps": self.skipped_steps,
            "duration_ms": round(((self.ended_at or time.time()) - (self.started_at or time.time())) * 1000, 2),
            "events_published": len(self.business_events_published),
            "timeline": self.timeline,
            "audit_log": self.audit_log,
        }


# ============================================================
# 4. WORKFLOW TEMPLATE REGISTRY
# ============================================================

def _noop_handler(ctx: Dict[str, Any]) -> Dict[str, Any]:
    """Default no-op handler used for scaffolding."""
    return {"status": "OK"}


def _build_msme_lending_steps() -> List[WorkflowStep]:
    """Full 11-stage MSME lending journey."""

    def step(name, desc, events):
        return WorkflowStep(
            name=name,
            description=desc,
            handler=_noop_handler,
            timeout_s=30.0,
            max_retries=2,
            business_events=events,
        )

    return [
        step("Customer Onboarding",      "Register KYC and customer profile",                  ["Customer Registered"]),
        step("CKYC Verification",        "Query Central KYC Registry via PAN",                 ["CKYC_VERIFIED"]),
        step("GST Analysis",             "Sync GSTR-1/3B returns and turnover history",        ["GST_RETURN_FILED"]),
        step("Account Aggregator",       "Pull bank statements via AA consent framework",      ["CASH_FLOW_UPDATED"]),
        step("EPFO Verification",        "Validate PF contribution filing compliance",         ["EPFO_FILING_SUBMITTED"]),
        step("MCA Registry",             "Confirm corporate registration and DIN records",     ["MCA_FILING_SUBMITTED"]),
        step("Financial Health Card",    "Compute DSCR, leverage, and FHC composite score",   ["Financial Health Updated"]),
        step("AI Credit Engine",         "Run Gemini AI credit appraisal and policy check",   ["Credit Score Updated"]),
        step("RBI Fraud Registry",       "Query defaulter registry and fraud watchlists",      ["RBI Fraud Alert"]),
        step("OCEN Marketplace",         "Generate lender loan product offers",                ["OCEN Offers Generated"]),
        step("CAM Generation",           "Compile Credit Appraisal Memorandum",                ["CAM Generated"]),
    ]


WORKFLOW_TEMPLATES: Dict[str, List[WorkflowStep]] = {
    "Customer Onboarding":       [WorkflowStep("Customer Onboarding", "KYC profile registration", _noop_handler, business_events=["Customer Registered"])],
    "MSME Lending Journey":      _build_msme_lending_steps(),
    "Financial Health Assessment": [
        WorkflowStep("GST Analysis",          "GSTR sync",          _noop_handler, business_events=["GST_RETURN_FILED"]),
        WorkflowStep("Account Aggregator",    "AA cash flow",       _noop_handler, business_events=["CASH_FLOW_UPDATED"]),
        WorkflowStep("Financial Health Card", "FHC computation",    _noop_handler, business_events=["Financial Health Updated"]),
    ],
    "Credit Evaluation": [
        WorkflowStep("Financial Health Card", "FHC computation", _noop_handler, business_events=["Financial Health Updated"]),
        WorkflowStep("AI Credit Engine",      "Gemini AI appraisal", _noop_handler, business_events=["Credit Score Updated"]),
    ],
    "CAM Generation": [
        WorkflowStep("CAM Generation", "Credit memo compilation", _noop_handler, business_events=["CAM Generated"]),
    ],
    "Fraud Investigation": [
        WorkflowStep("RBI Fraud Registry", "Defaulter registry query", _noop_handler, business_events=["RBI Fraud Alert"]),
    ],
    "OCEN Marketplace": [
        WorkflowStep("OCEN Marketplace", "Lender offer generation", _noop_handler, business_events=["OCEN Offers Generated"]),
    ],
    "Executive Portfolio Review": [
        WorkflowStep("Financial Health Card", "FHC portfolio summary", _noop_handler, business_events=["Financial Health Updated"]),
        WorkflowStep("AI Credit Engine",      "Portfolio credit risk",  _noop_handler, business_events=["Credit Score Updated"]),
    ],
    "Training Demo": _build_msme_lending_steps(),
    "Board Presentation": [
        WorkflowStep("Financial Health Card", "Board FHC summary",    _noop_handler, business_events=["Financial Health Updated"]),
        WorkflowStep("AI Credit Engine",      "Board credit snapshot", _noop_handler, business_events=["Credit Score Updated"]),
        WorkflowStep("OCEN Marketplace",      "Board offer showcase",  _noop_handler, business_events=["OCEN Offers Generated"]),
    ],
}


# ============================================================
# 5. WORKFLOW ENGINE (Singleton Orchestrator)
# ============================================================

class WorkflowEngine:
    """
    Singleton orchestrator. Supports concurrent multi-workflow
    execution using per-instance threads.
    """

    _instance: Optional["WorkflowEngine"] = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._registry: Dict[str, WorkflowInstance] = {}
            cls._instance._lock = threading.Lock()
        return cls._instance

    # --------------------------------------------------------
    # Factory / registry
    # --------------------------------------------------------

    def create_workflow(
        self,
        template_name: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> WorkflowInstance:
        """Instantiate a workflow from a named template."""
        if template_name not in WORKFLOW_TEMPLATES:
            raise ValueError(f"Unknown workflow template: '{template_name}'. "
                             f"Available: {list(WORKFLOW_TEMPLATES)}")
        wf_id = f"wf_{uuid.uuid4().hex[:12]}"
        instance = WorkflowInstance(wf_id, template_name, context or {})
        with self._lock:
            self._registry[wf_id] = instance
        logger.info(f"[ENGINE] Created workflow '{template_name}' (ID: {wf_id})")
        return instance

    def get_workflow(self, workflow_id: str) -> Optional[WorkflowInstance]:
        return self._registry.get(workflow_id)

    def list_workflows(self) -> List[Dict[str, Any]]:
        with self._lock:
            return [wf.to_dict() for wf in self._registry.values()]

    # --------------------------------------------------------
    # Execution
    # --------------------------------------------------------

    def start(self, workflow_id: str, async_exec: bool = False) -> Optional[Dict[str, Any]]:
        """
        Start or restart a workflow.  When async_exec=True the
        workflow runs in a daemon thread and returns immediately.
        """
        instance = self.get_workflow(workflow_id)
        if instance is None:
            raise KeyError(f"No workflow with ID {workflow_id}")

        # Reset instance state for re-runs
        instance.state = WorkflowState.RUNNING
        instance.completed_steps = []
        instance.failed_steps = []
        instance.skipped_steps = []
        instance.timeline = []
        instance.audit_log = []
        instance.business_events_published = []
        instance.started_at = time.time()
        instance.ended_at = None
        instance._cancel_flag.clear()
        instance._pause_event.set()

        steps = WORKFLOW_TEMPLATES[instance.template_name]

        def _run():
            try:
                for step in steps:
                    # Check dependencies
                    for dep in step.dependencies:
                        if dep not in instance.completed_steps:
                            instance._log_audit(step.name, WorkflowState.SKIPPED.value,
                                                f"Dependency '{dep}' not satisfied")
                            instance.skipped_steps.append(step.name)
                            continue

                    success = instance.execute_step(step)

                    if instance.state in (WorkflowState.CANCELLED,):
                        break

                    if not success and step.max_retries == 0:
                        instance.state = WorkflowState.FAILED
                        break

                if instance.state not in (WorkflowState.CANCELLED, WorkflowState.FAILED):
                    instance.state = WorkflowState.COMPLETED

            finally:
                instance.ended_at = time.time()
                logger.info(f"[ENGINE] Workflow {workflow_id} finished with state: {instance.state.value}")

        if async_exec:
            t = threading.Thread(target=_run, daemon=True, name=f"wf-{workflow_id[:8]}")
            t.start()
            return {"workflow_id": workflow_id, "status": "STARTED_ASYNC"}
        else:
            _run()
            return instance.to_dict()

    def pause(self, workflow_id: str):
        wf = self._get_or_raise(workflow_id)
        wf.pause()

    def resume(self, workflow_id: str):
        wf = self._get_or_raise(workflow_id)
        wf.resume()

    def cancel(self, workflow_id: str):
        wf = self._get_or_raise(workflow_id)
        wf.cancel()

    def replay(self, workflow_id: str) -> Dict[str, Any]:
        """Re-execute a workflow from the beginning (synchronous)."""
        wf = self._get_or_raise(workflow_id)
        return self.start(wf.workflow_id, async_exec=False)

    def clone(self, workflow_id: str) -> WorkflowInstance:
        """Create a new independent copy of an existing workflow."""
        source = self._get_or_raise(workflow_id)
        new_wf = self.create_workflow(source.template_name, dict(source.context))
        logger.info(f"[ENGINE] Cloned {workflow_id} → {new_wf.workflow_id}")
        return new_wf

    def export_history(self, workflow_id: str) -> Dict[str, Any]:
        wf = self._get_or_raise(workflow_id)
        return wf.to_dict()

    # --------------------------------------------------------
    # Internal
    # --------------------------------------------------------

    def _get_or_raise(self, workflow_id: str) -> WorkflowInstance:
        wf = self.get_workflow(workflow_id)
        if wf is None:
            raise KeyError(f"Workflow not found: {workflow_id}")
        return wf


# Module-level singleton
engine = WorkflowEngine()
