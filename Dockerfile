FROM python:3

RUN pip install --upgrade pip
RUN pip install requests beautifulsoup4
RUN pip install cssutils
