#include <iostream>
#include <pybind11/pybind11.h>

#include "google/protobuf/message.h"
#include "pybind11_protobuf/native_proto_caster.h"

#include "my_package/proto/example.pb.h"

namespace py = ::pybind11;

// In real use, these 2 functions would probably be defined in a python-agnostic library.
MyMessage ReturnMyMessage() { 
  MyMessage msg;
  msg.set_my_string("Hello World");
  return msg;
 }

void TakeMyMessage(const MyMessage& in) {
    std::cout << "Took Message" << std::endl;
}

void MutateMessage(MyMessage* in_out) {
  in_out->set_my_string("I changed the value");
}

PYBIND11_MODULE(my_extension, m) {
  pybind11_protobuf::ImportNativeProtoCasters();
  m.def("return_my_message", &ReturnMyMessage);
  m.def("take_my_message", &TakeMyMessage, pybind11::arg("in"));
  m.def("mutate_message", [](MyMessage in) {
    MutateMessage(&in);
    return in;
  },  pybind11::arg("in")); }