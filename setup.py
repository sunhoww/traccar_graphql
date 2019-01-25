from setuptools import find_packages, setup

__version__ = "0.0.1"

setup(
    name="traccar_graphql",
    version=__version__,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "flask",
        "graphene",
        "flask_graphql",
        "requests",
        "flask-jwt-extended",
    ],
)
