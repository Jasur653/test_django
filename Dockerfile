# Python bazasida image yaratamiz
FROM python:3.11-slim

# Ishchi katalog yaratamiz
WORKDIR /app

# Talablar faylini ko‘chiramiz
COPY requirements.txt .

# Kutubxonalarni o‘rnatamiz
RUN pip install --no-cache-dir -r requirements.txt

# Butun loyihani konteynerga ko‘chiramiz
COPY . .

# Django development serverni ishga tushiramiz
CMD ["python", "wms_project/manage.py", "runserver", "0.0.0.0:8000"]
