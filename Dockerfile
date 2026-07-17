# استخدام نسخة بايثون رسمية وخفيفة
FROM python:3.10-slim

# تحديد مجلد العمل داخل الحاوية الافتراضية لجوجل
WORKDIR /workspace

# نسخ ملف المكتبات وتثبيتها أولاً
COPY requirements.txt /workspace/
RUN pip install --no-cache-dir -r requirements.txt

# نسخ بقية ملفات مشروع الفلاسك بالكامل
COPY . /workspace/

# تشغيل التطبيق باستخدام Gunicorn (متوافق مع app = Flask(__name__) في ملف app.py)
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app