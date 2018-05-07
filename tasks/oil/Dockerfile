FROM ubuntu:16.04

RUN apt-get update
RUN apt-get install -y xinetd libc6-i386 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*


RUN useradd -M oil
RUN useradd --no-create-home --shell /bin/false getflag


COPY ./oil.xinetd /etc/xinetd.d/oil
RUN chmod 400 /etc/xinetd.d/oil


COPY ./chroot_run.sh /chroot_run.sh
RUN chmod 100 /chroot_run.sh


COPY ./xinetd_start.sh /xinetd_start.sh
RUN chmod 100 /xinetd_start.sh


RUN mkdir /chroot
WORKDIR /chroot

RUN echo "cd /home/oil && ./oil" >./start.sh
RUN chmod 555 ./start.sh

RUN cp -R /lib* . && \
    cp -R /usr/lib* .

RUN mkdir ./dev && \
    mknod ./dev/null c 1 3 && \
    mknod ./dev/zero c 1 5 && \
    mknod ./dev/random c 1 8 && \
    mknod ./dev/urandom c 1 9 && \
    chmod 666 ./dev/*

RUN mkdir ./bin && \
    cp /bin/sh ./bin && \
    cp /bin/ls ./bin && \
    cp /bin/cat ./bin && \
    cp /bin/pwd ./bin && \
    cp /bin/bash ./bin && \
    cp /usr/bin/whoami ./bin

RUN mkdir ./etc && \
    cp /etc/passwd ./etc

RUN mkdir -p ./home/oil

RUN chown -R root:root .


COPY ./service/oil ./home/oil/oil
RUN chmod 111 ./home/oil/oil

COPY ./getflag/getflag ./home/oil/getflag
RUN chown -R getflag:getflag ./home/oil/getflag && \
    chmod 111 ./home/oil/getflag && \
    chmod +s ./home/oil/getflag

RUN mkdir -p ./etc/tokens
COPY ./getflag/tokens ./etc/tokens/tokens
RUN chown -R root:getflag ./etc/tokens/tokens && \
    chmod 440 ./etc/tokens/tokens


CMD ["/xinetd_start.sh"]

EXPOSE 9999
