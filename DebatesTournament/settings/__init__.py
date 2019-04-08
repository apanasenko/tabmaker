import os
if not int(os.getenv('ENVIRONMENT_LOADED', 0)):
    # TODO Убрать после правильной настройки прода, пока так
    import dotenv
    dotenv.read_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env'))

from .defaults import *
from .database import *
from .allauth import *
from .smtp_email import *
from .static import *
from .telegram_bot import *
from .detact_language import *
from .debug import *
from .logging import *
