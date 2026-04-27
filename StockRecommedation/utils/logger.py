"""Logging utilities for the application."""

import logging
import sys
from config.settings import settings


def setup_logger(name: str = "stock_recommendation") -> logging.Logger:
    """Set up and configure logger.
    
    Args:
        name: Logger name
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, settings.log_level.upper(), logging.INFO))
    
    # Create console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)
    
    # Add handler to logger
    if not logger.handlers:
        logger.addHandler(handler)
    
    return logger


# Global logger instance
logger = setup_logger()
