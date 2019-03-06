"""Templates API.

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
import json

from marshmallow import Schema, fields, post_load
import mongoengine
from responder import Request, Response

from ztp.mongo.models.template import Template
from ztp.web import api


logger = logging.getLogger(__name__)


@api.schema("Template")
class TemplateSchema(Schema):
    """API DeviceData data model."""
    name = fields.String()
    template = fields.String()
    sha256 = fields.String()
    updated = fields.DateTime()

    class Meta:
        ordered = True

    @post_load
    def make_template_object(self, data: dict) -> Template:
        """Deserialize template data to a Template object."""
        return Template(**data)


@api.route("/api/templates")
class TemplateCollectionResource(object):
    """API endpoint for collection-level template operations.

    ---
    get:
        summary: List Templates
        description: List all templates.
        tags:
            - Templates
        responses:
            200:
                description: OK
                content:
                    application/json:
                        schema:
                            type: array
                            items:
                                $ref: "#/components/schemas/Template"
    """

    @staticmethod
    def on_get(req: Request, resp: Response):
        """List all device data records."""
        template_objects = list(Template.objects())
        schema = TemplateSchema(many=True)
        data = list(schema.dump(template_objects)[0])
        resp.media = data


@api.route("/api/templates/{name}")
class TemplatesResource(object):
    """API endpoint for individual template operations.

    ---
    get:
        summary: Get Template Details
        description: Get template details, by name.
        tags:
            - Templates
        parameters:
        - in: path
          name: name
          description: Template name.
          schema:
            type: string
        responses:
            200:
                description: OK
                content:
                    application/json:
                        schema:
                            $ref: "#/components/schemas/Template"
                    text/plain:
                        schema:
                            type: string
            404:
                description: Not Found
                schema:
                    type: object
                    required:
                        - error
                    properties:
                        error:
                            type: string

    post:
        summary: Create or Update a Template
        description: >
            Create a new template or update an existing template, by name.
        tags:
            - Templates
        parameters:
        - in: path
          name: name
          description: Template name.
          schema:
            type: string
        requestBody:
            description: A Jinja2 formatted template file.
            content:
                application/octet-stream:
                    schema:
                        type: string
                        format: binary
                    application/json:
                        schema:
                            $ref: "#/components/schemas/Template"
        responses:
            200:
                description: OK
                content:
                    application/json:
                        schema:
                            $ref: "#/components/schemas/Template"
                    text/plain:
                        schema:
                            type: string
            400:
                description: Bad Request
                schema:
                    type: object
                    required:
                        - error
                    properties:
                        error:
                            type: string

    delete:
        summary: Delete Template
        description: Delete a template, by name.
        tags:
            - Templates
        parameters:
        - in: path
          name: name
          description: Template name.
          schema:
            type: string
        responses:
            204:
                description: No Content
            404:
                description: Not Found
                schema:
                    type: object
                    required:
                        - error
                    properties:
                        error:
                            type: string
            500:
                description: Internal Server Error
                schema:
                    type: object
                    required:
                        - error
                    properties:
                        error:
                            type: string
  """

    @staticmethod
    def on_get(req: Request, resp: Response, *, name: str):
        """Get template details, by name."""
        try:
            template_object = Template.objects.get(template_name=name)

        except mongoengine.DoesNotExist:
            resp.status_code = api.status_codes.HTTP_404

        except mongoengine.MultipleObjectsReturned as error:
            logger.error(error)
            resp.status_code = api.status_codes.HTTP_500
            resp.media = {"error": str(error)}

        else:
            if req.accepts("text/plain"):
                resp.content = template_object.template.encode("utf-8")
                resp.headers["Content-Type"] = "text/plain; encoding=utf-8"
            else:
                schema = TemplateSchema()
                resp.media = schema.dump(template_object)[0]

    @staticmethod
    async def on_post(req: Request, resp: Response, *, name: str):
        """Create a new template or update an existing template, by name."""
        try:
            # Parse the post data and extract the template text
            if req.headers["Content-Type"] == "application/json":
                data = await req.media()
                assert isinstance(data, dict) and data.get("template")
                template_text = data["template"]
            else:
                template_text = await req.text

            # Get the template from MongoDB, if it exists, otherwise create a
            # new template object.
            try:
                template_object = Template.objects.get(name=name)
            except mongoengine.DoesNotExist:
                template_object = Template(name=name)

            template_object.template = template_text
            template_object.save()

        except (json.JSONDecodeError, mongoengine.ValidationError) as error:
            logger.error(error)
            resp.status_code = api.status_codes.HTTP_400
            resp.media = {"error": str(error)}

        except AssertionError as error:
            logger.error(error)
            resp.status_code = api.status_codes.HTTP_400
            resp.media = {
                "error": "Missing Template Attribute: The posted data should "
                         "be a object (dictionary) containing a `template` "
                         "key."
            }

        except mongoengine.MultipleObjectsReturned as error:
            logger.error(error)
            resp.status_code = api.status_codes.HTTP_500
            resp.media = {"error": str(error)}

        else:
            if req.headers["Accept"] == "text/plain":
                resp.media = template_object.template
            else:
                schema = TemplateSchema()
                resp.media = schema.dump(template_object)[0]

    @staticmethod
    def on_delete(req: Request, resp: Response, *, name: str):
        """Delete a device data record, by device serial number."""
        try:
            template_object = Template.objects.get(name=name)

        except mongoengine.DoesNotExist:
            resp.status_code = api.status_codes.HTTP_404

        except mongoengine.MultipleObjectsReturned as error:
            logger.error(error)
            resp.status_code = api.status_codes.HTTP_500
            resp.media = {"error": str(error)}

        else:
            template_object.delete()
            resp.status_code = api.status_codes.HTTP_204
