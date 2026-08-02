# syntax=docker/dockerfile:1.7
# escape=\ (backslash)
# Source: https://docs.docker.com/engine/reference/builder/

ARG VERSION=1.0
FROM image:${VERSION} as builder
WORKDIR /etc/test
RUN mkdir -p some/dirs
ONBUILD RUN echo "\
    hello\
    world"

FROM builder as builder2
WORKDIR /etc/test
USER user:notroot
COPY app some/dirs/

FROM image2:latest
LABEL org.label-schema.schema-version="1.0"
COPY --from=builder2 /etc/test .
ADD test.txt /absoluteDir/
SHELL ["bash", "--login"]
RUN --mount=type=cache,target=/var/cache/apk <<'EOF'
set -eu
echo "Building..."
EOF
RUN \
    /bin/bash | grep -e "test" \
    || echo "fail" \
    && echo -e 'bash' "is running" > /dev/null;
RUN ls /etc/*
RUN ["uname"]
ENV \
    PORT_TO_EXPOSE=4242 \
    LANG=C.UTF-8 \
    PATH="/opt/bin:${PATH}"

EXPOSE $PORT_TO_EXPOSE 8080/tcp
VOLUME [/my_files]
STOPSIGNAL SIGKILL
HEALTHCHECK --interval=30s --timeout=5s \
    CMD ["test", "-f", "/etc/os-release"] || exit 1
CMD [/usr/bin/zsh, -D]
CMD echo "String...." 'also string'
ENTRYPOINT su-exec user:group application
