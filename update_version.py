#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

if __name__ == '__main__':

    version: str = sys.argv[1]
    version = version.split('.')
    build = int(version[1])

    params: dict = {
        'filename': 'setup',
        'package_name': 'msu_helpers',
        'build_num': build,
        'url': 'https://github.com/Ujinjinjin/msu_helpers'
    }

    if len(sys.argv) > 2 and sys.argv[2] == 'dev':
        params['filename'] += '_dev'
        params['package_name'] += '_dev'
        params['url'] += '/tree/dev'
        version = f'0.4.{build}'
    elif len(sys.argv) == 2:
        version = f'1.0.{build}'

    setup = (
        "#!/usr/bin/env python\n"
        "# -*- coding: utf-8 -*-\n"
        "\n"
        "from setuptools import setup, find_packages\n"
        "\n"
        "with open('README.md', 'r') as fh:\n"
        "    long_description = fh.read()\n\n"
        "setup(\n"
        f"    name='{params['package_name']}',\n"
        "    packages=find_packages(),\n"
        "    description='Package created for the university project to store common application logic in one place.'\n"
        "                'I am pretty sure that you do not need it',\n"
        "    long_description=long_description,\n"
        "    long_description_content_type='text/markdown',\n"
        f"    version='{version}',\n"
        f"    url='{params['url']}',\n"
        "    author='ujinjinjin',\n"
        "    author_email='gallkam@outlook.com ',\n"
        "    keywords=['pip','msu_sqluniversity'],\n"
        ")\n"
    )

    with open(f'{params["filename"]}.py', 'w') as fw:
        fw.write(setup)
