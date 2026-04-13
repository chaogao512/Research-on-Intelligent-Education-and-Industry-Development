"""
graph_builder.py
================
Builds and queries the domain knowledge graph used by CollabLearn.

The knowledge graph represents concepts in the intelligent education domain and
their relationships (prerequisite, related-to, part-of, applied-in, etc.).

The graph uses NetworkX DiGraph as the underlying data structure.
Nodes represent knowledge concepts; directed edges represent relationships.

Node attributes:
    label (str): Human-readable concept name.
    description (str): Brief definition or explanation of the concept.
    difficulty (int): Estimated difficulty level 1–5.
    domain (str): Sub-domain this concept belongs to.

Edge attributes:
    relation (str): Relationship type (prerequisite, related-to, part-of, applied-in).
    weight (float): Relationship strength (0.0–1.0).
"""

from __future__ import annotations

from typing import Any

import networkx as nx


class KnowledgeGraphBuilder:
    """Builds a knowledge graph for the intelligent education domain.

    Args:
        domain: The knowledge domain to build a graph for. Currently supports
                'intelligent-education' (default) and 'hccl'.
    """

    def __init__(self, domain: str = "intelligent-education") -> None:
        self.domain = domain
        self._graph: nx.DiGraph | None = None

    def build_seed_graph(self) -> nx.DiGraph:
        """Build and return the seed knowledge graph for the domain.

        The seed graph contains 20 foundational concepts and their relationships,
        sufficient to support initial prototype sessions.

        Returns:
            A NetworkX DiGraph representing the domain knowledge.
        """
        graph = nx.DiGraph()
        self._add_seed_nodes(graph)
        self._add_seed_edges(graph)
        self._graph = graph
        return graph

    def _add_seed_nodes(self, graph: nx.DiGraph) -> None:
        """Add seed concept nodes to the graph.

        Args:
            graph: The graph to add nodes to (modified in place).
        """
        concepts = [
            {
                "id": "intelligent-education",
                "label": "Intelligent Education",
                "description": (
                    "Educational systems and practices that leverage AI and data-driven "
                    "technologies to personalize and enhance learning experiences."
                ),
                "difficulty": 2,
                "domain": "foundations",
            },
            {
                "id": "hccl",
                "label": "Human-Computer Collaborative Learning",
                "description": (
                    "Learning paradigms in which human learners and AI systems actively "
                    "collaborate toward shared educational goals."
                ),
                "difficulty": 3,
                "domain": "hccl",
            },
            {
                "id": "its",
                "label": "Intelligent Tutoring System",
                "description": (
                    "Software systems that provide personalized instruction and feedback "
                    "without human teacher intervention."
                ),
                "difficulty": 3,
                "domain": "systems",
            },
            {
                "id": "adaptive-learning",
                "label": "Adaptive Learning",
                "description": (
                    "Instructional method that dynamically adjusts content and pacing "
                    "based on individual learner performance and characteristics."
                ),
                "difficulty": 3,
                "domain": "pedagogy",
            },
            {
                "id": "knowledge-tracing",
                "label": "Knowledge Tracing",
                "description": (
                    "The task of modeling and predicting a student's knowledge state "
                    "over time as they interact with a learning system."
                ),
                "difficulty": 4,
                "domain": "algorithms",
            },
            {
                "id": "learner-model",
                "label": "Learner Model",
                "description": (
                    "A computational representation of a learner's knowledge, skills, "
                    "goals, and preferences maintained by an intelligent education system."
                ),
                "difficulty": 3,
                "domain": "systems",
            },
            {
                "id": "cscl",
                "label": "Computer-Supported Collaborative Learning",
                "description": (
                    "Research field studying how digital technologies mediate and support "
                    "collaborative learning between human learners."
                ),
                "difficulty": 3,
                "domain": "theory",
            },
            {
                "id": "distributed-cognition",
                "label": "Distributed Cognition",
                "description": (
                    "Theory that cognitive processes are distributed across individuals, "
                    "artifacts, and the environment rather than located solely in the mind."
                ),
                "difficulty": 4,
                "domain": "theory",
            },
            {
                "id": "cognitive-scaffolding",
                "label": "Cognitive Scaffolding",
                "description": (
                    "Instructional support that helps learners accomplish tasks beyond "
                    "their current independent capability, gradually fading as competence grows."
                ),
                "difficulty": 3,
                "domain": "pedagogy",
            },
            {
                "id": "llm",
                "label": "Large Language Model",
                "description": (
                    "Transformer-based neural network models trained on large text corpora, "
                    "capable of generating and understanding natural language."
                ),
                "difficulty": 4,
                "domain": "technology",
            },
            {
                "id": "learning-analytics",
                "label": "Learning Analytics",
                "description": (
                    "The measurement, collection, analysis, and reporting of data about "
                    "learners and their contexts, for purposes of understanding and optimizing learning."
                ),
                "difficulty": 3,
                "domain": "analytics",
            },
            {
                "id": "bkt",
                "label": "Bayesian Knowledge Tracing",
                "description": (
                    "A probabilistic model that estimates the probability of a student "
                    "knowing a given concept based on their response history."
                ),
                "difficulty": 4,
                "domain": "algorithms",
            },
            {
                "id": "zone-of-proximal-development",
                "label": "Zone of Proximal Development",
                "description": (
                    "Vygotsky's concept: the difference between what a learner can do "
                    "independently and what they can accomplish with guidance."
                ),
                "difficulty": 2,
                "domain": "theory",
            },
            {
                "id": "dialogue-based-tutoring",
                "label": "Dialogue-based Tutoring",
                "description": (
                    "Instructional approach using conversational AI to engage learners in "
                    "Socratic-style dialogue that promotes reflection and understanding."
                ),
                "difficulty": 3,
                "domain": "pedagogy",
            },
            {
                "id": "educational-data-mining",
                "label": "Educational Data Mining",
                "description": (
                    "Applying data mining techniques to educational datasets to discover "
                    "patterns that improve learning outcomes and system design."
                ),
                "difficulty": 4,
                "domain": "analytics",
            },
            {
                "id": "knowledge-graph",
                "label": "Knowledge Graph",
                "description": (
                    "A structured representation of domain concepts and their "
                    "relationships, used to support context-aware AI reasoning."
                ),
                "difficulty": 3,
                "domain": "technology",
            },
            {
                "id": "chinese-higher-education",
                "label": "Chinese Higher Education",
                "description": (
                    "The system of higher education in China, characterized by large class sizes, "
                    "Confucian learning culture, national policy environment, and rapid digitalization."
                ),
                "difficulty": 2,
                "domain": "context",
            },
            {
                "id": "edtech-policy",
                "label": "EdTech Policy",
                "description": (
                    "Government policies shaping the development and use of educational "
                    "technology, including China's 'Double Reduction' and informatization plans."
                ),
                "difficulty": 2,
                "domain": "context",
            },
            {
                "id": "personalized-learning",
                "label": "Personalized Learning",
                "description": (
                    "Educational approach that tailors content, pace, and instructional "
                    "methods to individual learner needs, interests, and prior knowledge."
                ),
                "difficulty": 2,
                "domain": "pedagogy",
            },
            {
                "id": "ai-ethics-in-education",
                "label": "AI Ethics in Education",
                "description": (
                    "Ethical considerations in AI deployment in educational settings, including "
                    "fairness, privacy, transparency, and the power dynamics of AI-mediated learning."
                ),
                "difficulty": 3,
                "domain": "ethics",
            },
        ]

        for concept in concepts:
            node_id = concept.pop("id")
            graph.add_node(node_id, **concept)

    def _add_seed_edges(self, graph: nx.DiGraph) -> None:
        """Add relationship edges between seed concept nodes.

        Args:
            graph: The graph to add edges to (modified in place).
        """
        edges = [
            # Foundational relationships
            ("intelligent-education", "hccl", "part-of", 0.9),
            ("intelligent-education", "its", "part-of", 0.8),
            ("intelligent-education", "adaptive-learning", "part-of", 0.8),
            ("intelligent-education", "learning-analytics", "part-of", 0.7),
            # HCCL relationships
            ("cscl", "hccl", "prerequisite", 0.7),
            ("distributed-cognition", "hccl", "foundation-of", 0.8),
            ("zone-of-proximal-development", "cognitive-scaffolding", "foundation-of", 0.9),
            ("cognitive-scaffolding", "hccl", "applied-in", 0.8),
            ("dialogue-based-tutoring", "hccl", "part-of", 0.7),
            ("llm", "dialogue-based-tutoring", "enables", 0.9),
            ("llm", "hccl", "enables", 0.8),
            # Knowledge modeling
            ("bkt", "knowledge-tracing", "implements", 1.0),
            ("knowledge-tracing", "learner-model", "part-of", 0.9),
            ("learner-model", "adaptive-learning", "enables", 0.9),
            ("learner-model", "its", "part-of", 0.8),
            ("knowledge-graph", "its", "applied-in", 0.7),
            ("knowledge-graph", "hccl", "applied-in", 0.7),
            # Analytics
            ("learning-analytics", "educational-data-mining", "related-to", 0.8),
            ("educational-data-mining", "knowledge-tracing", "related-to", 0.7),
            # Context
            ("chinese-higher-education", "hccl", "context-for", 0.9),
            ("edtech-policy", "chinese-higher-education", "shapes", 0.8),
            # Ethics
            ("learning-analytics", "ai-ethics-in-education", "raises", 0.7),
            ("its", "ai-ethics-in-education", "raises", 0.7),
            # Pedagogy
            ("personalized-learning", "adaptive-learning", "related-to", 0.9),
            ("personalized-learning", "learner-model", "requires", 0.8),
        ]

        for src, dst, relation, weight in edges:
            graph.add_edge(src, dst, relation=relation, weight=weight)

    def get_concept_info(self, concept_id: str) -> dict[str, Any] | None:
        """Get attributes of a concept node.

        Args:
            concept_id: The node ID to look up.

        Returns:
            A dictionary of node attributes, or None if not found.
        """
        if self._graph is None:
            return None
        if not self._graph.has_node(concept_id):
            return None
        return dict(self._graph.nodes[concept_id])

    def get_prerequisites(self, concept_id: str) -> list[str]:
        """Get prerequisite concepts for a given concept.

        Args:
            concept_id: The target concept ID.

        Returns:
            List of concept IDs that are prerequisites for the given concept.
        """
        if self._graph is None:
            return []
        return [
            src
            for src, dst, data in self._graph.in_edges(concept_id, data=True)
            if data.get("relation") == "prerequisite"
        ]

    def get_related_concepts(self, concept_id: str, max_results: int = 5) -> list[str]:
        """Get concepts related to a given concept.

        Args:
            concept_id: The source concept ID.
            max_results: Maximum number of related concepts to return.

        Returns:
            List of related concept IDs, sorted by edge weight descending.
        """
        if self._graph is None:
            return []
        neighbors = list(self._graph.successors(concept_id))
        # Sort by edge weight
        weighted = [
            (nb, self._graph[concept_id][nb].get("weight", 0.5))
            for nb in neighbors
        ]
        weighted.sort(key=lambda x: x[1], reverse=True)
        return [nb for nb, _ in weighted[:max_results]]
