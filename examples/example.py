#!/usr/bin/env python
"""Example script demonstrating template and data upload and config retrieval.

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

import requests
from pathlib import Path
import json


SERVER_HOST = "localhost"


here = Path(__file__).parent

device_data_file = here/"switch-device-data.json"
with open(device_data_file) as file:
    device_data = json.load(file)

template_file = here/"switch-template.txt"
template_name = template_file.stem
with open(template_file) as file:
    template_text = file.read()


print(f"==> Uploading template '{template_file.name}'")
response = requests.post(
    url=f"http://{SERVER_HOST}/api/templates/{template_name}",
    headers={'Content-type': 'text/plain; charset=utf-8'},
    data=template_text.encode('utf-8'),
)
response.raise_for_status()


print(
    f"==> Uploading device data for {len(device_data)} device(s) from "
    f"'{device_data_file.name}'"
)
response = requests.post(
    url=f"http://{SERVER_HOST}/api/device_data",
    json=device_data,
)
response.raise_for_status()


print(f"""
Zero-Touch Provisioning uploads completed successfully.
You can access the interactive app APIs at:

    http://{SERVER_HOST}/api

You can request rendered device configurations using the following URL syntax:

    http://{SERVER_HOST}/config/<device-serial-number>

See the following example URLs:
""")
for device in device_data:
    print(f"    http://{SERVER_HOST}/config/{device.get('serial_number')}")
