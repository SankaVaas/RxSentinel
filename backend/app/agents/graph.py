"""LangGraph state machine wiring together all agent nodes.

    patient_context_agent
            |
            v
    retrieval_agent
            |
            v
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
"""
from langgraph.graph import END, StateGraph
from sqlalchemy.ext.asyncio import AsyncSession

from app.agents import nodes
from app.agents.state import AgentState


def build_graph(db: AsyncSession):
    graph = StateGraph(AgentState)

    async def _patient_context_node(state: AgentState) -> dict:
        return await nodes.patient_context_agent.run(state, db)

    async def _interaction_tool_node(state: AgentState) -> dict:
        return await nodes.interaction_tool_agent.run(state, db)

    graph.add_node("patient_context", _patient_context_node)
    graph.add_node("retrieval", nodes.retrieval_agent.run)
    graph.add_node("interaction_tool", _interaction_tool_node)
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