import os

class Config:
    """Configuration settings for NewsBreeze application"""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'newsbreeze-secret-key-2024'
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    HOST = os.environ.get('FLASK_HOST', '0.0.0.0')
    PORT = int(os.environ.get('FLASK_PORT', 5000))
    
    # RSS Feed sources
    RSS_FEEDS = [
        "http://feeds.bbci.co.uk/news/rss.xml",
        "https://rss.cnn.com/rss/edition.rss", 
        "https://feeds.npr.org/1001/rss.xml",
        "https://feeds.reuters.com/reuters/topNews",
        "https://feeds.feedburner.com/TechCrunch",
        "https://feeds.washingtonpost.com/rss/world",
        "https://www.theguardian.com/world/rss",
    ]
    
    # AI Model settings
    SUMMARIZATION_MODEL = os.environ.get('SUMMARIZATION_MODEL', 'Falconsai/text_summarization')
    SUMMARIZATION_FALLBACK = os.environ.get('SUMMARIZATION_FALLBACK', 'facebook/bart-large-cnn')
    
    TTS_MODEL_PRIMARY = os.environ.get('TTS_MODEL_PRIMARY', 'tts_models/multilingual/multi-dataset/xtts_v2')
    TTS_MODEL_FALLBACK = os.environ.get('TTS_MODEL_FALLBACK', 'tts_models/en/ljspeech/tacotron2-DDC')
    
    # Voice options
    CELEBRITY_VOICES = {
        "default": "Default Voice",
        "celebrity1": "Morgan Freeman Style", 
        "celebrity2": "David Attenborough Style",
        "celebrity3": "News Anchor Style",
        "celebrity4": "Radio DJ Style"
    }
    
    # Summarization settings
    SUMMARY_MAX_LENGTH = int(os.environ.get('SUMMARY_MAX_LENGTH', 100))
    SUMMARY_MIN_LENGTH = int(os.environ.get('SUMMARY_MIN_LENGTH', 30))
    ARTICLES_PER_FEED = int(os.environ.get('ARTICLES_PER_FEED', 5))
    
    # File paths
    STATIC_FOLDER = 'static'
    TEMPLATE_FOLDER = 'templates'
    AUDIO_FOLDER = os.path.join(STATIC_FOLDER, 'audio')
    
    # Cache settings
    AUDIO_CACHE_ENABLED = os.environ.get('AUDIO_CACHE_ENABLED', 'True').lower() == 'true'
    CACHE_CLEANUP_HOURS = int(os.environ.get('CACHE_CLEANUP_HOURS', 24))
    
    # Performance settings
    MODEL_LOADING_TIMEOUT = int(os.environ.get('MODEL_LOADING_TIMEOUT', 300))  # 5 minutes
    NEWS_REFRESH_INTERVAL = int(os.environ.get('NEWS_REFRESH_INTERVAL', 300))  # 5 minutes
    
    # API settings
    API_RATE_LIMIT = os.environ.get('API_RATE_LIMIT', '100 per hour')
    
    @classmethod
    def init_app(cls, app):
        """Initialize application with configuration"""
        app.config.from_object(cls)
        
        # Create necessary directories
        os.makedirs(cls.AUDIO_FOLDER, exist_ok=True)
        os.makedirs(cls.TEMPLATE_FOLDER, exist_ok=True)

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    
class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    
class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
} 