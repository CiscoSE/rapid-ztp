"""Device Data API.

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

from ztp.mongo.models.device_data import DeviceData
from ztp.web import api


logger = logging.getLogger(__name__)


@api.schema("DeviceData")
class DeviceDataSchema(Schema):
    """API DeviceData data model."""
    serial_number = fields.String()
    template_name = fields.String()
    config_data = fields.Dict()
    updated = fields.DateTime()

    class Meta:
        ordered = True

    @post_load
    def make_device_data_object(self, data: dict) -> DeviceData:
        """Deserialize device-data to a DeviceData object."""
        return DeviceData(**data)


@api.route("/api/device_data")
class DeviceDataCollectionResource(object):
    """API endpoint for collection-level device-data operations.

    ---
    get:
        summary: List Device Data Records
        description: List all device data records.
        tags:
            - Device Data
        responses:
            200:
                description: OK
                content:
                    application/json:
                        schema:
                            type: array
                            items:
                                $ref: "#/components/schemas/DeviceData"

    post:
        summary: Upload and Replace all Device Data Records
        description: >
            Clear all existing device data records and replace with the
            uploaded device data.
        tags:
            - Device Data
        requestBody:
            description: List of device-data records.
            content:
                application/json:
                    schema:
                        type: array
                        items:
                            $ref: "#/components/schemas/DeviceData"
        responses:
            200:
                description: OK
                content:
                    application/json:
                        schema:
                            type: array
                            items:
                                $ref: "#/components/schemas/DeviceData"
            400:
                description: Bad Request
                schema:
                    type: object
                    required:
                        - error
                    properties:
                        error:
                            type: string
    """

    @staticmethod
    def on_get(req: Request, resp: Response):
        """List all device data records."""
        device_data_objects = list(DeviceData.objects())
        schema = DeviceDataSchema(many=True)
        data = list(schema.dump(device_data_objects)[0])
        resp.media = data

    @staticmethod
    async def on_post(req: Request, resp: Response):
        """Replace device data collection."""
        try:
            data = await req.media()
            schema = DeviceDataSchema(many=True)
            device_data_objects = schema.load(data)[0]
            for device_data_object in device_data_objects:
                device_data_object.validate()

        except (json.JSONDecodeError, mongoengine.ValidationError) as error:
            logger.error(error)
            resp.status_code = api.status_codes.HTTP_400
            resp.media = {"error": str(error)}

        else:
            DeviceData.drop_collection()
            for device_data_object in device_data_objects:
                device_data_object.save()
            resp.media = schema.dump(device_data_objects)[0]


@api.route("/api/device_data/{serial_number}")
class DeviceDataResource(object):
    """API endpoint for device-level data operations.

    ---
    get:
        summary: Device Data
        description: Get device data.
        tags:
            - Device Data
        parameters:
        - in: path
          name: serial_number
          description: Device serial number.
          schema:
            type: string
        responses:
            200:
                description: OK
                content:
                    application/json:
                        schema:
                            $ref: "#/components/schemas/DeviceData"
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

    post:
        summary: New Device Data
        description: Create a new device data record.
        tags:
            - Device Data
        parameters:
        - in: path
          name: serial_number
          description: Device serial number.
          schema:
            type: string
        requestBody:
            description: Device data record.
            content:
                application/json:
                    schema:
                        $ref: "#/components/schemas/DeviceData"
        responses:
            200:
                description: OK
                content:
                    application/json:
                        schema:
                            $ref: "#/components/schemas/DeviceData"
            500:
                description: Internal Server Error
                schema:
                    type: object
                    required:
                        - error
                    properties:
                        error:
                            type: string
    put:
        summary: Update Device Data
        description: Update a device data record.
        tags:
            - Device Data
        parameters:
        - in: path
          name: serial_number
          description: Device serial number.
          schema:
            type: string
        requestBody:
            description: Device data record.
            content:
                application/json:
                    schema:
                        $ref: "#/components/schemas/DeviceData"
        responses:
            200:
                description: OK
                content:
                    application/json:
                        schema:
                            $ref: "#/components/schemas/DeviceData"
            400:
                description: Bad Request
                schema:
                    type: object
                    required:
                        - error
                    properties:
                        error:
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
    def on_get(req: Request, resp: Response, *, serial_number: str):
        """Get device data."""
        try:
            device_data_object = DeviceData.objects.get(
                serial_number=serial_number
            )

        except mongoengine.DoesNotExist:
            resp.status_code = api.status_codes.HTTP_404

        except mongoengine.MultipleObjectsReturned as error:
            logger.error(error)
            resp.status_code = api.status_codes.HTTP_500
            resp.media = {"error": str(error)}

        else:
            schema = DeviceDataSchema()
            resp.media = schema.dump(device_data_object)[0]

    @staticmethod
    async def on_post(req: Request, resp: Response, *, serial_number: str):
        """Create a new device data record."""
        try:
            data = await req.media()
            schema = DeviceDataSchema()
            device_data_object = schema.load(data)[0]
            device_data_object.serial_number = serial_number
            device_data_object.save()

        except (json.JSONDecodeError, mongoengine.ValidationError) as error:
            logger.error(error)
            resp.status_code = api.status_codes.HTTP_400
            resp.media = {"error": str(error)}

        except mongoengine.NotUniqueError as error:
            logger.error(error)
            resp.status_code = api.status_codes.HTTP_400
            resp.media = {
                "error": f"Device data has already been uploaded for "
                         f"{serial_number}. Please use the PUT HTTP method to "
                         f"update this record."
            }

        else:
            resp.media = schema.dump(device_data_object)

    @staticmethod
    async def on_put(req: Request, resp: Response, *, serial_number: str):
        """Update a device data record."""
        try:
            data = await req.media()
            assert isinstance(data, dict)

            device_data_object = DeviceData.objects.get(
                serial_number=serial_number
            )
            device_data_object.template_name = data.get("template_name")
            device_data_object.config_data = data.get("config_data")
            device_data_object.save()
            device_data_object.reload()

        except (json.JSONDecodeError, mongoengine.ValidationError) as error:
            logger.error(error)
            resp.status_code = api.status_codes.HTTP_400
            resp.media = {"error": str(error)}

        except mongoengine.DoesNotExist:
            resp.status_code = api.status_codes.HTTP_404

        except mongoengine.MultipleObjectsReturned as error:
            logger.error(error)
            resp.status_code = api.status_codes.HTTP_500
            resp.media = {"error": str(error)}

        else:
            schema = DeviceDataSchema()
            resp.media = schema.dump(device_data_object)[0]
