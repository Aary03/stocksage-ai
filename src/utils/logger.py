import logging
from rich.logging import RichHandler
from rich.traceback import install

# Install rich traceback handling
install(show_locals=True)

# Configure logging with rich handler
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)

# Get logger instance
logger = logging.getLogger("src.utils.logger")