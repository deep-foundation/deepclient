#include "PyPhpBridge.h"

Php::Value PyPhpBridge::convertPyDictToPhpArray(PyObject* pyDict) {
    Php::Value phpArray;

    PyObject* pyKey;
    PyObject* pyValue;
    Py_ssize_t pos = 0;

    while (PyDict_Next(pyDict, &pos, &pyKey, &pyValue)) {
        Php::Value phpKey(PyUnicode_AsUTF8(pyKey));

        if (PyLong_Check(pyValue)) {
            phpArray[phpKey] = Php::Value((long)PyLong_AsLong(pyValue));
        } else if (PyFloat_Check(pyValue)) {
            phpArray[phpKey] = Php::Value(PyFloat_AsDouble(pyValue));
        } else if (PyUnicode_Check(pyValue)) {
            phpArray[phpKey] = Php::Value(PyUnicode_AsUTF8(pyValue));
        } else if (PyDict_Check(pyValue)) {
            phpArray[phpKey] = PyPhpBridge::convertPyDictToPhpArray(pyValue);
        } else if (PyList_Check(pyValue)) {
            phpArray[phpKey] = PyPhpBridge::convertPyListToPhpArray(pyValue);
        } else {
            phpArray[phpKey] = Php::Value();
        }
    }

    return phpArray;
}

Php::Value PyPhpBridge::convertPyListToPhpArray(PyObject* pyList) {
    Php::Value phpArray;

    Py_ssize_t size = PyList_Size(pyList);
    for (Py_ssize_t i = 0; i < size; ++i) {
        PyObject* pyValue = PyList_GetItem(pyList, i);

        if (PyLong_Check(pyValue)) {
            phpArray[i] = Php::Value((long)PyLong_AsLong(pyValue));
        } else if (PyFloat_Check(pyValue)) {
            phpArray[i] = Php::Value(PyFloat_AsDouble(pyValue));
        } else if (PyUnicode_Check(pyValue)) {
            phpArray[i] = Php::Value(PyUnicode_AsUTF8(pyValue));
        } else if (PyList_Check(pyValue)) {
            phpArray[i] = PyPhpBridge::convertPyListToPhpArray(pyValue);
        } else if (PyDict_Check(pyValue)) {
            phpArray[i] = PyPhpBridge::convertPyDictToPhpArray(pyValue);
        } else {
            phpArray[i] = Php::Value();
        }
    }

    return phpArray;
}

std::string PyPhpBridge::getPythonErrorText() {
    PyObject *exc_type, *exc_value, *exc_traceback;
    PyErr_Fetch(&exc_type, &exc_value, &exc_traceback);
    
    if (exc_value) {
        PyObject *str_exc_value = PyObject_Str(exc_value);
        if (str_exc_value) {
            const char *c_str = PyUnicode_AsUTF8(str_exc_value);
            std::string errorText(c_str);
            Py_XDECREF(str_exc_value);
            PyErr_Restore(exc_type, exc_value, exc_traceback);
            return errorText;
        }
    }
    
    PyErr_Restore(exc_type, exc_value, exc_traceback);
    return "Unknown runtime error";
}

PyObject* PyPhpBridge::convertPhpArrayToPyDict(const Php::Value& phpArray) {
    PyObject* pyDict = PyDict_New();

    for (auto& pair : phpArray) {
        std::string key = pair.first.stringValue();
        Php::Value value = pair.second;

        PyObject* pyKey = PyUnicode_DecodeUTF8(key.c_str(), key.length(), "replace");
        PyObject* pyValue = convertPhpValueToPyObject(value);

        PyDict_SetItem(pyDict, pyKey, pyValue);
        Py_DECREF(pyKey);
        Py_DECREF(pyValue);
    }

    return pyDict;
}


PyObject* PyPhpBridge::convertPhpArrayToPyList(const Php::Value& phpArray) {
    PyObject* pyList = PyList_New(phpArray.size());

    for (size_t i = 0; i < phpArray.size(); ++i) {
        Php::Value value = phpArray[i];
        PyObject* pyValue = convertPhpValueToPyObject(value);

        PyList_SET_ITEM(pyList, i, pyValue);
    }

    return pyList;
}

bool PyPhpBridge::isAssociativeArray(const Php::Value& phpArray) {
    if (!phpArray.isArray()) {
        return false;
    }

    for (auto& pair : phpArray) {
        if (!pair.first.isNumeric()) {
            return true;
        }
    }

    return false;
}

PyObject* PyPhpBridge::convertPhpValueToPyObject(const Php::Value& phpValue) {
    if (phpValue.isNumeric()) {
        return PyFloat_FromDouble(phpValue.numericValue());
    } else if (phpValue.isString()) {
        return PyUnicode_DecodeFSDefault(phpValue.stringValue().c_str());
    } else if (phpValue.isArray()) {
        if (phpValue.count() == 0) {
            return PyList_New(0);
        } else if (PyPhpBridge::isAssociativeArray(phpValue)) {
            return convertPhpArrayToPyDict(phpValue);
        } else {
            return convertPhpArrayToPyList(phpValue);
        }
    } else {
        // Py_RETURN_NONE;
        throw Php::Exception("Runtime error, variable undefined");
    }
}