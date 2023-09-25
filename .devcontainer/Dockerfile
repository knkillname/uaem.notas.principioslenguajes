# Usar Debian Linux 12 (Bookworm) como base para la imagen.
FROM buildpack-deps:bookworm

# Instalar compiladores e intérpretes de varios lenguajes de programación:
# Assembly, C/C++, Haskell, Java, Prolog, Python, SQL, etc.
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get --yes install --no-install-recommends \
    build-essential \
    graphviz \
    graphviz-dev \
    haskell-stack \
    nasm \
    openjdk-17-jdk \
    pipenv \
    gprolog \
    python3-dev \
    python3-full \
    scala \
    sqlite3 \
    && apt-get clean
