FROM alpine:3.9.6
ENV FLASK_SKIP_DOTENV 1
ENV XDG_RUNTIME_DIR /tmp/runtime-root

WORKDIR /home/app

ADD requirements.txt /home/app
ADD . /home/app
ADD server.py /home/app

RUN apk update && \
    apk add ca-certificates && \
    apk add linux-headers && \
    apk add g++ && \
    apk add make && \
    apk  add python3 && \
    apk  add python3-dev && \
    apk add xvfb && \
    apk add xdpyinfo && \
    apk add --no-cache wkhtmltopdf && \
    pip3 install --upgrade pip && \
    pip3 install -r requirements.txt

RUN apk update && \
    apk add --no-cache curl fontconfig && \
    curl -O https://noto-website.storage.googleapis.com/pkgs/NotoSansCJKjp-hinted.zip && \
    mkdir -p /usr/share/fonts/NotoSansCJKjp && \
    unzip NotoSansCJKjp-hinted.zip -d /usr/share/fonts/NotoSansCJKjp/ && \
    rm NotoSansCJKjp-hinted.zip && \
    curl https://fonts.google.com/download?family=Abel > Abel.zip && \
    mkdir -p /usr/share/fonts/Abel && \
    unzip Abel.zip -d /usr/share/fonts/Abel/ && \
    rm Abel.zip && \
    fc-cache -fv

CMD python3 server.py
EXPOSE 3020
