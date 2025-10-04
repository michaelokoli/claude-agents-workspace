#!/usr/bin/env python3
"""
Test script to demonstrate project-coordinator logging functionality.
This simulates how the coordinator would log sub-agent delegations.

Run with: python test_coordinator_logging.py 2>coordinator.log
Then view logs: cat coordinator.log
"""

import sys
import time
import random
from datetime import datetime, timedelta

class CoordinatorLogger:
    """Simulates project-coordinator logging behavior"""

    def __init__(self):
        self.start_time = datetime.utcnow()
        self.agents_used = 0
        self.tasks_completed = 0
        self.errors_encountered = 0

    def log(self, event_type, **kwargs):
        """Log an event to stderr with structured format"""
        timestamp = datetime.utcnow().isoformat() + "Z"

        # Build key-value pairs
        kv_pairs = []
        for key, value in kwargs.items():
            # Convert key from snake_case to readable format
            readable_key = key.replace('_', ' ').title()
            kv_pairs.append(f"{readable_key}: {value}")

        # Construct log line
        if kv_pairs:
            log_line = f"[{timestamp}] COORDINATOR | {event_type} | {' | '.join(kv_pairs)}"
        else:
            log_line = f"[{timestamp}] COORDINATOR | {event_type}"

        # Always log to stderr
        print(log_line, file=sys.stderr)

    def simulate_youtube_analysis(self, video_url):
        """Simulate a full YouTube video analysis workflow with logging"""

        # Task initiation
        self.log("TASK_START", request="Analyze YouTube video and create knowledge base entry")
        time.sleep(0.1)  # Simulate processing time

        # Analysis phase
        tasks = ['fetch_transcript', 'analyze_content', 'extract_claims', 'build_knowledge']
        self.log("ANALYSIS", tasks_identified=str(tasks))
        self.log("PLANNING", execution_order="sequential (data pipeline)")
        time.sleep(0.1)

        # Task 1: Media Fetcher
        self.log("DELEGATING", agent="media-fetcher", task="Fetch YouTube transcript")
        self.log("STATUS_CHANGE", task="fetch_transcript", from_status="PENDING", to="IN_PROGRESS")

        # Simulate agent work
        time.sleep(random.uniform(0.5, 1.5))
        self.agents_used += 1

        # Simulate success
        self.log("RESPONSE_RECEIVED", agent="media-fetcher", status="SUCCESS")
        self.log("RESULT_SUMMARY", agent="media-fetcher",
                output="Transcript saved to learning/raw-transcripts/XuvKFsktX0Q.txt (563 segments)")
        self.log("STATUS_CHANGE", task="fetch_transcript", from_status="IN_PROGRESS", to="COMPLETED")
        self.tasks_completed += 1
        time.sleep(0.1)

        # Task 2: Content Analyzer
        self.log("DELEGATING", agent="content-analyzer", task="Analyze content and extract claims")
        self.log("PROMPT_SENT", agent="content-analyzer", context_length="12500 tokens")
        self.log("STATUS_CHANGE", task="analyze_content", from_status="PENDING", to="IN_PROGRESS")

        time.sleep(random.uniform(1.0, 2.0))
        self.agents_used += 1

        # Simulate random error (20% chance)
        if random.random() < 0.2:
            self.log("ERROR", agent="content-analyzer", error="Token limit exceeded")
            self.log("FALLBACK", original="content-analyzer", alternative="Retry with chunking")
            self.errors_encountered += 1
            time.sleep(0.5)
            # Retry with success
            self.log("RESPONSE_RECEIVED", agent="content-analyzer", status="SUCCESS (after retry)")
        else:
            self.log("RESPONSE_RECEIVED", agent="content-analyzer", status="SUCCESS")

        self.log("RESULT_SUMMARY", agent="content-analyzer",
                output="15 claims extracted (5 recommendations, 2 predictions, 8 opinions)")
        self.log("STATUS_CHANGE", task="analyze_content", from_status="IN_PROGRESS", to="COMPLETED")
        self.tasks_completed += 1
        time.sleep(0.1)

        # Task 3: Knowledge Builder
        self.log("DELEGATING", agent="knowledge-builder", task="Create knowledge base entry")
        self.log("STATUS_CHANGE", task="build_knowledge", from_status="PENDING", to="IN_PROGRESS")

        time.sleep(random.uniform(0.8, 1.2))
        self.agents_used += 1

        self.log("RESPONSE_RECEIVED", agent="knowledge-builder", status="SUCCESS")
        self.log("RESULT_SUMMARY", agent="knowledge-builder",
                output="Entry created: learning/knowledge/by-topic/claude-agents/2025-10-test.md")
        self.log("STATUS_CHANGE", task="build_knowledge", from_status="IN_PROGRESS", to="COMPLETED")
        self.tasks_completed += 1

        # Final metrics
        end_time = datetime.utcnow()
        duration = (end_time - self.start_time).total_seconds()
        self.log("TASK_COMPLETE", total_time=f"{duration:.2f} seconds")
        self.log("METRICS",
                agents_used=self.agents_used,
                tasks_completed=self.tasks_completed,
                errors=self.errors_encountered)

    def simulate_multi_video_comparison(self, video_urls):
        """Simulate comparing multiple videos with parallel processing"""

        self.log("TASK_START", request=f"Compare {len(video_urls)} YouTube videos")
        time.sleep(0.1)

        # Analysis
        tasks = ['fetch_transcripts_parallel', 'analyze_parallel', 'compare_findings', 'synthesize']
        self.log("ANALYSIS", tasks_identified=str(tasks))
        self.log("PLANNING", execution_order="parallel fetch -> parallel analyze -> sequential synthesis")
        time.sleep(0.1)

        # Parallel fetch simulation
        self.log("STATUS_CHANGE", task="fetch_transcripts_parallel", from_status="PENDING", to="IN_PROGRESS")
        for i, url in enumerate(video_urls, 1):
            self.log("DELEGATING", agent=f"media-fetcher-{i}", task=f"Fetch transcript {i}")
            self.agents_used += 1

        time.sleep(random.uniform(1.0, 1.5))  # Simulate parallel work

        for i in range(len(video_urls)):
            self.log("RESPONSE_RECEIVED", agent=f"media-fetcher-{i+1}", status="SUCCESS")
            self.tasks_completed += 1

        self.log("STATUS_CHANGE", task="fetch_transcripts_parallel", from_status="IN_PROGRESS", to="COMPLETED")

        # Continue with analysis...
        # (truncated for brevity)

        # Final metrics
        end_time = datetime.utcnow()
        duration = (end_time - self.start_time).total_seconds()
        self.log("TASK_COMPLETE", total_time=f"{duration:.2f} seconds")
        self.log("METRICS",
                agents_used=self.agents_used,
                tasks_completed=self.tasks_completed,
                errors=self.errors_encountered)


def main():
    """Run test scenarios"""
    print("=== Coordinator Logging Test ===", file=sys.stdout)
    print("Logs are being written to stderr.", file=sys.stdout)
    print("To capture logs: python test_coordinator_logging.py 2>coordinator.log\n", file=sys.stdout)

    # Create logger instance
    logger = CoordinatorLogger()

    # Test 1: Single video analysis
    print("Test 1: Single YouTube video analysis...", file=sys.stdout)
    logger.simulate_youtube_analysis("https://youtube.com/watch?v=XuvKFsktX0Q")

    print("\nTest 1 complete!", file=sys.stdout)
    time.sleep(1)

    # Reset for test 2
    logger = CoordinatorLogger()

    # Test 2: Multi-video comparison
    print("\nTest 2: Multi-video comparison...", file=sys.stdout)
    video_urls = [
        "https://youtube.com/watch?v=video1",
        "https://youtube.com/watch?v=video2",
        "https://youtube.com/watch?v=video3"
    ]
    logger.simulate_multi_video_comparison(video_urls)

    print("\nTest 2 complete!", file=sys.stdout)

    print("\n=== All tests complete ===", file=sys.stdout)
    print("Check the log output to see structured logging in action.", file=sys.stdout)
    print("\nExample commands to analyze logs:", file=sys.stdout)
    print("  grep 'DELEGATING' coordinator.log     # See all delegations", file=sys.stdout)
    print("  grep 'ERROR' coordinator.log          # Find errors", file=sys.stdout)
    print("  grep 'METRICS' coordinator.log        # See performance metrics", file=sys.stdout)


if __name__ == "__main__":
    main()