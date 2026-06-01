FROM python:3.12

RUN apt-get update && apt-get install -y tzdata

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 7860

CMD panel serve AI_Software_Engineer_Assistant.py \
    --address 0.0.0.0 \
    --port 7860 \
    --allow-websocket-origin=*