
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


## Notes

It is possible to run this **outside** of a binary (i.e. from a separate python process).
However, this currently only seems to work if the corresponding python library has the `python` implementation of protobuf.

### Working Example

```shell
# Install Protobuf (Force Python implementation)
export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
pip install protobuf==3.19.1
bazel build my_package:example
```

You can now import the build extension and protobuf files in a separate python process

```python
# Check protobuf implementation
from google.protobuf.internal import api_implementation
api_implementation.Type() # >>> Should say 'python'

# Import proto + pybind11 extension
import sys
sys.path.append('./bazel-bin/my_package')
from proto import example_pb2
from pybind11 import my_extension as m

msg = m.return_my_message()
assert isinstance(msg, example_pb2.MyMessage) # >>> True

m.take_my_message(msg)

# ...
```





















