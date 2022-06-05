FROM centos

MAINTAINER tarutaru

LABEL title="sampleImage"\
      version="1.0"\
      description="This is a sample."

RUN mkdir /myvol
RUN echo "hello world" > /myvol/greeting
VOLUME /myvol

ENV hoge=hogehoge

EXPOSE 80

WORKDIR /tmp
RUN ["pwd"]

ADD https://github.com/docker/cli/blob/master/README.md /tmp

COPY sample.txt /tmp
