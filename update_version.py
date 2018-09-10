#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

if __name__ == '__main__':

    with open('version.json', 'r', encoding='utf-8') as f:
        version_dict = json.load(f)

    version_dict['build'] += 1

    with open('version.json', 'w', encoding='utf-8') as f:
        json.dump(version_dict, f)
