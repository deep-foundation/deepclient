cmake_minimum_required(VERSION 3.12)
project(deep_client_php_extension)

set( CMAKE_CXX_STANDARD 11 )
set( CMAKE_CXX_STANDARD_REQUIRED ON )

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fPIC")

INCLUDE_DIRECTORIES(
  "${CMAKE_SOURCE_DIR}/php_headers"
  "${CMAKE_SOURCE_DIR}/ext_php_headers"
  "${CMAKE_SOURCE_DIR}/TSRM"
  "${CMAKE_SOURCE_DIR}/zend_headers"
  "${CMAKE_SOURCE_DIR}/python"
)

SET(PHPCPP_COMMON_SOURCES
  common/modifiers.cpp
  common/streambuf.cpp
)

SET(PHPCPP_COMMON_HEADERS
  common/extensionbase.h
  common/includes.h
  common/streambuf.h
)

ADD_LIBRARY(phpcpp-common STATIC
  ${PHPCPP_COMMON_HEADERS}
  ${PHPCPP_COMMON_SOURCES}
)

set_target_properties(phpcpp-common
  PROPERTIES
  ARCHIVE_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}"
  LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}"
  RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}"
)

SET(PHPCPP_ZEND_SOURCES
  zend/base.cpp
  zend/callable.cpp
  zend/classbase.cpp
  zend/classimpl.cpp
  zend/constant.cpp
  zend/constantfuncs.cpp
  zend/eval.cpp
  zend/exception_handler.cpp
  zend/exists.cpp
  zend/extension.cpp
  zend/extensionimpl.cpp
  # zend/fatalerror.cpp
  zend/file.cpp
  zend/function.cpp
  zend/functor.cpp
  zend/global.cpp
  zend/globals.cpp
  zend/hashmember.cpp
  zend/ini.cpp
  zend/inivalue.cpp
  zend/iteratorimpl.cpp
  zend/members.cpp
  zend/module.cpp
  zend/namespace.cpp
  zend/object.cpp
  zend/sapi.cpp
  zend/script.cpp
  zend/streambuf.cpp
  zend/streams.cpp
  zend/super.cpp
  zend/value.cpp
  zend/valueiterator.cpp
  zend/zendcallable.cpp
  zend/zval.cpp
)

SET(PHPCPP_ZEND_HEADERS
  zend/arithmetic.h
  zend/boolmember.h
  zend/callable.h
  zend/classimpl.h
  zend/compileroptions.h
  zend/constantimpl.h
  zend/delayedfree.h
  zend/executestate.h
  zend/extensionimpl.h
  zend/extensionpath.h
  zend/floatmember.h
  zend/functor.h
  zend/hashiterator.h
  zend/includes.h
  zend/init.h
  zend/invaliditerator.h
  zend/iteratorimpl.h
  zend/lowercase.h
  zend/member.h
  zend/method.h
  zend/module.h
  zend/nativefunction.h
  zend/notimplemented.h
  zend/nullmember.h
  zend/numericmember.h
  zend/objectimpl.h
  zend/opcodes.h
  # zend/origexception.h
  zend/parametersimpl.h
  zend/property.h
  zend/string.h
  zend/stringmember.h
  zend/symbol.h
  zend/symbol.h
  zend/traverseiterator.h
  zend/valueiteratorimpl.h
)

SET(PHPCPP_HEADERS_INCLUDE
  include/argument.h
  include/array.h
  include/arrayaccess.h
  include/base.h
  include/byref.h
  include/byval.h
  include/call.h
  include/class.h
  include/classbase.h
  include/classtype.h
  include/constant.h
  include/countable.h
  include/deprecated.h
  include/error.h
  include/exception.h
  include/extension.h
  # include/fatalerror.h
  include/file.h
  include/function.h
  include/global.h
  include/globals.h
  include/hashmember.h
  include/hashparent.h
  include/ini.h
  include/inivalue.h
  include/interface.h
  include/iterator.h
  include/modifiers.h
  include/namespace.h
  include/noexcept.h
  include/object.h
  include/parameters.h
  include/platform.h
  include/script.h
  include/serializable.h
  include/streams.h
  include/super.h
  include/thread_local.h
  include/traversable.h
  include/type.h
  include/value.h
  include/valueiterator.h
  include/version.h
  include/visibility.h
  include/zendcallable.h
  include/zval.h
)

ADD_LIBRARY(phpcpp STATIC
    ${PHPCPP_HEADERS_INCLUDE}
    ${PHPCPP_ZEND_HEADERS}
    ${PHPCPP_ZEND_SOURCES}
    phpcpp.h
)


ADD_LIBRARY(deep_client_php_extension MODULE
    zend/error.cpp
    zend/exception.cpp
    common/streambuf.cpp
    PyPhpBridge.h
    PyPhpBridge.cpp
	  deep_client_php_wrapper.cpp
)

# Find Boost package
find_package(Boost REQUIRED COMPONENTS python)

# Add the Boost include directory
include_directories(${Boost_INCLUDE_DIRS})

find_package(PythonLibs REQUIRED)

# Link against Boost libraries
TARGET_LINK_LIBRARIES(deep_client_php_extension phpcpp phpcpp-common ${Boost_LIBRARIES} ${PYTHON_LIBRARIES})

set_target_properties(deep_client_php_extension
  PROPERTIES
  ARCHIVE_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}"
  LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}"
  RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}"
  PREFIX ""
)