from validators import url as validator
import logging
logger = logging.getLogger(__name__)

def validate_url(url):
    if not url:
        return False
    try:
        return validator(url)
    except Exception as e:
        logger.error(e.args)
        return False