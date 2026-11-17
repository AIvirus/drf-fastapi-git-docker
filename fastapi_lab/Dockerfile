# Lesson 18: a recipe for building an image of the Study Tasks API.

# 1. Start from an official, small image that already has Python installed.
FROM python:3.13-slim

# 2. Python settings that are good inside containers:
#    don't write .pyc files, and print logs immediately.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 3. All the next commands run inside /app (in the image).
WORKDIR /app

# 4. Install packages FIRST. Docker caches this step, so rebuilding after
#    a code change is fast (packages are only re-installed if requirements.txt changes).
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Now copy our code (.dockerignore keeps .venv, tasks.db, .env etc. out).
COPY . .

# 6. Document which port the app listens on.
EXPOSE 8000

# 7. The command that runs when a container starts.
#    --host 0.0.0.0 = accept connections from outside the container.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
