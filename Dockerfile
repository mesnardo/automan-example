# Dockerfile for aeropython with automan framework

FROM ubuntu:16.04
MAINTAINER Olivier Mesnard <mesnardo@gwu.edu>

# Install base system
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      build-essential git vim wget ca-certificates

# Install Miniconda
RUN shscript=Miniconda3-latest-Linux-x86_64.sh && \
    url=https://repo.continuum.io/miniconda/${shscript} && \
    wget ${url} -P /tmp && \
    bash /tmp/${shscript} -b -p "/opt/miniconda3" && \
    rm -f /tmp/${shscript}
ENV PATH="/opt/miniconda3/bin":$PATH

# Install aeropython-0.1.1-lite
COPY aeropython-0.1.1-lite.tar.gz /tmp
RUN version=0.1.1-lite && \
    tarball=aeropython-${version}.tar.gz && \
    srcdir=/opt/aeropython/${version} && \
    mkdir -p ${srcdir} && \
    tar -xzf /tmp/${tarball} -C ${srcdir} --strip-components=1 && \
    cd ${srcdir} && \
    conda install scipy numpy pandas matplotlib && \
    python setup.py install && \
    rm -f /tmp/${tarball}

# Install automan-0.2
RUN version=0.2 && \
    tarball=release-${version}.tar.gz && \
    url=https://github.com/pypr/automan/archive/${tarball} && \
    wget ${url} -P /tmp && \
    srcdir=/opt/automan/${version} && \
    mkdir -p ${srcdir} && \
    tar -xzf /tmp/${tarball} -C ${srcdir} --strip-components=1 && \
    cd ${srcdir} && \
    python setup.py install && \
    rm -f /tmp/${tarball}
