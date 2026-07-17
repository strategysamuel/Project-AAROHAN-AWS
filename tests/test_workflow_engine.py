"""
Tests for the Enterprise Lending Workflow Engine.
AAR-BUILD-007 – Workflow Orchestrator
"""
import os
import sys
import threading
import time

import pytest

# Ensure ese-core is on the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../services/ese-core")))

from workflow_engine import (
    WorkflowEngine,
    WorkflowState,
    WorkflowStep,
    WORKFLOW_TEMPLATES,
)


# ============================================================
# Fixtures
# ============================================================

@pytest.fixture
def engine():
    """Return a fresh WorkflowEngine instance (singleton – cleared between tests)."""
    wf = WorkflowEngine()
    # Clear registry between tests
    wf._registry.clear()
    return wf


@pytest.fixture
def msme_workflow(engine):
    """Create a full MSME Lending Journey workflow."""
    return engine.create_workflow("MSME Lending Journey", {"persona": "Priya Textile Works"})


# ============================================================
# 1. Workflow Registration & Template Lookup
# ============================================================

def test_all_templates_registered():
    """All 10 workflow templates must be present."""
    expected = [
        "Customer Onboarding",
        "MSME Lending Journey",
        "Financial Health Assessment",
        "Credit Evaluation",
        "CAM Generation",
        "Fraud Investigation",
        "OCEN Marketplace",
        "Executive Portfolio Review",
        "Training Demo",
        "Board Presentation",
    ]
    for name in expected:
        assert name in WORKFLOW_TEMPLATES, f"Missing template: {name}"


def test_msme_journey_has_11_steps():
    steps = WORKFLOW_TEMPLATES["MSME Lending Journey"]
    assert len(steps) == 11, f"Expected 11 steps, got {len(steps)}"


def test_invalid_template_raises(engine):
    with pytest.raises(ValueError, match="Unknown workflow template"):
        engine.create_workflow("NonExistentWorkflow")


# ============================================================
# 2. Workflow Instance Creation
# ============================================================

def test_create_workflow(engine):
    wf = engine.create_workflow("Customer Onboarding", {"persona": "TestUser"})
    assert wf.state == WorkflowState.PENDING
    assert wf.template_name == "Customer Onboarding"
    assert wf.context["persona"] == "TestUser"
    assert wf.workflow_id.startswith("wf_")


def test_registry_stores_workflow(engine):
    wf = engine.create_workflow("MSME Lending Journey")
    retrieved = engine.get_workflow(wf.workflow_id)
    assert retrieved is not None
    assert retrieved.workflow_id == wf.workflow_id


# ============================================================
# 3. Synchronous Workflow Execution
# ============================================================

def test_full_execution_completes(msme_workflow, engine):
    result = engine.start(msme_workflow.workflow_id, async_exec=False)
    assert result["state"] == WorkflowState.COMPLETED.value
    assert len(result["completed_steps"]) == 11


def test_execution_publishes_events(msme_workflow, engine):
    engine.start(msme_workflow.workflow_id, async_exec=False)
    events = msme_workflow.business_events_published
    event_types = [e["event_type"] for e in events]
    # Spot-check key events
    assert "Customer Registered" in event_types
    assert "Financial Health Updated" in event_types
    assert "CAM Generated" in event_types


def test_timeline_populated(msme_workflow, engine):
    engine.start(msme_workflow.workflow_id, async_exec=False)
    assert len(msme_workflow.timeline) >= 11


def test_audit_log_populated(msme_workflow, engine):
    engine.start(msme_workflow.workflow_id, async_exec=False)
    assert len(msme_workflow.audit_log) >= 11


def test_duration_recorded(msme_workflow, engine):
    result = engine.start(msme_workflow.workflow_id, async_exec=False)
    assert result["duration_ms"] > 0


# ============================================================
# 4. State Transitions
# ============================================================

def test_state_transitions_pending_to_completed(engine):
    wf = engine.create_workflow("Customer Onboarding")
    assert wf.state == WorkflowState.PENDING
    engine.start(wf.workflow_id)
    assert wf.state == WorkflowState.COMPLETED


def test_failed_step_marks_workflow_failed(engine):
    """A step that always raises should cause FAILED state."""
    def bad_handler(ctx):
        raise RuntimeError("Simulated permanent failure")

    bad_step = WorkflowStep(
        name="Bad Step",
        description="Always fails",
        handler=bad_handler,
        max_retries=0,
    )
    WORKFLOW_TEMPLATES["_test_bad"] = [bad_step]
    wf = engine.create_workflow("_test_bad")
    engine.start(wf.workflow_id)
    assert wf.state == WorkflowState.FAILED
    del WORKFLOW_TEMPLATES["_test_bad"]


# ============================================================
# 5. Retry Logic
# ============================================================

def test_retry_succeeds_on_second_attempt(engine):
    attempt_counts = {"count": 0}

    def flaky_handler(ctx):
        attempt_counts["count"] += 1
        if attempt_counts["count"] < 2:
            raise RuntimeError("Transient error – will succeed on retry")
        return {"recovered": True}

    retry_step = WorkflowStep(
        name="Flaky Step",
        description="Fails once, then succeeds",
        handler=flaky_handler,
        max_retries=2,
    )
    WORKFLOW_TEMPLATES["_test_retry"] = [retry_step]
    wf = engine.create_workflow("_test_retry")
    result = engine.start(wf.workflow_id)
    assert result["state"] == WorkflowState.COMPLETED.value
    assert attempt_counts["count"] == 2
    del WORKFLOW_TEMPLATES["_test_retry"]


# ============================================================
# 6. Cancel
# ============================================================

def test_cancel_stops_execution(engine):
    """Start a long workflow asynchronously and cancel it."""
    def slow_handler(ctx):
        time.sleep(2)
        return {}

    # Build a multi-step slow template
    WORKFLOW_TEMPLATES["_test_cancel"] = [
        WorkflowStep(f"Slow-{i}", "Slow step", slow_handler, max_retries=0)
        for i in range(5)
    ]
    wf = engine.create_workflow("_test_cancel")
    engine.start(wf.workflow_id, async_exec=True)
    time.sleep(0.1)           # let the first step start
    engine.cancel(wf.workflow_id)
    time.sleep(3)             # allow cancellation to propagate
    assert wf.state in (WorkflowState.CANCELLED, WorkflowState.COMPLETED)
    del WORKFLOW_TEMPLATES["_test_cancel"]


# ============================================================
# 7. Replay
# ============================================================

def test_replay_workflow(engine):
    wf = engine.create_workflow("Board Presentation")
    engine.start(wf.workflow_id)
    first_run_count = len(wf.completed_steps)
    result = engine.replay(wf.workflow_id)
    assert result["state"] == WorkflowState.COMPLETED.value
    # Timeline resets on replay
    assert len(wf.timeline) > 0


# ============================================================
# 8. Clone
# ============================================================

def test_clone_workflow(engine):
    wf = engine.create_workflow("Financial Health Assessment", {"persona": "Clone Source"})
    clone = engine.clone(wf.workflow_id)
    assert clone.workflow_id != wf.workflow_id
    assert clone.template_name == wf.template_name
    assert clone.context["persona"] == "Clone Source"


# ============================================================
# 9. Export History
# ============================================================

def test_export_history(engine):
    wf = engine.create_workflow("Credit Evaluation")
    engine.start(wf.workflow_id)
    export = engine.export_history(wf.workflow_id)
    assert "audit_log" in export
    assert "timeline" in export
    assert export["template_name"] == "Credit Evaluation"


# ============================================================
# 10. Concurrent Multi-Workflow Execution
# ============================================================

def test_concurrent_workflows_complete(engine):
    """Spawn 5 concurrent workflows and verify all complete."""
    names = [
        "Customer Onboarding",
        "Financial Health Assessment",
        "Credit Evaluation",
        "CAM Generation",
        "Board Presentation",
    ]
    instances = [engine.create_workflow(n) for n in names]

    threads = [
        threading.Thread(
            target=engine.start,
            args=(wf.workflow_id,),
            kwargs={"async_exec": False},
            daemon=True,
        )
        for wf in instances
    ]

    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=30)

    for wf in instances:
        assert wf.state == WorkflowState.COMPLETED, (
            f"Workflow '{wf.template_name}' ended in state {wf.state}"
        )
