FROM ubuntu:16.04

RUN apt-get update
RUN apt-get install -y xinetd libc6-i386 && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN useradd -m oil

WORKDIR /home/oil

RUN mkdir /home/oil/dev && \
    mknod /home/oil/dev/null c 1 3 && \
    mknod /home/oil/dev/zero c 1 5 && \
    mknod /home/oil/dev/random c 1 8 && \
    mknod /home/oil/dev/urandom c 1 9 && \
    chmod 666 /home/oil/dev/*

RUN mkdir /home/oil/bin && \
    cp /bin/sh /home/oil/bin && \
    cp /bin/ls /home/oil/bin && \
    cp /bin/cat /home/oil/bin && \
    cp /bin/su /home/oil/bin

COPY ./oil.xinetd /etc/xinetd.d/oil
COPY ./start.sh /start.sh
COPY ./service/oil /home/oil/oil
COPY ./run.sh /run.sh

RUN chmod +x /start.sh
RUN chmod 777 /home/oil/oil
RUN chmod +x /run.sh

RUN echo "HELLO!" > /home/oil/flag
RUN chown -R root:oil /home/oil && \
    chmod -R 750 /home/oil && \
    chmod 777    /home/oil/flag

CMD ["/start.sh"]

EXPOSE 9999