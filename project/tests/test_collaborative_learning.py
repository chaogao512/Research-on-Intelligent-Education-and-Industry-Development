"""Tests for the collaborative learning session manager."""

from __future__ import annotations

import pytest
import networkx as nx

from src.collaborative_learning.session_manager import (
    DialogueTurn,
    SessionManager,
    SessionState,
    TurnRole,
)
from src.knowledge_graph.graph_builder import KnowledgeGraphBuilder
from src.recommendation.recommender import Recommender


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def small_graph() -> nx.DiGraph:
    """A minimal knowledge graph for testing."""
    g = nx.DiGraph()
    g.add_node("concept-a", label="Concept A", description="Test concept A", difficulty=1)
    g.add_node("concept-b", label="Concept B", description="Test concept B", difficulty=2)
    g.add_node("concept-c", label="Concept C", description="Test concept C", difficulty=3)
    g.add_edge("concept-a", "concept-b", relation="prerequisite", weight=0.9)
    g.add_edge("concept-b", "concept-c", relation="related-to", weight=0.7)
    return g


@pytest.fixture
def seed_graph() -> nx.DiGraph:
    """The full seed knowledge graph for the intelligent-education domain."""
    builder = KnowledgeGraphBuilder(domain="intelligent-education")
    return builder.build_seed_graph()


@pytest.fixture
def recommender(small_graph: nx.DiGraph) -> Recommender:
    """A recommender initialized with the small test graph."""
    return Recommender(knowledge_graph=small_graph)


@pytest.fixture
def session_manager(small_graph: nx.DiGraph, recommender: Recommender) -> SessionManager:
    """A SessionManager with mock AI backend for testing."""
    return SessionManager(
        learner_id="test-learner-001",
        knowledge_graph=small_graph,
        recommender=recommender,
        max_turns=5,
    )


# ---------------------------------------------------------------------------
# DialogueTurn tests
# ---------------------------------------------------------------------------


class TestDialogueTurn:
    def test_to_dict_contains_required_fields(self) -> None:
        turn = DialogueTurn(
            role=TurnRole.HUMAN,
            content="Hello, what is HCCL?",
            timestamp="2026-04-13T00:00:00+00:00",
            concepts_referenced=["hccl"],
            turn_index=0,
        )
        d = turn.to_dict()
        assert d["role"] == "human"
        assert d["content"] == "Hello, what is HCCL?"
        assert d["concepts_referenced"] == ["hccl"]
        assert d["turn_index"] == 0

    def test_role_enum_values(self) -> None:
        assert TurnRole.HUMAN.value == "human"
        assert TurnRole.AI.value == "ai"
        assert TurnRole.SYSTEM.value == "system"


# ---------------------------------------------------------------------------
# SessionState tests
# ---------------------------------------------------------------------------


class TestSessionState:
    def test_add_turn_increments_index(self) -> None:
        state = SessionState(
            session_id="test-session",
            learner_id="learner-001",
            start_time="2026-04-13T00:00:00+00:00",
        )
        t0 = state.add_turn(TurnRole.HUMAN, "First message")
        t1 = state.add_turn(TurnRole.AI, "First response")
        assert t0.turn_index == 0
        assert t1.turn_index == 1
        assert len(state.turns) == 2

    def test_add_turn_updates_active_concepts(self) -> None:
        state = SessionState(
            session_id="test-session",
            learner_id="learner-001",
            start_time="2026-04-13T00:00:00+00:00",
        )
        state.add_turn(TurnRole.HUMAN, "content", concepts=["concept-a", "concept-b"])
        assert "concept-a" in state.active_concepts
        assert "concept-b" in state.active_concepts

    def test_to_dict_structure(self) -> None:
        state = SessionState(
            session_id="abc123",
            learner_id="learner-001",
            start_time="2026-04-13T00:00:00+00:00",
        )
        d = state.to_dict()
        assert d["session_id"] == "abc123"
        assert d["learner_id"] == "learner-001"
        assert isinstance(d["turns"], list)
        assert isinstance(d["active_concepts"], list)

    def test_export_markdown_contains_session_id(self) -> None:
        state = SessionState(
            session_id="my-session-id",
            learner_id="learner-001",
            start_time="2026-04-13T00:00:00+00:00",
        )
        state.add_turn(TurnRole.HUMAN, "What is intelligent education?")
        state.add_turn(TurnRole.AI, "Great question! It refers to...")
        md = state.export_markdown()
        assert "my-session-id" in md
        assert "What is intelligent education?" in md
        assert "Great question!" in md


# ---------------------------------------------------------------------------
# SessionManager tests
# ---------------------------------------------------------------------------


class TestSessionManager:
    def test_session_id_is_unique(
        self, small_graph: nx.DiGraph, recommender: Recommender
    ) -> None:
        m1 = SessionManager("l1", small_graph, recommender)
        m2 = SessionManager("l2", small_graph, recommender)
        assert m1.state.session_id != m2.state.session_id

    def test_process_human_turn_records_turn(
        self, session_manager: SessionManager
    ) -> None:
        turn = session_manager.process_human_turn("Tell me about concept-a")
        assert turn.role == TurnRole.HUMAN
        assert "concept-a" in turn.content
        assert len(session_manager.state.turns) == 1

    def test_process_human_turn_detects_concepts(
        self, session_manager: SessionManager
    ) -> None:
        turn = session_manager.process_human_turn("What is concept-a and concept-b?")
        assert "concept-a" in turn.concepts_referenced or "concept-b" in turn.concepts_referenced

    def test_generate_response_adds_ai_turn(
        self, session_manager: SessionManager
    ) -> None:
        human_turn = session_manager.process_human_turn("Hello")
        ai_turn = session_manager.generate_response(human_turn)
        assert ai_turn.role == TurnRole.AI
        assert len(ai_turn.content) > 0
        assert len(session_manager.state.turns) == 2

    def test_end_session_sets_inactive(
        self, session_manager: SessionManager
    ) -> None:
        session_manager.end_session()
        assert session_manager.state.is_active is False
        assert session_manager.state.end_time is not None

    def test_export_session_returns_markdown(
        self, session_manager: SessionManager
    ) -> None:
        session_manager.process_human_turn("What is HCCL?")
        session_manager.end_session()
        md = session_manager.export_session()
        assert "HCCL Session Transcript" in md
        assert "What is HCCL?" in md

    def test_custom_ai_backend_is_used(
        self, small_graph: nx.DiGraph, recommender: Recommender
    ) -> None:
        def custom_backend(prompt: str) -> str:
            return "Custom backend response"

        manager = SessionManager(
            learner_id="test-learner",
            knowledge_graph=small_graph,
            recommender=recommender,
            ai_backend=custom_backend,
        )
        human_turn = manager.process_human_turn("Hello")
        ai_turn = manager.generate_response(human_turn)
        assert ai_turn.content == "Custom backend response"


# ---------------------------------------------------------------------------
# KnowledgeGraphBuilder tests
# ---------------------------------------------------------------------------


class TestKnowledgeGraphBuilder:
    def test_seed_graph_has_expected_node_count(self, seed_graph: nx.DiGraph) -> None:
        assert seed_graph.number_of_nodes() == 20

    def test_seed_graph_has_edges(self, seed_graph: nx.DiGraph) -> None:
        assert seed_graph.number_of_edges() > 0

    def test_node_has_required_attributes(self, seed_graph: nx.DiGraph) -> None:
        for node_id in seed_graph.nodes:
            data = seed_graph.nodes[node_id]
            assert "label" in data, f"Node {node_id} missing 'label'"
            assert "description" in data, f"Node {node_id} missing 'description'"
            assert "difficulty" in data, f"Node {node_id} missing 'difficulty'"

    def test_hccl_node_exists(self, seed_graph: nx.DiGraph) -> None:
        assert seed_graph.has_node("hccl")

    def test_get_related_concepts_returns_list(self) -> None:
        builder = KnowledgeGraphBuilder()
        graph = builder.build_seed_graph()
        related = builder.get_related_concepts("hccl")
        assert isinstance(related, list)

    def test_get_concept_info_returns_dict(self) -> None:
        builder = KnowledgeGraphBuilder()
        builder.build_seed_graph()
        info = builder.get_concept_info("hccl")
        assert info is not None
        assert "label" in info

    def test_get_concept_info_returns_none_for_unknown(self) -> None:
        builder = KnowledgeGraphBuilder()
        builder.build_seed_graph()
        assert builder.get_concept_info("nonexistent-concept") is None


# ---------------------------------------------------------------------------
# Recommender tests
# ---------------------------------------------------------------------------


class TestRecommender:
    def test_recommendations_are_list(self, recommender: Recommender) -> None:
        recs = recommender.get_recommendations("learner-001")
        assert isinstance(recs, list)

    def test_recommendations_respect_top_k(self, recommender: Recommender) -> None:
        recs = recommender.get_recommendations("learner-001", top_k=2)
        assert len(recs) <= 2

    def test_mastery_starts_low(self, recommender: Recommender) -> None:
        level = recommender.get_mastery_level("new-learner", "concept-a")
        assert level < 0.5

    def test_mastery_increases_after_correct_interactions(
        self, recommender: Recommender
    ) -> None:
        initial = recommender.get_mastery_level("learner-x", "concept-a")
        for _ in range(20):
            recommender.record_interaction("learner-x", "concept-a", correct=True)
        final = recommender.get_mastery_level("learner-x", "concept-a")
        assert final > initial

    def test_mastery_lower_after_incorrect_interactions(
        self, recommender: Recommender
    ) -> None:
        # First build up some mastery
        for _ in range(10):
            recommender.record_interaction("learner-y", "concept-a", correct=True)
        mid = recommender.get_mastery_level("learner-y", "concept-a")
        for _ in range(5):
            recommender.record_interaction("learner-y", "concept-a", correct=False)
        final = recommender.get_mastery_level("learner-y", "concept-a")
        assert final <= mid

    def test_learner_summary_contains_all_concepts(
        self, recommender: Recommender, small_graph: nx.DiGraph
    ) -> None:
        summary = recommender.get_learner_summary("learner-001")
        for node_id in small_graph.nodes:
            label = small_graph.nodes[node_id].get("label", node_id)
            assert label in summary

    def test_prerequisite_check_blocks_advanced_concept(
        self, recommender: Recommender
    ) -> None:
        # concept-b has concept-a as prerequisite; with default low mastery, should not recommend concept-b before concept-a
        recs = recommender.get_recommendations("fresh-learner", top_k=10)
        concept_b_label = "Concept B"
        concept_a_label = "Concept A"
        if concept_b_label in recs:
            assert concept_a_label in recs
            assert recs.index(concept_a_label) <= recs.index(concept_b_label)
