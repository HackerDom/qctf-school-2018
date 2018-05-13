FROM ubuntu:16.04

RUN apt-get update
RUN apt-get install -y xinetd libc6-i386 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*


RUN useradd -M library && \
    echo "library - nproc 1000" > /etc/security/limits.d/library.conf


RUN mkdir /chroot
WORKDIR /chroot

RUN mkdir -p ./home/library/

RUN echo "cd /home/library/ && ./library" >./start.sh && \
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


COPY ./service/library ./home/library/library
COPY ./service/*.txt ./home/library/

RUN chmod 111 ./home/library/library && \
    chmod 444 ./home/library/*.txt


COPY ./library.xinetd /etc/xinetd.d/library
COPY ./xinetd_start.sh /xinetd_start.sh

RUN chmod 400 /etc/xinetd.d/library && \
    chmod 100 /xinetd_start.sh


CMD ["/xinetd_start.sh"]

EXPOSE 9999
