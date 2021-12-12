#include <iostream>
#include <pybind11/pybind11.h>

#include "google/protobuf/message.h"
#include "pybind11_protobuf/native_proto_caster.h"

#include "my_package/proto/example.pb.h"

namespace py = ::pybind11;

MyMessage ReturnMyMessage()
{
  std::cout << "Creating message in C++" << std::endl;
  MyMessage msg;
  msg.set_my_string("Hello World");
  return msg;
}

bool TakeMyMessage(const ::google::protobuf::Message* message)
{
  std::cout << "Took Message" << std::endl;
  return true;
}

// void MutateMessage(MyMessage *in_out)
// {
//   in_out->set_my_string("I changed the value");
// }

void bind(pybind11::module &m)
{
  pybind11_protobuf::ImportNativeProtoCasters();
  m.def("return_my_message", &ReturnMyMessage);
  // m.def("take_my_message", &TakeMyMessage, pybind11::arg("in"));

  m.def(
      "take_my_message",
      [](MyMessage message)
      {
        return TakeMyMessage(&message);
      },
      py::arg("message"));


//   m.def(
//       "mutate_message", [](MyMessage in)
//       {
//         MutateMessage(&in);
//         return in;
//       },
//       pybind11::arg("in"));
}

PYBIND11_MODULE(_my_extension, m) { bind(m); }
