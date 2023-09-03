FROM mcr.microsoft.com/devcontainers/base:jammy

# Selección de shell
SHELL ["/bin/bash", "-c"]

# Instalar compiladores e intérpretes de varios lenguajes de programación:
# C/C++, Python, Assembly, SQL, etc.
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get --yes install --no-install-recommends \
    build-essential \
    nasm \
    python3-full \
    python3-pip \
    sqlite3 \
    && apt-get clean

# Agregar el usuario UAEM
ARG USERNAME=uaem
ARG USER_UID=1001
ARG USER_GID=$USER_UID
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && mkdir -p /home/$USERNAME/ \
    && chown -R $USER_UID:$USER_GID /home/$USERNAME \
    && echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/99-$USERNAME
USER $USERNAME
    