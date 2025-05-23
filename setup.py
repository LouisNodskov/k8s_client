from setuptools import setup, find_packages

setup(
    name="k8s-client",
    version="0.0",
    packages=find_packages(),
    install_requires=["kubernetes>=32.0.1"],
    entry_points={
        "console_scripts": [
            "k8s-client = k8s_client.main:main"
        ],
    }
)