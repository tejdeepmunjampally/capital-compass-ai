from langgraph.graph import StateGraph
from .state import AgentState

from .agents.compliance_agent import compliance_agent
from .agents.profile_agent import profile_agent
from .agents.strategy_agent import strategy_agent
from .agents.simulation_agent import simulation_agent
from .agents.critic_agent import critic_agent
from .agents.explanation_agent import explanation_agent


def build_graph():

    graph = StateGraph(AgentState)

    graph.add_node("profile", profile_agent)
    graph.add_node("strategy", strategy_agent)
    graph.add_node("simulation", simulation_agent)
    graph.add_node("compliance", compliance_agent)
    graph.add_node("critic", critic_agent)
    graph.add_node("explanation", explanation_agent)

    graph.set_entry_point("profile")

    graph.add_edge("profile", "strategy")
    graph.add_edge("strategy", "simulation")
    graph.add_edge("simulation", "compliance")
    graph.add_edge("compliance", "critic")

    graph.add_conditional_edges(
        "critic",
        lambda state: "strategy" if state.get("retry") else "explanation",
        {
            "strategy": "strategy",
            "explanation": "explanation"
        }
    )

    graph.add_edge("explanation", "__end__")

    return graph.compile()