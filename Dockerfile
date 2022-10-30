FROM python:3.9

RUN mkdir /kudrinka_django

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

WORKDIR /kudrinka_django
COPY . /kudrinka_django/
COPY requirements.txt /kudrinka_django/
ADD . /kudrinka_django/

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
