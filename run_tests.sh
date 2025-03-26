#!/bin/bash

# Run all tests with coverage
echo "Running tests with coverage..."
pytest tests/ --cov=src --cov-report=term --cov-report=html --junitxml=junit.xml -v

# Check if tests passed
if [ $? -eq 0 ]; then
    echo "All tests passed successfully!"
    echo "Coverage report available in htmlcov/index.html"
    echo "JUnit XML report available in junit.xml"
else
    echo "Tests failed. Please check the output above."
    exit 1
fi