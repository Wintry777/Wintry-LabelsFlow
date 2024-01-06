# setup.py
from setuptools import setup, find_packages
import os

package_name = 'Wintry_LabelsFlow'

here = os.path.abspath(os.path.dirname(__file__))
about = {}
with open(os.path.join(here, package_name, 'version.py'), 'r', encoding='utf-8') as f:
    exec(f.read(), about)

setup(
    name=package_name,
    version=about['__version__'],
    author=about['__author__'],
    author_email=about['__author_email__'],
    description=about['__description__'],
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url=about['__url__'],
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        # 依赖列表
    ],
    # 其他选项
)
