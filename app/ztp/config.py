"""App default and imported configurations.

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

import os


# Logging
_log_levels = {"CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"}
LOG_LEVEL = os.environ.get("LOG_LEVEL", "").upper() \
    if os.environ.get("LOG_LEVEL", "").upper() in _log_levels else "WARNING"


# Responder
RESPONDER_ADDRESS = os.environ.get("RESPONDER_ADDRESS", "0.0.0.0")
RESPONDER_PORT = int(os.environ.get("PORT")) \
                 or int(os.environ.get("RESPONDER_PORT")) \
                 or 8000
RESPONDER_DEBUG = os.environ.get("RESPONDER_DEBUG", "false").lower() == "true"


# MondoDB
MONGO_DATABASE = "ztp"
MONGO_URL = os.environ.get("MONGO_URL", "mongodb://localhost:27017")
