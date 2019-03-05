"""Web service launcher.

Copyright (c) 2019 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

import logging

import ztp.web
from ztp.config import LOG_LEVEL, RESPONDER_ADDRESS, RESPONDER_PORT


logger = logging.getLogger(__name__)


def configure_logging():
    """Configure application logging services.

    As a containerized app all output should be directed to stdout and stderr
    for collection by the container runtime environment.
    """
    logging.basicConfig(
        level=LOG_LEVEL,
        datefmt="%Y-%m-%dT%H:%M:%S%z",
        format="%(asctime)s %(levelname)-8s [%(name)s] %(message)s",
    )


if __name__ == "__main__":
    configure_logging()

    ztp.web.api.run(address=RESPONDER_ADDRESS, port=RESPONDER_PORT)

    logging.shutdown()
