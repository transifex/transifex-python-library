FROM debian:stable
MAINTAINER Konstantinos Koukopoulos <kouk@transifex.com>

ENV PYENV_ROOT $HOME/.pyenv
ENV PATH $HOME/.pyenv/shims:$HOME/.pyenv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

RUN apt-get update && \
    apt-get install -y make git build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev \
                       libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils && \
    curl -L https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash

RUN pyenv install 2.7.13
RUN pyenv install 3.6.1
RUN pyenv install pypy-5.7.1

RUN pyenv local 2.7.13 && \
    pip install --upgrade setuptools pip tox tox-pyenv && \
    pyenv local --unset
RUN pyenv local 3.6.1 && \
    pip install --upgrade setuptools pip tox tox-pyenv && \
    pyenv local --unset
RUN pyenv local pypy-5.7.1 && \
    pip install --upgrade setuptools pip tox tox-pyenv && \
    pyenv local --unset

RUN pyenv local 2.7.13 3.6.1 pypy-5.7.1

