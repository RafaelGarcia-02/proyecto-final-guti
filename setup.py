from setuptools import setup

# List of dependencies installed from pip
requires = [
    'pyramid',
    'sqlalchemy',
    'pyramid-jinja2',
]

setup(
    name='myapp',
    install_requires=requires,
    entry_points={
        'paste.app_factory': [
            'main = myapp:main',
        ],
    },
)