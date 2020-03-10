FROM python:3.8-alpine

WORKDIR /app

COPY . .

RUN apk add --no-cache --virtual .build-deps \
    gcc musl-dev \
    libxslt-dev libxml2-dev &&\
    pip install lxml && \
    apk del .build-deps && \
    apk add --no-cache libxslt libxml2 && \
    pip install -r requirements.txt

EXPOSE 80

CMD ["python"]
