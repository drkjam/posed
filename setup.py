from setuptools import setup, find_packages
import pathlib

HERE = pathlib.Path(__file__).parent.resolve()

setup(
    name='posed',
    version='0.0.1',
    description='An experimental compiler and virtual machine runtime',
    long_description=(HERE / 'README.md').read_text(encoding='utf-8'),
    long_description_content_type='text/markdown',
    url='https://github.com/drkjam/posed',
    author='David P. D. Moss',
    author_email='drkjam@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
    ],
    packages=find_packages(),
    python_requires='>=3.7, <4',
    install_requires=(HERE / 'requirements.txt').read_text(encoding='utf-8').strip().split('\n'),
    #   $ pip install posed[dev]
    extras_require={
        'dev': ['check-manifest', 'coverage', 'pytest', 'pytest-cov'],
    },
)
