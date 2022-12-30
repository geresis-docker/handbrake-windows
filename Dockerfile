# handbrake, compile 64 bit version of hb.dll and HandBrake.exe with aac-fdk support
# based on https://handbrake.fr/docs/en/latest/developer/build-windows.html
FROM ubuntu:22.04

# VARIABLES
ARG DEBIAN_FRONTEND=noninteractive
ARG VERSION="1.6.0"

# INFORMATION
LABEL version=$VERSION

# ENVIRONMENT
ENV VERSION=$VERSION

# CREATE FOLDER
RUN mkdir /app /data

# COPY FILE
COPY app.py /app

# UPDATE AND INSTALL DEPENDENCIES
RUN apt-get update && \
	apt-get install -y automake autoconf autopoint build-essential cmake gcc git intltool libtool libtool-bin m4 make meson nasm ninja-build patch pkg-config tar zlib1g-dev && \
# Install the additional dependencies required to build the MinGW-w64 toolchain
	apt-get install -y bison bzip2 curl flex g++ gzip pax && \
# Additional for docker app.py
	apt-get install -y python3 && \
# Cleanup
	rm -rf /var/lib/apt/lists/*

# VOLUME
VOLUME ["/data"]

# ENTRYPOINT
WORKDIR /app
CMD ["python3", "app.py"]
