#!/usr/bin/env python3
"""
Architecture Scanner - Auto-generates architecture documentation
Scans the workspace and updates the architecture overview based on current state
"""

import os
import json
import glob
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set
import re

class ArchitectureScanner:
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.agents = {}
        self.scripts = []
        self.knowledge_structure = {}
        self.docs = []
        self.tests = []

    def scan_agents(self) -> Dict:
        """Scan all agent YAML files and extract their metadata"""
        agents_dir = self.base_path / "agents"
        agent_files = glob.glob(str(agents_dir / "*.yml"))

        for agent_file in sorted(agent_files):
            agent_name = Path(agent_file).stem
            try:
                with open(agent_file, 'r') as f:
                    content = f.read()
                    # Extract description from first comment or name field
                    desc_match = re.search(r'name:\s*"([^"]+)"', content)
                    if not desc_match:
                        desc_match = re.search(r'#\s*(.+)', content[:200])

                    # Check for tools mentioned
                    tools = []
                    if 'web_search' in content:
                        tools.append('web_search')
                    if 'web_fetch' in content:
                        tools.append('web_fetch')
                    if 'read_file' in content or 'Read' in content:
                        tools.append('file_operations')

                    # Detect agent type
                    agent_type = 'support'
                    if 'coordinator' in agent_name:
                        agent_type = 'orchestrator'
                    elif 'fetcher' in agent_name or 'media' in agent_name:
                        agent_type = 'acquisition'
                    elif 'analyzer' in agent_name or 'analysis' in agent_name:
                        agent_type = 'analysis'
                    elif 'builder' in agent_name or 'knowledge' in agent_name:
                        agent_type = 'knowledge'
                    elif 'meta' in agent_name:
                        agent_type = 'meta'

                    self.agents[agent_name] = {
                        'description': desc_match.group(1) if desc_match else 'Agent',
                        'type': agent_type,
                        'tools': tools,
                        'file': agent_file,
                        'lines': len(content.split('\n'))
                    }
            except Exception as e:
                print(f"Error reading {agent_file}: {e}")

        return self.agents

    def scan_scripts(self) -> List:
        """Scan all Python scripts"""
        scripts_dir = self.base_path / "scripts"
        script_files = glob.glob(str(scripts_dir / "*.py"))

        for script_file in sorted(script_files):
            script_name = Path(script_file).stem
            try:
                with open(script_file, 'r') as f:
                    content = f.read()
                    # Extract docstring if present
                    doc_match = re.search(r'"""(.*?)"""', content, re.DOTALL)
                    description = doc_match.group(1).strip() if doc_match else ""

                    self.scripts.append({
                        'name': script_name,
                        'description': description.split('\n')[0] if description else "",
                        'file': script_file,
                        'lines': len(content.split('\n'))
                    })
            except Exception as e:
                print(f"Error reading {script_file}: {e}")

        return self.scripts

    def scan_knowledge_base(self) -> Dict:
        """Scan knowledge base structure and content"""
        kb_path = self.base_path / "learning" / "knowledge"

        if kb_path.exists():
            # Count entries in each category
            self.knowledge_structure = {
                'by-topic': {},
                'by-speaker': [],
                'timeline': [],
                'relationships': []
            }

            # Scan by-topic
            topic_dir = kb_path / "by-topic"
            if topic_dir.exists():
                for topic in topic_dir.iterdir():
                    if topic.is_dir():
                        entries = list(topic.glob("*.md"))
                        self.knowledge_structure['by-topic'][topic.name] = len(entries)

            # Scan by-speaker
            speaker_dir = kb_path / "by-speaker"
            if speaker_dir.exists():
                self.knowledge_structure['by-speaker'] = len(list(speaker_dir.glob("*.md")))

            # Scan relationships
            rel_dir = kb_path / "relationships"
            if rel_dir.exists():
                self.knowledge_structure['relationships'] = len(list(rel_dir.glob("*.md")))

        # Also scan for transcripts
        transcript_dir = self.base_path / "learning" / "raw-transcripts"
        if transcript_dir.exists():
            self.knowledge_structure['raw_transcripts'] = len(list(transcript_dir.glob("*.txt")))

        return self.knowledge_structure

    def scan_docs(self) -> List:
        """Scan documentation files"""
        docs_dir = self.base_path / "docs"
        doc_files = glob.glob(str(docs_dir / "*.md"))

        for doc_file in sorted(doc_files):
            doc_name = Path(doc_file).stem
            self.docs.append({
                'name': doc_name,
                'file': doc_file
            })

        return self.docs

    def scan_tests(self) -> List:
        """Scan test files"""
        test_patterns = [
            "test_*.py",
            "*_test.py",
            "tests/*.py"
        ]

        for pattern in test_patterns:
            test_files = glob.glob(str(self.base_path / pattern))
            for test_file in test_files:
                self.tests.append(Path(test_file).name)

        return self.tests

    def generate_architecture_md(self) -> str:
        """Generate updated architecture markdown"""

        # Scan everything
        self.scan_agents()
        self.scan_scripts()
        self.scan_knowledge_base()
        self.scan_docs()
        self.scan_tests()

        # Categorize agents
        agents_by_type = {}
        for name, info in self.agents.items():
            agent_type = info['type']
            if agent_type not in agents_by_type:
                agents_by_type[agent_type] = []
            agents_by_type[agent_type].append((name, info))

        # Build the markdown
        md = f"""# Claude Agents Workspace - Architecture Overview
*Auto-generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*

## 📊 Current System Statistics

- **Total Agents**: {len(self.agents)}
- **Python Scripts**: {len(self.scripts)}
- **Documentation Files**: {len(self.docs)}
- **Test Files**: {len(self.tests)}
- **Knowledge Base Entries**: {sum(self.knowledge_structure.get('by-topic', {}).values())}
- **Raw Transcripts**: {self.knowledge_structure.get('raw_transcripts', 0)}

## 🤖 Agent Hierarchy

### Orchestrator Layer
"""

        # Add orchestrator agents
        if 'orchestrator' in agents_by_type:
            for name, info in agents_by_type['orchestrator']:
                md += f"- **`{name}`** - {info['description']}\n"
                if info['tools']:
                    md += f"  - Tools: {', '.join(info['tools'])}\n"
                md += f"  - Size: {info['lines']} lines\n"

        md += "\n### Content Acquisition Layer\n"
        if 'acquisition' in agents_by_type:
            for name, info in agents_by_type['acquisition']:
                md += f"- **`{name}`** - {info['description']}\n"

        md += "\n### Analysis & Processing Layer\n"
        if 'analysis' in agents_by_type:
            for name, info in agents_by_type['analysis']:
                md += f"- **`{name}`** - {info['description']}\n"

        md += "\n### Knowledge Management Layer\n"
        if 'knowledge' in agents_by_type:
            for name, info in agents_by_type['knowledge']:
                md += f"- **`{name}`** - {info['description']}\n"

        md += "\n### Meta & Support Layer\n"
        if 'meta' in agents_by_type:
            for name, info in agents_by_type['meta']:
                md += f"- **`{name}`** - {info['description']}\n"
        if 'support' in agents_by_type:
            for name, info in agents_by_type['support']:
                md += f"- **`{name}`** - {info['description']}\n"

        # Add scripts section
        md += "\n## 🔧 Supporting Scripts\n\n"
        for script in self.scripts[:10]:  # Show top 10
            if script['description']:
                md += f"- **`{script['name']}.py`** - {script['description']}\n"
            else:
                md += f"- **`{script['name']}.py`**\n"

        if len(self.scripts) > 10:
            md += f"- *... and {len(self.scripts) - 10} more scripts*\n"

        # Add knowledge base structure
        md += "\n## 📚 Knowledge Base Structure\n\n"
        md += "```\nlearning/knowledge/\n"

        if self.knowledge_structure.get('by-topic'):
            md += "├── by-topic/\n"
            for topic, count in self.knowledge_structure['by-topic'].items():
                md += f"│   ├── {topic}/ ({count} entries)\n"

        md += f"├── by-speaker/ ({self.knowledge_structure.get('by-speaker', 0)} profiles)\n"
        md += f"├── timeline/ (chronological organization)\n"
        md += f"└── relationships/ ({self.knowledge_structure.get('relationships', 0)} connections)\n"
        md += "```\n"

        # Add data flow diagram
        md += """
## 🔄 Data Flow Architecture

```
USER REQUEST
    ↓
[PROJECT COORDINATOR]
    ├── Analyzes request
    ├── Plans execution
    └── Delegates to agents
         ↓
[PARALLEL/SEQUENTIAL EXECUTION]
    ├── Media Fetcher → Raw Content
    ├── Content Analyzer → Claims & Insights
    └── Knowledge Builder → Structured Entries
         ↓
[KNOWLEDGE BASE]
    ├── Searchable entries
    ├── Relationship tracking
    └── Speaker profiles
```

## 📁 Directory Structure

"""

        # Add actual directory scan
        dirs_to_show = [
            "agents/",
            "docs/",
            "scripts/",
            "learning/",
            "learning/knowledge/",
            "learning/raw-transcripts/",
            "learning/podcasts/",
            "tests/",
            "logs/",
            "output/"
        ]

        md += "```\n"
        for dir_path in dirs_to_show:
            full_path = self.base_path / dir_path
            if full_path.exists():
                # Count files
                if full_path.is_dir():
                    file_count = len(list(full_path.glob("*")))
                    md += f"{dir_path:<30} ({file_count} items)\n"
        md += "```\n"

        # Add documentation section
        md += "\n## 📖 Documentation\n\n"
        for doc in self.docs:
            md += f"- `{doc['name']}.md`\n"

        # Add test section
        if self.tests:
            md += f"\n## 🧪 Test Coverage\n\n"
            for test in self.tests:
                md += f"- `{test}`\n"

        md += f"""
## 🔄 Auto-Update Information

This architecture document is auto-generated by `scripts/architecture_scanner.py`.

To update this document after making changes:
```bash
python scripts/architecture_scanner.py
```

The scanner automatically detects:
- New agents added to `agents/` directory
- New scripts in `scripts/` directory
- Knowledge base growth in `learning/knowledge/`
- New documentation in `docs/`
- Test files following `test_*.py` pattern

---

**Last Scan**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Scanner Version**: 1.0
"""

        return md

    def update_architecture_doc(self):
        """Update the architecture documentation file"""
        architecture_md = self.generate_architecture_md()

        doc_path = self.base_path / "docs" / "architecture-overview.md"

        # Save backup
        if doc_path.exists():
            backup_path = doc_path.with_suffix('.md.backup')
            with open(doc_path, 'r') as f:
                backup_content = f.read()
            with open(backup_path, 'w') as f:
                f.write(backup_content)
            print(f"Backed up existing architecture to {backup_path}")

        # Write new architecture
        with open(doc_path, 'w') as f:
            f.write(architecture_md)

        print(f"✅ Architecture documentation updated: {doc_path}")
        print(f"   - Found {len(self.agents)} agents")
        print(f"   - Found {len(self.scripts)} scripts")
        print(f"   - Knowledge base has {sum(self.knowledge_structure.get('by-topic', {}).values())} entries")

        return doc_path


def main():
    """Run the architecture scanner"""
    import argparse

    parser = argparse.ArgumentParser(description="Scan and update architecture documentation")
    parser.add_argument('--path', default=".", help="Base path of the workspace")
    parser.add_argument('--print', action='store_true', help="Print to stdout instead of updating file")

    args = parser.parse_args()

    scanner = ArchitectureScanner(args.path)

    if args.print:
        print(scanner.generate_architecture_md())
    else:
        scanner.update_architecture_doc()


if __name__ == "__main__":
    main()