FROM python:latest
ENV PYTHONUNBUFFERED 1

WORKDIR /var/www/backend

COPY requirements.txt .

RUN python3 -m venv env 
RUN . env/bin/activate
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# COPY . .

#RUN python manage.py makemigrations
