FROM python:3.7
COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip3 install --upgrade pip
RUN venv/bin/pip3 install -r requirements.txt

COPY project/* application/
ENV FLASK_DEBUG=1
EXPOSE 5050
WORKDIR application/
CMD ../venv/bin/gunicorn --workers=1 --bind 0.0.0.0:5050 service1:app

