# Rapid ZTP App | Docker Image
FROM python:3.6


ENV LC_ALL=C.UTF-8 \
    LANG=C.UTF-8


RUN pip install -q --upgrade --no-cache-dir pip setuptools wheel && \
    pip install pipenv -q --no-cache-dir


# Setup working directory and non-priviledged user
WORKDIR /app
RUN groupadd -r ztpapp && \
    useradd --no-log-init -r -g ztpapp ztpapp && \
    mkdir -p /home/ztpapp && \
    chown -R ztpapp:ztpapp /home/ztpapp /app && \
    chmod 755 /home/ztpapp /app
USER ztpapp


# Install app dependencies and setup Python virtual environment
COPY Pipfile Pipfile.lock ./
RUN set -ex && \
    pipenv sync && \
    rm -rf ~/.cache


# Copy Application Code
COPY ./ ./


# Expose Volumes and Ports
VOLUME /app


CMD ["/bin/bash"]
