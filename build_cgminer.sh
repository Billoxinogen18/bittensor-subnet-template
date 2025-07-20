#!/usr/bin/env bash
set -e

# Simple build script for cgminer_zeus on Debian/Ubuntu
apt-get update && apt-get install -y \
  git build-essential automake autoconf pkg-config libtool \
  libcurl4-openssl-dev libusb-1.0-0-dev libjansson-dev libncurses5-dev

mkdir -p /opt && cd /opt
if [ ! -d cgminer_zeus ]; then
  git clone https://github.com/zeusminer/cgminer_zeus.git
fi
cd cgminer_zeus
git submodule update --init --recursive || true
chmod +x autogen.sh configure || true
./autogen.sh || true
CFLAGS="-O2 -Wall" ./configure --enable-icarus --disable-scrypt --disable-opencl --disable-adl
make -j$(nproc)
make install 