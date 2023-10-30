"""Logging."""

# Internal libraries
from onclusiveml.core.logging import get_default_logger
from onclusiveml.tracking.tracking_settings import TrackingLibraryLogSettings


tracking_library_logger = get_default_logger(
    __name__, **TrackingLibraryLogSettings().dict()
)
