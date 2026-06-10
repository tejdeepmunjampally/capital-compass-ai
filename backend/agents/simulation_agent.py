from backend.tools import stress_test

def simulation_agent(state):

    amount = state["profile"].get("amount", 10000)
    stress = stress_test(amount)

    state["stress_test"] = stress
    state["logs"].append("Simulation Agent ran stress scenarios.")

    return state