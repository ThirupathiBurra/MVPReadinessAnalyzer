import logging
from flask import g

def setup_logging(app):
    # Configure the base logger
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Specific logger for AI Observability
    ai_logger = logging.getLogger('ai.observability')
    ai_logger.setLevel(logging.INFO)
    
    # Attach to app if needed, or simply make it accessible
    app.logger.info("Logging configured.")
    return ai_logger
