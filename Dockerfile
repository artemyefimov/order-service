FROM python:3.14-slim

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:0.9.17 /uv /bin/uv

# Copy project files
COPY pyproject.toml uv.lock ./
COPY src/ src/

# Install dependencies
RUN uv sync --locked --no-dev

# Expose port
EXPOSE 8000

# Run application
CMD ["uv", "run", "python", "src/main.py"]
