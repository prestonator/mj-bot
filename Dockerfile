FROM python:3.11.2-slim

WORKDIR /bot

COPY requirements.txt /bot/

RUN apt update && apt install -y git

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . /bot

RUN pip install -U py-cord==2.4.1

# Set environment variables from build arguments
ARG DAVINCI_TOKEN
ARG SERVER_ID
ARG SALAI_TOKEN
ARG CHANNEL_ID
ARG MID_JOURNEY_ID
ARG USE_MESSAGED_CHANNEL
ARG IMAGE_WEBHOOK_URL

ENV DAVINCI_TOKEN=$DAVINCI_TOKEN
ENV SERVER_ID=$SERVER_ID
ENV SALAI_TOKEN=$SALAI_TOKEN
ENV CHANNEL_ID=$CHANNEL_ID
ENV MID_JOURNEY_ID=$MID_JOURNEY_ID
ENV USE_MESSAGED_CHANNEL=$USE_MESSAGED_CHANNEL
ENV IMAGE_WEBHOOK_URL=$IMAGE_WEBHOOK_URL

# Expose the FastAPI server port
EXPOSE 8269

CMD python run.py