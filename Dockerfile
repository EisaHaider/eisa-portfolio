# استخدام نسخة بايثون رسمية وخفيفة
FROM python:3.10-slim

# تحديد مجلد العمل داخل الحاوية الافتراضية لجوجل
WORKDIR /workspace

# نسخ ملف المكتبات وتثبيتها أولاً
COPY requirements.txt /workspace/
RUN pip install --no-cache-dir -r requirements.txt

# نسخ بقية ملفات مشروع الفلاسك بالكامل
COPY . /workspace/

# تشغيل التطبيق باستخدام Gunicorn والربط مع 0.0.0.0 لضمان وصول الاتصالات من Cloud Run
CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 0 app:app