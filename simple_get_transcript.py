#!/usr/bin/env python3
"""
Simple YouTube Transcript Fetcher
Fetches transcripts from YouTube videos using video ID or URL
"""

import sys
import re
from youtube_transcript_api import YouTubeTranscriptApi


def extract_video_id(url_or_id):
    """Extract video ID from YouTube URL or return the ID if already provided"""
    # If it's already just an ID (11 characters)
    if re.match(r'^[a-zA-Z0-9_-]{11}$', url_or_id):
        return url_or_id

    # Try to extract from various YouTube URL formats
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([a-zA-Z0-9_-]{11})',
        r'youtube\.com\/watch\?.*&v=([a-zA-Z0-9_-]{11})'
    ]

    for pattern in patterns:
        match = re.search(pattern, url_or_id)
        if match:
            return match.group(1)

    return None


def get_transcript(video_id):
    """Fetch transcript for a YouTube video"""
    try:
        # Create an instance and fetch transcript
        api = YouTubeTranscriptApi()
        transcript = api.fetch(video_id)

        # Format the transcript
        full_text = []
        for snippet in transcript.snippets:
            text = snippet.text.replace('\n', ' ')
            full_text.append(text)

        return ' '.join(full_text)

    except Exception as e:
        return f"Error fetching transcript: {str(e)}"


def main():
    if len(sys.argv) < 2:
        print("Usage: python simple_get_transcript.py <YouTube URL or Video ID>")
        print("Example: python simple_get_transcript.py https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        print("         python simple_get_transcript.py dQw4w9WgXcQ")
        sys.exit(1)

    url_or_id = sys.argv[1]
    video_id = extract_video_id(url_or_id)

    if not video_id:
        print(f"Error: Could not extract video ID from '{url_or_id}'")
        sys.exit(1)

    print(f"Fetching transcript for video ID: {video_id}")
    print("-" * 50)

    transcript = get_transcript(video_id)
    print(transcript)


if __name__ == "__main__":
    main()