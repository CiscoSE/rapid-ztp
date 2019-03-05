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

import jinja2
import mongoengine
from responder import Request, Response

from ztp.mongo.models.device_data import DeviceData
from ztp.template_engine import get_template
from ztp.web import api


logger = logging.getLogger(__name__)


@api.route("/config/{serial_number}")
class ConfigurationTemplateEngineResource(object):
    """API endpoint for configuration template operations.

    ---
    get:
        summary: Get Rendered Device Configuration
        description: >
            Get rendered device configuration, by device serial number.
        tags:
            - Device Configurations
        parameters:
        - in: path
          name: serial_number
          description: Device serial number.
          schema:
            type: string
        responses:
            200:
                description: OK
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
        """Get rendered device configuration, by device serial number."""
        try:
            device_data_object = DeviceData.objects.get(
                serial_number=serial_number
            )
            template = get_template(device_data_object.template_name)

        except mongoengine.DoesNotExist:
            resp.status_code = api.status_codes.HTTP_404
            resp.media = {
                "error": f"The device data for serial number "
                         f"`{serial_number}` could not be found.",
            }

        except jinja2.TemplateNotFound as error:
            logger.error(error)
            resp.status_code = api.status_codes.HTTP_404
            resp.media = {
                "error": f"The template `{device_data_object.template_name}` "
                         f"specified in the device data record could not be "
                         f"found.",
            }

        except mongoengine.MultipleObjectsReturned as error:
            logger.error(error)
            resp.status_code = api.status_codes.HTTP_500
            resp.media = {"error": str(error)}

        else:
            resp.media = template.render(
                config_data=device_data_object.config_data
            )
