FROM python:3.10.11-slim-bullseye

# set work directory
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y --no-install-recommends build-essential libpq-dev curl default-libmysqlclient-dev default-mysql-client


# Install Node to build Frontend
RUN curl -sL https://deb.nodesource.com/setup_16.x | bash -
RUN apt-get install -y nodejs

COPY . .

WORKDIR /app/client
#COPY client/package*.json ./
RUN node -v
RUN npm install

RUN npm run build

WORKDIR /app
RUN pip install --upgrade pip
RUN pip install pymysql
RUN pip install mysqlclient
RUN pip install -r requirements.txt


EXPOSE 8000

ADD docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod a+x /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]