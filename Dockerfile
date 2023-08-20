FROM buildpack-deps:bookworm-scm
ENV USER=uaem
ENV GID=1000
ENV UID=1000

RUN apt-get update && apt-get install -y \
    build-essential \
    openjdk-17-jdk \
    pipenv

RUN groupadd -g ${GID} ${USER} && \
    useradd -m -u ${UID} -g ${GID} ${USER}

USER ${USER}