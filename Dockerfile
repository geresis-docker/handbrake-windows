# Handbrake, compile hb.dll with aac-fdk support
# based on https://forum.videohelp.com/threads/383208-How-to-get-HandBrake-with-FDK-AAC-for-Windows
# and https://handbrake.fr/docs/en/latest/developer/build-windows.html
FROM ubuntu:latest

LABEL version="1.3.3"

# INSTALL NON INTERACTIVE
ARG DEBIAN_FRONTEND=noninteractive

# VARIABLES
ENV HANDBRAKE_VERSION 1.3.3
ENV HANDBRAKE_32BIT false
ENV UID 0
ENV GID 0

# CREATE FOLDER
RUN mkdir /app /data

# COPY FILE
COPY app.py /app

# UPDATE AND INSTALL DEPENDENCIES
RUN apt-get update && \
	apt-get install -y automake autoconf autopoint build-essential cmake gcc git intltool libtool libtool-bin m4 make meson nasm ninja-build patch pkg-config python tar zlib1g-dev && \
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
