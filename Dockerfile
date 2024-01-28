# syntax=docker/dockerfile:1
FROM python:3-slim-bookworm
# VOLUME /dist
WORKDIR /temp
COPY dist .
# ENV MYVAR=hello
ENV MYUSER=danaukes
ENV MYGID=1000
ENV MYUID=1000
#export PATH=$PATH:$HOME/.local/bin

COPY docker-requirements.txt requirements.txt

#RUN apt update && apt install -y git python3 python3-pip
RUN apt update && apt install -y git
RUN groupadd -g ${MYGID} ${MYUSER}
RUN useradd -u ${MYUID} -g ${MYGID} -p $(perl -e 'print crypt($ARGV[0], "password")' 'test') -G adm,sudo ${MYUSER} && mkdir /home/${MYUSER} && chown ${MYUSER}:${MYUSER} /home/${MYUSER}

USER ${MYUSER}

#RUN pwd
#RUN ls -la 
# RUN ls -la dist/

RUN pip3 install -r requirements.txt
RUN pip3 install git_manage-0.0.9-py2.py3-none-any.whl
ENV PATH=${PATH}:/home/${MYUSER}/.local/bin

# ENV PATH=${PATH}:/home/danaukes/code_git_tools/python/git_manage/
# ENV PYTHONPATH=${PYTHONPATH}:/home/danaukes/code_git_tools/python/

# COPY . .
#ADD /test/code_git_tools /test/code_git_tools/
#CMD ["gitman", "status"]


# docker build --progress plain -t gitman ./build/
