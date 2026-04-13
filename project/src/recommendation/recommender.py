"""
recommender.py
==============
Adaptive learning recommendation engine for CollabLearn.

Implements a simplified Bayesian Knowledge Tracing (BKT) model to estimate
learner knowledge states and recommend appropriate next concepts.

BKT models the probability of a learner knowing a concept using four parameters:
    p_L0: Prior probability of knowing the concept
    p_T:  Probability of learning the concept after an opportunity (transition)
    p_S:  Probability of a slip (incorrect response despite knowing)
    p_G:  Probability of a guess (correct response despite not knowing)

The recommender selects concepts that are:
  1. Not yet mastered (P(L) < mastery_threshold)
  2. Have all prerequisites mastered
  3. Sorted by expected learning gain
"""

from __future__ import annotations

from dataclasses import dataclass, field

import networkx as nx


# Default BKT parameters (can be overridden per concept)
DEFAULT_P_L0 = 0.2    # Low prior knowledge assumed
DEFAULT_P_T = 0.15    # Moderate learning transition probability
DEFAULT_P_S = 0.1     # Low slip probability
DEFAULT_P_G = 0.2     # Low guess probability
MASTERY_THRESHOLD = 0.95  # P(L) >= this is considered mastered


@dataclass
class ConceptKnowledgeState:
    """BKT knowledge state for a single learner-concept pair.

    Attributes:
        concept_id: The knowledge concept identifier.
        p_l: Current probability that the learner knows the concept.
        p_l0: Prior probability.
        p_t: Learning transition probability.
        p_s: Slip probability.
        p_g: Guess probability.
        n_observations: Total number of observations (practice attempts).
    """

    concept_id: str
    p_l: float = DEFAULT_P_L0
    p_l0: float = DEFAULT_P_L0
    p_t: float = DEFAULT_P_T
    p_s: float = DEFAULT_P_S
    p_g: float = DEFAULT_P_G
    n_observations: int = 0

    @property
    def is_mastered(self) -> bool:
        """Return True if the concept is considered mastered."""
        return self.p_l >= MASTERY_THRESHOLD

    def update(self, correct: bool) -> None:
        """Update the knowledge state given an observed response.

        Uses standard BKT update equations.

        Args:
            correct: True if the learner's response was correct.
        """
        p_l = self.p_l

        # Probability of correct response
        p_correct = p_l * (1 - self.p_s) + (1 - p_l) * self.p_g
        p_incorrect = p_l * self.p_s + (1 - p_l) * (1 - self.p_g)

        # Posterior update (Bayesian inference step)
        if correct:
            p_l_given_obs = (p_l * (1 - self.p_s)) / p_correct if p_correct > 0 else p_l
        else:
            p_l_given_obs = (p_l * self.p_s) / p_incorrect if p_incorrect > 0 else p_l

        # Clamp to valid probability range
        p_l_given_obs = max(0.0, min(1.0, p_l_given_obs))

        # Apply learning transition
        self.p_l = p_l_given_obs + (1 - p_l_given_obs) * self.p_t
        self.p_l = max(0.0, min(1.0, self.p_l))
        self.n_observations += 1


@dataclass
class LearnerKnowledgeModel:
    """Full knowledge model for a single learner across all domain concepts.

    Args:
        learner_id: Unique identifier for the learner.
    """

    learner_id: str
    concept_states: dict[str, ConceptKnowledgeState] = field(default_factory=dict)

    def get_state(self, concept_id: str) -> ConceptKnowledgeState:
        """Get or create the knowledge state for a concept.

        Args:
            concept_id: The concept identifier.

        Returns:
            The ConceptKnowledgeState for this learner-concept pair.
        """
        if concept_id not in self.concept_states:
            self.concept_states[concept_id] = ConceptKnowledgeState(concept_id=concept_id)
        return self.concept_states[concept_id]

    def record_interaction(self, concept_id: str, correct: bool) -> None:
        """Record a learner interaction with a concept.

        Args:
            concept_id: The concept the learner interacted with.
            correct: Whether the interaction was correct/successful.
        """
        self.get_state(concept_id).update(correct)

    def get_mastery_level(self, concept_id: str) -> float:
        """Get the current mastery probability for a concept.

        Args:
            concept_id: The concept identifier.

        Returns:
            Probability of knowing the concept (0.0–1.0).
        """
        return self.get_state(concept_id).p_l

    def get_mastered_concepts(self) -> list[str]:
        """Return list of concept IDs where mastery threshold is reached.

        Returns:
            List of mastered concept IDs.
        """
        return [cid for cid, state in self.concept_states.items() if state.is_mastered]


class Recommender:
    """Adaptive learning pathway recommender using BKT-based knowledge modeling.

    Maintains learner knowledge models and recommends next concepts to study
    based on the learner's current knowledge state and concept prerequisites.

    Args:
        knowledge_graph: A NetworkX DiGraph representing the domain knowledge.
        mastery_threshold: P(L) threshold above which a concept is considered mastered.
    """

    def __init__(
        self,
        knowledge_graph: nx.DiGraph,
        mastery_threshold: float = MASTERY_THRESHOLD,
    ) -> None:
        self.knowledge_graph = knowledge_graph
        self.mastery_threshold = mastery_threshold
        self._learner_models: dict[str, LearnerKnowledgeModel] = {}

    def _get_learner_model(self, learner_id: str) -> LearnerKnowledgeModel:
        """Get or create a knowledge model for a learner.

        Args:
            learner_id: The learner's unique identifier.

        Returns:
            The LearnerKnowledgeModel for this learner.
        """
        if learner_id not in self._learner_models:
            self._learner_models[learner_id] = LearnerKnowledgeModel(learner_id=learner_id)
        return self._learner_models[learner_id]

    def record_interaction(self, learner_id: str, concept_id: str, correct: bool) -> None:
        """Record a learner's interaction with a concept and update their model.

        Args:
            learner_id: The learner's unique identifier.
            concept_id: The concept the learner interacted with.
            correct: Whether the interaction was correct/successful.
        """
        model = self._get_learner_model(learner_id)
        model.record_interaction(concept_id, correct)

    def get_mastery_level(self, learner_id: str, concept_id: str) -> float:
        """Get a learner's current mastery level for a specific concept.

        Args:
            learner_id: The learner's unique identifier.
            concept_id: The concept to query.

        Returns:
            Mastery probability (0.0–1.0).
        """
        return self._get_learner_model(learner_id).get_mastery_level(concept_id)

    def _prerequisites_met(self, learner_id: str, concept_id: str) -> bool:
        """Check whether all prerequisites for a concept are mastered.

        Args:
            learner_id: The learner's unique identifier.
            concept_id: The concept to check.

        Returns:
            True if all prerequisites are mastered (or there are none).
        """
        model = self._get_learner_model(learner_id)
        for src, _, data in self.knowledge_graph.in_edges(concept_id, data=True):
            if data.get("relation") == "prerequisite":
                if model.get_mastery_level(src) < self.mastery_threshold:
                    return False
        return True

    def get_recommendations(self, learner_id: str, top_k: int = 5) -> list[str]:
        """Generate personalized learning concept recommendations for a learner.

        Selects concepts from the knowledge graph that:
        1. Are not yet mastered (P(L) < mastery_threshold)
        2. Have all prerequisite concepts mastered
        3. Are sorted by estimated learning gain (proximity to mastery)

        Args:
            learner_id: The learner's unique identifier.
            top_k: Maximum number of recommendations to return.

        Returns:
            List of recommended concept labels (not IDs), most useful first.
        """
        model = self._get_learner_model(learner_id)
        candidates = []

        for concept_id in self.knowledge_graph.nodes:
            mastery = model.get_mastery_level(concept_id)
            if mastery >= self.mastery_threshold:
                continue  # Already mastered
            if not self._prerequisites_met(learner_id, concept_id):
                continue  # Prerequisites not met

            # Estimate learning gain: concepts closer to mastery are prioritized
            expected_gain = 1.0 - mastery
            candidates.append((concept_id, expected_gain))

        # Sort by expected gain descending
        candidates.sort(key=lambda x: x[1], reverse=True)

        # Return human-readable labels
        result = []
        for concept_id, _ in candidates[:top_k]:
            label = self.knowledge_graph.nodes[concept_id].get("label", concept_id)
            result.append(label)
        return result

    def get_learner_summary(self, learner_id: str) -> dict[str, float]:
        """Get a summary of a learner's knowledge state across all concepts.

        Args:
            learner_id: The learner's unique identifier.

        Returns:
            Dictionary mapping concept labels to mastery probabilities.
        """
        model = self._get_learner_model(learner_id)
        summary = {}
        for concept_id in self.knowledge_graph.nodes:
            label = self.knowledge_graph.nodes[concept_id].get("label", concept_id)
            summary[label] = round(model.get_mastery_level(concept_id), 3)
        return summary
