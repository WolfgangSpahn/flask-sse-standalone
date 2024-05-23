from setuptools import setup, find_packages

# Read contents of README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='flask_sse_standalone',
    version='0.1.0',
    author='Wolfgang Spahn',
    author_email='wolfgang.spahn@gmail.com',
    description='Server-Sent Events (SSE) for Flask applications',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/WolfgangSpahn/flask-sse-standalone',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'flask',
    ],
    extras_require={
        'dev': [
            'pytest',
            'flake8',
        ],
    },
)
