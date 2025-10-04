#!/usr/bin/env python3

import sys
import re
from youtube_transcript_api import YouTubeTranscriptApi

def extract_video_id(url):
    """Extract video ID from YouTube URL"""
    # Handle different YouTube URL formats
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
        r'(?:embed\/)([0-9A-Za-z_-]{11})',
        r'(?:youtu\.be\/)([0-9A-Za-z_-]{11})'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    # Assume it's already a video ID if no pattern matches
    return url

def main():
    if len(sys.argv) < 2:
        print("Usage: python simple_get_transcript.py <YouTube_URL>")
        sys.exit(1)
    
    url = sys.argv[1]
    video_id = extract_video_id(url)
    
    print(f"Fetching transcript for video ID: {video_id}")
    
    try:
        # Get transcript
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        
        # Extract just the text
        text_only = '\n'.join([entry['text'] for entry in transcript])
        
        # Save to file
        filename = f"learning/raw-transcripts/{video_id}.txt"
        
        # Create directory if it doesn't exist
        import os
        os.makedirs('learning/raw-transcripts', exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(text_only)
        
        print(f"\n✅ Success!")
        print(f"Transcript saved to: {filename}")
        print(f"Total segments: {len(transcript)}")
        print(f"\nFirst 200 characters:")
        print(text_only[:200] + "...")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nTroubleshooting:")
        print("1. Check if video has captions")
        print("2. Try running: pip install --upgrade youtube-transcript-api")
        print("3. Video might be private or age-restricted")

if __name__ == "__main__":
    main()