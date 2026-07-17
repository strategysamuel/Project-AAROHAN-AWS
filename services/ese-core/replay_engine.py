import time
import json
import uuid
from typing import Dict, Any, List

class ExecutiveReplayEngine:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ExecutiveReplayEngine, cls).__new__(cls, *args, **kwargs)
            cls._instance.recordings: Dict[str, Dict[str, Any]] = {}
            cls._instance.active_recording_id = None
        return cls._instance

    def start_recording(self, journey_name: str) -> str:
        recording_id = f"rec_{uuid.uuid4().hex[:12]}"
        self.active_recording_id = recording_id
        self.recordings[recording_id] = {
            "recording_id": recording_id,
            "journey_name": journey_name,
            "recorded_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "steps": [],
            "events_captured": [],
            "portfolio_snapshots": []
        }
        return recording_id

    def log_step(self, step_name: str, details: Dict[str, Any]):
        if not self.active_recording_id:
            return
        recording = self.recordings[self.active_recording_id]
        recording["steps"].append({
            "step_name": step_name,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "details": details
        })

    def log_event(self, event_type: str, payload: Dict[str, Any]):
        if not self.active_recording_id:
            return
        recording = self.recordings[self.active_recording_id]
        recording["events_captured"].append({
            "event_type": event_type,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "payload": payload
        })

    def capture_portfolio_snapshot(self, snapshot: Dict[str, Any]):
        if not self.active_recording_id:
            return
        recording = self.recordings[self.active_recording_id]
        recording["portfolio_snapshots"].append({
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "snapshot": snapshot
        })

    def stop_recording(self) -> Dict[str, Any]:
        rec_id = self.active_recording_id
        self.active_recording_id = None
        if rec_id and rec_id in self.recordings:
            return self.recordings[rec_id]
        return {}

    def get_recording(self, recording_id: str) -> Dict[str, Any]:
        return self.recordings.get(recording_id, {})

    def list_recordings(self) -> List[Dict[str, Any]]:
        return [
            {
                "recording_id": r["recording_id"],
                "journey_name": r["journey_name"],
                "recorded_at": r["recorded_at"],
                "steps_count": len(r["steps"]),
                "events_count": len(r["events_captured"])
            }
            for r in self.recordings.values()
        ]

    def export_summary(self, recording_id: str) -> str:
        rec = self.get_recording(recording_id)
        if not rec:
            return "No recording found."
        
        summary = (
            f"=== EXECUTIVE JOURNEY REPLAY SUMMARY ===\n"
            f"Recording ID: {rec['recording_id']}\n"
            f"Journey Name: {rec['journey_name']}\n"
            f"Recorded At: {rec['recorded_at']}\n"
            f"Steps Executed: {len(rec['steps'])}\n"
            f"Events Dispatched: {len(rec['events_captured'])}\n"
            f"Portfolio Snapshots: {len(rec['portfolio_snapshots'])}\n"
            f"========================================\n"
        )
        return summary
