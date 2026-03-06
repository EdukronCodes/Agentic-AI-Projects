from __future__ import annotations

from typing import TypedDict

from langgraph.graph import END, START, StateGraph

from .agents import AGENT_REGISTRY


class AnalysisState(TypedDict):
    prescription_text: str
    analysis: dict[str, str]


def build_analysis_graph() -> StateGraph[AnalysisState, dict, AnalysisState, AnalysisState]:
    """Build a langgraph StateGraph that runs the full suite of agents."""

    builder = StateGraph(AnalysisState)

    def make_node(name: str, agent_cls):
        def node(state: AnalysisState, config: dict) -> dict[str, dict[str, str]]:
            # Each node appends its own analysis result into the shared analysis dict.
            results = dict(state.get("analysis", {}))
            results[name] = agent_cls().run(state["prescription_text"])
            return {"analysis": results}

        node.__name__ = f"agent_{name}"
        return node

    # Add all registered agents as sequential nodes in the graph.
    agent_names = list(AGENT_REGISTRY.keys())
    for agent_name in agent_names:
        builder.add_node(agent_name, make_node(agent_name, AGENT_REGISTRY[agent_name]))

    # Connect the nodes in a simple linear pipeline.
    if agent_names:
        builder.add_edge(START, agent_names[0])
        for src, dst in zip(agent_names, agent_names[1:]):
            builder.add_edge(src, dst)
        builder.add_edge(agent_names[-1], END)
    else:
        builder.add_edge(START, END)

    return builder


def run_full_analysis(prescription_text: str) -> dict:
    """Run all agents over a prescription text and return combined analysis."""

    graph = build_analysis_graph()
    compiled = graph.compile()
    # Initial state must match the typed dict schema
    state: AnalysisState = {"prescription_text": prescription_text, "analysis": {}}
    output = compiled.invoke(state)
    # The output includes the full state; return just the analysis portion.
    return {"analysis": output.get("analysis", {})}
