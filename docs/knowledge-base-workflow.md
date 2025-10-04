# Knowledge Base Workflow Documentation

## Overview

The temporal knowledge base system tracks how ideas, predictions, and opinions evolve over time. It extracts structured claims from analyzed content, identifies relationships between entries, and maintains speaker position tracking.

## System Architecture

```
User Request
    ↓
Project Coordinator (orchestrates workflow)
    ↓
    ├─→ Media Fetcher (gets transcript)
    ↓
    ├─→ Content Analyzer (extracts insights + structured claims)
    ↓
    ├─→ Knowledge Builder (creates KB entry with relationships)
    ↓
    └─→ Summary Agent (optional: creates condensed version)
    ↓
Final Report to User
```

## Agent Responsibilities

### 1. Media Fetcher
- **Input**: URL or search term
- **Output**: Transcript file path
- **Actions**:
  - Fetches YouTube transcripts using existing `get_transcript.py`
  - Processes podcasts using `podcast_processor.py`
  - Handles multiple sources with fallback logic
  - Saves to `learning/raw-transcripts/` or `learning/podcasts/transcripts/`

### 2. Content Analyzer (Enhanced)
- **Input**: Transcript file path
- **Output**:
  - Standard analysis report (markdown)
  - Structured knowledge extraction (JSON)
- **Actions**:
  - Performs deep content analysis
  - **NEW**: Extracts structured claims:
    - **Predictions**: Future-focused statements with confidence levels
    - **Factual Claims**: Data points, trends, observations
    - **Opinions**: Subjective viewpoints and recommendations
  - Identifies topics (primary, secondary, domain)
  - Extracts speaker information and credibility indicators
  - Generates hierarchical tags
  - Saves both analysis.md and knowledge.json

### 3. Knowledge Builder (New Agent)
- **Input**: Knowledge extraction JSON from content-analyzer
- **Output**: Knowledge base entry with relationships
- **Actions**:
  - Parses structured claims from content-analyzer
  - **Searches for related content**:
    - By topic (same subject matter)
    - By speaker (track position evolution)
    - By temporal proximity (±6 months)
  - **Identifies relationships**:
    - **Confirms**: Agreements with previous claims
    - **Contradicts**: Conflicts with earlier positions
    - **Extends**: Builds upon previous ideas
    - **Updates**: Supersedes dated information
  - Creates knowledge entry using TEMPLATE.md format
  - Updates indices:
    - `learning/knowledge/by-topic/[topic]/index.md`
    - `learning/knowledge/by-speaker/[speaker]/profile.md`
    - `learning/knowledge/timeline/YYYY-MM.md`
  - Saves to appropriate topic directory

### 4. Summary Agent (Optional)
- Creates condensed versions if requested
- Multiple formats: executive, learning, content summaries

## Knowledge Entry Structure

Each knowledge entry follows this format:

```markdown
# [Title]

**Source**: [Platform/Show Name]
**Date**: YYYY-MM-DD
**Speaker(s)**: [Names]
**Topic**: [Primary Topic]
**Content Type**: [Interview/Solo/Tutorial/etc]

## Executive Summary
[1-2 sentence overview]

## Key Claims & Predictions

### Predictions
- **[PREDICTION]** "Quote" - Confidence: High/Medium/Low @ timestamp
  - Context and reasoning

### Factual Claims
- **[DATA]** "Statistic" @ timestamp
- **[TREND]** "Observed pattern" @ timestamp

### Opinions
- **[OPINION]** "Viewpoint" @ timestamp
- **[RECOMMENDATION]** "Advice" @ timestamp

## Historical Context & Evolution

### Related Past Content
- **Confirms**: [2025-09 entry] "similar claim"
- **Contradicts**: [2024-12 entry] "conflicting position"
- **Extends**: [2025-08 entry] "foundational idea"

### Speaker's Position Evolution
- **Then** (Date): Earlier position
- **Now** (Date): Current position
- **Change**: What shifted and why

## Metadata

```json
{
  "entry_id": "unique-identifier",
  "created_date": "YYYY-MM-DD",
  "topics": ["topic1", "topic2"],
  "speakers": ["Name"],
  "claim_count": 5,
  "prediction_count": 2,
  "confidence_score": 0.8,
  "related_entries": ["entry-id-1", "entry-id-2"]
}
```
```

## Directory Organization

```
learning/knowledge/
├── by-topic/
│   ├── housing-market/
│   │   ├── index.md                          # Topic overview
│   │   ├── 2025-09-biggerpockets-*.md       # Entry 1
│   │   └── 2025-10-redfin-analysis.md       # Entry 2
│   └── ai-coding/
│       ├── index.md
│       └── 2025-10-claude-code-subagents.md
├── by-speaker/
│   ├── dave-meyer/
│   │   ├── profile.md                        # Speaker bio & track record
│   │   └── timeline.md                       # Chronological positions
│   └── indie-dev-dan/
│       └── profile.md
├── timeline/
│   ├── 2025-09.md                           # All Sept 2025 entries
│   └── 2025-10.md                           # All Oct 2025 entries
└── relationships/
    ├── contradictions.md                     # Known conflicts
    └── evolution.md                          # Position changes

TEMPLATE.md                                   # Standard format
sample_knowledge_extraction.json              # Example output from content-analyzer
```

## File Naming Convention

Format: `YYYY-MM-source-short-title.md`

Examples:
- `2025-10-youtube-claude-code-subagents.md`
- `2025-09-biggerpockets-housing-correction.md`
- `2025-10-lex-fridman-ai-safety.md`

## Workflow Examples

### Example 1: Analyze YouTube Video with KB Integration

**User Request:**
```
Analyze this video and add to knowledge base: https://youtube.com/watch?v=7B2HJr0Y68g
```

**Project Coordinator Process:**

1. **Delegate to media-fetcher**
   ```
   Task: "Fetch transcript from YouTube URL: https://youtube.com/watch?v=7B2HJr0Y68g"
   Result: learning/raw-transcripts/7B2HJr0Y68g.txt
   ```

2. **Delegate to content-analyzer** (with knowledge extraction)
   ```
   Task: "Analyze transcript at learning/raw-transcripts/7B2HJr0Y68g.txt
          Extract structured claims for knowledge base"
   Result:
   - learning/analyses/claude-code-subagents_analysis.md
   - learning/analyses/claude-code-subagents_knowledge.json
   ```

3. **Delegate to knowledge-builder**
   ```
   Task: "Build knowledge entry from learning/analyses/claude-code-subagents_knowledge.json
          Search for related entries on ai-coding and agent-architecture topics"
   Result:
   - learning/knowledge/by-topic/ai-coding/2025-10-youtube-claude-code-subagents.md
   - Updated learning/knowledge/by-topic/ai-coding/index.md
   - Updated learning/knowledge/by-speaker/indie-dev-dan/profile.md
   - Updated learning/knowledge/timeline/2025-10.md
   ```

4. **Synthesize and report**
   ```
   Report to user:
   - Video analyzed successfully
   - Extracted 6 claims (1 prediction, 1 data point, 4 recommendations)
   - Identified 4 key concepts about sub-agent architecture
   - Found 2 related entries on ai-coding topic
   - No contradictions with existing knowledge
   - Knowledge entry created with temporal tracking
   ```

### Example 2: Track Speaker Position Evolution

**User Request:**
```
Search knowledge base for all Dave Meyer housing market predictions
```

**Using Search Utility:**
```bash
python scripts/search_knowledge.py --speaker "Dave Meyer" --topic housing-market
```

**Result:**
```
Found 3 entries:

1. Housing Market Sept 2025 - Mild Correction
   Speakers: Dave Meyer
   Topics: housing-market, real-estate, market-correction
   Prediction: Buyer's market will continue strengthening - Confidence: High

2. Housing Market July 2025 - Summer Trends
   Speakers: Dave Meyer
   Topics: housing-market, seasonal-analysis
   Prediction: Cooling expected into fall - Confidence: Medium

3. Housing Market Jan 2025 - Year Ahead Forecast
   Speakers: Dave Meyer
   Topics: housing-market, forecasting
   Prediction: Stable year with regional variations - Confidence: Medium

Position Evolution:
- Jan 2025: Predicted stability
- July 2025: Shifted to cooling expectation
- Sept 2025: Confirmed buyer's market strengthening
```

### Example 3: Find Contradictions

**Scenario:** New podcast claims "AI coding tools will plateau by 2026"

**Knowledge Builder Process:**
1. Extracts prediction: "AI coding tools will plateau by 2026"
2. Searches KB for related claims on "ai-coding" topic
3. Finds contradicting claim from previous entry:
   - "AI coding tools will continue exponential growth through 2027" (Confidence: High)
4. Documents relationship:
   ```markdown
   ### Related Past Content
   - **Contradicts**: [2025-09 entry] "Previous prediction of continued exponential growth"
   ```
5. Updates `learning/knowledge/relationships/contradictions.md`

## Testing the Knowledge Base

### Test 1: Sample Knowledge Extraction

A sample knowledge extraction JSON has been created:
`learning/knowledge/sample_knowledge_extraction.json`

This demonstrates the expected output format from content-analyzer for the Claude Code sub-agents video.

**To test manually:**
```bash
# 1. Review the sample extraction
cat learning/knowledge/sample_knowledge_extraction.json

# 2. Manually create a knowledge entry from it (simulating knowledge-builder)
# Use the TEMPLATE.md as a guide

# 3. Search for the entry
python scripts/search_knowledge.py --topic claude-code-sub-agents
```

### Test 2: Full Workflow Test

**Prerequisites:**
- YouTube transcript available at `learning/raw-transcripts/7B2HJr0Y68g.txt`
- Sample knowledge extraction at `learning/knowledge/sample_knowledge_extraction.json`

**Test Steps:**
1. User provides YouTube URL
2. Media-fetcher retrieves transcript (already done)
3. Content-analyzer extracts claims (sample provided)
4. Knowledge-builder creates entry with relationships
5. Search utility can find the entry

### Test 3: Relationship Detection

**Setup:**
Create two knowledge entries on the same topic with:
- One confirming claim
- One contradicting claim

**Expected:**
Knowledge-builder should detect and document the relationship in both entries.

## Search Capabilities

The `scripts/search_knowledge.py` utility provides:

```bash
# Search by topic
python scripts/search_knowledge.py --topic housing-market

# Search by speaker
python scripts/search_knowledge.py --speaker "Dave Meyer"

# Search by date range
python scripts/search_knowledge.py --date-from 2025-09-01 --date-to 2025-10-31

# Search by claim type
python scripts/search_knowledge.py --claim-type prediction

# Full-text search
python scripts/search_knowledge.py --query "market correction"

# Find relationships
python scripts/search_knowledge.py --relationships bp-housing-2025-09-mild-correction

# List all topics
python scripts/search_knowledge.py --list-topics

# List all speakers
python scripts/search_knowledge.py --list-speakers
```

## Best Practices

### For Content Analyzer
1. **Extract complete context** for each claim
2. **Preserve nuance** in confidence levels
3. **Cite timestamps** when available
4. **Identify speaker expertise** indicators
5. **Generate comprehensive tags** for discoverability

### For Knowledge Builder
1. **Search broadly** for related content (topics, speakers, temporal)
2. **Document all relationships** (confirms, contradicts, extends)
3. **Maintain temporal accuracy** (dates are critical)
4. **Update indices consistently** (topic, speaker, timeline)
5. **Flag incomplete data** (e.g., metadata-only entries)

### For Using the Knowledge Base
1. **Check speaker track records** before trusting predictions
2. **Look for contradictions** to understand debate nuances
3. **Track position evolution** to see how thinking changes
4. **Use temporal context** to understand currency of claims
5. **Cross-reference** multiple sources on same topic

## Future Enhancements

See [ROADMAP.md](../ROADMAP.md) for the complete project roadmap including:

### Tier 2: Vector Database (Short-term - 1-3 months)
- Semantic search using ChromaDB
- Similarity matching for related claims
- Embedding-based retrieval
- Better than keyword matching

### Tier 3: Temporal Knowledge Graph (Medium-term - 3-6 months)
- Using Graphiti framework
- Track claim evolution as graph nodes
- Relationship edges (confirms, contradicts, extends)
- Query patterns: "Show evolution of speaker's position on topic X"

**Note**: All future enhancements are tracked centrally in [ROADMAP.md](../ROADMAP.md)

## Troubleshooting

**Issue:** Knowledge entry not found by search
- Check topic directory naming (use hyphens, lowercase)
- Verify metadata JSON is properly formatted
- Ensure entry_id is unique

**Issue:** Relationships not detected
- Confirm related_entries array in metadata
- Check if relationship keywords appear in markdown
- Verify entry_ids match exactly

**Issue:** Speaker profile not updated
- Check if speaker name matches exactly (case-sensitive)
- Verify by-speaker directory exists
- Ensure profile.md follows template

## Summary

The knowledge base system provides:
✅ Temporal tracking of ideas and predictions
✅ Speaker position evolution monitoring
✅ Relationship detection (confirms, contradicts, extends)
✅ Multi-dimensional search capabilities
✅ Structured claim extraction with confidence levels
✅ Integration with existing agent workflow

This creates a queryable historical context that informs future analysis and decision-making.
