# Docker Setup for Flask Personal Website

This document explains how to containerize and deploy the Flask personal website using Docker.

## Files Overview

### `Dockerfile`
The main Docker configuration file that:
- Uses Python 3.11 slim base image
- Installs system dependencies (gcc, sqlite3)
- Sets up Python environment
- Creates non-root user for security
- Includes health checks
- Exposes port 5000

### `.dockerignore`
Excludes unnecessary files from Docker build context:
- Git files and version control
- Python cache and compiled files
- Virtual environments
- IDE files
- Test files and coverage reports
- Documentation files
- Temporary files

### `docker-compose.yml`
Orchestrates the application with:
- Web service (Flask app)
- Optional nginx reverse proxy for production
- Volume mounts for data persistence
- Environment configuration
- Health checks

### `nginx.conf`
Production-ready nginx configuration with:
- Reverse proxy to Flask app
- Static file serving
- Security headers
- Health check endpoint
- Proper timeouts

## Quick Start

### 1. Build and Run with Docker Compose (Recommended)

```bash
# Build and start the application
docker-compose up --build

# Run in background
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop the application
docker-compose down
```

### 2. Build and Run with Docker Commands

```bash
# Build the Docker image
docker build -t flask-personal-website .

# Run the container
docker run -p 5000:5000 flask-personal-website

# Run with volume mount for data persistence
docker run -p 5000:5000 -v $(pwd)/data:/app/data flask-personal-website
```

## Development vs Production

### Development Mode
```bash
# Use docker-compose with development settings
docker-compose up --build

# The application will be available at http://localhost:5000
```

### Production Mode
```bash
# Use docker-compose with nginx reverse proxy
docker-compose --profile production up -d --build

# The application will be available at http://localhost:80
```

## Environment Variables

You can customize the application behavior using environment variables:

```bash
# Development
docker run -p 5000:5000 \
  -e FLASK_ENV=development \
  -e FLASK_DEBUG=1 \
  flask-personal-website

# Production
docker run -p 5000:5000 \
  -e FLASK_ENV=production \
  -e FLASK_DEBUG=0 \
  flask-personal-website
```

## Data Persistence

The database file needs to persist between container restarts:

```bash
# Create data directory
mkdir -p ./data

# Run with volume mount
docker run -p 5000:5000 \
  -v $(pwd)/data:/app/data \
  flask-personal-website
```

## Health Checks

The Dockerfile includes health checks that verify the application is running:

```bash
# Check container health
docker ps

# View health check logs
docker inspect <container_id> | grep -A 10 Health
```

## Building for Different Platforms

### Build for Linux AMD64
```bash
docker build --platform linux/amd64 -t flask-personal-website .
```

### Build for ARM64 (Apple Silicon)
```bash
docker build --platform linux/arm64 -t flask-personal-website .
```

### Multi-platform build
```bash
docker buildx build --platform linux/amd64,linux/arm64 -t flask-personal-website .
```

## Security Considerations

### Non-root User
The Dockerfile creates and uses a non-root user (`appuser`) for security.

### Security Headers
The nginx configuration includes security headers:
- X-Frame-Options
- X-XSS-Protection
- X-Content-Type-Options
- Referrer-Policy
- Content-Security-Policy

### Resource Limits
You can add resource limits to prevent resource exhaustion:

```yaml
# In docker-compose.yml
services:
  web:
    # ... other configuration
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: '0.5'
        reservations:
          memory: 256M
          cpus: '0.25'
```

## Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Check what's using port 5000
   lsof -i :5000
   
   # Use a different port
   docker run -p 8080:5000 flask-personal-website
   ```

2. **Database Permission Issues**
   ```bash
   # Fix data directory permissions
   sudo chown -R $USER:$USER ./data
   ```

3. **Build Failures**
   ```bash
   # Clean Docker cache
   docker system prune -a
   
   # Rebuild without cache
   docker build --no-cache -t flask-personal-website .
   ```

4. **Container Won't Start**
   ```bash
   # Check container logs
   docker logs <container_id>
   
   # Run interactively for debugging
   docker run -it flask-personal-website /bin/bash
   ```

### Debugging Commands

```bash
# Enter running container
docker exec -it <container_id> /bin/bash

# View container processes
docker exec <container_id> ps aux

# Check file permissions
docker exec <container_id> ls -la /app

# Test database connection
docker exec <container_id> sqlite3 /app/data/projects.db ".tables"
```

## Deployment Options

### 1. Local Development
```bash
docker-compose up --build
```

### 2. Cloud Deployment (AWS, GCP, Azure)
- Build and push image to container registry
- Deploy using container services
- Configure load balancers and SSL

### 3. Self-hosted VPS
```bash
# On your server
git clone <your-repo>
cd personal_webpage
docker-compose --profile production up -d --build
```

### 4. Docker Swarm
```bash
# Initialize swarm
docker swarm init

# Deploy stack
docker stack deploy -c docker-compose.yml flask-app
```

## Performance Optimization

### Multi-stage Build (Optional)
For smaller images, you could use a multi-stage build:

```dockerfile
# Build stage
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Runtime stage
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
# ... rest of configuration
```

### Image Optimization
```bash
# Analyze image size
docker images flask-personal-website

# Remove unused layers
docker image prune

# Use .dockerignore to exclude unnecessary files
```

## Monitoring and Logging

### View Logs
```bash
# Docker Compose logs
docker-compose logs -f

# Docker logs
docker logs -f <container_id>

# Follow specific service logs
docker-compose logs -f web
```

### Log Rotation
Add log rotation to prevent disk space issues:

```yaml
# In docker-compose.yml
services:
  web:
    # ... other configuration
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

## Backup and Recovery

### Database Backup
```bash
# Backup database
docker exec <container_id> sqlite3 /app/data/projects.db ".backup /app/data/backup.db"

# Copy backup from container
docker cp <container_id>:/app/data/backup.db ./backup.db
```

### Full Container Backup
```bash
# Save container as image
docker commit <container_id> flask-personal-website:backup

# Save image to file
docker save flask-personal-website:backup > backup.tar
```

This Docker setup provides a robust, secure, and scalable way to deploy your Flask personal website!
