FROM ubuntu:16.04

RUN apt-get update
RUN apt-get install -y xinetd libc6-i386 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*


RUN useradd -m oil
WORKDIR /home/oil


RUN cp -R /lib* /home/oil && \
    cp -R /usr/lib* /home/oil

RUN mkdir /home/oil/dev && \
    mknod /home/oil/dev/null c 1 3 && \
    mknod /home/oil/dev/zero c 1 5 && \
    mknod /home/oil/dev/random c 1 8 && \
    mknod /home/oil/dev/urandom c 1 9 && \
    chmod 666 /home/oil/dev/*

RUN mkdir /home/oil/bin && \
    cp /bin/sh /home/oil/bin && \
    cp /bin/ls /home/oil/bin && \
    cp /bin/cat /home/oil/bin

RUN chown -R root:oil /home/oil

COPY ./oil.xinetd /etc/xinetd.d/oil
RUN chmod 400 /etc/xinetd.d/oil

COPY ./xinetd_start.sh /start.sh
RUN chmod 100 /start.sh

COPY ./run.sh /run.sh
RUN chmod 100 /run.sh

COPY ./service/oil /home/oil/task/oil
RUN chmod 111 /home/oil/task/oil


RUN useradd --no-create-home --shell /bin/false getflag

COPY ./getflag/getflag /home/oil/task/getflag
RUN chown -R getflag:getflag /home/oil/task/getflag
RUN chmod 111 /home/oil/task/getflag
RUN chmod +s /home/oil/task/getflag

RUN mkdir -p /home/oil/etc/tokens
COPY ./getflag/tokens /home/oil/etc/tokens/tokens
RUN chown -R root:getflag /home/oil/etc/tokens/tokens
RUN chmod 440 /home/oil/etc/tokens/tokens


CMD ["/start.sh"]

EXPOSE 9999
