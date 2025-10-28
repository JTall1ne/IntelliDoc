# Use official Python runtime as a parent image
FROM python:3.10-slim

# Set work directory
WORKDIR /app

# Copy pyproject and install dependencies
COPY pyproject.toml ./
RUN pip install --upgrade pip && pip install .

# Copy the rest of the application code
COPY . .

# Default command runs CLI help
CMD ["intellidoc", "--help"]
