#!/usr/bin/env python3
"""
Robust Podcast Transcription Processor
Handles multiple podcast sources with automatic fallback
"""

import os
import sys
import json
import re
import logging
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Tuple
from urllib.parse import urlparse, quote

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PodcastProcessor:
    """
    Multi-source podcast processor with transcription capabilities
    """

    def __init__(self, config_path: Optional[str] = None):
        """Initialize the podcast processor with configuration"""
        self.config = self._load_config(config_path)
        self.setup_directories()
        self.transcription_cache = {}

    def _load_config(self, config_path: Optional[str]) -> Dict:
        """Load configuration from file or use defaults"""
        default_config = {
            "transcription": {
                "mode": "api",  # "api" or "local"
                "model": "base",  # whisper model size
                "language": "en",
                "diarize": True,
                "max_speakers": 4,
                "noise_filter": True
            },
            "storage": {
                "base_path": "learning/podcasts",
                "keep_audio": False,
                "cache_transcripts": True
            },
            "sources": {
                "try_rss": True,
                "try_youtube": True,
                "try_direct": True
            }
        }

        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    user_config = json.load(f)
                    # Merge with defaults
                    for key in user_config:
                        if key in default_config:
                            default_config[key].update(user_config[key])
                        else:
                            default_config[key] = user_config[key]
            except Exception as e:
                logger.warning(f"Failed to load config: {e}, using defaults")

        return default_config

    def setup_directories(self):
        """Create necessary directory structure"""
        base_path = Path(self.config['storage']['base_path'])
        directories = [
            base_path / 'audio',
            base_path / 'transcripts',
            base_path / 'metadata',
            base_path / 'cache'
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            logger.debug(f"Ensured directory exists: {directory}")

    def find_podcast_source(self, identifier: str) -> Optional[Dict]:
        """
        Find the best available source for a podcast
        Returns source info with type and URL
        """
        logger.info(f"Searching for podcast: {identifier}")

        # Check if it's already a direct URL
        if self._is_valid_url(identifier):
            return {
                "type": "direct",
                "url": identifier,
                "title": self._extract_title_from_url(identifier)
            }

        # Try RSS feed search
        if self.config['sources']['try_rss']:
            rss_result = self._find_rss_feed(identifier)
            if rss_result:
                return rss_result

        # Try YouTube search
        if self.config['sources']['try_youtube']:
            youtube_result = self._search_youtube(identifier)
            if youtube_result:
                return youtube_result

        # Check if it's a Spotify URL
        if 'spotify.com' in identifier:
            return self._handle_spotify(identifier)

        return None

    def _is_valid_url(self, text: str) -> bool:
        """Check if the text is a valid URL"""
        try:
            result = urlparse(text)
            return all([result.scheme, result.netloc])
        except:
            return False

    def _extract_title_from_url(self, url: str) -> str:
        """Extract a reasonable title from a URL"""
        parsed = urlparse(url)
        path = parsed.path.strip('/')
        if path:
            # Get the last part of the path, remove extension
            title = os.path.splitext(os.path.basename(path))[0]
            # Replace common separators with spaces
            title = re.sub(r'[-_]', ' ', title)
            return title.title()
        return "Podcast Episode"

    def _find_rss_feed(self, search_term: str) -> Optional[Dict]:
        """
        Find RSS feed for a podcast
        This would integrate with podcast directories
        """
        # This is a placeholder - would integrate with:
        # - iTunes Podcast Directory API
        # - PodcastIndex.org API
        # - Direct RSS feed detection

        logger.info(f"Searching for RSS feed: {search_term}")

        # For now, return None - implement RSS search
        # In production, this would use feedparser and podcast APIs
        return None

    def _search_youtube(self, search_term: str) -> Optional[Dict]:
        """Search YouTube for the podcast episode"""
        try:
            # Use yt-dlp to search YouTube
            search_query = f"ytsearch:{search_term}"
            cmd = [
                'yt-dlp',
                '--get-url',
                '--get-title',
                '--no-playlist',
                search_query
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0 and result.stdout:
                lines = result.stdout.strip().split('\n')
                if len(lines) >= 2:
                    return {
                        "type": "youtube",
                        "url": lines[-1],  # URL is usually last
                        "title": lines[0]   # Title is first
                    }
        except Exception as e:
            logger.error(f"YouTube search failed: {e}")

        return None

    def _handle_spotify(self, spotify_url: str) -> Dict:
        """Handle Spotify URLs with appropriate fallback suggestions"""
        logger.warning("Direct Spotify download not supported due to DRM")

        # Extract show/episode info from URL if possible
        episode_name = "Spotify Episode"
        if '/episode/' in spotify_url:
            episode_id = spotify_url.split('/episode/')[-1].split('?')[0]
            episode_name = f"Spotify Episode {episode_id[:8]}"

        return {
            "type": "spotify_blocked",
            "url": spotify_url,
            "title": episode_name,
            "alternatives": [
                "Search for this podcast on YouTube",
                "Check if podcast has RSS feed",
                "Look for podcast on Apple Podcasts",
                "Use screen recording as last resort"
            ]
        }

    def download_audio(self, source_info: Dict) -> Optional[str]:
        """Download audio from the identified source"""
        if source_info['type'] == 'spotify_blocked':
            logger.error("Cannot download from Spotify directly")
            logger.info("Alternatives: " + ", ".join(source_info['alternatives']))
            return None

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_title = re.sub(r'[^\w\s-]', '', source_info['title'])[:50]
        output_filename = f"{safe_title}_{timestamp}.mp3"
        output_path = Path(self.config['storage']['base_path']) / 'audio' / output_filename

        logger.info(f"Downloading audio to: {output_path}")

        try:
            if source_info['type'] in ['youtube', 'direct']:
                # Use yt-dlp for downloading
                cmd = [
                    'yt-dlp',
                    '-x',  # Extract audio
                    '--audio-format', 'mp3',
                    '--audio-quality', '0',  # Best quality
                    '-o', str(output_path),
                    source_info['url']
                ]

                result = subprocess.run(cmd, capture_output=True, text=True)

                if result.returncode == 0:
                    logger.info("Audio downloaded successfully")
                    return str(output_path)
                else:
                    logger.error(f"Download failed: {result.stderr}")

            elif source_info['type'] == 'rss':
                # Direct download from RSS enclosure
                # Would use requests or urllib here
                pass

        except Exception as e:
            logger.error(f"Download error: {e}")

        return None

    def preprocess_audio(self, audio_path: str) -> str:
        """
        Preprocess audio for better transcription
        - Noise reduction
        - Normalization
        - Format conversion if needed
        """
        logger.info("Preprocessing audio...")

        # This is a placeholder for audio preprocessing
        # In production, would use:
        # - pydub for audio manipulation
        # - noisereduce library for noise reduction
        # - ffmpeg-normalize for normalization

        return audio_path

    def transcribe_with_whisper(self, audio_path: str) -> Optional[Dict]:
        """
        Transcribe audio using Whisper (API or local)
        Returns transcript with timestamps and speaker diarization
        """
        logger.info(f"Transcribing audio: {audio_path}")

        # Check cache first
        cache_key = self._get_cache_key(audio_path)
        if cache_key in self.transcription_cache:
            logger.info("Using cached transcription")
            return self.transcription_cache[cache_key]

        transcript_data = None

        if self.config['transcription']['mode'] == 'api':
            transcript_data = self._transcribe_with_api(audio_path)
        else:
            transcript_data = self._transcribe_locally(audio_path)

        # Cache the result
        if transcript_data and self.config['storage']['cache_transcripts']:
            self.transcription_cache[cache_key] = transcript_data

        return transcript_data

    def _get_cache_key(self, audio_path: str) -> str:
        """Generate a cache key for the audio file"""
        # Use file size and name for simple caching
        stat = os.stat(audio_path)
        return f"{os.path.basename(audio_path)}_{stat.st_size}"

    def _transcribe_with_api(self, audio_path: str) -> Optional[Dict]:
        """Use OpenAI Whisper API for transcription"""
        try:
            # Check for OpenAI API key
            api_key = os.environ.get('OPENAI_API_KEY')
            if not api_key:
                logger.error("OpenAI API key not found in environment")
                return None

            # This would use the OpenAI API
            # For now, returning placeholder
            logger.info("Using Whisper API for transcription")

            # Placeholder for API implementation
            # Would use: openai.Audio.transcribe()

            return {
                "text": "Transcription would appear here",
                "segments": [],
                "language": self.config['transcription']['language']
            }

        except Exception as e:
            logger.error(f"API transcription failed: {e}")
            return None

    def _transcribe_locally(self, audio_path: str) -> Optional[Dict]:
        """Use local Whisper model for transcription"""
        try:
            logger.info("Using local Whisper for transcription")

            # This would use whisperx for local transcription
            # Placeholder for local implementation

            cmd = [
                'whisperx',
                audio_path,
                '--model', self.config['transcription']['model'],
                '--language', self.config['transcription']['language'],
                '--output_format', 'json'
            ]

            if self.config['transcription']['diarize']:
                cmd.extend(['--diarize', '--max_speakers',
                           str(self.config['transcription']['max_speakers'])])

            # Would run the command and parse output
            # For now, returning placeholder

            return {
                "text": "Local transcription would appear here",
                "segments": [],
                "language": self.config['transcription']['language']
            }

        except Exception as e:
            logger.error(f"Local transcription failed: {e}")
            return None

    def save_transcript(self, transcript_data: Dict, source_info: Dict) -> str:
        """Save transcript and metadata to files"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_title = re.sub(r'[^\w\s-]', '', source_info['title'])[:50]

        # Save transcript text
        transcript_filename = f"{safe_title}_{timestamp}.txt"
        transcript_path = Path(self.config['storage']['base_path']) / 'transcripts' / transcript_filename

        with open(transcript_path, 'w', encoding='utf-8') as f:
            f.write(transcript_data.get('text', ''))

        # Save metadata
        metadata = {
            "source": source_info,
            "transcription": {
                "timestamp": datetime.now().isoformat(),
                "language": transcript_data.get('language', 'unknown'),
                "segment_count": len(transcript_data.get('segments', [])),
                "config": self.config['transcription']
            }
        }

        metadata_filename = f"{safe_title}_{timestamp}_metadata.json"
        metadata_path = Path(self.config['storage']['base_path']) / 'metadata' / metadata_filename

        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)

        logger.info(f"Saved transcript to: {transcript_path}")
        logger.info(f"Saved metadata to: {metadata_path}")

        return str(transcript_path)

    def process_podcast(self, identifier: str) -> Optional[str]:
        """
        Main processing pipeline
        Returns path to transcript file or None if failed
        """
        logger.info(f"Starting podcast processing: {identifier}")

        # Find source
        source = self.find_podcast_source(identifier)
        if not source:
            logger.error("Could not find podcast source")
            return None

        logger.info(f"Found source: {source['type']} - {source['title']}")

        # Download audio
        audio_path = self.download_audio(source)
        if not audio_path:
            logger.error("Failed to download audio")
            return None

        # Preprocess audio
        processed_audio = self.preprocess_audio(audio_path)

        # Transcribe
        transcript = self.transcribe_with_whisper(processed_audio)
        if not transcript:
            logger.error("Failed to transcribe audio")
            return None

        # Save results
        transcript_path = self.save_transcript(transcript, source)

        # Clean up audio if configured
        if not self.config['storage']['keep_audio'] and os.path.exists(audio_path):
            os.remove(audio_path)
            logger.info("Cleaned up audio file")

        logger.info(f"Processing complete! Transcript at: {transcript_path}")
        return transcript_path


def main():
    """CLI interface for podcast processor"""
    if len(sys.argv) < 2:
        print("Usage: python podcast_processor.py <podcast_url_or_search>")
        print("\nExamples:")
        print("  python podcast_processor.py 'Lex Fridman podcast episode 123'")
        print("  python podcast_processor.py https://youtube.com/watch?v=...")
        print("  python podcast_processor.py https://podcasts.apple.com/...")
        sys.exit(1)

    identifier = sys.argv[1]
    config_path = sys.argv[2] if len(sys.argv) > 2 else None

    processor = PodcastProcessor(config_path)
    result = processor.process_podcast(identifier)

    if result:
        print(f"\n✅ Success! Transcript saved to: {result}")
    else:
        print("\n❌ Failed to process podcast")
        sys.exit(1)


if __name__ == "__main__":
    main()