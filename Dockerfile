FROM python:3.6-alpine


COPY ./requirements.txt /img/requirements.txt


WORKDIR /img

RUN apk add mariadb  mariadb-connector-c

RUN pip3 install -r requirements.txt


RUN pip3 install mysql-connector-python


COPY .  /img




ENV DB_NAME=statistics
ENV DB_USER=app
ENV DB_PASSWORD=123456Hh@
ENV DB_HOST=10.0.2.4
ENV DB_PORT=3306

ENTRYPOINT [ "python3" ]

CMD ["app.py" ]

