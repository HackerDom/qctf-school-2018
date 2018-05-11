FROM ubuntu:16.04

RUN apt-get update
RUN apt-get install -y xinetd && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*


RUN useradd -M auth
RUN useradd -M --shell /bin/false getflag


COPY ./hard-pwn.xinetd /etc/xinetd.d/auth
RUN chmod 400 /etc/xinetd.d/auth


RUN mkdir /chroot
WORKDIR /chroot


RUN cp -R /lib* . && \
    cp -R /usr/lib* .

RUN mkdir ./dev && \
    mknod ./dev/null c 1 3 && \
    mknod ./dev/zero c 1 5 && \
    mknod ./dev/random c 1 8 && \
    mknod ./dev/urandom c 1 9 && \
    chmod 666 ./dev/*

RUN mkdir ./bin && \
    cp /bin/sh ./bin/ && \
    cp /bin/ls ./bin/ && \
    cp /bin/cat ./bin/ && \
    cp /bin/pwd ./bin/ && \
    cp /bin/bash ./bin/ && \
    cp /usr/bin/whoami ./bin/

RUN mkdir ./etc/ && \
    cp /etc/passwd ./etc/


RUN mkdir -p ./home/auth/

RUN echo "cd /home/auth && ./auth" >./start.sh
RUN chmod 555 ./start.sh

RUN chown -R root:root .


COPY ./getflag/getflag ./home/auth/
RUN chown -R getflag:getflag ./home/auth/getflag && \
    chmod 111 ./home/auth/getflag && \
    chmod +s ./home/auth/getflag

COPY ./getflag/tokens ./etc/
RUN chown -R root:getflag ./etc/tokens && \
    chmod 440 ./etc/tokens


COPY ./service/main ./home/auth/auth
RUN chmod 555 ./home/auth/auth


COPY ./xinetd_start.sh /xinetd_start.sh
RUN chmod 700 /xinetd_start.sh

CMD ["/xinetd_start.sh"]


EXPOSE 9999
