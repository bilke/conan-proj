project(MyProj C)
cmake_minimum_required(VERSION 2.8.12)

include(conanbuildinfo.cmake)
conan_basic_setup()

add_executable(test test.c)

target_link_libraries(test ${CONAN_LIBS})
