# Claude Agents Workspace

A hierarchical multi-agent system for Claude Code that enables sophisticated task orchestration and content analysis.

## 🏗️ Architecture

```
User ←→ Project Coordinator ←→ Specialized Sub-Agents
```

The system uses a Project Coordinator as the main orchestrator that delegates tasks to specialized sub-agents, each focused on specific capabilities.

## 📦 Agents

### Core Orchestrator
- **project-coordinator** - Main project manager that breaks down complex tasks and delegates to sub-agents

### Specialized Sub-Agents
- **media-fetcher** - Fetches content from YouTube, podcasts, articles, and PDFs
- **content-analyzer** - Analyzes content for insights and extracts structured knowledge claims
- **knowledge-builder** - Builds temporal knowledge base tracking claim evolution and speaker positions
- **podcast-analyzer** - Specialized analysis for podcast conversations and speaker dynamics
- **summary-agent** - Creates concise summaries in multiple formats
- **code-reviewer** - Reviews Python code for best practices and issues
- **greeting-agent** - Handles user greetings with friendly responses
- **meta-agent** - Creates new agent configurations **+ MCP server builder** ⚡ NEW

## 🚀 Features

- **Hierarchical Task Management**: Complex requests are broken down and delegated efficiently
- **Context Isolation**: Each sub-agent operates in its own context window
- **Parallel Processing**: Multiple sub-agents can work simultaneously
- **YouTube Transcript Fetching**: Fixed and working implementation
- **Podcast Transcription**: Multi-source support with WhisperX integration
- **Temporal Knowledge Base**: Track how ideas, predictions, and speaker positions evolve over time
- **Relationship Tracking**: Automatically detect claims that confirm, contradict, or extend previous content
- **Advanced Search**: Search knowledge base by topic, speaker, date range, or claim type
- **MCP Server Builder**: Meta-agent can now build Model Context Protocol servers to connect AI to external systems ⚡ NEW
- **Comprehensive Testing**: Includes test suite for validation

## 📁 Project Structure

```
agents/                 # Agent configuration files
├── project-coordinator.yml
├── media-fetcher.yml
├── content-analyzer.yml
├── knowledge-builder.yml
├── podcast-analyzer.yml
├── summary-agent.yml
├── code-reviewer.yml
├── greeting-agent.yml
└── meta-agent.yml

scripts/
├── get_transcript.py          # YouTube transcript fetcher (fixed)
├── podcast_processor.py       # Multi-source podcast transcription
├── search_knowledge.py        # Knowledge base search utility
└── test_agents.py             # Comprehensive test suite

learning/
├── raw-transcripts/           # YouTube transcripts
├── podcasts/                  # Podcast audio and transcripts
└── knowledge/                 # Temporal knowledge base
    ├── by-topic/              # Organized by subject
    ├── by-speaker/            # Speaker profiles and timelines
    ├── timeline/              # Chronological entries
    ├── relationships/         # Tracked contradictions and evolution
    └── TEMPLATE.md            # Standard knowledge entry format

docs/
├── agent-dispatcher.md        # System documentation
├── implementation-report.md   # Detailed implementation report
├── podcast-setup.md           # Podcast transcription guide
└── knowledge-base-workflow.md # Knowledge base documentation
```

## 🔧 Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. For podcast transcription (optional):
   ```bash
   # For API mode (simpler)
   export OPENAI_API_KEY="your-api-key"

   # For local mode (see docs/podcast-setup.md)
   pip install whisperx
   ```
4. Configure Claude Code to use the agents directory

## 🎯 Usage Examples

### YouTube Video Analysis with Knowledge Base
```
"Analyze this video and add to knowledge base: https://youtube.com/watch?v=..."
```
The system will:
- Fetch transcript
- Extract structured claims (predictions, data, opinions)
- Create knowledge base entry
- Track relationships with existing entries
- Provide analysis with historical context

### Podcast Analysis with Speaker Tracking
```
"Analyze this podcast: https://open.spotify.com/episode/..."
```
The system will:
- Fetch transcript (YouTube/RSS) or extract metadata (Spotify)
- Identify speakers and their positions
- Track position evolution over time
- Detect contradictions with previous claims

### Multi-Source Comparison
```
"Compare these 3 YouTube videos about machine learning"
```

### Search Knowledge Base
```bash
# Search by topic
python scripts/search_knowledge.py --topic housing-market

# Search by speaker
python scripts/search_knowledge.py --speaker "Dave Meyer"

# Find predictions
python scripts/search_knowledge.py --claim-type prediction

# List all topics
python scripts/search_knowledge.py --list-topics
```

### Code Review
```
"Review this Python file for best practices"
```

### MCP Server Creation ⚡ NEW
```
"Create an MCP server to search my project files"
"Build an MCP server for GitHub operations"
"Make an MCP server that accesses my database"
```
The meta-agent will:
- Generate complete MCP server code (Python or other languages)
- Create Claude Desktop configuration
- Provide installation and testing instructions
- Apply security best practices automatically

See [MCP Meta-Agent Guide](docs/mcp-meta-agent-guide.md) for details.

## ✅ Testing

Run the test suite to validate functionality:
```bash
python test_agents.py
```

Current test status: **8/9 tests passing**

## 🛠️ Technical Details

### YouTube Transcript API Fix
The project includes a corrected implementation for the YouTube Transcript API:
```python
# Correct usage
api = YouTubeTranscriptApi()
transcript_data = api.fetch(video_id)
```

### Agent Communication Flow
1. User prompts Project Coordinator
2. Coordinator analyzes request and delegates to sub-agents
3. Sub-agents execute tasks and report back to Coordinator
4. Coordinator synthesizes results and responds to user

## 📝 Recent Updates

### Agent Architecture Validation (Latest - Oct 2025) 🎯
- **Anthropic official guidance analyzed** - Video from platform leadership team
- **Architecture validated** - 80% aligned with Anthropic's recommendations
- **Claude Code SDK insights** - Confirmed as recommended starting point for agents
- **"Unhobble the model" philosophy** - Less scaffolding, more autonomy validated
- **Roadmap enhanced** - Added observability, business metrics, platform tools integration

### MCP Server Building (Oct 2025) ⚡
- **Meta-agent enhanced with MCP knowledge** - Can now build Model Context Protocol servers
- **Comprehensive MCP guide** - Official docs + video tutorials synthesized
- **Python server templates** - Ready-to-use code generation for Tools, Resources, Prompts
- **Security-conscious** - Automatic validation, error handling, logging best practices
- **Multi-transport support** - STDIO (local) and HTTP (remote) server generation
- **Claude Desktop integration** - Automatic configuration file generation

### Knowledge Base System
- **Temporal knowledge tracking** - Monitor how ideas and predictions evolve
- **Claim extraction** - Structured extraction of predictions, data, opinions, recommendations
- **Speaker position tracking** - See how speakers' views change over time
- **Relationship detection** - Automatically find confirms/contradicts/extends patterns
- **Multi-dimensional search** - Search by topic, speaker, date, claim type
- **Enhanced content-analyzer** - Now extracts structured knowledge for KB integration

### Podcast Support
- **Multi-source transcription** - YouTube, RSS feeds, direct URLs
- **WhisperX integration** - Local or API-based transcription with speaker diarization
- **Spotify handling** - Graceful metadata extraction for DRM-protected content
- **Specialized podcast-analyzer** - Conversation dynamics and speaker attribution

### Core System
- Implemented hierarchical multi-agent architecture
- Fixed YouTube transcript fetching issues
- Added comprehensive test suite
- Created specialized agents for content processing
- Enhanced agent communication patterns

## 🗺️ Roadmap

See [ROADMAP.md](ROADMAP.md) for:
- **Immediate priorities** and bug fixes
- **Short-term plans** (Tier 2 vector database)
- **Medium-term goals** (Tier 3 knowledge graph)
- **Long-term vision** (AI-powered fact-checking, web interface)
- **Completed milestones** and success metrics

## 🤝 Contributing

Feel free to create new agents using the meta-agent or enhance existing ones. Follow the agent YAML structure documented in the implementation report.

Check [ROADMAP.md](ROADMAP.md) for planned features and areas where contributions would be valuable.

## 📄 License

This project is part of the Claude Code ecosystem and follows standard open-source practices.

---

🤖 Built with Claude Code