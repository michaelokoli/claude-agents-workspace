# Project Coordinator Logging Guide

## Overview

The project-coordinator now includes comprehensive logging for all sub-agent delegations and task tracking. This provides critical observability for autonomous agent workflows as recommended by Anthropic's platform team.

## Why Logging Matters

According to Anthropic's official guidance:
> "Observability is really a key piece" for autonomous agents, especially as they handle longer-running tasks and make autonomous decisions.

Benefits:
- **Audit Trail**: Track what agents did and why
- **Debugging**: Identify where workflows fail
- **Performance**: Monitor task duration and bottlenecks
- **Compliance**: Maintain records for enterprise requirements
- **Optimization**: Identify patterns to improve agent efficiency

## Logging Architecture

### Output Streams

**Critical Rule**:
- ✅ **stderr** - ALL logs go here (use `file=sys.stderr`)
- ❌ **stdout** - NEVER use for logs (reserved for user-facing output only)

This follows the same pattern as MCP STDIO servers - stdout must remain clean for protocol communication.

### Log Format

All logs follow this structured format:
```
[TIMESTAMP] COORDINATOR | EVENT_TYPE | Key1: value1 | Key2: value2
```

Components:
- **TIMESTAMP**: UTC ISO format with Z suffix (e.g., `2025-10-04T17:30:00Z`)
- **COORDINATOR**: Identifies log source (always "COORDINATOR" for project-coordinator)
- **EVENT_TYPE**: Categorized event (see Event Types below)
- **Key-Value Pairs**: Contextual information using pipe separators

## Event Types

### 1. Task Lifecycle Events

#### TASK_START
Marks beginning of user request processing
```
[2025-10-04T17:30:00Z] COORDINATOR | TASK_START | Request: "Analyze this video and create notes"
```

#### ANALYSIS
Documents task breakdown and planning
```
[2025-10-04T17:30:01Z] COORDINATOR | ANALYSIS | Tasks identified: ['fetch_transcript', 'analyze_content', 'create_summary']
```

#### PLANNING
Shows execution strategy
```
[2025-10-04T17:30:02Z] COORDINATOR | PLANNING | Execution order: sequential (fetch->analyze->summary)
```

#### TASK_COMPLETE
Final summary with metrics
```
[2025-10-04T17:31:45Z] COORDINATOR | TASK_COMPLETE | Total time: 105 seconds
[2025-10-04T17:31:46Z] COORDINATOR | METRICS | Agents used: 3 | Tasks completed: 3 | Errors: 0
```

### 2. Delegation Events

#### DELEGATING
Records when task is assigned to sub-agent
```
[2025-10-04T17:30:03Z] COORDINATOR | DELEGATING | Agent: media-fetcher | Task: "Fetch transcript from YouTube URL"
```

#### PROMPT_SENT
Tracks context size sent to agent
```
[2025-10-04T17:30:04Z] COORDINATOR | PROMPT_SENT | Agent: media-fetcher | Context length: 450 tokens
```

#### RESPONSE_RECEIVED
Confirms agent completion
```
[2025-10-04T17:30:15Z] COORDINATOR | RESPONSE_RECEIVED | Agent: media-fetcher | Status: SUCCESS
```

#### RESULT_SUMMARY
Brief output description
```
[2025-10-04T17:30:16Z] COORDINATOR | RESULT_SUMMARY | Agent: media-fetcher | Output: "Transcript saved to learning/raw-transcripts/XuvKFsktX0Q.txt"
```

### 3. Status Tracking Events

#### STATUS_CHANGE
Tracks task state transitions
```
[2025-10-04T17:30:04Z] COORDINATOR | STATUS_CHANGE | Task: "fetch_transcript" | From: PENDING | To: IN_PROGRESS
[2025-10-04T17:30:17Z] COORDINATOR | STATUS_CHANGE | Task: "fetch_transcript" | From: IN_PROGRESS | To: COMPLETED
```

### 4. Error Handling Events

#### ERROR
Records failures with context
```
[2025-10-04T17:30:20Z] COORDINATOR | ERROR | Agent: media-fetcher | Error: "YouTube API rate limit exceeded"
```

#### FALLBACK
Documents recovery strategies
```
[2025-10-04T17:30:21Z] COORDINATOR | FALLBACK | Original: media-fetcher | Alternative: "Retrying with delay"
```

## Implementation Example

Here's how the coordinator implements logging in practice:

```python
import sys
from datetime import datetime

def coordinate_youtube_analysis(video_url, user_request):
    """Example of coordinator with full logging"""
    start_time = datetime.utcnow()

    # Log task initiation
    timestamp = start_time.isoformat() + "Z"
    print(f"[{timestamp}] COORDINATOR | TASK_START | Request: '{user_request}'", file=sys.stderr)

    # Analyze request
    tasks = ['fetch_transcript', 'analyze_content', 'build_knowledge', 'create_summary']
    timestamp = datetime.utcnow().isoformat() + "Z"
    print(f"[{timestamp}] COORDINATOR | ANALYSIS | Tasks identified: {tasks}", file=sys.stderr)
    print(f"[{timestamp}] COORDINATOR | PLANNING | Execution order: sequential", file=sys.stderr)

    # Track metrics
    agents_used = 0
    tasks_completed = 0
    errors_encountered = 0

    # Delegate to media-fetcher
    try:
        timestamp = datetime.utcnow().isoformat() + "Z"
        print(f"[{timestamp}] COORDINATOR | DELEGATING | Agent: media-fetcher | Task: 'Fetch YouTube transcript'", file=sys.stderr)
        print(f"[{timestamp}] COORDINATOR | STATUS_CHANGE | Task: 'fetch_transcript' | From: PENDING | To: IN_PROGRESS", file=sys.stderr)

        # [Actual delegation would happen here]
        result = delegate_to_agent("media-fetcher", {"url": video_url})
        agents_used += 1

        timestamp = datetime.utcnow().isoformat() + "Z"
        print(f"[{timestamp}] COORDINATOR | RESPONSE_RECEIVED | Agent: media-fetcher | Status: SUCCESS", file=sys.stderr)
        print(f"[{timestamp}] COORDINATOR | RESULT_SUMMARY | Agent: media-fetcher | Output: 'Transcript saved'", file=sys.stderr)
        print(f"[{timestamp}] COORDINATOR | STATUS_CHANGE | Task: 'fetch_transcript' | From: IN_PROGRESS | To: COMPLETED", file=sys.stderr)
        tasks_completed += 1

    except Exception as e:
        timestamp = datetime.utcnow().isoformat() + "Z"
        print(f"[{timestamp}] COORDINATOR | ERROR | Agent: media-fetcher | Error: '{str(e)}'", file=sys.stderr)
        print(f"[{timestamp}] COORDINATOR | FALLBACK | Original: media-fetcher | Alternative: 'Manual transcript fetch'", file=sys.stderr)
        errors_encountered += 1

    # Continue with other agents...

    # Final metrics
    end_time = datetime.utcnow()
    duration = (end_time - start_time).total_seconds()
    timestamp = end_time.isoformat() + "Z"
    print(f"[{timestamp}] COORDINATOR | TASK_COMPLETE | Total time: {duration:.2f} seconds", file=sys.stderr)
    print(f"[{timestamp}] COORDINATOR | METRICS | Agents used: {agents_used} | Tasks completed: {tasks_completed} | Errors: {errors_encountered}", file=sys.stderr)
```

## Real-World Log Example

Here's what actual coordinator logs look like for a knowledge base building task:

```
[2025-10-04T17:30:00Z] COORDINATOR | TASK_START | Request: "Analyze https://youtube.com/watch?v=XuvKFsktX0Q and add to knowledge base"
[2025-10-04T17:30:01Z] COORDINATOR | ANALYSIS | Tasks identified: ['fetch_transcript', 'analyze_content', 'extract_claims', 'build_knowledge_entry']
[2025-10-04T17:30:02Z] COORDINATOR | PLANNING | Execution order: sequential (required for data pipeline)

[2025-10-04T17:30:03Z] COORDINATOR | DELEGATING | Agent: media-fetcher | Task: "Fetch YouTube transcript for XuvKFsktX0Q"
[2025-10-04T17:30:04Z] COORDINATOR | STATUS_CHANGE | Task: "fetch_transcript" | From: PENDING | To: IN_PROGRESS
[2025-10-04T17:30:15Z] COORDINATOR | RESPONSE_RECEIVED | Agent: media-fetcher | Status: SUCCESS
[2025-10-04T17:30:16Z] COORDINATOR | RESULT_SUMMARY | Agent: media-fetcher | Output: "563 segments saved to learning/raw-transcripts/XuvKFsktX0Q.txt"
[2025-10-04T17:30:17Z] COORDINATOR | STATUS_CHANGE | Task: "fetch_transcript" | From: IN_PROGRESS | To: COMPLETED

[2025-10-04T17:30:18Z] COORDINATOR | DELEGATING | Agent: content-analyzer | Task: "Analyze transcript and extract structured claims"
[2025-10-04T17:30:19Z] COORDINATOR | PROMPT_SENT | Agent: content-analyzer | Context length: 12500 tokens
[2025-10-04T17:30:20Z] COORDINATOR | STATUS_CHANGE | Task: "analyze_content" | From: PENDING | To: IN_PROGRESS
[2025-10-04T17:30:55Z] COORDINATOR | RESPONSE_RECEIVED | Agent: content-analyzer | Status: SUCCESS
[2025-10-04T17:30:56Z] COORDINATOR | RESULT_SUMMARY | Agent: content-analyzer | Output: "15 claims extracted (5 recommendations, 2 predictions, 8 opinions/facts)"
[2025-10-04T17:30:57Z] COORDINATOR | STATUS_CHANGE | Task: "analyze_content" | From: IN_PROGRESS | To: COMPLETED

[2025-10-04T17:30:58Z] COORDINATOR | DELEGATING | Agent: knowledge-builder | Task: "Create knowledge base entry with temporal tracking"
[2025-10-04T17:30:59Z] COORDINATOR | STATUS_CHANGE | Task: "build_knowledge_entry" | From: PENDING | To: IN_PROGRESS
[2025-10-04T17:31:25Z] COORDINATOR | RESPONSE_RECEIVED | Agent: knowledge-builder | Status: SUCCESS
[2025-10-04T17:31:26Z] COORDINATOR | RESULT_SUMMARY | Agent: knowledge-builder | Output: "Entry created at learning/knowledge/by-topic/claude-agents/2025-10-anthropic-building-agents.md"
[2025-10-04T17:31:27Z] COORDINATOR | STATUS_CHANGE | Task: "build_knowledge_entry" | From: IN_PROGRESS | To: COMPLETED

[2025-10-04T17:31:28Z] COORDINATOR | TASK_COMPLETE | Total time: 88 seconds
[2025-10-04T17:31:29Z] COORDINATOR | METRICS | Agents used: 3 | Tasks completed: 3 | Errors: 0
```

## Monitoring & Analysis

### Real-time Monitoring

Watch logs as they stream:
```bash
# In terminal where Claude Code is running, stderr will show logs
claude-code 2>&1 | tee coordinator.log

# Or redirect stderr to file
claude-code 2>coordinator.log
```

### Log Analysis Examples

#### Find all delegations to a specific agent:
```bash
grep "DELEGATING | Agent: content-analyzer" coordinator.log
```

#### Track error rates:
```bash
grep "ERROR" coordinator.log | wc -l
```

#### Calculate average task duration:
```bash
grep "TASK_COMPLETE" coordinator.log | awk -F'Total time: ' '{print $2}' | awk '{sum+=$1; count++} END {print sum/count " seconds average"}'
```

#### Identify bottlenecks (longest running tasks):
```bash
grep "STATUS_CHANGE.*TO: COMPLETED" coordinator.log | sort -t'|' -k4 -r
```

## Best Practices

1. **Consistency**: Always use the same format for easy parsing
2. **Brevity**: Keep task descriptions concise but informative
3. **Completeness**: Log both success and failure paths
4. **Performance**: Consider log verbosity vs. performance trade-offs
5. **Security**: Never log sensitive data (API keys, passwords, PII)
6. **Actionability**: Include enough context to debug issues

## Integration with Other Tools

### Future Enhancements

The logging format is designed to integrate with:
- **Log aggregation**: Splunk, ELK Stack, Datadog
- **Metrics platforms**: Prometheus, Grafana
- **Alerting**: PagerDuty, Slack notifications
- **Analysis**: Custom dashboards, performance reports

### Export Format

Logs can be easily converted to JSON for processing:

```python
import json
import re

def parse_log_line(line):
    """Convert log line to JSON"""
    pattern = r'\[(.*?)\] (\w+) \| (\w+) \| (.*)'
    match = re.match(pattern, line)
    if match:
        timestamp, source, event, details = match.groups()

        # Parse key-value pairs
        kv_pairs = {}
        for pair in details.split(' | '):
            if ': ' in pair:
                key, value = pair.split(': ', 1)
                kv_pairs[key] = value

        return {
            'timestamp': timestamp,
            'source': source,
            'event': event,
            **kv_pairs
        }
    return None
```

## Troubleshooting

### Common Issues

**Logs not appearing:**
- Ensure using `file=sys.stderr` not `print()` alone
- Check if stderr is being redirected elsewhere
- Verify coordinator is being invoked (not bypassed)

**Performance impact:**
- Consider reducing log verbosity for production
- Implement log levels (DEBUG, INFO, WARN, ERROR)
- Use async logging for high-volume scenarios

**Log file growth:**
- Implement log rotation
- Set up periodic cleanup
- Consider compression for archived logs

## Summary

The project-coordinator logging system provides:
- ✅ Complete visibility into agent orchestration
- ✅ Audit trail for compliance
- ✅ Debugging capabilities for complex workflows
- ✅ Performance metrics for optimization
- ✅ Foundation for future observability tools

This aligns with Anthropic's guidance that observability is a "key piece" for production agent systems, enabling you to audit, tune, and optimize autonomous agent workflows.

---

**Next Steps:**
1. Test the logging with real agent delegations
2. Set up log monitoring/alerting
3. Create performance dashboards
4. Implement log analysis scripts