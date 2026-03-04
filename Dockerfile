FROM python:3.13-slim

# Instalar Node.js 20 + Chromium + dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    chromium \
    fonts-liberation \
    fonts-noto-color-emoji \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && rm -rf /var/lib/apt/lists/*

# Puppeteer usa el Chromium del sistema
ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true
ENV PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium

WORKDIR /app

# Dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Dependencias Node (pdf-generator)
COPY pdf-generator/package.json pdf-generator/package-lock.json pdf-generator/
RUN cd pdf-generator && npm ci --omit=dev

# Codigo de la app
COPY app_unified.py .
COPY pdf-generator/generate-pdf-api.js pdf-generator/

# Puerto
EXPOSE 8080

CMD ["uvicorn", "app_unified:app", "--host", "0.0.0.0", "--port", "8080"]
