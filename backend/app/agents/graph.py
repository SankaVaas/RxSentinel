"""LangGraph state machine wiring together all agent nodes.

    patient_context_agent
            |
            v
    retrieval_agent ----+
            |            | (sequential in this version; see note below)
            v            v
    interaction_tool_agent
            |
            v
    reasoning_agent
            |
            v
    critique_agent
            |
            v
    escalation_agent

NOTE: retrieval_agent and interaction_tool_agent are natural candidates to
run in parallel (both only need patient_context), but are kept sequential
here because interaction_tool_agent currently enriches retrieval_agent's
candidate list in place. Splitting them into independent branches that merge
via the `interaction_candidates` reducer (see state.py) is a clean follow-up
once both are stable independently.
"""
from langgraph.graph import END, StateGraph
from sqlalchemy.ext.asyncio import AsyncSession

from app.agents import nodes
from app.agents.state import AgentState


def build_graph(db: AsyncSession):
    graph = StateGraph(AgentState)

    graph.add_node("patient_context", lambda state: nodes.patient_context_agent.run(state, db))
    graph.add_node("retrieval", nodes.retrieval_agent.run)
    graph.add_node("interaction_tool", nodes.interaction_tool_agent.run)
    graph.add_node("reasoning", nodes.reasoning_agent.run)
    graph.add_node("critique", nodes.critique_agent.run)
    graph.add_node("escalation", nodes.escalation_agent.run)

    graph.set_entry_point("patient_context")
    graph.add_edge("patient_context", "retrieval")
    graph.add_edge("retrieval", "interaction_tool")
    graph.add_edge("interaction_tool", "reasoning")
    graph.add_edge("reasoning", "critique")
    graph.add_edge("critique", "escalation")
    graph.add_edge("escalation", END)

    return graph.compile()
