# Build stage
FROM python:3.13-alpine AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Runtime stage
FROM python:3.13-alpine

WORKDIR /app

# Create non-root user
RUN adduser -D -u 1000 appuser && chown -R appuser:appuser /app

# Copy dependencies from builder [ Multi stage build]
COPY --from=builder --chown=appuser:appuser /root/.local /home/appuser/.local

# Copy application
COPY --chown=appuser:appuser app.py .

# Switch to non-root user
USER appuser

# Add local bin to PATH
ENV PATH=/home/appuser/.local/bin:$PATH

EXPOSE 8080

CMD ["python", "app.py"]
