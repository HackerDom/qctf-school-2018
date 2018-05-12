FROM ubuntu:16.04

RUN apt-get update
RUN apt-get install -y xinetd libc6-i386 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*


RUN useradd -M --shell /bin/false getflag && \
    useradd -M auth

RUN echo "auth - nproc 1000" > /etc/security/limits.d/auth.conf && \
    echo "getflag - nproc 1000" > /etc/security/limits.d/getflag.conf


RUN mkdir /chroot
WORKDIR /chroot

RUN mkdir -p ./home/auth/

RUN echo "cd /home/auth/ && ./auth" >./start.sh && \
    chmod 555 ./start.sh


RUN cp -R /lib* . && \
    cp -R /usr/lib* .

RUN mkdir ./dev && \
    mknod ./dev/null c 1 3 && \
    mknod ./dev/zero c 1 5 && \
    mknod ./dev/random c 1 8 && \
    mknod ./dev/urandom c 1 9 && \
    chmod 666 ./dev/*

RUN mkdir ./bin/ && \
    cp /bin/sh ./bin/ && \
    cp /bin/ls ./bin/ && \
    cp /bin/cat ./bin/ && \
    cp /bin/pwd ./bin/ && \
    cp /usr/bin/whoami ./bin/ && \
    ln -s /bin/sh ./bin/bash

RUN mkdir ./etc/ && \
    cp /etc/passwd ./etc/

RUN chown -R root:root .


COPY ./getflag/getflag ./home/auth/
RUN chown -R getflag:getflag ./home/auth/getflag && \
    chmod 111 ./home/auth/getflag && \
    chmod +s ./home/auth/getflag

COPY ./getflag/tokens ./etc/tokens
RUN chown -R root:getflag ./etc/tokens && \
    chmod 440 ./etc/tokens

COPY ./service/main ./home/auth/auth
RUN chmod 111 ./home/auth/auth


COPY ./hard-pwn.xinetd /etc/xinetd.d/auth
COPY ./xinetd_start.sh /xinetd_start.sh

RUN chmod 400 /etc/xinetd.d/auth && \
    chmod 100 /xinetd_start.sh


CMD ["/xinetd_start.sh"]

EXPOSE 9999
