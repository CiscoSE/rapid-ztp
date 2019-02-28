"""Rapid ZTP MongoDB database interface and models.

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
from hashlib import sha256

import jinja2
import pymongo.database
from mongoengine import (
    DENY, DateTimeField, DictField, DynamicDocument, ReferenceField,
    StringField, connect, signals,
)

from ztp.config import MONGO_DATABASE, MONGO_URL


# Initialize pymongo and mongoengine
client = connect(MONGO_DATABASE, host=MONGO_URL)
assert isinstance(client, pymongo.MongoClient)

# Initialize database connection object
db = client[MONGO_DATABASE]
assert isinstance(db, pymongo.database.Database)


# MongoDB Data Models

class ConfigurationTemplate(DynamicDocument):
    """Configuration Template Document."""
    name = StringField(required=True, unique=True)
    template = StringField(required=True)
    sha256 = StringField()
    updated = DateTimeField()

    meta = {
        "collection": "configuration_templates",
        "indexes": [
            "name",
            "sha256",
        ]
    }

    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        """Update the template attributes before saving the document."""
        assert isinstance(document, ConfigurationTemplate)
        document.updated = datetime.utcnow()
        document.sha256 = sha256(document.template.encode("utf-8")).hexdigest()


signals.pre_save.connect(
    ConfigurationTemplate.pre_save,
    sender=ConfigurationTemplate
)


class ConfigurationData(DynamicDocument):
    """Configuration Data Document."""
    serial_number = StringField(required=True, unique=True)
    configuration_template = ReferenceField(
        "ConfigurationTemplate",
        reverse_delete_rule=DENY,
    )
    configuration_data = DictField()
    updated = DateTimeField()

    meta = {
        "collection": "configuration_data",
        "indexes": [
            "serial_number",
        ]
    }

    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        """Update the config data attributes before saving the document."""
        assert isinstance(document, ConfigurationTemplate)
        document.updated = datetime.utcnow()

    def render(self) -> str:
        """Render the configuration template with the configuration data."""
        template = jinja2.Template(self.configuration_template.template)
        return template.render(config_data=self.configuration_data)


signals.pre_save.connect(
    ConfigurationTemplate.pre_save,
    sender=ConfigurationTemplate
)
