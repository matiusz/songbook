# No reasonable latex packages for alpine
FROM ubuntu:focal

RUN apt-get update && apt-get install -y \
    python3 python3-pip \
    apt-transport-https \
    ca-certificates \
    dirmngr \
    ghostscript \
    gnupg \
    gosu \
    make \
    perl \
    language-pack-pl \
    language-pack-pl-base

RUN apt-get clean

RUN echo 'Acquire::https::ctan.gust.org.pl::Verify-Peer "false";' > /etc/apt/apt.conf.d/99influxdata-cert

RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys D6BC243565B2087BC3F897C9277A7293F59E4889

RUN echo "deb http://miktex.org/download/ubuntu focal universe" | tee /etc/apt/sources.list.d/miktex.list

RUN apt-get update -y \
    &&  DEBIAN_FRONTEND='noninteractive' apt-get install -y --no-install-recommends \
    miktex

RUN miktexsetup finish \
    && initexmf --admin --set-config-value=[MPM]AutoInstall=1 \
    && miktex packages update \
    && miktex packages install amsfonts \
    && initexmf --admin --update-fndb
    
ENV PATH="${PATH}:/root/bin"

RUN cd ~/.miktex/texmfs/install/miktex/config && miktex-makefmt --engine=pdftex --dest-name=pdflatex --no-dump pdflatex.ini

RUN pip install aiofiles

WORKDIR /app
