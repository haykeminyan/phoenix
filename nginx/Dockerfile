FROM ubuntu:23.04

RUN apt-get update -y \
    && apt-get install python3-certbot-nginx -y \
    && apt-get clean

EXPOSE 80
EXPOSE 443


STOPSIGNAL SIGTERM

CMD ["nginx", "-g", "daemon off;"]
