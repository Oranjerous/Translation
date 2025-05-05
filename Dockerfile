# استخدم صورة بايثون الرسمية كأساس
FROM python:3.11-slim

# تثبيت المتطلبات الأساسية للنظام
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1-mesa-glx \
    fonts-dejavu-core \
    libgomp1 \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# إنشاء مجلد للتطبيق
WORKDIR /app

# نسخ الملفات
COPY . /app

# تثبيت المتطلبات
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# تعيين المنفذ
ENV PORT=8080
EXPOSE 8080

# تشغيل التطبيق
CMD ["python", "app.py"]