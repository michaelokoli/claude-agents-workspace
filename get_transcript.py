#!/usr/bin/env python3
"""
YouTube Transcript Fetcher for Claude Code Agents
Saves transcripts for analysis by youtube-learning-agent
"""

import sys
import os
from datetime import datetime
from youtube_transcript_api import YouTubeTranscriptApi
import re
import json

def extract_video_id(url):
    """Extract video ID from various YouTube URL formats"""
    patterns = [
        r'(?:youtube\.com\/watch\?v=)([\w-]+)',
        r'(?:youtu\.be\/)([\w-]+)',
        r'(?:youtube\.com\/embed\/)([\w-]+)',
        r'(?:youtube\.com\/v\/)([\w-]+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    # If no pattern matches, assume it's already a video ID
    return url

def get_video_info(video_id):
    """Get basic video info (you could expand this with youtube-dl if needed)"""
    return {
        'video_id': video_id,
        'url': f'https://youtube.com/watch?v={video_id}',
        'fetched_at': datetime.now().isoformat()
    }

def save_transcript(video_id, transcript_data, metadata=None):
    """Save transcript to file system for agent processing"""
    
    # Create directory structure
    os.makedirs('learning/raw-transcripts', exist_ok=True)
    os.makedirs('learning/youtube-metadata', exist_ok=True)
    
    # Process transcript text (handle snippet objects)
    if transcript_data and hasattr(transcript_data[0], 'text'):
        # Handle snippet objects
        transcript_text = '\n'.join([snippet.text for snippet in transcript_data])
    else:
        # Handle dict format
        transcript_text = '\n'.join([entry['text'] for entry in transcript_data])
    
    # Create filename (sanitize video_id)
    safe_filename = re.sub(r'[^\w\-_]', '_', video_id)
    
    # Save raw transcript
    transcript_path = f'learning/raw-transcripts/{safe_filename}.txt'
    with open(transcript_path, 'w', encoding='utf-8') as f:
        f.write(transcript_text)
    
    # Save metadata with timestamps
    metadata_path = f'learning/youtube-metadata/{safe_filename}.json'

    # Convert snippets to dict format for JSON serialization
    if transcript_data and hasattr(transcript_data[0], 'text'):
        transcript_dict = [
            {'text': s.text, 'start': s.start, 'duration': s.duration}
            for s in transcript_data
        ]
        total_duration = transcript_data[-1].start + transcript_data[-1].duration if transcript_data else 0
    else:
        transcript_dict = transcript_data
        total_duration = transcript_data[-1]['start'] + transcript_data[-1]['duration'] if transcript_data else 0

    full_metadata = {
        'video_info': metadata or get_video_info(video_id),
        'transcript_with_timestamps': transcript_dict,
        'total_duration': total_duration
    }

    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(full_metadata, f, indent=2)
    
    return transcript_path, metadata_path

def main():
    """Main function to fetch and save transcript"""
    
    if len(sys.argv) < 2:
        print("Usage: python get_transcript.py <YouTube_URL_or_ID> [language_code]")
        print("Example: python get_transcript.py https://youtube.com/watch?v=abc123")
        print("Example: python get_transcript.py abc123 en")
        sys.exit(1)
    
    url_or_id = sys.argv[1]
    language = sys.argv[2] if len(sys.argv) > 2 else 'en'
    
    try:
        # Extract video ID
        video_id = extract_video_id(url_or_id)
        print(f"Fetching transcript for video ID: {video_id}")
        
        # Get transcript
        api = YouTubeTranscriptApi()
        transcript_data = api.fetch(video_id, languages=[language])
        transcript_list = transcript_data.snippets
        
        # Get video info
        video_info = get_video_info(video_id)
        
        # Save transcript
        transcript_path, metadata_path = save_transcript(video_id, transcript_list, video_info)
        
        print(f"\n✅ Success!")
        print(f"Transcript saved to: {transcript_path}")
        print(f"Metadata saved to: {metadata_path}")
        print(f"\nTotal segments: {len(transcript_list)}")
        print(f"\nTo analyze with Claude Code:")
        print(f"  'Use youtube-learning-agent to analyze {transcript_path}'")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nCommon issues:")
        print("- Video might not have captions")
        print("- Video might be private or deleted")
        print("- Try a different language code (e.g., 'es' for Spanish)")
        sys.exit(1)

if __name__ == "__main__":
    main()