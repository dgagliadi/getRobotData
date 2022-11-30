# Reduce image size using the slim python base
FROM python:3.8-slim

WORKDIR /app

COPY src /app/
RUN python3 -m pip install -r docker-requirements.txt --find-links .

RUN apt-get update
RUN apt-get install -y procps curl ftp

CMD ["/bin/bash", "/app/run_example_service.sh"]
