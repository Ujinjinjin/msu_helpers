#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Status:
    OK: str = 'Ok'
    FAILED: str = 'Failed'


class Code:
    OK: int = 200
    FAILED: int = 400
    UNAUTHORIZED: int = 401
    FORBIDDEN: int = 403
    NOT_FOUND: int = 404
    INTERNAL_SERVER_ERROR: int = 500
