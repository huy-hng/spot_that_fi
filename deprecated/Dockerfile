FROM python:3.8-slim-buster

WORKDIR /usr/src/app
RUN mkdir -p /usr/src/app/logs
COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .
COPY ./src/.cache ./.cache
CMD [ "python", "src/main.py" ]

# docker build -t kasa_controller .
# docker run -p 5000:5000 --detach --name kasa_controller kasa_controller