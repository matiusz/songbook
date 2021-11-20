# No reasonable latex packages for alpine
FROM ubuntu:focal

RUN apt-get update && apt-get install -y \
    python3 python3-pip \
    perl wget libfontconfig1 && \
    # The only reasonable way of installing pdflatex I found, see https://tex.stackexchange.com/a/493882
    wget -qO- "https://yihui.name/gh/tinytex/tools/install-unx.sh" | sh  && \
    apt-get clean

ENV PATH="${PATH}:/root/bin"

# This will probably install all the latex crap ever invented
# so it takes forever, occupies several GB and returns error if any plugin fails
RUN tlmgr install scheme-full || echo "who cares ¯\_(ツ)_/¯"

RUN pip install aiofiles pyside6

COPY . /app
WORKDIR /app