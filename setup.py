from setuptools import setup
from traccar_graphql import __version__

setup(
    name='traccar_graphql',
    version=__version__,
    packages=['traccar_graphql'],
    include_package_data=True,
    install_requires=[
        'flask',
        'graphene',
        'flask_graphql',
        'requests',
    ],
)
