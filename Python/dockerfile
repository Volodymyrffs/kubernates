FROM python:3.13.3-slim as base
RUN apt-get update && apt-get install -y curl ca-certificates && rm -rf /var/lib/apt/lists/*


WORKDIR /app
COPY aws.py .
# COPY obama.jpg .
# COPY obama1.jpg .


RUN pip install --no-cache-dir boto3 requests

ENTRYPOINT ["python", "/app/aws.py"] 

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV TELEGRAM_BOT_TOKEN=" "
ENV TELEGRAM_CHAT_ID=" " 
ENV AWS_ACCESS_KEY_ID=" "
ENV AWS_SECRET_ACCESS_KEY=" "

#Better docker run -e TELEGRAM_BOT_TOKEN=xxx -e AWS_SECRET_ACCESS_KEY=yyy  -e TELEGRAM_CHAT_ID=sss -e AWS_ACCESS_KEY_ID=ttt
