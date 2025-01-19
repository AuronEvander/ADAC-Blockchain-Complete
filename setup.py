from setuptools import setup, find_namespace_packages

setup(
    name="adac-blockchain",
    version="0.1.0",
    package_dir={'': 'src'},
    packages=find_namespace_packages(include=['src*']),
    install_requires=[
        'fastapi',
        'uvicorn',
        'sqlalchemy',
        'alembic',
        'psycopg2-binary',
    ],
    python_requires='>=3.8',
)