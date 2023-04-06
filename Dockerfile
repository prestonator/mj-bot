FROM python:3.11.2-slim

WORKDIR /bot

COPY requirements.txt /bot/

RUN apt update && apt install -y git

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . /bot

RUN pip install -U py-cord==2.4.1

# Expose the FastAPI server port
EXPOSE 8269

CMD python main.py