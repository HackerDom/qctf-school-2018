FROM python:3.6

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /service/
WORKDIR /service/

COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r ./requirements.txt

COPY ./ ./

EXPOSE 80

CMD ["./run-with-gunicorn.sh"]
