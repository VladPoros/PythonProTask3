FROM python:3.8

WORKDIR /task5

COPY . .

RUN pip install -r requirements.txt

ENV FLASK_APP Task3.py

EXPOSE 5000

CMD ["flask", "run", "-h", "0.0.0.0", "-p", "80"]
