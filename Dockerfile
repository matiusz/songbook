# No reasonable latex packages for alpine
FROM texlive/texlive:latest-basic

RUN apt-get clean && apt-get update && apt-get install -y locales locales-all && locale-gen pl_PL pl_PL.UTF-8 && update-locale 

RUN tlmgr install babel blindtext paracol geometry tools changepage graphics hyperref inconsolata etoolbox pgf xkeyval upquote collection-fontsrecommended

RUN apt-get install -y --no-install-recommends python3-pip

RUN pip3 install aiofiles --break-system-packages

WORKDIR /app