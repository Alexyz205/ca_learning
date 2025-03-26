.PHONY: build test dev prod clean

build:
	docker-compose build

test:
	docker-compose run --rm test

dev:
	docker-compose -f docker-compose.yaml -f .devcontainer/docker-compose.dev.yaml up app

prod:
	docker-compose up app

clean:
	docker-compose down -v
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type d -name ".pytest_cache" -exec rm -r {} +
	find . -type d -name "htmlcov" -exec rm -r {} +
	find . -type f -name ".coverage" -delete