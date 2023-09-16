FROM python:3-alpine3.15



WORKDIR /app

COPY . /app
RUN pip instal -r requirements.txt
EXPOSE 3000

CMD python ./index.py