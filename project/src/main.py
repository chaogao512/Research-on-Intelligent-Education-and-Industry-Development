"""
main.py — Application entry point for CollabLearn.

Provides a CLI to start an interactive human-computer collaborative learning session.
"""

import click
from rich.console import Console
from rich.panel import Panel

from src.collaborative_learning.session_manager import SessionManager
from src.knowledge_graph.graph_builder import KnowledgeGraphBuilder
from src.recommendation.recommender import Recommender

console = Console()


@click.group()
def main() -> None:
    """CollabLearn — Human-Computer Collaborative Learning System."""


@main.command()
@click.option("--learner-id", "-l", required=True, help="Unique learner identifier.")
@click.option(
    "--topic",
    "-t",
    default="intelligent-education",
    show_default=True,
    help="Knowledge domain topic for the session.",
)
@click.option(
    "--max-turns",
    "-m",
    default=10,
    show_default=True,
    type=int,
    help="Maximum number of dialogue turns.",
)
def session(learner_id: str, topic: str, max_turns: int) -> None:
    """Start an interactive HCCL collaborative learning session."""
    console.print(
        Panel(
            f"[bold green]CollabLearn Session[/bold green]\n"
            f"Learner: [cyan]{learner_id}[/cyan]  |  Topic: [cyan]{topic}[/cyan]  |  "
            f"Max turns: [cyan]{max_turns}[/cyan]",
            title="🎓 Human-Computer Collaborative Learning",
            border_style="green",
        )
    )

    # Initialize components
    kg_builder = KnowledgeGraphBuilder(domain=topic)
    graph = kg_builder.build_seed_graph()
    recommender = Recommender(knowledge_graph=graph)
    manager = SessionManager(
        learner_id=learner_id,
        knowledge_graph=graph,
        recommender=recommender,
        max_turns=max_turns,
    )

    # Run the session
    manager.run_interactive()


@main.command()
@click.option("--learner-id", "-l", required=True, help="Unique learner identifier.")
def recommend(learner_id: str) -> None:
    """Get personalized learning recommendations for a learner."""
    kg_builder = KnowledgeGraphBuilder(domain="intelligent-education")
    graph = kg_builder.build_seed_graph()
    recommender = Recommender(knowledge_graph=graph)

    recommendations = recommender.get_recommendations(learner_id=learner_id, top_k=5)

    console.print(f"\n[bold]Recommendations for learner [cyan]{learner_id}[/cyan]:[/bold]")
    for i, rec in enumerate(recommendations, 1):
        console.print(f"  {i}. {rec}")


if __name__ == "__main__":
    main()
