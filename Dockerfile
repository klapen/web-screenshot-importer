FROM ubuntu:16.04

LABEL maintainer="Orlando Saavedra <osaavedra@bora.com.co>"
RUN apt-get update -y && apt-get install -y python3 python3-dev python3-pip

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

ENV EQ_HOST=0.0.0.0
ENV EQ_PORT=5000

COPY ./src /app
RUN python3 init_db.py
EXPOSE 5000

ENTRYPOINT [ "python3" ]

CMD [ "api.py" ]

