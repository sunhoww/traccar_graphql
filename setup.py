import re
import ast
from setuptools import find_packages, setup


with open("traccar_graphql/__init__.py", "rb") as f:
    version = ast.literal_eval(
        re.compile(r"VERSION\s+=\s+(.*)").search(f.read().decode("utf-8")).group(1)
    )

setup(
    name="traccar_graphql",
    version=version,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "flask",
        "graphene",
        "flask_graphql",
        "requests",
        "flask-jwt-extended",
        "toolz",
    ],
)
