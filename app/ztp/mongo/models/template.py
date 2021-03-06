"""Template MongoDB data model.

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

from mongoengine import (
    DateTimeField, DynamicDocument, StringField, signals,
)


class Template(DynamicDocument):
    """Template document."""
    name = StringField(required=True, unique=True)
    template = StringField(required=True)
    sha256 = StringField()
    updated = DateTimeField()

    meta = {
        "collection": "templates",
        "indexes": [
            "name",
            "sha256",
        ]
    }

    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        """Update the template attributes before saving the document."""
        assert isinstance(document, Template)
        document.updated = datetime.utcnow()
        document.sha256 = sha256(document.template.encode("utf-8")).hexdigest()


signals.pre_save.connect(
    Template.pre_save,
    sender=Template
)
