FROM python:3.10

WORKDIR /app

COPY . .

EXPOSE 80

RUN pip3 install -r requirements.txt

CMD ["python", "server.py"] 
