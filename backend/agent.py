from backend.llm import generate_response
from backend.risk_engine import calculate_risk_score
from backend.tools import compute_allocation,  stress_test

def run_agent(profile):

    logs = []

    # Step 1: Risk
    risk_score = calculate_risk_score(
        profile["age"],
        profile["income"],
        profile["years"],
        profile["loss"]
    )
    logs.append(f"Risk Score calculated: {risk_score}")

    # Step 2: Base Allocation
    allocation = compute_allocation(risk_score)
    logs.append(f"Initial Allocation: {allocation}")
    investment_amount = profile.get("amount", 10000)

    stress_results = stress_test(investment_amount)
    logs.append(f"Stress test results: {stress_results}")

    # Step 3: Critic Logic (Self-Correction)
    if risk_score > 70 and allocation["Stocks"] < 60:
        allocation["Stocks"] += 10
        allocation["Bonds"] -= 5
        allocation["Cash"] -= 5
        logs.append("Critic triggered: Increased stock allocation for high risk.")

    elif risk_score < 40 and allocation["Stocks"] > 40:
        allocation["Stocks"] -= 10
        allocation["Bonds"] += 5
        allocation["Cash"] += 5
        logs.append("Critic triggered: Reduced stock allocation for low risk.")

    else:
        logs.append("Critic approved allocation.")

    # Step 4: LLM Explanation
    prompt = f"""
    Risk score: {risk_score}
    Final allocation: {allocation}

    Explain why this allocation suits the user.
    """

    explanation = generate_response(prompt)

    return {
    "risk_score": risk_score,
    "allocation": allocation,
    "stress_test": stress_results,
    "explanation": explanation,
    "logs": logs
}