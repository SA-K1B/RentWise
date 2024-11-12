FROM python:latest
WORKDIR /mainapp

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY ./requirements.txt /mainapp
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /mainapp
CMD [ "python3","manage.py","runserver" ]