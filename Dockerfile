FROM python:3.11-slim

# Install cgminer build deps
RUN apt-get update && apt-get install -y git build-essential automake autoconf pkg-config libtool libcurl4-openssl-dev libusb-1.0-0-dev libjansson-dev libncurses5-dev && rm -rf /var/lib/apt/lists/*

# Copy code
WORKDIR /app
COPY . /app

# Build cgminer
RUN bash build_cgminer.sh

# Install python dependencies
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "neurons/miner.py"] 