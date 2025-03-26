import asyncio
import signal
import sys
from pathlib import Path
from typing import Set
import uvicorn
from src.config.settings import Settings
from src.config.logging_config import configure_logging
from src.infrastructure.rest_server import create_app
from src.infrastructure.logging_context import get_contextual_logger

logger = None  # Will be configured by configure_logging

class SignalHandler:
    """Handle system signals for graceful shutdown."""
    
    def __init__(self):
        self._shutdown_requested = False
        self._tasks: Set[asyncio.Task] = set()
        
    @property
    def shutdown_requested(self) -> bool:
        return self._shutdown_requested
        
    def request_shutdown(self, signum, frame):
        """Request application shutdown."""
        if logger:
            logger.info(f"Received signal {signum}, initiating shutdown")
        self._shutdown_requested = True
        
    def setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown."""
        signal.signal(signal.SIGTERM, self.request_shutdown)
        signal.signal(signal.SIGINT, self.request_shutdown)

async def start_application(settings: Settings, signal_handler: SignalHandler):
    """Start and manage the application lifecycle."""
    config = uvicorn.Config(
        app=create_app(settings),
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_config=None,  # Disable uvicorn's logging config to use ours
        lifespan="on"  # Ensure lifespan events are properly handled
    )
    server = uvicorn.Server(config)
    
    # Override server signal handling to use our handler
    server.should_exit = lambda: signal_handler.shutdown_requested
    
    # Use a cleaner approach to handle server shutdown
    try:
        await server.serve()
    except asyncio.CancelledError:
        logger.info("Server task was cancelled, shutting down gracefully")

def main():
    try:
        # Load settings from YAML and environment variables
        config_path = Path(__file__).parent / "config" / "service_config.yaml"
        settings = Settings.from_yaml(config_path)
        
        # Configure logging first
        configure_logging(debug=settings.debug)
        
        # Get logger after configuration
        global logger
        logger = get_contextual_logger(__name__)
        
        logger.info(f"Loading configuration from {config_path}")
        logger.info(f"Starting {settings.app_name} version {settings.app_version}")
        
        # Setup signal handling
        signal_handler = SignalHandler()
        signal_handler.setup_signal_handlers()
        
        # Run the application
        asyncio.run(start_application(settings, signal_handler))
        
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt, shutting down")
    except Exception as e:
        # If logger isn't configured yet, print to stderr
        if logger:
            logger.error(f"Failed to start application: {str(e)}", exc_info=True)
        else:
            print(f"Failed to start application: {str(e)}", file=sys.stderr)
        sys.exit(1)
    finally:
        if logger:
            logger.info("Application shutdown complete")

if __name__ == "__main__":
    main()