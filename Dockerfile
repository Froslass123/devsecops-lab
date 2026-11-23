FROM python:3.15-slim@sha256:65a65fc7b30b06cb6df4930fd4650697cb23f4c2698ab81fc87e4b031bc36928

# CVE-2026-85091 (zlib): patched in Debian, but not yet in the base image, so install the exact fixed version
# remove this once a newer base image (Dependabot bump) already contains it
RUN apt-get update && apt-get install -y --no-install-recommends zlib1g=1:1.3.dfsg+really1.3.1-1+deb13u1 \
 && rm -rf /var/lib/apt/lists/*

#Dont cache compiled .pyc files to disk. They're useless inside a container that never changes
ENV PYTHONDONTWRITEBYTECODE=1 \
#logs are printed right away instead of waiting in a buffer, so they cant be lost if the container crashes
    PYTHONUNBUFFERED=1

WORKDIR /app

#copy and install our dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --require-hashes -r requirements.txt \
#remove pip after installing requirements  because its dependencies have unfixed CVEs and we don't need it anymore
 && pip uninstall -y pip

COPY app.py .

#Create a new user instead of root, so if somebody take over the app it's harder to tamper/escape the container
RUN useradd --create-home --uid 10001 appuser
USER appuser

#documents which port the app listens on and run gunicorn
EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]