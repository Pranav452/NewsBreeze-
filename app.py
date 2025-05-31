from flask import Flask, render_template, jsonify, send_file, request
from flask_cors import CORS
import feedparser
import requests
from transformers import pipeline
from TTS.api import TTS
import os
import hashlib
import json
from datetime import datetime, timedelta
import threading
import time
import logging
from config import config

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Load configuration
config_name = os.environ.get('FLASK_CONFIG', 'default')
app.config.from_object(config[config_name])
config[config_name].init_app(app)

# Initialize models
summarizer = None
tts_model = None
model_loading_status = {'summarizer': False, 'tts': False}

def initialize_models():
    """Initialize AI models in a separate thread to avoid blocking startup"""
    global summarizer, tts_model, model_loading_status
    
    logger.info("Initializing summarization model...")
    try:
        summarizer = pipeline(
            "summarization", 
            model=app.config['SUMMARIZATION_MODEL'],
            max_length=app.config['SUMMARY_MAX_LENGTH'],
            min_length=app.config['SUMMARY_MIN_LENGTH'],
            do_sample=False
        )
        model_loading_status['summarizer'] = True
        logger.info("Summarization model loaded successfully!")
    except Exception as e:
        logger.error(f"Error loading primary summarization model: {e}")
        try:
            # Fallback to simpler model
            summarizer = pipeline("summarization", model=app.config['SUMMARIZATION_FALLBACK'])
            model_loading_status['summarizer'] = True
            logger.info("Fallback summarization model loaded!")
        except Exception as e2:
            logger.error(f"Failed to load fallback summarization model: {e2}")
    
    logger.info("Initializing TTS model...")
    try:
        tts_model = TTS(model_name=app.config['TTS_MODEL_PRIMARY'])
        model_loading_status['tts'] = True
        logger.info("TTS model loaded successfully!")
    except Exception as e:
        logger.error(f"Error loading primary TTS model: {e}")
        try:
            # Fallback to simpler TTS
            tts_model = TTS(model_name=app.config['TTS_MODEL_FALLBACK'])
            model_loading_status['tts'] = True
            logger.info("Fallback TTS model loaded!")
        except Exception as e2:
            logger.error(f"Failed to load fallback TTS model: {e2}")

def cleanup_old_audio_files():
    """Clean up old audio files to save disk space"""
    if not app.config['AUDIO_CACHE_ENABLED']:
        return
        
    try:
        audio_dir = app.config['AUDIO_FOLDER']
        if not os.path.exists(audio_dir):
            return
            
        cutoff_time = datetime.now() - timedelta(hours=app.config['CACHE_CLEANUP_HOURS'])
        
        for filename in os.listdir(audio_dir):
            filepath = os.path.join(audio_dir, filename)
            if os.path.isfile(filepath):
                file_time = datetime.fromtimestamp(os.path.getctime(filepath))
                if file_time < cutoff_time:
                    os.remove(filepath)
                    logger.info(f"Cleaned up old audio file: {filename}")
    except Exception as e:
        logger.error(f"Error during audio cleanup: {e}")

def fetch_news():
    """Fetch news from multiple RSS feeds"""
    all_articles = []
    
    for feed_url in app.config['RSS_FEEDS']:
        try:
            logger.info(f"Fetching from: {feed_url}")
            feed = feedparser.parse(feed_url)
            
            if feed.bozo:
                logger.warning(f"Feed parsing warning for {feed_url}: {feed.bozo_exception}")
            
            for entry in feed.entries[:app.config['ARTICLES_PER_FEED']]:
                article = {
                    'title': entry.title,
                    'summary': getattr(entry, 'summary', entry.title),
                    'link': entry.link,
                    'published': getattr(entry, 'published', 'Unknown'),
                    'source': getattr(feed.feed, 'title', 'Unknown Source'),
                    'author': getattr(entry, 'author', 'Unknown Author')
                }
                all_articles.append(article)
        except Exception as e:
            logger.error(f"Error fetching from {feed_url}: {e}")
    
    logger.info(f"Fetched {len(all_articles)} articles total")
    return all_articles

def summarize_text(text, max_length=None):
    """Summarize text using Hugging Face model"""
    if not summarizer:
        return text[:200] + "..." if len(text) > 200 else text
    
    max_length = max_length or app.config['SUMMARY_MAX_LENGTH']
    
    try:
        # Clean and prepare text
        text = text.strip()
        if len(text) < 50:
            return text
        
        # Summarize
        summary = summarizer(
            text, 
            max_length=max_length, 
            min_length=app.config['SUMMARY_MIN_LENGTH'], 
            do_sample=False
        )
        return summary[0]['summary_text']
    except Exception as e:
        logger.error(f"Error in summarization: {e}")
        return text[:200] + "..." if len(text) > 200 else text

def generate_audio(text, voice_style="default"):
    """Generate audio from text using TTS"""
    if not tts_model:
        logger.warning("TTS model not available")
        return None
    
    try:
        # Generate unique filename
        text_hash = hashlib.md5(text.encode()).hexdigest()
        audio_file = os.path.join(app.config['AUDIO_FOLDER'], f"{text_hash}_{voice_style}.wav")
        
        # Check if audio already exists and caching is enabled
        if app.config['AUDIO_CACHE_ENABLED'] and os.path.exists(audio_file):
            logger.info(f"Using cached audio: {audio_file}")
            return audio_file
        
        # Generate audio
        logger.info(f"Generating audio for voice style: {voice_style}")
        tts_model.tts_to_file(
            text=text,
            file_path=audio_file
        )
        
        logger.info(f"Audio generated: {audio_file}")
        return audio_file
    except Exception as e:
        logger.error(f"Error generating audio: {e}")
        return None

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/news')
def get_news():
    """API endpoint to get summarized news"""
    try:
        articles = fetch_news()
        
        # Summarize articles
        for article in articles:
            original_summary = article['summary']
            article['ai_summary'] = summarize_text(original_summary)
            article['id'] = hashlib.md5(article['title'].encode()).hexdigest()
        
        return jsonify({
            'success': True,
            'articles': articles,
            'timestamp': datetime.now().isoformat(),
            'total_articles': len(articles)
        })
    except Exception as e:
        logger.error(f"Error in get_news: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/audio/<article_id>')
def get_audio(article_id):
    """Generate and serve audio for an article"""
    try:
        voice_style = request.args.get('voice', 'default')
        text = request.args.get('text', '')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        if len(text) > 1000:  # Limit text length
            text = text[:1000] + "..."
        
        audio_file = generate_audio(text, voice_style)
        
        if audio_file and os.path.exists(audio_file):
            return send_file(audio_file, mimetype='audio/wav')
        else:
            return jsonify({'error': 'Audio generation failed'}), 500
    
    except Exception as e:
        logger.error(f"Error in get_audio: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/voices')
def get_voices():
    """Get available voice options"""
    return jsonify(app.config['CELEBRITY_VOICES'])

@app.route('/api/status')
def get_status():
    """Get system status"""
    return jsonify({
        'summarizer_loaded': model_loading_status['summarizer'],
        'tts_loaded': model_loading_status['tts'],
        'models_ready': all(model_loading_status.values()),
        'config': {
            'articles_per_feed': app.config['ARTICLES_PER_FEED'],
            'cache_enabled': app.config['AUDIO_CACHE_ENABLED'],
            'total_feeds': len(app.config['RSS_FEEDS'])
        },
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Initialize models in background
    model_thread = threading.Thread(target=initialize_models)
    model_thread.daemon = True
    model_thread.start()
    
    # Start cleanup thread
    cleanup_thread = threading.Thread(target=cleanup_old_audio_files)
    cleanup_thread.daemon = True
    cleanup_thread.start()
    
    logger.info("Starting NewsBreeze server...")
    logger.info("Note: AI models are loading in the background...")
    logger.info(f"Configuration: {config_name}")
    
    app.run(
        debug=app.config['DEBUG'],
        host=app.config['HOST'],
        port=app.config['PORT']
    ) 