"""Common app utility functions.

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

from urllib.parse import urljoin, urlparse


# URL Utilities
def is_url(string: str) -> bool:
    """Check a string to see if it contains a URL."""
    parsed_url = urlparse(string)
    return parsed_url.scheme and parsed_url.netloc


def create_abs_url(base_url: str, relative_path: str) -> str:
    """Create an absolute URL from a base + a relative path."""
    return urljoin(base_url, relative_path)
