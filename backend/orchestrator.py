from backend.agents.profile_agent import profile_agent
from backend.agents.strategy_agent import strategy_agent
from backend.agents.simulation_agent import simulation_agent
from backend.agents.critic_agent import critic_agent
from backend.agents.explanation_agent import explanation_agent

def run_multi_agent(profile):

    state = {
        "profile": profile,
        "logs": []
    }

    state = profile_agent(state)
    state = strategy_agent(state)
    state = simulation_agent(state)
    state = critic_agent(state)
    state = explanation_agent(state)

    return state