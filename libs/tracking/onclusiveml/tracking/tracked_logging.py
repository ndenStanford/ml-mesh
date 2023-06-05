# Internal libraries
from onclusiveml.core.logging import get_default_logger
from onclusiveml.core.logging.constants import DEFAULT_LOGGING_HANDLER
from onclusiveml.tracking.tracking_settings import (
    TrackingLibraryLoggingSettings,
)


tracking_library_logger = get_default_logger(
    handler=DEFAULT_LOGGING_HANDLER, **TrackingLibraryLoggingSettings().dict()
)
