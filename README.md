# NewsBreeze - Celebrity-Powered Audio News Reader

## 🎙️ Overview

NewsBreeze is an AI-powered news aggregation application that fetches the latest headlines from multiple RSS feeds, summarizes them using advanced AI models, and reads them aloud in celebrity-style voices. Built with Python, Flask, and cutting-edge machine learning models.

## ✨ Features

- **📰 Multi-Source News Aggregation**: Fetches news from BBC, CNN, NPR, Reuters, and TechCrunch
- **🤖 AI-Powered Summarization**: Uses Hugging Face's `Falconsai/text_summarization` model
- **🎭 Celebrity Voice Synthesis**: Text-to-speech with multiple voice styles using `coqui/xtts-v2`
- **🎨 Modern Beautiful UI**: Clean, responsive design with Tailwind CSS
- **🔄 Real-time Updates**: Automatic news refresh and status monitoring
- **📱 Mobile Responsive**: Works seamlessly on all devices

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- At least 4GB RAM (for AI models)
- Internet connection (for RSS feeds and model downloads)

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd NewsBreeze
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv newsbreeze_env
   
   # On Windows
   newsbreeze_env\Scripts\activate
   
   # On macOS/Linux
   source newsbreeze_env/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   Open your browser and go to `http://localhost:5000`

## 🏗️ Project Structure

```
NewsBreeze/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/
│   └── index.html        # Frontend HTML template
└── static/
    └── audio/            # Generated audio files (created automatically)
```

## 🤖 AI Models Used

### Summarization Model
- **Model**: `Falconsai/text_summarization`
- **Fallback**: `facebook/bart-large-cnn`
- **Purpose**: Generates concise summaries of news articles
- **Features**: Optimized for news content, maintains key information

### Text-to-Speech Model
- **Primary**: `tts_models/multilingual/multi-dataset/xtts_v2` (Coqui TTS)
- **Fallback**: `tts_models/en/ljspeech/tacotron2-DDC`
- **Purpose**: Converts text summaries to natural-sounding audio
- **Features**: Multiple voice styles, high-quality speech synthesis

## 🎛️ API Endpoints

- `GET /` - Main application interface
- `GET /api/news` - Fetch and summarize latest news
- `GET /api/audio/<article_id>` - Generate audio for specific article
- `GET /api/voices` - Get available voice options
- `GET /api/status` - Check AI model loading status

## 🔧 Configuration

### RSS Feeds
Modify the `RSS_FEEDS` list in `app.py` to add or remove news sources:

```python
RSS_FEEDS = [
    "http://feeds.bbci.co.uk/news/rss.xml",
    "https://rss.cnn.com/rss/edition.rss",
    "https://feeds.npr.org/1001/rss.xml",
    "https://feeds.reuters.com/reuters/topNews",
    "https://feeds.feedburner.com/TechCrunch",
]
```

### Voice Options
Customize celebrity voices in the `CELEBRITY_VOICES` dictionary:

```python
CELEBRITY_VOICES = {
    "default": "Default Voice",
    "celebrity1": "Morgan Freeman Style",
    "celebrity2": "David Attenborough Style",
    "celebrity3": "News Anchor Style"
}
```

## 🎨 User Interface Features

- **Voice Selection**: Choose from multiple celebrity-style voices
- **Audio Controls**: Play, pause, and control audio playback
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Real-time Status**: See when AI models are loading/ready
- **Source Attribution**: Clear indication of news sources and timestamps
- **External Links**: Direct access to full articles

## 🔄 How It Works

1. **News Fetching**: Application polls RSS feeds from major news sources
2. **Text Processing**: Raw article content is cleaned and prepared
3. **AI Summarization**: Hugging Face model generates concise summaries
4. **Voice Synthesis**: TTS model converts summaries to audio
5. **Caching**: Generated audio files are cached for performance
6. **Real-time Updates**: Frontend polls for new content and status

## 📋 System Requirements

### Minimum Requirements
- **CPU**: 2+ cores, 2GHz
- **RAM**: 4GB (8GB recommended)
- **Storage**: 2GB free space (for models and cache)
- **Network**: Stable internet connection

### Recommended Requirements
- **CPU**: 4+ cores, 3GHz
- **RAM**: 8GB or more
- **Storage**: 5GB free space
- **GPU**: Optional, but improves TTS performance

## 🐛 Troubleshooting

### Common Issues

1. **Models taking too long to load**
   - Ensure stable internet connection
   - Models are downloaded on first run (can take 10-15 minutes)
   - Check available storage space

2. **Audio generation fails**
   - Verify TTS model loaded successfully
   - Check system audio capabilities
   - Try refreshing the page

3. **News not loading**
   - Check internet connection
   - Some RSS feeds may be temporarily unavailable
   - Try refreshing or wait for automatic retry

### Performance Tips

- **First Run**: Allow 10-15 minutes for initial model downloads
- **Memory**: Close other applications if experiencing slowdowns
- **Network**: Stable connection required for RSS feeds and model downloads

## 🚀 Deployment Options

### Local Development
```bash
python app.py
```

### Production (using Gunicorn)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker (Optional)
Create a `Dockerfile` for containerized deployment:

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

## 📈 Future Enhancements

- [ ] User authentication and personalized feeds
- [ ] Social media integration
- [ ] Podcast-style episode generation
- [ ] Sentiment analysis and categorization
- [ ] Multi-language support
- [ ] Voice customization options
- [ ] Offline mode capabilities

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- **Hugging Face** for the summarization models
- **Coqui TTS** for voice synthesis technology
- **RSS Feed Providers** for news content
- **Flask Community** for the web framework
- **Tailwind CSS** for beautiful styling

## 📧 Support

For issues, questions, or contributions, please use the GitHub issues page or contact the development team.

---

**Built with ❤️ using Python, AI, and modern web technologies** 