cmake_minimum_required(VERSION 3.12)
project(cpp-deep-client)

set( CMAKE_CXX_STANDARD 20 )
set( CMAKE_CXX_STANDARD_REQUIRED ON )

INCLUDE_DIRECTORIES(
        "${CMAKE_SOURCE_DIR}/python"
)

# Find Boost package
find_package(Boost REQUIRED COMPONENTS python)

# Add the Boost include directory
include_directories(${Boost_INCLUDE_DIRS})

find_package(PythonLibs REQUIRED)

message("Python libraries: ${PYTHON_LIBRARIES}")

add_library(cpp-deep-client SHARED
        nlohmann/json.hpp
        PyCppBridge.h
        httplib.h
        DeepClientCppWrapper.h
        PyCppBridge.cpp
        DeepClientCppWrapper.cpp
)

# Link against Boost libraries
TARGET_LINK_LIBRARIES(cpp-deep-client ${Boost_LIBRARIES} ${PYTHON_LIBRARIES})

target_include_directories(cpp-deep-client PRIVATE ${CMAKE_SOURCE_DIR}/nlohmann)

set_target_properties(cpp-deep-client
  PROPERTIES
  ARCHIVE_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}"
  LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}"
  RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}"
)

add_executable(test_deep_client
        tests/test_deep_client.cpp
)

target_link_libraries(test_deep_client cpp-deep-client)

add_test(NAME test_deep_client COMMAND tests)