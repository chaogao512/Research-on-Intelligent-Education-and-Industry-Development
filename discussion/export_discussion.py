#!/usr/bin/env python3
"""
export_discussion.py
====================
Export group discussion files to clean, formatted Markdown files suitable
for use as assignment appendices or shared reports.

Usage
-----
# Export a single topic
python discussion/export_discussion.py --topic topic-00-course-orientation-and-learning-methods

# Export all topics into one compiled file
python discussion/export_discussion.py --all

# Export all topics into one file with a custom output path
python discussion/export_discussion.py --all --output exports/full_discussion_export.md

# Export a single topic with a custom output path
python discussion/export_discussion.py --topic topic-04-practical-exploration-of-educational-informatization-governance \
    --output exports/topic-04-export.md

Requirements
------------
Python 3.8+ (standard library only — no third-party packages needed).
"""

import argparse
import os
import re
import sys
from datetime import datetime
from pathlib import Path


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

# Root of the discussion directory (relative to repo root, or absolute)
DISCUSSION_DIR = Path(__file__).parent

# Pattern that marks a member contribution header
CONTRIBUTION_PATTERN = re.compile(
    r"^\*\*\[(?P<name>[^\]]+)\]\s*[—-]\s*(?P<timestamp>[^\*]+):\*\*",
    re.MULTILINE,
)

# Standard section headers in a discussion file
SECTION_HEADERS = {
    "background": "## 📌 Topic Background",
    "questions": "## ❓ Discussion Questions",
    "contributions": "## 👥 Member Contributions",
    "conclusions": "## 🔑 Key Conclusions",
    "actions": "## ✅ Action Items",
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def find_topic_dirs(discussion_dir: Path) -> list[Path]:
    """Return sorted list of topic subdirectories."""
    return sorted(
        [d for d in discussion_dir.iterdir() if d.is_dir() and d.name.startswith("topic-")]
    )


def find_discussion_file(topic_dir: Path) -> Path | None:
    """Find the primary discussion .md file in a topic directory."""
    candidates = list(topic_dir.glob("discussion.md")) + list(topic_dir.glob("*.md"))
    return candidates[0] if candidates else None


def parse_metadata(content: str) -> dict:
    """Extract YAML-style metadata from the top blockquote lines of a discussion file."""
    meta = {}
    for line in content.splitlines():
        line = line.strip()
        if not line.startswith(">"):
            break
        line = line.lstrip(">").strip()
        if "**Status**" in line:
            meta["status"] = re.sub(r"\*\*Status\*\*:?\s*", "", line).strip()
        elif "**Opened by**" in line:
            meta["opened_by"] = re.sub(r"\*\*Opened by\*\*:?\s*", "", line).strip()
        elif "**Open date**" in line:
            meta["open_date"] = re.sub(r"\*\*Open date\*\*:?\s*", "", line).strip()
        elif "**Facilitator**" in line:
            meta["facilitator"] = re.sub(r"\*\*Facilitator\*\*:?\s*", "", line).strip()
    return meta


def extract_section(content: str, header: str) -> str:
    """Extract the content of a named section from a Markdown file."""
    lines = content.splitlines()
    capturing = False
    result = []
    for line in lines:
        if line.strip() == header.strip():
            capturing = True
            continue
        if capturing and line.startswith("## "):
            break
        if capturing:
            result.append(line)
    return "\n".join(result).strip()


def count_contributions(content: str) -> dict:
    """Count contributions per member."""
    counts: dict[str, int] = {}
    for match in CONTRIBUTION_PATTERN.finditer(content):
        name = match.group("name").strip()
        counts[name] = counts.get(name, 0) + 1
    return counts


def format_topic_export(topic_dir: Path, discussion_file: Path) -> str:
    """Format a single topic discussion as a clean export block."""
    content = discussion_file.read_text(encoding="utf-8")

    # Extract title from H1
    title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else topic_dir.name

    meta = parse_metadata(content)
    background = extract_section(content, SECTION_HEADERS["background"])
    questions = extract_section(content, SECTION_HEADERS["questions"])
    contributions = extract_section(content, SECTION_HEADERS["contributions"])
    conclusions = extract_section(content, SECTION_HEADERS["conclusions"])
    actions = extract_section(content, SECTION_HEADERS["actions"])
    contribution_counts = count_contributions(content)

    total_contributions = sum(contribution_counts.values())
    word_count = len(content.split())

    lines = [
        f"# {title}",
        "",
        "## Metadata",
        "",
        f"| Field | Value |",
        f"|-------|-------|",
        f"| **Topic folder** | `{topic_dir.name}` |",
        f"| **Status** | {meta.get('status', '—')} |",
        f"| **Opened by** | {meta.get('opened_by', '—')} |",
        f"| **Open date** | {meta.get('open_date', '—')} |",
        f"| **Facilitator** | {meta.get('facilitator', '—')} |",
        f"| **Exported** | {datetime.now().strftime('%Y-%m-%d %H:%M')} |",
        f"| **Total contributions** | {total_contributions} |",
        f"| **Source word count** | {word_count} |",
        "",
    ]

    if contribution_counts:
        lines += [
            "## Participation Summary",
            "",
            "| Member | Contributions |",
            "|--------|---------------|",
        ]
        for name, count in sorted(contribution_counts.items()):
            lines.append(f"| {name} | {count} |")
        lines.append("")

    if background:
        lines += ["## Topic Background", "", background, ""]

    if questions:
        lines += ["## Discussion Questions", "", questions, ""]

    if contributions:
        lines += ["## Member Contributions", "", contributions, ""]

    if conclusions:
        lines += ["## Key Conclusions", "", conclusions, ""]

    if actions:
        lines += ["## Action Items", "", actions, ""]

    lines += ["---", ""]
    return "\n".join(lines)


def build_export_header(topics_exported: list[str]) -> str:
    """Build a header block for a compiled multi-topic export."""
    return "\n".join([
        "# Discussion Export — Research on Intelligent Education and Industry Development",
        "",
        f"> **Exported**: {datetime.now().strftime('%Y-%m-%d %H:%M')}  ",
        f"> **Topics included**: {len(topics_exported)}  ",
        "> **Course**: 《智能教育及行业发展研究》  ",
        "",
        "---",
        "",
        "## Table of Contents",
        "",
        *[f"{i + 1}. [{t}](#{t.lower().replace(' ', '-').replace('/', '')})"
          for i, t in enumerate(topics_exported)],
        "",
        "---",
        "",
    ])


# ---------------------------------------------------------------------------
# Main export logic
# ---------------------------------------------------------------------------

def export_topic(topic_name: str, output_path: Path | None, discussion_dir: Path) -> None:
    """Export a single topic to a Markdown file."""
    topic_dir = discussion_dir / topic_name
    if not topic_dir.exists():
        print(f"[ERROR] Topic directory not found: {topic_dir}", file=sys.stderr)
        sys.exit(1)

    discussion_file = find_discussion_file(topic_dir)
    if discussion_file is None:
        print(f"[ERROR] No discussion .md file found in: {topic_dir}", file=sys.stderr)
        sys.exit(1)

    export_content = format_topic_export(topic_dir, discussion_file)

    if output_path is None:
        output_path = discussion_dir / f"{topic_name}-export.md"

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(export_content, encoding="utf-8")
    print(f"[OK] Exported '{topic_name}' → {output_path}")


def export_all(output_path: Path | None, discussion_dir: Path) -> None:
    """Export all topics into a single compiled Markdown file."""
    topic_dirs = find_topic_dirs(discussion_dir)
    if not topic_dirs:
        print("[WARN] No topic directories found.", file=sys.stderr)
        return

    sections = []
    topic_titles = []

    for topic_dir in topic_dirs:
        discussion_file = find_discussion_file(topic_dir)
        if discussion_file is None:
            print(f"[SKIP] No discussion file in: {topic_dir.name}")
            continue
        print(f"[INFO] Processing: {topic_dir.name}")
        content = discussion_file.read_text(encoding="utf-8")
        title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
        title = title_match.group(1).strip() if title_match else topic_dir.name
        topic_titles.append(title)
        sections.append(format_topic_export(topic_dir, discussion_file))

    header = build_export_header(topic_titles)
    compiled = header + "\n\n".join(sections)

    if output_path is None:
        timestamp = datetime.now().strftime("%Y%m%d-%H%M")
        output_path = discussion_dir / f"all-discussions-export-{timestamp}.md"

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(compiled, encoding="utf-8")
    print(f"[OK] All {len(sections)} topic(s) exported → {output_path}")


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Export discussion threads to clean, formatted Markdown files.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--topic",
        metavar="TOPIC_DIR_NAME",
        help="Name of the topic subfolder to export (e.g., topic-00-course-orientation-and-learning-methods)",
    )
    group.add_argument(
        "--all",
        action="store_true",
        help="Export all topic discussions into a single compiled file",
    )
    parser.add_argument(
        "--output",
        metavar="OUTPUT_PATH",
        type=Path,
        default=None,
        help="Custom output file path (default: auto-generated in discussion/ folder)",
    )
    parser.add_argument(
        "--discussion-dir",
        metavar="DIR",
        type=Path,
        default=DISCUSSION_DIR,
        help=f"Path to the discussion directory (default: {DISCUSSION_DIR})",
    )

    args = parser.parse_args()

    if args.all:
        export_all(args.output, args.discussion_dir)
    else:
        export_topic(args.topic, args.output, args.discussion_dir)


if __name__ == "__main__":
    main()
