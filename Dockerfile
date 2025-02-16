
FROM python:3.9-slim

WORKDIR /osunsk

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "main.py"]