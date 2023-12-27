FROM python:3.10

WORKDIR /usr/src/app

COPY requirements.txt ./
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["gunicorn", "gctic_pbi.wsgi:application", "--bind", "0.0.0.0:8000"]