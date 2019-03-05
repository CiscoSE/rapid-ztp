# Rapid ZTP App | Docker Image
FROM python:3.6


ENV LC_ALL=C.UTF-8 \
    LANG=C.UTF-8


# Ensure Python package installation tools are up-to-date and install pipenv
RUN pip install -q --upgrade --no-cache-dir pip setuptools wheel && \
    pip install pipenv -q --no-cache-dir


# Setup non-priviledged user and working directory
RUN groupadd -r --gid 25639 ztpapp && \
    useradd -r --uid 25639 --no-log-init --create-home -g ztpapp ztpapp
USER ztpapp
WORKDIR /app

#    chown -R ztpapp:ztpapp /home/ztpapp /app && \
#    chmod 755 /home/ztpapp /app


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
