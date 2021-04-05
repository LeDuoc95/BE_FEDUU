FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install --upgrade pip && pip install -r requirements.txt
# RUN apt-get update && apt-get install -y build-essential curl git libfreetype6-dev libpng12-dev libzmq3-dev pkg-config python-dev python-numpy python-pip software-properties-common swig zip zlib1g-d && pip install -r requirements.txt
# RUN apk update && apk add --no-cache libffi-dev && apk add --no-cache python3-dev jpeg-dev zlib-dev && apk add --no-cache postgresql-libs && \
#  apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
#  python3 -m pip install -r requirements.txt --no-cache-dir && \
#  apk --purge del .build-deps
COPY . /code/

# # entrypoint, must be executable file chmod +x entrypoint.sh
# COPY entrypoint.sh /home/docker/entrypoint.sh

# # what happens when I start the container
# CMD ["/home/docker/entrypoint.sh"]