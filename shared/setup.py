from setuptools import setup, find_packages

setup(
    name="shared",
    version="0.1.0",
    packages=find_packages(include=["grpc_clients*", "db*"]),
    include_package_data=True,
    install_requires=["grpcio", "protobuf"]
)
