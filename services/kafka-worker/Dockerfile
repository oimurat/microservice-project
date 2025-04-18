FROM python:3.11
WORKDIR /app
COPY ./app /app
RUN pip install kafka-python
CMD ["python", "consumer.py"]