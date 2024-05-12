FROM python:3.12.3 AS base
WORKDIR /app
EXPOSE 5000

RUN pip3 install -U Flask
RUN pip3 install -U flask-restplus

COPY ./Src /app/Src
COPY ./main.py /app/main.py
#COPY . /app/.

CMD ["python", "main.py"]