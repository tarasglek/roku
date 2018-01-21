FROM python:2.7-alpine3.7
RUN pip install wakeonlan requests
COPY roku.py server.py /