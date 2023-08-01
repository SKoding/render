FROM python:3.10.7

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /TPK/gisTrees

COPY requirements.txt /TPK/gisTrees/

# Build psycopg2-binary from source -- add required required dependencies
RUN apk add --virtual .build-deps --no-cache postgresql-dev gcc python3-dev musl-dev && \
        pip install --no-cache-dir -r requirements.txt && \
        apk --purge del .build-deps

COPY . /TPK/gisTrees/

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]