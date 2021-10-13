
# Pybind11 Protobuf Bazel Example

Simple example of how to define a protobuf schema and work with it in python & c++ 
interchangably using [pybind11_protobuf](https://github.com/pybind/pybind11_protobuf)



## Usage

To run a very small example try:

```shell
bazel clean --expunge
bazel run my_package:example
```


## Project Structure

```
├── external
│   └── com_google_protobuf_build.patch
├── my_package
│   ├── BUILD.bazel
│   ├── example.py            # Example python code interacting with protobuf / c++
│   ├── __init__.py
│   ├── proto
│   │   ├── BUILD.bazel
│   │   └── example.proto     # Protobuf schema definition
│   └── pybind11
│       ├── BUILD.bazel
│       └── my_extension.cc   # Pybind11 extension module
├── README.md
├── setup.py # (WIP)
└── WORKSPACE.bazel
```











