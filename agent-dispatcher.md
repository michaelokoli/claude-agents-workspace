# Hierarchical Agent System

## Architecture Overview

This is a hierarchical multi-agent system with a Project Coordinator that manages specialized sub-agents.

```
User ←→ Project Coordinator ←→ Specialized Sub-Agents
```

## How to Use This System

1. For complex tasks: Tell Claude to "Use the project coordinator"
2. For simple tasks: Directly trigger specific agents
3. The coordinator will automatically delegate to appropriate sub-agents

## Primary Orchestrator

### Project-Coordinator

* **Role**: Main project manager and orchestrator
* **Trigger**: Complex multi-step requests, "analyze and summarize", "research and create"
* **Action**: Breaks down tasks, delegates to sub-agents, synthesizes results
* **Tools**: read_file, write_to_file, bash, task

## Specialized Sub-Agents

### Media-Fetcher

* **Trigger**: "fetch transcript", "get content from", YouTube/podcast/article URLs
* **Action**: Fetches content from YouTube, podcasts, articles, PDFs
* **Tools**: bash, read_file, write_to_file, web_fetch

### Content-Analyzer

* **Trigger**: "analyze content", "extract insights", "identify key concepts"
* **Action**: Deep analysis of fetched content for learning and insights
* **Tools**: read_file, write_to_file, bash

### Summary-Agent

* **Trigger**: "summarize", "recap", "TL;DR", "what did we accomplish"
* **Action**: Creates concise summaries of work or content
* **Tools**: read_file, write_to_file, bash

### Code-Reviewer

* **Trigger**: "review code", "check Python file", "code review"
* **Action**: Analyzes Python code for best practices and issues
* **Tools**: read_file, bash

### Greeting-Agent

* **Trigger**: "hello", "hi", "hey", "good morning"
* **Action**: Provides friendly greeting responses
* **Tools**: bash

### Meta-Agent

* **Trigger**: "create agent", "build agent", "new agent"
* **Action**: Creates new agent configurations
* **Tools**: write_to_file, read_file

## Workflow Examples

### Example 1: YouTube Learning
**User**: "Learn from this YouTube video [URL] and create study notes"

**Process**:
1. Project-Coordinator receives request
2. Delegates to Media-Fetcher to get transcript
3. Delegates to Content-Analyzer for insights
4. Delegates to Summary-Agent for study notes format
5. Coordinator synthesizes and presents final study notes

### Example 2: Multi-Source Research
**User**: "Compare these 3 YouTube videos about machine learning"

**Process**:
1. Project-Coordinator plans parallel fetching
2. Media-Fetcher runs 3 parallel transcript fetches
3. Content-Analyzer analyzes each transcript
4. Coordinator creates comparison matrix
5. Summary-Agent creates executive summary

### Example 3: Simple Greeting
**User**: "Hello!"

**Process**:
1. Greeting-Agent triggered directly
2. Returns friendly response

## Implementation Instructions

When triggered:
1. For complex tasks → Route to Project-Coordinator
2. For simple tasks → Route to specific agent
3. Read agent YAML from `agents/` directory
4. Execute system_prompt instructions
5. Return results in specified format

## Adding New Agents

1. Use Meta-Agent to generate configuration
2. Place in `agents/` directory
3. Update this dispatcher documentation
4. Test with Project-Coordinator

## File Structure

```
agents/
├── project-coordinator.yml   # Main orchestrator
├── media-fetcher.yml         # Content fetching
├── content-analyzer.yml      # Analysis engine
├── summary-agent.yml         # Summarization
├── code-reviewer.yml         # Code analysis
├── greeting-agent.yml        # Greetings
└── meta-agent.yml           # Agent creation

scripts/
├── get_transcript.py         # YouTube transcript fetcher
└── test_agents.py           # Test suite
```

## Testing

Run `python test_agents.py` to validate agent system functionality.
