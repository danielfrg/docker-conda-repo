FROM nginx

RUN apt-get update && apt-get install -y wget bzip2

RUN wget -q http://repo.continuum.io/miniconda/Miniconda-latest-Linux-x86_64.sh
RUN /bin/bash /Miniconda-latest-Linux-x86_64.sh -b -p /opt/conda
RUN rm Miniconda-latest-Linux-x86_64.sh
RUN /opt/conda/bin/conda install -y -q conda-build
ENV PATH /opt/conda/bin:$PATH

RUN /opt/conda/bin/pip install watchdog
COPY watch.py /opt/watch.py

RUN mkdir /channel
WORKDIR /channel

RUN mv /etc/nginx/conf.d/default.conf /tmp
COPY channel.conf /etc/nginx/conf.d/channel.conf

COPY start.sh /opt/start.sh
CMD ["bash", "/opt/start.sh"]
