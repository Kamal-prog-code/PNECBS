FROM python:3
ENV PYTHONUNBUFFERED 1
WORKDIR /PNECBS
ADD . /PNECBS
COPY ./requirements.txt /PNECBS/requirements.txt
RUN --mount=type=cache,target=/root/.cache/pip pip3 install -r requirements.txt
COPY . /PNECBS
