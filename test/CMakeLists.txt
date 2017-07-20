project(MyProj C)
cmake_minimum_required(VERSION 2.8.12)

find_package (Threads)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

include_directories(${CONAN_INCLUDE_DIRS_PROJ})
add_executable(test test.c)

target_link_libraries(test ${CONAN_LIBS})
if(UNIX AND NOT APPLE)
    TARGET_LINK_LIBRARIES(test m)
endif()
if(CMAKE_THREAD_LIBS_INIT)
  target_link_libraries(test "${CMAKE_THREAD_LIBS_INIT}")
endif()
