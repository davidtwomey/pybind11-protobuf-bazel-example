from typing import List


try:
    import my_package.python.my_extension as m
except ImportError as e:
    print(f'Extension Import error -> {e}')
    import _my_extension as m

try:
    from my_package.proto.example_pb2 import MyMessage
except ImportError as e:
    print(f'Protobuf Import error -> {e}')
    from my_extension.example_pb2 import MyMessage

def my_function():
    print('Hello World')

def main():
  """DO something"""
  
  print('Creating Protobuf Message in Python...')
  msg_py = MyMessage(my_int = 3, my_string = "hello")
  print(msg_py)
  print('Success.')


  print('Creating Protobuf Message in C++...')
  msg_cpp = m.return_my_message()
  print(msg_cpp)
  print('Success')
  
  print('Changing Protobuf message (C++ generated) in Python')
  msg_cpp.my_string = "I changed this value!"
  msg_cpp.my_int = 3
  print(msg_cpp)
  print('Success')


  print('Give Protobuf (C++ generated) to C++')
  # T: Take c++ generated msg
  m.take_my_message(msg_cpp)
  print('Success')

  print('Give Protobuf (Py generated) to C++')
  # T: Take py generated msg
  m.take_my_message(msg_py)
  print('Success')

  # T: Mutate c++ generated msg
#   print('Mutating Protobuf message (C++ generated)..')
#   msg_cpp = m.mutate_message(msg_cpp)
#   print(msg_cpp)
#   print('Sucess.')

#   print('Mutating Protobuf Message (Py generated)')
#   msg_py_updated = m.mutate_message(msg_py)
#   print(msg_py_updated)
#   print('Success.')


if __name__ == "__main__":
  main()