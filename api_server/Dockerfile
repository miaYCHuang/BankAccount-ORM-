FROM python:3-alpine3.15 
WORKDIR /app
COPY . /app
ENV SQLALCHEMY_DATABASE_URI=mysql://root:12345678@db_mysql/api
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add --no-cache mariadb-dev
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 3000
CMD python ./main.py
