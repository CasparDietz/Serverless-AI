# FROM ghcr.io/openfaas/classic-watchdog:0.2.0 as watchdog

# FROM alpine:3.12

# RUN mkdir -p /home/app

# COPY --from=watchdog /fwatchdog /usr/bin/fwatchdog
# RUN chmod +x /usr/bin/fwatchdog

# # Add non root user
# RUN addgroup -S app && adduser app -S -G app
# RUN chown app /home/app

# WORKDIR /home/app

# USER app

# # Populate example here - i.e. "cat", "sha512sum" or "node index.js"
# ENV fprocess="cat"
# # Set to true to see request in function logs
# ENV write_debug="false"

# EXPOSE 8080

# HEALTHCHECK --interval=3s CMD [ -e /tmp/.lock ] || exit 1

# CMD ["fwatchdog"]

###############################################################################
FROM --platform=${TARGETPLATFORM:-linux/amd64} openfaas/of-watchdog:0.7.7 as watchdog
FROM --platform=${TARGETPLATFORM:-linux/amd64} python:3.7-slim-buster

COPY --from=watchdog /fwatchdog /usr/bin/fwatchdog 
RUN chmod +x /usr/bin/fwatchdog 

# Uncomment if you want to use native modules
RUN apt-get -qy update && apt-get -qy install gcc make

# Add non root user
RUN addgroup --system app && adduser app --system --ingroup app 
RUN chown app /home/app 

USER app 
ENV PATH=$PATH:/home/app/.local/bin 

WORKDIR /home/app/

#COPY server.py          .
#COPY ../server.py    .
COPY server.py/        .
#COPY requirements.txt   .
COPY requirements.txt    .
RUN mkdir -p /home/app/RecievedFrames
RUN mkdir -p /home/app/Frames

USER root
RUN pip install -r requirements.txt

WORKDIR /home/app/

RUN chown -R app:app *
USER app

ENV fprocess="python3 server.py"

# Now set the watchdog as the start-up process
# Along with the HTTP mode, and an upstream URL to 
# where your HTTP server will be running from the original
# image.
ENV upstream_url="http://127.0.0.1:5000" 
ENV mode="http"
ENV cgi_headers="true"

CMD ["fwatchdog"]

