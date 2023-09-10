#ifndef CPP_DOCKER_ISOLATION_PROVIDER_PYCPPBRIDGE_H
#define CPP_DOCKER_ISOLATION_PROVIDER_PYCPPBRIDGE_H

#include "nlohmann/json.hpp"
#include <iostream>
#include <utility>
#include <variant>
#include <string>
#include <vector>
#include <Python.h>
#include "httplib.h"
#include <ctime>
#include <cstdlib>
#include <map>

using json = nlohmann::json;

class DynamicValue {
public:
    virtual void print() const = 0;
    [[nodiscard]] virtual json toJson() const = 0;
    virtual ~DynamicValue() = default;
};

class IntValue : public DynamicValue {
public:
    int cppValue;

    explicit IntValue(int val) : cppValue(val) {}

    void print() const override {
        std::cout << "Int value: " << cppValue << std::endl;
    }

    [[nodiscard]] json toJson() const override {
        return
                cppValue
                ;
    }

    static auto make(int val) {
        return std::make_shared<IntValue>(val);
    }
};

class FloatValue : public DynamicValue {
public:
    double cppValue;

    explicit FloatValue(double val) : cppValue(val) {}

    void print() const override {
        std::cout << "Float value: " << cppValue << std::endl;
    }

    [[nodiscard]] json toJson() const override {
        return
                cppValue
                ;
    }

    static auto make(double val) {
        return std::make_shared<FloatValue>(val);
    }
};

class StringValue : public DynamicValue {
public:
    std::string cppValue;

    explicit StringValue(std::string val) : cppValue(std::move(val)) {}

    void print() const override {
        std::cout << "String value: " << cppValue << std::endl;
    }

    [[nodiscard]] json toJson() const override {
        return
                cppValue
        ;
    }

    static auto make(auto val) {
        return std::make_shared<StringValue>(val);
    }
};

class NoneValue : public DynamicValue {
public:
    std::string cppValue;

    NoneValue() = default;

    void print() const override {
        std::cout << "None" << std::endl;
    }

    [[nodiscard]] json toJson() const override {
        return
                "none"
        ;
    }

    static auto make(auto val) {
        return std::make_shared<NoneValue>(val);
    }
};

class ArrayValue : public DynamicValue {
public:
    std::variant<std::string, int> cppValue;

    explicit ArrayValue(const std::variant<std::string, int>& val) : cppValue(val) {}

    void print() const override {
        std::cout << "Array value: ";
        std::visit([](const auto& v) { std::cout << v; }, cppValue);
        std::cout << std::endl;
    }

    [[nodiscard]] json toJson() const override {
        json result;
        if (std::holds_alternative<std::string>(cppValue)) {
            result["type"] = "string";
            result["value"] = std::get<std::string>(cppValue);
        } else if (std::holds_alternative<int>(cppValue)) {
            result["type"] = "int";
            result["value"] = std::get<int>(cppValue);
        }
        return result;
    }
};

class AssociativeArray : public DynamicValue {
public:
    std::map<std::string, std::shared_ptr<DynamicValue>> cppValue;

    AssociativeArray() = default;

    AssociativeArray(const std::initializer_list<std::pair<std::string, int>>& values) {
        for (const auto& pair : values) {
            cppValue[pair.first] = std::make_shared<IntValue>(pair.second);
        }
    }

    void addValue(const std::string& key, int value) {
        cppValue[key] = std::make_shared<IntValue>(value);
    }

    void print() const override {
        for (const auto& pair : cppValue) {
            std::cout << "Key: " << pair.first << ", value: ";
            pair.second->print();
        }
    }

    [[nodiscard]] json toJson() const override {
        json json_obj;
        for (const auto& pair : cppValue) {
            json_obj[pair.first] = pair.second->toJson();
        }
        return json_obj;
    }

    static auto make(const std::initializer_list<std::pair<std::string, int>>& values) {
        return std::make_shared<AssociativeArray>(values);
    }
};

class IndexedArray : public DynamicValue {
public:
    std::vector<std::shared_ptr<DynamicValue>> cppValue;

    void print() const override {
        for (const auto& item : cppValue) {
            item->print();
        }
    }

    [[nodiscard]] json toJson() const override {
        json json_obj;
        for (size_t i = 0; i < cppValue.size(); i++) {
            json_obj[i] = cppValue[i]->toJson();
        }
        return json_obj;
    }
};


class PyCppBridge {
public:
    static std::shared_ptr<AssociativeArray> convertPyDictToCppArray(PyObject* pyDict);
    static std::shared_ptr<IndexedArray> convertPyListToCppArray(PyObject* pyList);
    static PyObject* convertCppArrayToPyDict(const std::shared_ptr<AssociativeArray>& cppArray);
    static PyObject* convertCppArrayToPyList(const std::shared_ptr<IndexedArray>& cppArray);
    static std::string getPythonErrorText();

    static PyObject *convertCppArrayToPyObject(const std::shared_ptr<DynamicValue>& sharedPtr);
};


#endif //CPP_DOCKER_ISOLATION_PROVIDER_PYCPPBRIDGE_H
