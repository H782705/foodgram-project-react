FROM python:3.8.5
WORKDIR /code
COPY requirements.txt .
RUN pip3 install --upgrade pip && pip install  -r requirements.txt
COPY . .
CMD ["gunicorn", "backend.wsgi:application", "--bind", "0:8000" ]
