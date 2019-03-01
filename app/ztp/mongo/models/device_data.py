"""DeviceData MongoDB data model.

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

from datetime import datetime

from mongoengine import (
    DateTimeField, DictField, DynamicDocument, StringField, signals,
)

from ztp.mongo.models.template import Template


class DeviceData(DynamicDocument):
    """Device data document."""
    serial_number = StringField(required=True, unique=True)
    template_name = StringField(required=True)
    config_data = DictField()
    updated = DateTimeField()

    meta = {
        "collection": "device_data",
        "indexes": [
            "serial_number",
        ]
    }

    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        """Update the device data attributes before saving the document."""
        assert isinstance(document, Template)
        document.updated = datetime.utcnow()


signals.pre_save.connect(
    DeviceData.pre_save,
    sender=DeviceData
)
