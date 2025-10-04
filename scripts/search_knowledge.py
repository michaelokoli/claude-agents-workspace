#!/usr/bin/env python3
"""
Knowledge Base Search Utility

Provides search capabilities for the temporal knowledge base.
Supports topic search, speaker search, date range filtering, and claim type filtering.

Usage:
    python scripts/search_knowledge.py --topic housing-market
    python scripts/search_knowledge.py --speaker "Dave Meyer"
    python scripts/search_knowledge.py --date-from 2025-09-01 --date-to 2025-10-31
    python scripts/search_knowledge.py --claim-type prediction
    python scripts/search_knowledge.py --query "market correction"
"""

import os
import json
import argparse
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
import re

# Knowledge base root directory
KB_ROOT = Path(__file__).parent.parent / "learning" / "knowledge"

class KnowledgeSearcher:
    """Search and query the temporal knowledge base."""

    def __init__(self, kb_root: Path = KB_ROOT):
        self.kb_root = kb_root
        self.by_topic_dir = kb_root / "by-topic"
        self.by_speaker_dir = kb_root / "by-speaker"
        self.timeline_dir = kb_root / "timeline"

    def search_by_topic(self, topic: str) -> List[Dict]:
        """Search knowledge entries by topic."""
        results = []
        topic_dir = self.by_topic_dir / topic

        if not topic_dir.exists():
            # Try fuzzy matching
            available_topics = [d.name for d in self.by_topic_dir.iterdir() if d.is_dir()]
            matches = [t for t in available_topics if topic.lower() in t.lower()]
            if matches:
                print(f"Topic '{topic}' not found. Did you mean: {', '.join(matches)}?")
            return results

        # Read all markdown files in topic directory
        for entry_file in topic_dir.glob("*.md"):
            if entry_file.name == "index.md":
                continue

            entry_data = self._parse_entry(entry_file)
            if entry_data:
                results.append(entry_data)

        return results

    def search_by_speaker(self, speaker_name: str) -> List[Dict]:
        """Search knowledge entries by speaker."""
        results = []

        # Search through all topics for speaker mentions
        for topic_dir in self.by_topic_dir.iterdir():
            if not topic_dir.is_dir():
                continue

            for entry_file in topic_dir.glob("*.md"):
                if entry_file.name == "index.md":
                    continue

                entry_data = self._parse_entry(entry_file)
                if entry_data:
                    metadata = entry_data.get('metadata', {})
                    speakers = metadata.get('speakers', [])

                    if any(speaker_name.lower() in speaker.lower() for speaker in speakers):
                        results.append(entry_data)

        return results

    def search_by_date_range(self, date_from: str, date_to: str) -> List[Dict]:
        """Search knowledge entries within date range (YYYY-MM-DD)."""
        results = []

        date_from_obj = datetime.strptime(date_from, "%Y-%m-%d")
        date_to_obj = datetime.strptime(date_to, "%Y-%m-%d")

        for topic_dir in self.by_topic_dir.iterdir():
            if not topic_dir.is_dir():
                continue

            for entry_file in topic_dir.glob("*.md"):
                if entry_file.name == "index.md":
                    continue

                entry_data = self._parse_entry(entry_file)
                if entry_data:
                    # Extract date from filename (YYYY-MM-...)
                    date_match = re.match(r'(\d{4}-\d{2})-', entry_file.name)
                    if date_match:
                        entry_date_str = date_match.group(1) + "-01"  # Use first of month
                        entry_date = datetime.strptime(entry_date_str, "%Y-%m-%d")

                        if date_from_obj <= entry_date <= date_to_obj:
                            results.append(entry_data)

        return results

    def search_by_claim_type(self, claim_type: str) -> List[Dict]:
        """Search for entries containing specific claim types (prediction, data, opinion, recommendation)."""
        results = []

        for topic_dir in self.by_topic_dir.iterdir():
            if not topic_dir.is_dir():
                continue

            for entry_file in topic_dir.glob("*.md"):
                if entry_file.name == "index.md":
                    continue

                content = entry_file.read_text()

                # Check if claim type appears in the content
                pattern = rf'\*\*\[{claim_type.upper()}\]\*\*'
                if re.search(pattern, content, re.IGNORECASE):
                    entry_data = self._parse_entry(entry_file)
                    if entry_data:
                        # Count claims of this type
                        claim_count = len(re.findall(pattern, content, re.IGNORECASE))
                        entry_data['matching_claims'] = claim_count
                        results.append(entry_data)

        return results

    def search_by_query(self, query: str) -> List[Dict]:
        """Full-text search across all knowledge entries."""
        results = []

        for topic_dir in self.by_topic_dir.iterdir():
            if not topic_dir.is_dir():
                continue

            for entry_file in topic_dir.glob("*.md"):
                if entry_file.name == "index.md":
                    continue

                content = entry_file.read_text()

                # Case-insensitive search
                if query.lower() in content.lower():
                    entry_data = self._parse_entry(entry_file)
                    if entry_data:
                        # Count occurrences
                        occurrences = content.lower().count(query.lower())
                        entry_data['occurrences'] = occurrences
                        results.append(entry_data)

        return results

    def find_relationships(self, entry_id: str) -> Dict:
        """Find all relationships (confirms, contradicts, extends) for a given entry."""
        relationships = {
            'confirms': [],
            'contradicts': [],
            'extends': [],
            'confirmed_by': [],
            'contradicted_by': [],
            'extended_by': []
        }

        # Search all entries for mentions of this entry_id
        for topic_dir in self.by_topic_dir.iterdir():
            if not topic_dir.is_dir():
                continue

            for entry_file in topic_dir.glob("*.md"):
                if entry_file.name == "index.md":
                    continue

                content = entry_file.read_text()
                entry_data = self._parse_entry(entry_file)

                if entry_data and entry_data.get('metadata', {}).get('entry_id') == entry_id:
                    # This is the entry itself - extract its relationships
                    if '**Confirms**:' in content:
                        # Parse confirms section
                        pass  # TODO: Parse markdown sections
                    if '**Contradicts**:' in content:
                        pass  # TODO: Parse markdown sections
                    if '**Extends**:' in content:
                        pass  # TODO: Parse markdown sections
                else:
                    # Check if this entry references our target entry
                    if entry_id in content:
                        current_id = entry_data.get('metadata', {}).get('entry_id')
                        if f'**Confirms**: {entry_id}' in content or f'Confirms**: [{entry_id}]' in content:
                            relationships['confirmed_by'].append(current_id)
                        if f'**Contradicts**: {entry_id}' in content or f'Contradicts**: [{entry_id}]' in content:
                            relationships['contradicted_by'].append(current_id)
                        if f'**Extends**: {entry_id}' in content or f'Extends**: [{entry_id}]' in content:
                            relationships['extended_by'].append(current_id)

        return relationships

    def list_topics(self) -> List[str]:
        """List all available topics."""
        if not self.by_topic_dir.exists():
            return []
        return [d.name for d in self.by_topic_dir.iterdir() if d.is_dir()]

    def list_speakers(self) -> List[str]:
        """List all speakers in the knowledge base."""
        speakers = set()

        for topic_dir in self.by_topic_dir.iterdir():
            if not topic_dir.is_dir():
                continue

            for entry_file in topic_dir.glob("*.md"):
                if entry_file.name == "index.md":
                    continue

                entry_data = self._parse_entry(entry_file)
                if entry_data:
                    metadata = entry_data.get('metadata', {})
                    for speaker in metadata.get('speakers', []):
                        speakers.add(speaker)

        return sorted(list(speakers))

    def _parse_entry(self, entry_file: Path) -> Optional[Dict]:
        """Parse a knowledge entry markdown file and extract metadata."""
        try:
            content = entry_file.read_text()

            # Extract metadata JSON block
            metadata_match = re.search(r'```json\s*(\{.*?\})\s*```', content, re.DOTALL)
            metadata = {}
            if metadata_match:
                metadata = json.loads(metadata_match.group(1))

            # Extract title (first heading)
            title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
            title = title_match.group(1) if title_match else entry_file.stem

            # Extract executive summary
            summary_match = re.search(r'## Executive Summary\s*\n(.+?)(?=\n##|\n\*\*|$)', content, re.DOTALL)
            summary = summary_match.group(1).strip() if summary_match else ""

            return {
                'file_path': str(entry_file),
                'title': title,
                'summary': summary,
                'metadata': metadata
            }
        except Exception as e:
            print(f"Error parsing {entry_file}: {e}")
            return None


def main():
    parser = argparse.ArgumentParser(description="Search the temporal knowledge base")
    parser.add_argument('--topic', help='Search by topic (e.g., housing-market)')
    parser.add_argument('--speaker', help='Search by speaker name')
    parser.add_argument('--date-from', help='Start date (YYYY-MM-DD)')
    parser.add_argument('--date-to', help='End date (YYYY-MM-DD)')
    parser.add_argument('--claim-type', choices=['prediction', 'data', 'opinion', 'recommendation'],
                       help='Search by claim type')
    parser.add_argument('--query', help='Full-text search query')
    parser.add_argument('--relationships', help='Find relationships for entry ID')
    parser.add_argument('--list-topics', action='store_true', help='List all available topics')
    parser.add_argument('--list-speakers', action='store_true', help='List all speakers')

    args = parser.parse_args()

    searcher = KnowledgeSearcher()

    # List commands
    if args.list_topics:
        topics = searcher.list_topics()
        print(f"\nAvailable topics ({len(topics)}):")
        for topic in topics:
            print(f"  - {topic}")
        return

    if args.list_speakers:
        speakers = searcher.list_speakers()
        print(f"\nKnown speakers ({len(speakers)}):")
        for speaker in speakers:
            print(f"  - {speaker}")
        return

    # Search commands
    results = []

    if args.topic:
        results = searcher.search_by_topic(args.topic)
        print(f"\n=== Results for topic: {args.topic} ===")
    elif args.speaker:
        results = searcher.search_by_speaker(args.speaker)
        print(f"\n=== Results for speaker: {args.speaker} ===")
    elif args.date_from and args.date_to:
        results = searcher.search_by_date_range(args.date_from, args.date_to)
        print(f"\n=== Results from {args.date_from} to {args.date_to} ===")
    elif args.claim_type:
        results = searcher.search_by_claim_type(args.claim_type)
        print(f"\n=== Results for claim type: {args.claim_type} ===")
    elif args.query:
        results = searcher.search_by_query(args.query)
        print(f"\n=== Results for query: {args.query} ===")
    elif args.relationships:
        relationships = searcher.find_relationships(args.relationships)
        print(f"\n=== Relationships for: {args.relationships} ===")
        for rel_type, entries in relationships.items():
            if entries:
                print(f"\n{rel_type.upper().replace('_', ' ')}:")
                for entry_id in entries:
                    print(f"  - {entry_id}")
        return
    else:
        parser.print_help()
        return

    # Display results
    if results:
        print(f"\nFound {len(results)} entries:\n")
        for i, entry in enumerate(results, 1):
            print(f"{i}. {entry['title']}")
            print(f"   File: {entry['file_path']}")
            if 'summary' in entry and entry['summary']:
                print(f"   Summary: {entry['summary'][:150]}...")
            if 'matching_claims' in entry:
                print(f"   Matching claims: {entry['matching_claims']}")
            if 'occurrences' in entry:
                print(f"   Occurrences: {entry['occurrences']}")

            metadata = entry.get('metadata', {})
            if 'speakers' in metadata:
                print(f"   Speakers: {', '.join(metadata['speakers'])}")
            if 'topics' in metadata:
                print(f"   Topics: {', '.join(metadata['topics'])}")
            print()
    else:
        print("\nNo results found.")


if __name__ == "__main__":
    main()
