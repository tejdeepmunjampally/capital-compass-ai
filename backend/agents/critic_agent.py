def critic_agent(state):

    risk = state["risk_score"]
    allocation = state["allocation"]

    if risk > 70 and allocation["Stocks"] < 60:
        allocation["Stocks"] += 10
        allocation["Bonds"] -= 5
        allocation["Cash"] -= 5

        state["allocation"] = allocation
        state["retry"] = True
        state["logs"].append("Critic triggered re-allocation.")

    else:
        state["retry"] = False
        state["logs"].append("Critic approved strategy.")

    return state