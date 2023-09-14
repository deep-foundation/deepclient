#ifndef PYPHPBRIDGE_H
#define PYPHPBRIDGE_H

#include "phpcpp.h"
#include <string>
#include <Python.h>

class PyPhpBridge {
public:
    static bool isAssociativeArray(const Php::Value& phpArray);
    static Php::Value convertPyDictToPhpArray(PyObject* pyDict);
    static Php::Value convertPyListToPhpArray(PyObject* pyList);
    static PyObject* convertPhpArrayToPyDict(const Php::Value& phpArray);
    static PyObject* convertPhpArrayToPyList(const Php::Value& phpArray);
    static PyObject* convertPhpValueToPyObject(const Php::Value& phpValue);
    static std::string getPythonErrorText();
};

#endif // PYPHPBRIDGE_H