project(MyProj C)
cmake_minimum_required(VERSION 2.8.12)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

include_directories(${CONAN_INCLUDE_DIRS_PROJ})
add_executable(test test.c)

target_link_libraries(test ${CONAN_LIBS})
