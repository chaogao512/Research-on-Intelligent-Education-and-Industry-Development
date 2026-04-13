# 💬 Group Discussion Area

This folder contains all group discussion records for the 4-person research team in the course **《智能教育及行业发展研究》**.

---

## Discussion Rules

### 🗓️ Schedule & Format
- Discussions are **asynchronous** — contribute within 48 hours of a new topic being opened.
- Each member must contribute **at least one substantive comment** per discussion thread.
- Weekly sync meeting notes should be added to the relevant topic folder.

### 📝 How to Contribute
1. Navigate to the appropriate topic subfolder.
2. Open the topic's `.md` file and add your contribution under the **Member Contributions** section.
3. Use your name/handle and timestamp: `**[Name] — YYYY-MM-DD HH:MM:**`
4. Commit with message: `discussion(topic-XX): add contribution from [Name]`

### 🏷️ Labels & Tagging
- Use `[QUESTION]` to pose a question to the group.
- Use `[RESPONSE]` to respond to another member's point.
- Use `[SYNTHESIS]` to synthesize multiple views.
- Use `[ACTION]` to propose a concrete action item.

---

## Folder Structure

```
discussion/
├── README.md                                          # This file
├── main-discussion.md                                 # Master thread index
├── export_discussion.py                               # Export script
├── topic-01-human-computer-collaborative-learning/    # Topic 1 thread
├── topic-02-educational-data-governance/              # Topic 2 thread
├── topic-03-ai-tools-in-higher-education/             # Topic 3 thread
└── topic-04-industry-development-trends/              # Topic 4 thread
```

---

## Export Procedure

To export a discussion topic to a clean, shareable `.md` file:

```bash
# Export a specific topic
python discussion/export_discussion.py --topic topic-01-human-computer-collaborative-learning

# Export all topics to a single compiled file
python discussion/export_discussion.py --all --output discussion_export.md
```

The exported file will include:
- Topic metadata (title, date range, participants)
- All member contributions with attribution and timestamps
- Key conclusions section
- Action items list
- Word count and participation statistics

> The exported `.md` files can be directly used as appendices in assignment submissions.

---

## Version Control for Discussion Records

- **Never delete** past discussion entries — use strikethrough (`~~text~~`) to mark superseded points.
- When a discussion concludes, the member who facilitated it should add a **Conclusion** section.
- Archive completed discussions by adding `[CONCLUDED - YYYY-MM-DD]` to the topic title in `main-discussion.md`.

---

## Participation Tracking

| Member | Topic 01 | Topic 02 | Topic 03 | Topic 04 |
|--------|----------|----------|----------|----------|
| Member 1 | — | — | — | — |
| Member 2 | — | — | — | — |
| Member 3 | — | — | — | — |
| Member 4 | — | — | — | — |

> Update this table after each discussion concludes. ✅ = contributed, ❌ = missed, 🔄 = in progress
