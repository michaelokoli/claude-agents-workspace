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
- **content-analyzer** - Analyzes content for insights, learning points, and actionable knowledge
- **summary-agent** - Creates concise summaries in multiple formats
- **code-reviewer** - Reviews Python code for best practices and issues
- **greeting-agent** - Handles user greetings with friendly responses
- **meta-agent** - Creates new agent configurations

## 🚀 Features

- **Hierarchical Task Management**: Complex requests are broken down and delegated efficiently
- **Context Isolation**: Each sub-agent operates in its own context window
- **Parallel Processing**: Multiple sub-agents can work simultaneously
- **YouTube Transcript Fetching**: Fixed and working implementation
- **Comprehensive Testing**: Includes test suite for validation

## 📁 Project Structure

```
agents/                 # Agent configuration files
├── project-coordinator.yml
├── media-fetcher.yml
├── content-analyzer.yml
├── summary-agent.yml
├── code-reviewer.yml
├── greeting-agent.yml
└── meta-agent.yml

scripts/
├── get_transcript.py   # YouTube transcript fetcher (fixed)
├── test_agents.py      # Comprehensive test suite
└── simple_get_transcript.py # Backup transcript fetcher

docs/
├── agent-dispatcher.md # System documentation
└── implementation-report.md # Detailed implementation report
```

## 🔧 Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install youtube-transcript-api
   ```
3. Configure Claude Code to use the agents directory

## 🎯 Usage Examples

### YouTube Video Analysis
```
"Learn from this YouTube video [URL] and create study notes"
```

### Multi-Source Research
```
"Compare these 3 YouTube videos about machine learning"
```

### Code Review
```
"Review this Python file for best practices"
```

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

- Implemented hierarchical multi-agent architecture
- Fixed YouTube transcript fetching issues
- Added comprehensive test suite
- Created specialized agents for content processing
- Enhanced agent communication patterns

## 🤝 Contributing

Feel free to create new agents using the meta-agent or enhance existing ones. Follow the agent YAML structure documented in the implementation report.

## 📄 License

This project is part of the Claude Code ecosystem and follows standard open-source practices.

---

🤖 Built with Claude Code