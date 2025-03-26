import asyncio
import signal
import sys
import threading
from pathlib import Path
import uvicorn
from src.config.settings import Settings
from src.config.logging_config import configure_logging
from src.infrastructure.rest_server import create_app
from src.infrastructure.logging_context import get_contextual_logger

logger = None  # Will be configured by configure_logging


class AppServer:
    """Wrapper for Uvicorn server with proper shutdown handling."""

    def __init__(self, settings: Settings):
        self.settings = settings
        self.should_exit = threading.Event()
        self.app = create_app(settings)

    def run(self):
        """Run the server in a way that can be properly stopped."""
        logger.info(
            f"Starting server on http://{self.settings.host}:{self.settings.port}"
        )

        # Run Uvicorn directly (this is a blocking call)
        uvicorn.run(
            app=self.app,
            host=self.settings.host,
            port=self.settings.port,
            lifespan="on",
            loop="asyncio",
        )

    def handle_exit(self, sig, frame):
        """Handle exit signal."""
        logger.info(f"Received exit signal {sig}, shutting down...")
        self.should_exit.set()


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

        # Create and run server
        server = AppServer(settings)

        # Set up signal handlers
        signal.signal(signal.SIGINT, server.handle_exit)
        signal.signal(signal.SIGTERM, server.handle_exit)

        # Run the server (this is blocking)
        server.run()

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
