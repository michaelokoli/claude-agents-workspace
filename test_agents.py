#!/usr/bin/env python3
"""
Agent System Test Suite
Tests transcript fetching and agent functionality
"""

import sys
import os
import json
import subprocess
from datetime import datetime
from pathlib import Path

class Colors:
    """Terminal colors for output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

class TestResult:
    """Store test results"""
    def __init__(self, name, status, details=""):
        self.name = name
        self.status = status  # "pass", "fail", "skip"
        self.details = details
        self.timestamp = datetime.now()

class AgentTestSuite:
    """Test suite for agent system"""

    def __init__(self):
        self.results = []
        self.test_videos = [
            ("https://www.youtube.com/watch?v=dQw4w9WgXcQ", "Rick Astley - Never Gonna Give You Up"),
            ("https://www.youtube.com/watch?v=jNQXAC9IVRw", "Me at the zoo"),  # First YouTube video
            ("invalid_video_id_12345", "Invalid video test"),
        ]

    def run_command(self, cmd):
        """Run shell command and return result"""
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.returncode == 0, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return False, "", "Command timed out"
        except Exception as e:
            return False, "", str(e)

    def test_transcript_fetcher(self):
        """Test get_transcript.py functionality"""
        print(f"\n{Colors.BLUE}Testing Transcript Fetcher{Colors.RESET}")
        print("-" * 50)

        # Test 1: Valid video with captions
        video_url = self.test_videos[0][0]
        print(f"Test 1: Fetching transcript for valid video...")
        success, stdout, stderr = self.run_command(f"python get_transcript.py {video_url}")

        if success:
            # Check if files were created
            video_id = "dQw4w9WgXcQ"
            transcript_file = f"learning/raw-transcripts/{video_id}.txt"
            metadata_file = f"learning/youtube-metadata/{video_id}.json"

            if os.path.exists(transcript_file) and os.path.exists(metadata_file):
                self.results.append(TestResult(
                    "Transcript Fetcher - Valid Video",
                    "pass",
                    f"Successfully fetched and saved transcript"
                ))
                print(f"{Colors.GREEN}✓ Test passed{Colors.RESET}")
            else:
                self.results.append(TestResult(
                    "Transcript Fetcher - Valid Video",
                    "fail",
                    "Files not created properly"
                ))
                print(f"{Colors.RED}✗ Test failed: Files not created{Colors.RESET}")
        else:
            self.results.append(TestResult(
                "Transcript Fetcher - Valid Video",
                "fail",
                stderr
            ))
            print(f"{Colors.RED}✗ Test failed: {stderr}{Colors.RESET}")

        # Test 2: Invalid video ID
        print(f"\nTest 2: Testing error handling with invalid video...")
        success, stdout, stderr = self.run_command(f"python get_transcript.py invalid_id_xyz")

        if not success and "Error" in stderr:
            self.results.append(TestResult(
                "Transcript Fetcher - Error Handling",
                "pass",
                "Properly handled invalid video"
            ))
            print(f"{Colors.GREEN}✓ Error handling works{Colors.RESET}")
        else:
            self.results.append(TestResult(
                "Transcript Fetcher - Error Handling",
                "fail",
                "Did not handle error properly"
            ))
            print(f"{Colors.RED}✗ Error handling failed{Colors.RESET}")

    def test_metadata_structure(self):
        """Test metadata file structure"""
        print(f"\n{Colors.BLUE}Testing Metadata Structure{Colors.RESET}")
        print("-" * 50)

        metadata_file = "learning/youtube-metadata/dQw4w9WgXcQ.json"

        if os.path.exists(metadata_file):
            try:
                with open(metadata_file, 'r') as f:
                    metadata = json.load(f)

                required_fields = ['video_info', 'transcript_with_timestamps', 'total_duration']
                missing_fields = [field for field in required_fields if field not in metadata]

                if not missing_fields:
                    self.results.append(TestResult(
                        "Metadata Structure",
                        "pass",
                        "All required fields present"
                    ))
                    print(f"{Colors.GREEN}✓ Metadata structure valid{Colors.RESET}")
                else:
                    self.results.append(TestResult(
                        "Metadata Structure",
                        "fail",
                        f"Missing fields: {missing_fields}"
                    ))
                    print(f"{Colors.RED}✗ Missing fields: {missing_fields}{Colors.RESET}")
            except Exception as e:
                self.results.append(TestResult(
                    "Metadata Structure",
                    "fail",
                    str(e)
                ))
                print(f"{Colors.RED}✗ Failed to parse metadata: {e}{Colors.RESET}")
        else:
            self.results.append(TestResult(
                "Metadata Structure",
                "skip",
                "Metadata file not found"
            ))
            print(f"{Colors.YELLOW}⚠ Skipped: Metadata file not found{Colors.RESET}")

    def test_agent_files(self):
        """Test agent configuration files"""
        print(f"\n{Colors.BLUE}Testing Agent Configurations{Colors.RESET}")
        print("-" * 50)

        agent_dir = Path("agents")
        required_agents = [
            "meta-agent.yml",
            "greeting-agent.yml",
            "code-reviewer.yml"
        ]

        for agent_file in required_agents:
            agent_path = agent_dir / agent_file
            if agent_path.exists():
                # Check if it's valid YAML structure
                try:
                    with open(agent_path, 'r') as f:
                        content = f.read()
                        if 'name:' in content and 'tools:' in content and 'system_prompt:' in content:
                            self.results.append(TestResult(
                                f"Agent Config - {agent_file}",
                                "pass",
                                "Valid structure"
                            ))
                            print(f"{Colors.GREEN}✓ {agent_file} valid{Colors.RESET}")
                        else:
                            self.results.append(TestResult(
                                f"Agent Config - {agent_file}",
                                "fail",
                                "Missing required fields"
                            ))
                            print(f"{Colors.RED}✗ {agent_file} missing fields{Colors.RESET}")
                except Exception as e:
                    self.results.append(TestResult(
                        f"Agent Config - {agent_file}",
                        "fail",
                        str(e)
                    ))
                    print(f"{Colors.RED}✗ {agent_file} error: {e}{Colors.RESET}")
            else:
                self.results.append(TestResult(
                    f"Agent Config - {agent_file}",
                    "fail",
                    "File not found"
                ))
                print(f"{Colors.RED}✗ {agent_file} not found{Colors.RESET}")

    def test_directory_structure(self):
        """Test required directory structure"""
        print(f"\n{Colors.BLUE}Testing Directory Structure{Colors.RESET}")
        print("-" * 50)

        required_dirs = [
            "agents",
            "learning/raw-transcripts",
            "learning/youtube-metadata"
        ]

        for dir_path in required_dirs:
            if os.path.exists(dir_path) and os.path.isdir(dir_path):
                self.results.append(TestResult(
                    f"Directory - {dir_path}",
                    "pass",
                    "Exists"
                ))
                print(f"{Colors.GREEN}✓ {dir_path} exists{Colors.RESET}")
            else:
                self.results.append(TestResult(
                    f"Directory - {dir_path}",
                    "fail",
                    "Not found"
                ))
                print(f"{Colors.RED}✗ {dir_path} not found{Colors.RESET}")

    def generate_report(self):
        """Generate test report"""
        print(f"\n{Colors.BLUE}{'='*60}{Colors.RESET}")
        print(f"{Colors.BLUE}Test Report Summary{Colors.RESET}")
        print(f"{Colors.BLUE}{'='*60}{Colors.RESET}")

        passed = sum(1 for r in self.results if r.status == "pass")
        failed = sum(1 for r in self.results if r.status == "fail")
        skipped = sum(1 for r in self.results if r.status == "skip")
        total = len(self.results)

        print(f"\nTotal Tests: {total}")
        print(f"{Colors.GREEN}Passed: {passed}{Colors.RESET}")
        print(f"{Colors.RED}Failed: {failed}{Colors.RESET}")
        print(f"{Colors.YELLOW}Skipped: {skipped}{Colors.RESET}")

        if failed > 0:
            print(f"\n{Colors.RED}Failed Tests:{Colors.RESET}")
            for result in self.results:
                if result.status == "fail":
                    print(f"  - {result.name}: {result.details}")

        # Save report to file
        report_file = f"test-report-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total": total,
                "passed": passed,
                "failed": failed,
                "skipped": skipped
            },
            "results": [
                {
                    "name": r.name,
                    "status": r.status,
                    "details": r.details,
                    "timestamp": r.timestamp.isoformat()
                }
                for r in self.results
            ]
        }

        with open(report_file, 'w') as f:
            json.dump(report_data, f, indent=2)

        print(f"\n{Colors.BLUE}Report saved to: {report_file}{Colors.RESET}")

        return failed == 0

    def run_all_tests(self):
        """Run all tests"""
        print(f"{Colors.BLUE}{'='*60}{Colors.RESET}")
        print(f"{Colors.BLUE}Agent System Test Suite{Colors.RESET}")
        print(f"{Colors.BLUE}{'='*60}{Colors.RESET}")

        self.test_directory_structure()
        self.test_transcript_fetcher()
        self.test_metadata_structure()
        self.test_agent_files()

        success = self.generate_report()

        if success:
            print(f"\n{Colors.GREEN}✅ All tests passed!{Colors.RESET}")
        else:
            print(f"\n{Colors.RED}❌ Some tests failed. Please review the report.{Colors.RESET}")

        return success


if __name__ == "__main__":
    suite = AgentTestSuite()
    success = suite.run_all_tests()
    sys.exit(0 if success else 1)