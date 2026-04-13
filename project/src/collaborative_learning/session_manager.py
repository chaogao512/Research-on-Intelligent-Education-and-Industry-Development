"""
session_manager.py
==================
Manages human-computer collaborative learning (HCCL) sessions.

A session consists of alternating turns between the human learner and the AI agent.
The session manager:
  - Tracks session state (active concepts, turn history, learner contributions)
  - Coordinates with the knowledge graph to ground AI responses in domain knowledge
  - Coordinates with the recommender to suggest next learning steps
  - Persists session logs for later analysis

Design notes:
  - The AI agent role is deliberately kept modular: swap out the backend (GPT-4,
    local Qwen, mock) by changing the ``ai_backend`` parameter.
  - Session state is serializable to JSON for export and research analysis.
"""

from __future__ import annotations

import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any

import networkx as nx
from rich.console import Console
from rich.markdown import Markdown

console = Console()


class TurnRole(str, Enum):
    """Identifies who produced a given dialogue turn."""

    HUMAN = "human"
    AI = "ai"
    SYSTEM = "system"


@dataclass
class DialogueTurn:
    """A single turn in the HCCL session dialogue.

    Attributes:
        role: Who produced this turn (human, ai, or system).
        content: The text content of the turn.
        timestamp: ISO 8601 UTC timestamp when the turn was produced.
        concepts_referenced: Knowledge graph concept IDs referenced in this turn.
        turn_index: Sequential index of this turn in the session.
    """

    role: TurnRole
    content: str
    timestamp: str
    concepts_referenced: list[str] = field(default_factory=list)
    turn_index: int = 0

    def to_dict(self) -> dict[str, Any]:
        """Serialize the turn to a JSON-compatible dictionary."""
        return {
            "role": self.role.value,
            "content": self.content,
            "timestamp": self.timestamp,
            "concepts_referenced": self.concepts_referenced,
            "turn_index": self.turn_index,
        }


@dataclass
class SessionState:
    """Tracks the full state of an HCCL session.

    Attributes:
        session_id: Unique identifier for the session.
        learner_id: Identifier of the human learner.
        start_time: ISO 8601 UTC start timestamp.
        turns: Ordered list of dialogue turns.
        active_concepts: Set of concept IDs currently in focus.
        is_active: Whether the session is currently running.
    """

    session_id: str
    learner_id: str
    start_time: str
    turns: list[DialogueTurn] = field(default_factory=list)
    active_concepts: set[str] = field(default_factory=set)
    is_active: bool = True
    end_time: str | None = None

    def add_turn(self, role: TurnRole, content: str, concepts: list[str] | None = None) -> DialogueTurn:
        """Add a new dialogue turn to the session.

        Args:
            role: Who is producing the turn.
            content: Text content of the turn.
            concepts: Optional list of concept IDs referenced.

        Returns:
            The newly created DialogueTurn.
        """
        turn = DialogueTurn(
            role=role,
            content=content,
            timestamp=datetime.now(timezone.utc).isoformat(),
            concepts_referenced=concepts or [],
            turn_index=len(self.turns),
        )
        self.turns.append(turn)
        if concepts:
            self.active_concepts.update(concepts)
        return turn

    def to_dict(self) -> dict[str, Any]:
        """Serialize the full session state to a JSON-compatible dictionary."""
        return {
            "session_id": self.session_id,
            "learner_id": self.learner_id,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "is_active": self.is_active,
            "turn_count": len(self.turns),
            "active_concepts": sorted(self.active_concepts),
            "turns": [t.to_dict() for t in self.turns],
        }

    def export_markdown(self) -> str:
        """Export the session as a human-readable Markdown document.

        Returns:
            A formatted Markdown string representing the session transcript.
        """
        lines = [
            f"# HCCL Session Transcript",
            f"",
            f"| Field | Value |",
            f"|-------|-------|",
            f"| Session ID | `{self.session_id}` |",
            f"| Learner ID | `{self.learner_id}` |",
            f"| Start time | {self.start_time} |",
            f"| End time | {self.end_time or '(active)'} |",
            f"| Total turns | {len(self.turns)} |",
            f"",
            f"---",
            f"",
            f"## Dialogue",
            f"",
        ]
        for turn in self.turns:
            role_label = {
                TurnRole.HUMAN: "👤 **Learner**",
                TurnRole.AI: "🤖 **AI Agent**",
                TurnRole.SYSTEM: "⚙️ **System**",
            }.get(turn.role, turn.role.value)
            lines += [
                f"### {role_label} — Turn {turn.turn_index + 1}",
                f"_{turn.timestamp}_",
                f"",
                turn.content,
                f"",
            ]
            if turn.concepts_referenced:
                lines.append(f"_Concepts: {', '.join(f'`{c}`' for c in turn.concepts_referenced)}_")
                lines.append(f"")
        return "\n".join(lines)


class SessionManager:
    """Manages the full lifecycle of a human-computer collaborative learning session.

    Coordinates the learner input, AI response generation, knowledge graph grounding,
    and adaptive recommendations.

    Args:
        learner_id: Unique identifier of the human learner.
        knowledge_graph: A NetworkX DiGraph representing the domain knowledge.
        recommender: A Recommender instance for generating learning suggestions.
        max_turns: Maximum number of human turns before the session ends.
        ai_backend: Backend function that takes a prompt string and returns AI response string.
                    Defaults to a simple mock backend for testing.
    """

    def __init__(
        self,
        learner_id: str,
        knowledge_graph: nx.DiGraph,
        recommender: Any,
        max_turns: int = 10,
        ai_backend: Any | None = None,
    ) -> None:
        self.learner_id = learner_id
        self.knowledge_graph = knowledge_graph
        self.recommender = recommender
        self.max_turns = max_turns
        self._ai_backend = ai_backend or self._mock_ai_response

        self.state = SessionState(
            session_id=str(uuid.uuid4()),
            learner_id=learner_id,
            start_time=datetime.now(timezone.utc).isoformat(),
        )

    def _mock_ai_response(self, prompt: str) -> str:
        """Mock AI response for development and testing.

        Args:
            prompt: The conversation prompt sent to the AI.

        Returns:
            A placeholder response string.
        """
        return (
            "That's a thoughtful observation. In the context of human-computer collaborative "
            "learning, we might consider how the knowledge representation in this domain "
            "connects to your prior understanding. What specific aspect would you like to "
            "explore further together?"
        )

    def _generate_ai_response(self, human_turn: DialogueTurn) -> str:
        """Generate an AI response given the latest human turn.

        Builds a context-aware prompt using the session history and knowledge graph,
        then calls the AI backend.

        Args:
            human_turn: The most recent human dialogue turn.

        Returns:
            The AI-generated response string.
        """
        # Build a compact context from recent turns (last 6)
        recent_turns = self.state.turns[-6:]
        context_lines = []
        for t in recent_turns:
            role_label = "Learner" if t.role == TurnRole.HUMAN else "AI"
            context_lines.append(f"{role_label}: {t.content}")

        # Get relevant concepts from the knowledge graph
        relevant_concepts = self._get_relevant_concepts(human_turn.content)
        concept_descriptions = []
        for concept_id in relevant_concepts[:3]:
            if self.knowledge_graph.has_node(concept_id):
                desc = self.knowledge_graph.nodes[concept_id].get("description", "")
                if desc:
                    concept_descriptions.append(f"- {concept_id}: {desc}")

        prompt_parts = [
            "You are an AI collaborative learning partner supporting a graduate student in "
            "intelligent education research at a Chinese university.",
            "",
            "Domain context:",
            *concept_descriptions,
            "",
            "Recent conversation:",
            *context_lines,
            "",
            "As the AI learning partner, provide a thoughtful, Socratic-style collaborative "
            "response that helps the learner deepen their understanding. Ask follow-up "
            "questions, offer alternative perspectives, and connect ideas to the knowledge domain.",
        ]

        return self._ai_backend("\n".join(prompt_parts))

    def _get_relevant_concepts(self, text: str) -> list[str]:
        """Find knowledge graph concepts mentioned in the given text.

        Args:
            text: The text to search for concept mentions.

        Returns:
            List of concept node IDs found in the text.
        """
        text_lower = text.lower()
        found = []
        for node_id in self.knowledge_graph.nodes:
            label = self.knowledge_graph.nodes[node_id].get("label", node_id).lower()
            if label in text_lower or node_id.lower() in text_lower:
                found.append(node_id)
        return found

    def process_human_turn(self, human_input: str) -> DialogueTurn:
        """Process a human learner's input turn.

        Args:
            human_input: The text input from the human learner.

        Returns:
            The recorded human DialogueTurn.
        """
        concepts = self._get_relevant_concepts(human_input)
        return self.state.add_turn(TurnRole.HUMAN, human_input, concepts)

    def generate_response(self, human_turn: DialogueTurn) -> DialogueTurn:
        """Generate and record an AI response to a human turn.

        Args:
            human_turn: The human turn to respond to.

        Returns:
            The AI DialogueTurn with the generated response.
        """
        ai_response = self._generate_ai_response(human_turn)
        concepts = self._get_relevant_concepts(ai_response)
        return self.state.add_turn(TurnRole.AI, ai_response, concepts)

    def end_session(self) -> None:
        """Mark the session as ended and record the end timestamp."""
        self.state.is_active = False
        self.state.end_time = datetime.now(timezone.utc).isoformat()
        self.state.add_turn(
            TurnRole.SYSTEM,
            f"Session ended. Total turns: {len(self.state.turns) - 1}. "
            f"Concepts explored: {len(self.state.active_concepts)}.",
        )

    def export_session(self, output_path: str | None = None) -> str:
        """Export the session to a JSON file and return the Markdown transcript.

        Args:
            output_path: Optional path to save the JSON session log.

        Returns:
            The Markdown transcript of the session.
        """
        if output_path:
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(self.state.to_dict(), f, indent=2, ensure_ascii=False)

        return self.state.export_markdown()

    def run_interactive(self) -> None:
        """Run an interactive CLI session, reading input from stdin.

        Loops until the learner types 'exit', 'quit', or the max turns are reached.
        """
        human_turn_count = 0

        # Opening system message
        self.state.add_turn(
            TurnRole.SYSTEM,
            f"Session started. Learner: {self.learner_id}. Max turns: {self.max_turns}.",
        )

        # Initial AI greeting
        opening = (
            "Welcome to this collaborative learning session! I'm here as your AI learning "
            "partner. Together we'll explore the domain of intelligent education and "
            "human-computer collaborative learning. What topic or question would you like to "
            "start with today?"
        )
        ai_open_turn = self.state.add_turn(TurnRole.AI, opening)
        console.print(f"\n[bold cyan]🤖 AI Agent[/bold cyan]: {opening}\n")

        while self.state.is_active and human_turn_count < self.max_turns:
            try:
                user_input = console.input(
                    f"[bold green]👤 You[/bold green] (turn {human_turn_count + 1}/{self.max_turns}): "
                ).strip()
            except (EOFError, KeyboardInterrupt):
                console.print("\n[yellow]Session interrupted.[/yellow]")
                break

            if not user_input:
                console.print("[dim]Please enter a message.[/dim]")
                continue

            if user_input.lower() in {"exit", "quit", "bye"}:
                console.print("[yellow]Ending session...[/yellow]")
                break

            human_turn = self.process_human_turn(user_input)
            human_turn_count += 1

            # Get recommendations if applicable
            recs = self.recommender.get_recommendations(
                learner_id=self.learner_id, top_k=2
            )

            ai_turn = self.generate_response(human_turn)
            console.print(f"\n[bold cyan]🤖 AI Agent[/bold cyan]: {ai_turn.content}\n")

            if recs:
                console.print(
                    f"[dim]💡 Suggested next concepts: {', '.join(recs)}[/dim]\n"
                )

        self.end_session()
        markdown_export = self.export_session()
        console.print("\n[bold green]Session complete![/bold green]")
        console.print(
            f"[dim]Session ID: {self.state.session_id} | "
            f"Turns: {human_turn_count} | "
            f"Concepts explored: {len(self.state.active_concepts)}[/dim]\n"
        )
