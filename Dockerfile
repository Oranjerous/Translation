# استخدم صورة أساس تحتوي على Python و Debian لتثبيت Tesseract
FROM python:3.11-slim

# تثبيت أدوات النظام + Tesseract
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# تحديد مجلد العمل
WORKDIR /app

# نسخ جميع ملفات المشروع إلى داخل الحاوية
COPY . .

# تثبيت متطلبات المشروع
RUN pip install --no-cache-dir -r requirements.txt

# تحديد المنفذ الذي سيستمع عليه Flask
ENV PORT=5000

# تحديد أمر التشغيل
CMD ["python", "app.py"]