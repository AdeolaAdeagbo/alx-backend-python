FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose default Django port
EXPOSE 8000

# Run Django server on all interfaces (required for ALX checker)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# Run Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
