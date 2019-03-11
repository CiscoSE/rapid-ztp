"""Rapid ZTP App Client.

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

from ztpcli.utils import check_type
from typing import List
from pathlib import Path

BASE_URL = "http://{host}:port/"


class RapidZtpClient(object):
    """Rapid ZTP App Client."""

    def __init__(self, ztp_server: str, port: int = 80):
        """Initialize a new Rapid ZTP client object.

        Args:
            ztp_server: Hostname or IP address of the Rapid ZTP server.
            port: TCP port number of the Rapid ZTP web server.
        """
        check_type(ztp_server, str)
        check_type(port, int)

        self._ztp_server = ztp_server.strip().lower()
        self._port = port
        self.base_url = BASE_URL.format(
            host=self._ztp_server,
            port=self._port,
        )
        self._headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        self.session = requests.session()
        self.session.headers.update(self._headers)

    def upload_template_text(self, template_name: str, text: str) -> dict:
        """Create or update a template, by name, on the ZTP server.

        Args:
            template_name: The name of the template to be created or updated
                on the ZTP server.
            text: The template text.

        Returns:
            A dictionary with the created template object details.
        """
        check_type(template_name, str)
        check_type(text, str)

        template_name = template_name.strip()
        data = text.encode("utf-8")

        response = self.session.post(
            url=self.base_url + f"api/templates/{template_name}",
            data=data,
        )
        response.raise_for_status()

        return response.json()

    def upload_template(self, template_path: Path) -> dict:
        """Upload a template to the ZTP server.

        Args:
            template_path: The template path on the local file system.

        Returns:
            A dictionary with the created template object details.
        """
        check_type(template_path, Path)
        assert template_path.exists()
        assert template_path.is_file()
        template_name = template_path.stem
        with open(template_path, encoding="utf-8") as template_file:
            template_text = template_file.read()
        return self.upload_template_text(template_name, template_text)

    def upload_templates(self, template_paths: List[Path]) -> List[dict]:
        """Upload multiple templates to the ZTP server.

        Args:
            template_paths: The template paths on the local file system.

        Returns:
            A list of dictionaries containing the created template objects.
        """
        check_type(template_paths, list)
        return [
            self.upload_template(path)
            for path in template_paths
        ]

    def upload_device_data(self, serial_number: str, template_name: str,
                           config_data: dict) -> dict:
        """Upload a device-data record.

        Args:
            serial_number: The device's serial number.
            template_name: The name of the configuration template to be
                applied to the device.
            config_data: The data to be merged into the configuration template
                to generate the device's configuration.

        Returns:
            A dictionary containing the created device-data record.
        """
        check_type(serial_number, str)
        check_type(template_name, str)
        check_type(config_data, dict)

        serial_number = serial_number.strip().upper()
        template_name = template_name.strip()
        json_data = {
            "serial_number": serial_number,
            "template_name": template_name,
            "config_data": config_data,
        }

        response = self.session.post(
            url=self.base_url + f"api/device_data/{serial_number}",
            json=json_data,
        )
        response.raise_for_status()

        return response.json()

    def upload_device_data_records(self, data: List[dict]) -> List[dict]:
        """Upload device-data records.

        Args:
            data: A list of device-data records (dict). Each record should
                include the following key-value pairs: serial_number: str,
                template_name: str, and config_data: dict.

        Returns:
            A list of dictionaries containing the created data records.
        """
        check_type(data, list)

        created_records = []
        for record in data:
            serial_number = record.get("serial_number")
            template_name = record.get("template_name")
            config_data = record.get("config_data")
            assert serial_number and template_name and config_data

            created_record = self.upload_device_data(
                serial_number=serial_number,
                template_name=template_name,
                config_data=config_data,
            )

            created_records.append(created_record)

        return created_records

    def get_device_configuration(self, serial_number: str) -> str:
        """Get the rendered configuration for a device, by Serial Number.

        Args:
            serial_number: The device's serial number.

        Returns:
              A string containing the device's rendered configuration.
        """
        check_type(serial_number, str)
        serial_number = serial_number.strip().upper()

        response = self.session.get(
            url=self.base_url + f"config/{serial_number}"
        )
        response.raise_for_status()

        return response.text
