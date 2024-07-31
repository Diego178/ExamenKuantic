FROM python:3.12.3

RUN apt-get update && \
    apt-get install -y git nano && \
    apt-get clean

WORKDIR /app
RUN git clone https://github.com/Diego178/ExamenKuantic.git
WORKDIR /app/ExamenKuantic
COPY .env .env
RUN pip3 install --no-cache-dir -r requirements.txt
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]