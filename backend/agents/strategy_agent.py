from backend.tools import compute_allocation

def strategy_agent(state):

    allocation = compute_allocation(state["risk_score"])
    state["allocation"] = allocation
    state["logs"].append("Strategy Agent generated allocation.")

    return state