#!/usr/bin/env python
from werkzeug.routing import BaseConverter


class OnlyLettersConverter(BaseConverter):
    """A Flask converter to allow only letters."""

    regex = r"[a-zA-Z]+"
