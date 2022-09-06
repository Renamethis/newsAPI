FROM python:3.10.5

RUN pip install -U pip 
RUN pip install pipenv
ADD . .
RUN pipenv install --system --deploy --ignore-pipfile
RUN export LC_ALL="ru_RU.UTF-8"
RUN export LC_CTYPE="ru_RU.UTF-8"
RUN apt update
RUN apt-get install -y locales locales-all wget unzip
RUN dpkg-reconfigure locales