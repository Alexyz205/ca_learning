"""Server implementation module separating server concerns from application bootstrap."""

import threading
import uvicorn
from src.config.settings import Settings
from src.infrastructure.container import Container
from src.infrastructure.logging_context import get_contextual_logger
from src.infrastructure.rest_server import create_app

logger = get_contextual_logger(__name__)


class AppServer:
    """Server abstraction that hides implementation details."""

    def __init__(self, settings: Settings, container: Container):
        """Initialize server with settings and container."""
        self.settings = settings
        self.container = container
        self.should_exit = threading.Event()
        self.app = create_app(settings)
        # Ensure the container is available to the app
        self.app.state.container = container

    def run(self):
        """Run the server using Uvicorn."""
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
