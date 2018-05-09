FROM ubuntu:16.04

RUN apt-get update
RUN apt-get install -y xinetd && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*


RUN useradd -M library


COPY ./library.xinetd /etc/xinetd.d/library
RUN chmod 400 /etc/xinetd.d/library


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

RUN mkdir ./bin/ && \
    cp /bin/sh ./bin/ && \
    cp /bin/ls ./bin/ && \
    cp /bin/cat ./bin/ && \
    cp /bin/pwd ./bin/ && \
    cp /bin/bash ./bin/ && \
    cp /usr/bin/whoami ./bin/

RUN mkdir ./etc/ && \
    cp /etc/passwd ./etc/

RUN mkdir -p ./home/library/

RUN echo "cd /home/library/ && ./library" >./start.sh
RUN chmod 555 ./start.sh

RUN chown -R root:root .


COPY ./service/library ./home/library/
RUN chmod 555 ./home/library/library

COPY ./service/*.txt ./home/library/
RUN chmod 444 ./home/library/*.txt


COPY ./xinetd_start.sh /xinetd_start.sh
RUN chmod 100 /xinetd_start.sh

CMD ["/xinetd_start.sh"]


EXPOSE 9999
