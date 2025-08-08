from setuptools import setup, find_packages

setup(
    name='planckage',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'typer',      # For CLI
        'tomli; python_version<"3.11"',  # TOML parsing for older Python
		'platformdirs',
    ],
    entry_points={
        'console_scripts': [
            'planckage=planckage.cli:app',
        ],
    },
    author='Colin Kinz-Thompson',
    description='A tool for managing scientific data analysis',
    license='MIT',
)