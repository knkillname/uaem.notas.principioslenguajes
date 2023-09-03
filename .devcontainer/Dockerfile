FROM buildpack-deps:bookworm

# Instalar compiladores e intérpretes de varios lenguajes de programación:
# Assembly, C/C++, Java, Python, SQL, etc.
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get --yes install --no-install-recommends \
    build-essential \
    nasm \
    openjdk-17-jdk \
    pipenv \
    python3-full \
    sqlite3 \
    && apt-get clean
