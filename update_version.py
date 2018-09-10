#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

if __name__ == '__main__':
    version = sys.argv[1]
    setup = (
       "#!/usr/bin/env python\n"
       "# -*- coding: utf-8 -*-\n"
       "\n"
       "from setuptools import setup, find_packages\n"
       "\n"
       "with open('README.md', 'r') as fh:\n"
       "    long_description = fh.read()\n"
       "    setup(\n"
       "        name='msu_helpers',\n"
       "        packages=find_packages(),\n"
       "        description='Package created for the university project to store common "
       "applications logic in one place. I am pretty sure that you do not need it',\n"
       "        long_description=long_description,\n"
       "        long_description_content_type='text/markdown',\n"
       f"        version='{version}',\n"
       "        url='https://github.com/Ujinjinjin/msu_helpers',\n"
       "        author='ujinjinjin',\n"
       "        author_email='gallkam@outlook.com ',\n"
       "        keywords=['pip','msu_sqluniversity'],\n"
       "    )\n"
    )

    with open('setup.py', 'w') as fw:
        fw.write(setup)
