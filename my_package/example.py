
from my_package.proto.example_pb2 import MyMessage
from my_package.pybind11 import my_extension as m
# import my_package.my_extension as m

def main():
  """DO something"""
  
  msg_py = MyMessage(my_int = 3, my_string = "hello")
  print(msg_py)
  
  print(m.__dir__())
  msg_cpp = m.return_my_message()
  print(msg_cpp)
  
  msg_cpp.my_int = 3
  print(msg_cpp)


  # T: Take c++ generated msg
  m.take_my_message(msg_cpp)
  # T: Take py generated msg
  m.take_my_message(msg_py)

  # T: Mutate c++ generated msg
  msg_cpp = m.mutate_message(msg_cpp)
  print(msg_cpp)

  msg_py_updated = m.mutate_message(msg_py)
  print(msg_py_updated)
  


if __name__ == "__main__":
  main()
