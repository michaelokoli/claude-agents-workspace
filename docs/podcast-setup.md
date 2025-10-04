# Podcast Transcription System Documentation

## Overview

A robust, multi-source podcast transcription system that handles various podcast sources with automatic fallback mechanisms and high-quality transcription using WhisperX.

## Features

- ✅ **Multi-Source Support**: RSS feeds, YouTube, direct URLs
- ✅ **Automatic Fallback**: Tries multiple sources if primary fails
- ✅ **Speaker Diarization**: Identifies different speakers in conversations
- ✅ **Spotify Handling**: Provides alternatives for DRM-protected content
- ✅ **Transcript Caching**: Avoids re-processing identical content
- ✅ **Noise Filtering**: Preprocesses audio for better accuracy
- ✅ **Agent Integration**: Works with project-coordinator and podcast-analyzer

## Installation

### Basic Dependencies

```bash
# Core requirements
pip install feedparser       # RSS feed parsing
pip install yt-dlp           # Audio downloading
pip install pydub            # Audio processing

# For API mode (simpler setup)
pip install openai          # OpenAI Whisper API

# For local mode (better privacy/cost)
pip install whisperx        # Enhanced Whisper
pip install pyannote.audio  # Speaker diarization
```

### WhisperX Installation (for local transcription)

```bash
# Install WhisperX with GPU support
pip install git+https://github.com/m-bain/whisperx.git

# For CPU-only installation
pip install git+https://github.com/m-bain/whisperx.git --extra-index-url https://download.pytorch.org/whl/cpu

# Install speaker diarization models
pip install https://github.com/pyannote/pyannote-audio/archive/refs/heads/main.zip
```

### Environment Variables

```bash
# For Whisper API mode
export OPENAI_API_KEY="your-api-key-here"

# For speaker diarization (optional)
export HUGGINGFACE_TOKEN="your-huggingface-token"
```

## Configuration

Edit `scripts/whisper_config.yaml` to customize:

```yaml
transcription:
  mode: "api"        # Use "api" for simplicity or "local" for privacy
  model: "base"      # Model size: tiny, base, small, medium, large
  diarize: true      # Enable speaker identification

storage:
  keep_audio: false  # Set to true to keep downloaded audio files
  cache_transcripts: true  # Cache to avoid re-processing
```

## Usage

### 1. Via Command Line

```bash
# Process a podcast by search term
python scripts/podcast_processor.py "Lex Fridman podcast episode 123"

# Process a YouTube podcast
python scripts/podcast_processor.py "https://youtube.com/watch?v=..."

# Process a direct audio URL
python scripts/podcast_processor.py "https://example.com/podcast.mp3"

# With custom config
python scripts/podcast_processor.py "podcast name" scripts/whisper_config.yaml
```

### 2. Via Agent System

```
User: "Analyze this podcast: [URL or search term]"

Project Coordinator will:
1. Delegate to media-fetcher to get transcript
2. Delegate to podcast-analyzer for insights
3. Return comprehensive analysis
```

### 3. Programmatic Usage

```python
from scripts.podcast_processor import PodcastProcessor

# Initialize processor
processor = PodcastProcessor("scripts/whisper_config.yaml")

# Process podcast
transcript_path = processor.process_podcast("podcast identifier")

# Get specific components
source = processor.find_podcast_source("podcast name")
audio_path = processor.download_audio(source)
transcript = processor.transcribe_with_whisper(audio_path)
```

## Source Priority System

The system attempts sources in this order:

1. **Direct URL** - If a valid URL is provided
2. **RSS Feed** - Searches podcast directories for RSS feed
3. **YouTube** - Searches YouTube for the podcast
4. **Spotify** - Detects and provides alternatives (cannot download)

### Handling Spotify Podcasts

Since Spotify content is DRM-protected, the system:
1. Detects Spotify URLs
2. Suggests searching for the podcast on other platforms
3. Provides alternative sources (YouTube, Apple Podcasts, RSS)
4. As last resort, suggests recording for exclusive content

## File Structure

```
learning/podcasts/
├── audio/          # Downloaded audio files (optional)
├── transcripts/    # Text transcripts (.txt)
├── metadata/       # Episode metadata (.json)
└── cache/          # Cached transcriptions

Example files:
- Lex_Fridman_Episode_123_20240104_143022.txt (transcript)
- Lex_Fridman_Episode_123_20240104_143022_metadata.json (metadata)
```

## Performance Comparison

### API Mode (OpenAI Whisper)
- **Pros**: Simple setup, no GPU needed, consistent quality
- **Cons**: Costs $0.006/minute, requires internet, 25MB file limit
- **Speed**: 1-2 minutes for 60-minute podcast
- **Best for**: Occasional use, quick setup

### Local Mode (WhisperX)
- **Pros**: Free after setup, full privacy, unlimited file size
- **Cons**: Requires GPU for speed, complex setup
- **Speed**: 5-10 minutes on GPU, 30-60 minutes on CPU
- **Best for**: High volume, privacy concerns, batch processing

## Cost Analysis

For regular podcast consumption:
- **10 podcasts/month** (60 min each): ~$3.60 with API
- **50 podcasts/month**: ~$18 with API
- **100+ podcasts/month**: Local mode becomes cost-effective

## Advanced Features

### Speaker Diarization

When enabled, the system:
- Identifies different speakers
- Labels speech segments by speaker
- Provides speaker statistics
- Useful for interviews and panels

### Noise Filtering

Automatically:
- Removes background music during intros
- Filters out ambient noise
- Normalizes audio levels
- Improves transcription accuracy

### Transcript Caching

Prevents re-processing by:
- Generating unique cache keys
- Storing processed transcripts
- Checking cache before processing
- Configurable TTL and size limits

## Troubleshooting

### Common Issues

**"No module named whisperx"**
```bash
pip install git+https://github.com/m-bain/whisperx.git
```

**"yt-dlp: command not found"**
```bash
pip install yt-dlp
# or
brew install yt-dlp  # macOS
```

**"OpenAI API key not found"**
```bash
export OPENAI_API_KEY="your-key-here"
```

**Slow transcription on CPU**
- Switch to API mode for faster processing
- Use smaller model (tiny or base)
- Consider GPU upgrade for local mode

**Spotify podcast won't download**
- This is expected (DRM protection)
- Search for podcast on YouTube
- Check podcast website for RSS feed
- Try Apple Podcasts or Google Podcasts

## Integration with Agents

### Media-Fetcher Agent
- Handles podcast URL/search requests
- Runs podcast_processor.py
- Returns transcript path

### Podcast-Analyzer Agent
- Receives transcript from media-fetcher
- Performs deep conversation analysis
- Extracts insights and topics
- Identifies key moments

### Project-Coordinator
- Orchestrates the full pipeline
- Manages parallel processing
- Synthesizes final results

## Future Enhancements

- [ ] Real-time transcription streaming
- [ ] Multi-language support
- [ ] Automatic RSS feed discovery
- [ ] Podcast series analysis
- [ ] Integration with podcast APIs
- [ ] Chapter detection
- [ ] Sentiment analysis
- [ ] Topic modeling
- [ ] Knowledge graph generation

## Examples

### Process "Lex Fridman" Episode
```bash
python scripts/podcast_processor.py "Lex Fridman Elon Musk"
# Searches YouTube, downloads, transcribes
# Output: learning/podcasts/transcripts/Lex_Fridman_Elon_Musk_[timestamp].txt
```

### Analyze Tech Podcast
```
User: "Analyze the latest All-In Podcast episode"
# Coordinator → Media-Fetcher → Podcast-Analyzer
# Returns: Full analysis with insights, quotes, and takeaways
```

### Batch Process Series
```python
processor = PodcastProcessor()
episodes = ["episode 1", "episode 2", "episode 3"]
for ep in episodes:
    processor.process_podcast(ep)
```

## Support

For issues or questions:
1. Check troubleshooting section above
2. Verify dependencies are installed
3. Check logs in learning/podcasts/
4. Test with a known working YouTube podcast first