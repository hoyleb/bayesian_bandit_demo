# To enable ssh & remote debugging on app service change the base image to the one below
FROM python:3

RUN apt-get update -y
RUN apt-get install -y bash

RUN /usr/local/bin/python -m pip install --upgrade pip

COPY requirements.txt /
RUN pip install -r /requirements.txt

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app
# COPY data /app/data
COPY lib /app/lib


RUN export LC_ALL=en_US.UTF-8
RUN export LANG=en_US.UTF-8

EXPOSE 80
EXPOSE 8080
EXPOSE 5000

ENTRYPOINT [ "/bin/bash", "-c"]
CMD ["exec python app.py"]