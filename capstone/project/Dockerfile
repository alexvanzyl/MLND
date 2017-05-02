FROM continuumio/anaconda3:latest

MAINTAINER Alexander van Zyl <vanzyl.alex@gmail.com>

RUN conda install jupyter -y --quiet && \
    pip install beautifulsoup4 tabulate && \
    mkdir /opt/notebooks && \
    groupadd -r alex && \
    useradd -r -g alex alex && \
    chown -R alex:alex /opt/notebooks && \
    mkdir /home/alex && \
    chmod -R 0777 /home/alex 

RUN usermod -u 1000 alex

USER alex

EXPOSE 8888

CMD ["jupyter","notebook" ,"--notebook-dir=/opt/notebooks", "--ip='*'", "--port=8888", "--no-browser"]