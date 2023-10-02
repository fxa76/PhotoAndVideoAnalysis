FROM rabbitmq:3.12
RUN rabbitmq-plugins enable --offline rabbitmq_management
RUN apt-get update; apt-get --assume-yes install curl
RUN mkdir /userscript
ADD ./userscript/usersetup.sh /userscript
ENTRYPOINT ["./userscript/usersetup.sh"]
EXPOSE 5672 5672
EXPOSE 15671 15672
