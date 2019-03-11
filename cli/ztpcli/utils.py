"""Package helper functions, classes, and utilities.

Copyright (c) 2019 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.0 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""


def check_type(o, acceptable_types, may_be_none=False):
    """Object is an instance of one of the acceptable types or None.

    Args:
        o: The object to be inspected.
        acceptable_types: A type or tuple of acceptable types.
        may_be_none(bool): Whether or not the object may be None.

    Raises:
        TypeError: If the object is None and may_be_none=False, or if the
            object is not an instance of one of the acceptable types.

    """
    if not isinstance(acceptable_types, tuple):
        acceptable_types = (acceptable_types,)

    if may_be_none and o is None:
        # Object is None, and that is OK!
        pass
    elif isinstance(o, acceptable_types):
        # Object is an instance of an acceptable type.
        pass
    else:
        # Object is something else.
        error_message = (
            "We were expecting to receive an instance of one of the following "
            "types: {types}{none}; but instead we received {o} which is a "
            "{o_type}.".format(
                types=", ".join([repr(t.__name__) for t in acceptable_types]),
                none="or 'None'" if may_be_none else "",
                o=o,
                o_type=repr(type(o).__name__)
            )
        )
        raise TypeError(error_message)
