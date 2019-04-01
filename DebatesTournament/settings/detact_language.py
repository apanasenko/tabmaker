import detectlanguage
import os

DETECT_LANGUAGE_API_KEY = os.getenv('DETECT_LANGUAGE_API_KEY', None)
if DETECT_LANGUAGE_API_KEY:
    detectlanguage.configuration.api_key = DETECT_LANGUAGE_API_KEY
