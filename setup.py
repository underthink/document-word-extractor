from setuptools import setup

setup(
    name='document_parser',
    version='1.0',
    author='Rob Newman',
    author_email='rob@unnecessary.net',
    packages=['document_parser', 'document_parser.outputs'],
    install_requires=['stop-words', 'texttable'],
    entry_points={
        'console_scripts': ['document_parser=document_parser.cli:run_cli_program'],
    },
)