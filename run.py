#!/usr/bin/env python3
"""
NewsBreeze - Celebrity-Powered Audio News Reader
Startup script with environment detection
"""

import os
import sys
from app import app, logger

def main():
    """Main entry point for NewsBreeze application"""
    
    # Environment detection
    env = os.environ.get('FLASK_ENV', 'development')
    
    logger.info("=" * 50)
    logger.info("🎙️  NewsBreeze - Celebrity-Powered Audio News")
    logger.info("=" * 50)
    logger.info(f"Environment: {env}")
    logger.info(f"Debug Mode: {app.config.get('DEBUG', False)}")
    logger.info(f"Host: {app.config.get('HOST', 'localhost')}")
    logger.info(f"Port: {app.config.get('PORT', 5000)}")
    logger.info(f"RSS Feeds: {len(app.config.get('RSS_FEEDS', []))}")
    logger.info("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        logger.error("Python 3.8 or higher is required!")
        sys.exit(1)
    
    # Production vs Development
    if env == 'production':
        logger.info("Starting in PRODUCTION mode...")
        try:
            import gunicorn
            # Use Gunicorn for production
            os.system(f"gunicorn -w 4 -b {app.config['HOST']}:{app.config['PORT']} app:app")
        except ImportError:
            logger.warning("Gunicorn not found, falling back to Flask dev server")
            app.run(
                host=app.config['HOST'],
                port=app.config['PORT'],
                debug=False
            )
    else:
        logger.info("Starting in DEVELOPMENT mode...")
        logger.info("Note: AI models will load in the background...")
        logger.info(f"Access the app at: http://{app.config['HOST']}:{app.config['PORT']}")
        
        app.run(
            host=app.config['HOST'],
            port=app.config['PORT'],
            debug=app.config.get('DEBUG', True)
        )

if __name__ == '__main__':
    main() 