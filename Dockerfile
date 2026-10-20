
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Create a non-root user
RUN groupadd --system app && \
    useradd --system --gid app --create-home app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY --chown=app:app app ./app

# Prepare the directory used by Flask and SQLite
RUN mkdir -p /app/instance && \
    chown -R app:app /app

USER app

EXPOSE 5000

CMD ["python", "-m", "flask", "--app", "app", "run", "--host=0.0.0.0", "--port=5000"]
