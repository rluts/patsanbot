FROM python:3.8


WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt

ADD . /app

CMD ["python", "main.py"]