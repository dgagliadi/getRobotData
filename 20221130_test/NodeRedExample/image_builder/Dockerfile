# Reduce image size using the slim python base
#FROM python:3.7-slim
FROM nodered/node-red

COPY package.json .
RUN npm install --unsafe-perm --no-update-notifier --no-fund --only=production

COPY settings.js /data/settings.js
COPY flows_cred.json /data/flows_cred.json
COPY flows.json /data/flows.json

#WORKDIR /app

#COPY src /app/
#RUN python3 -m pip install -r docker-requirements.txt --find-links .

#RUN apt-get update
#RUN apt-get install -y procps curl ftp

#RUN npm install node-red-node-smooth

CMD ["/bin/bash", "/app/run_example_service.sh"]
