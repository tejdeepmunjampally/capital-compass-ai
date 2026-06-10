from backend.rag.compliance_rag import build_compliance_rag
from backend.llm import llm

vectordb = build_compliance_rag()


def compliance_agent(state):

    try:
        risk_score = state.get("risk_score")
        allocation = state.get("allocation")
        profile = state.get("profile", {})
        age = profile.get("age")

        if not allocation:
            state["compliance_review"] = "Compliance skipped: No allocation generated."
            state["logs"].append("Compliance skipped (no allocation).")
            return state

        query = f"""
        Risk Score: {risk_score}
        Allocation: {allocation}
        Age: {age}
        """

        docs = vectordb.similarity_search(query, k=3)
        context = "\n".join([doc.page_content for doc in docs])

        prompt = f"""
        You are a financial compliance auditor.

        Regulatory Guidelines:
        {context}

        Portfolio Allocation:
        {allocation}

        Investor Age: {age}
        Risk Score: {risk_score}

        Respond in this exact format:

        STATUS: Compliant or Not Compliant
        REASON: Short explanation
        SUGGESTION: If not compliant, provide corrected allocation.
        """

        response = llm.invoke(prompt)

        state["compliance_review"] = response.content.strip()
        state["logs"].append("Compliance Agent performed regulatory validation.")

        return state

    except Exception as e:
        state["compliance_review"] = "Compliance check failed."
        state["logs"].append(f"Compliance error: {str(e)}")
        return state