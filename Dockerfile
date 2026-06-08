# 1. Start FROM a base image: a minimal Linux that already has Python 3.12.
#    "slim" = a smaller, stripped-down variant. Good default.
FROM python:3.12-slim

# 2. git is needed because requirements.txt installs fairpyx from GitHub.
#    We install it, then delete the package lists to keep the image small.
RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*

# 3. Everything after this happens inside /app inside the image.
WORKDIR /app

# 4. Copy ONLY requirements first, then install. (Explained below — this is a
#    caching trick so you don't reinstall everything on every code change.)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Now copy the rest of your project into the image.
COPY . .

# 6. Document that the app listens on 5000 (Flask's default port).
EXPOSE 5000

# 7. The command Docker runs when the container starts.
CMD ["python", "app.py"]
