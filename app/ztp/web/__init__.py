"""Web service.

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

from pathlib import Path

import responder

here = Path(__file__).parent
static_dir = here/"static"
templates_dir = here/"templates"

api = responder.API(
    static_dir=str(static_dir),
    static_route="/static",
    templates_dir=str(templates_dir),
    title="Rapid Zero-Touch Provisioning (ZTP) App",
    version="0.1",
    openapi="3.0.0",
    docs_route="/api",
)


# Import Views
import ztp.web.views.api.device_data    # noqa
import ztp.web.views.api.templates      # noqa
import ztp.web.views.config             # noqa
