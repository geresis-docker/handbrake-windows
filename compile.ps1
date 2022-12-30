docker build -t handbrake:latest .
docker run --rm -it -v ${PWD}:/data handbrake:latest
docker image rm handbrake:latest
