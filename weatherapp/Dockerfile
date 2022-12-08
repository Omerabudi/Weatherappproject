FROM python:3.10-slim

WORKDIR /omerproject

COPY ./requirements.txt /omerproject/
RUN pip install -r requirements.txt

COPY . /omerproject/

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["python","manage.py","runserver","0.0.0.0:8000"]