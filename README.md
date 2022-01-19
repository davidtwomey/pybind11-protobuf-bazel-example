
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

It is possible to run this **outside** of a binary (i.e. from a separate python process) without any changes

Note that there is no safe way to enable passing native protos between C++ extensions and python even using fast_cpp_proto option **unless the build is hermetic**; 
that is, all the proto-using extensions, including python protobufs, are built using the same config settings.

Therefore, the current behaviour (as of 2021-Jan-19) is to disabled it in the latest cl, and we fallback to the python implementation.
Which means that this should work but **incur copies at the boundaries**.
More specifically, `pybind11_protobuf` will call the python methods to do the serialization, not that it would fallback to the pure python proto implementation.

In other words, raw C++ protos just won't be copied/referenced across the boundary; they'll be serialized by whatever python implementation is loaded--either native python or fast cpp protos--and deserialized into a C++ proto.

However, avoiding copies/serialization/deserialization using the proto API is still possible  with a config setting. See the comments here:

https://github.com/pybind/pybind11_protobuf/blob/main/pybind11_protobuf/proto_cast_util.cc#L226
https://github.com/pybind/pybind11_protobuf/blob/main/pybind11_protobuf/BUILD#L63







### Working Example

```shell
# Install Protobuf (Force Python implementation)
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





















