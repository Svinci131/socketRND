FROM python:3.4-alpine
RUN apk add --update python py-pip
ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]