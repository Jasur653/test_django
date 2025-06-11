# Python bazasida image yaratamiz
FROM python:3.11-slim

# Ishchi katalog
WORKDIR /app

# Talablar faylini ko‘chiramiz
COPY requirements.txt .

# Kutubxonalarni o‘rnatamiz
RUN pip install --no-cache-dir -r requirements.txt

# Butun loyihani konteynerga ko‘chiramiz
COPY . .

# Gunicorn bilan Django WSGI ilovasini ishga tushuramiz
CMD ["gunicorn", "wms_project.wsgi:application", "--bind", "0.0.0.0:8000"]
