from typing import TypedDict, Dict, Any

class AgentState(TypedDict, total=False):
    profile: Dict[str, Any]
    risk_score: int
    allocation: Dict[str, int]
    stress_test: Dict[str, float]
    explanation: str
    logs: list