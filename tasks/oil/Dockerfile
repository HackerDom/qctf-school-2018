FROM ubuntu:16.04

RUN apt-get update
RUN apt-get install -y xinetd libc6-i386 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*


RUN useradd oil


COPY ./oil.xinetd /etc/xinetd.d/oil
RUN chmod 400 /etc/xinetd.d/oil

COPY ./xinetd_start.sh /start.sh
RUN chmod 100 /start.sh

COPY ./service/oil /home/oil/oil
RUN chmod 111 /home/oil/oil


RUN useradd --no-create-home --shell /bin/false getflag

COPY ./getflag/getflag /home/oil/getflag
RUN chown -R getflag:getflag /home/oil/getflag
RUN chmod 111 /home/oil/getflag
RUN chmod +s /home/oil/getflag

RUN mkdir -p /usr/share/tokens
COPY ./getflag/tokens /usr/share/tokens/tokens
RUN chown -R getflag:getflag /usr/share/tokens/tokens
RUN chmod 440 /usr/share/tokens/tokens


CMD ["/start.sh"]

EXPOSE 9999
