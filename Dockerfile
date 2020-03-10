FROM python:3.7-alpine

RUN apk add --update --no-cache --virtual .build-deps \
        g++ \
        python-dev \
        libxml2 \
        libxml2-dev && \
    apk add libxslt-dev && \
    apk del .build-deps

COPY . /app

RUN pip install -r /app/requirements.txt

EXPOSE 80

CMD ["python"]
