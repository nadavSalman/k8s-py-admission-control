
FROM python:3.9-slim

WORKDIR /app

COPY . /app/


RUN update-ca-certificates


COPY "requirements.txt" ./

# RUN pip  install -r /app/requirements.txt

ENV FLASK_APP=/app/main.py

# ENV FLASK_ENV=development

EXPOSE 443


# flask run --host=0.0.0.0 --port=443 --debug --cert=/cert/cert.pem --key=/cert/private.key
CMD ["flask", "run", "--debug" ,"--port=443","--host=0.0.0.0" , "--cert=/cert/cert.pem" , "--key=/cert/private.key"]