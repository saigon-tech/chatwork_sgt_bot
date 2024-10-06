FROM python:3.9.15-slim
LABEL maintainer="Huy Nguyen <nqhuy.sgt@gmail.com>"


# install litestream
ADD https://github.com/benbjohnson/litestream/releases/download/v0.3.13/litestream-v0.3.13-linux-amd64.tar.gz /tmp/litestream.tar.gz
RUN tar -C /usr/local/bin -xzf /tmp/litestream.tar.gz

RUN pip3 install --upgrade pip

# set timezone
RUN apt-get update && apt-get install -y tzdata 
ENV TIME_ZONE Asia/Ho_Chi_Minh
RUN echo "${TIME_ZONE}" > /etc/timezone \
    && ln -sf /usr/share/zoneinfo/${TIME_ZONE} /etc/localtime

RUN useradd -m user
USER user

ENV INSTALL_PATH /home/user/sgtbot
RUN mkdir -p $INSTALL_PATH
WORKDIR $INSTALL_PATH

COPY --chown=user:user . .

ENV PATH="/home/user/.local/bin:${PATH}"

RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip3 install --user --editable .

ENV FLASK_APP ${INSTALL_PATH}/run.py
