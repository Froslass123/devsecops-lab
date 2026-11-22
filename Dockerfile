FROM python:3.13-slim@sha256:e48f59cdba69a3cbd9ed2cf0f348d90d45a8d350d98134cf1070bc106ee9ed90

#Dont cache compiled .pyc files to disk. They're useless inside a container that never changes
ENV PYTHONDONTWRITEBYTECODE=1 \
#logs are printed right away instead of waiting in a buffer, so they cant be lost if the container crashes
    PYTHONUNBUFFERED=1

WORKDIR /app

#copy and install our dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --require-hashes -r requirements.txt

COPY app.py .

#Create a new user instead of root, so if somebody take over the app it's harder to tamper/escape the container
RUN useradd --create-home --uid 10001 appuser
USER appuser

#documents which port the app listens on and run gunicorn
EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]