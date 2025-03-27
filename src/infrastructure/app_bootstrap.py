"""Application bootstrap module to separate infrastructure concerns."""

import sys
import signal
from pathlib import Path
from src.config.settings import Settings
from src.config.logging_config import configure_logging
from src.infrastructure.server import AppServer
from src.infrastructure.container import Container
from src.infrastructure.logging_context import get_contextual_logger

logger = None  # Will be configured by configure_logging


def bootstrap_application():
    """Bootstrap the application with proper separation of concerns."""
    try:
        # Load settings from YAML and environment variables
        config_path = Path(__file__).parent.parent / "config" / "service_config.yaml"
        settings = Settings.from_yaml(config_path)

        # Configure logging first
        configure_logging(debug=settings.debug)

        # Get logger after configuration
        global logger
        logger = get_contextual_logger(__name__)

        logger.info(f"Loading configuration from {config_path}")
        logger.info(f"Starting {settings.app_name} version {settings.app_version}")

        # Wire up dependency injection
        container = Container()
        container.set_settings(settings)

        # Create and run server
        server = AppServer(settings, container)

        # Set up signal handlers
        signal.signal(signal.SIGINT, server.handle_exit)
        signal.signal(signal.SIGTERM, server.handle_exit)

        # Run the server (this is blocking)
        server.run()

    except KeyboardInterrupt:
        if logger:
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
