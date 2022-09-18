FROM 164267459440.dkr.ecr.us-west-2.amazonaws.com/pyenv:latest

LABEL maintainer="Zella Zhong <zella@mask.io>"

WORKDIR /var/task/dataloader

RUN mkdir -p /var/task/dataloader/postgresql
RUN mkdir -p /var/task/dataloader/src

COPY run.sh .
COPY requirements.txt .
COPY supervisord.conf .
COPY postgresql ./postgresql
COPY src ./src

# ENTRYPOINT ["./run.sh"]
CMD ["./run.sh"]