# Imagem base Python 3.12 slim
FROM python:3.12-slim

# Variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libffi-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copiar arquivos de dependências
COPY requirements.txt /app/
COPY requirements-dev.txt /app/

# Instalar dependências Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copiar restante do projeto
COPY . /app/

# Rodar collectstatic no build
RUN python manage.py collectstatic --noinput

# Comando de start
CMD gunicorn stryn.wsgi:application --bind 0.0.0.0:${PORT} --workers=3 --timeout=180 --log-file -

