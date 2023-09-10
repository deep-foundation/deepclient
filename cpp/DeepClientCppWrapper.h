#ifndef DEEP_CLIENT_CPP_WRAPPER_H
#define DEEP_CLIENT_CPP_WRAPPER_H

#include "PyCppBridge.h"

class DeepClientCppWrapper {
private:
    std::string token;
    std::string url;
    PyObject* deepClientModule = nullptr;
    void initializePython();
    void finalizePython();
public:
    DeepClientCppWrapper();
    ~DeepClientCppWrapper();
    DeepClientCppWrapper(const std::string& jwt, const std::string& gql_urn_str);

    std::shared_ptr<DynamicValue> select(const std::shared_ptr<DynamicValue>& query);
    std::shared_ptr<DynamicValue> insert(const std::shared_ptr<DynamicValue>& query);
    std::shared_ptr<DynamicValue> update(const std::shared_ptr<DynamicValue>& query);
    std::shared_ptr<DynamicValue> deleteFunc(const std::shared_ptr<DynamicValue>& query);
    std::shared_ptr<DynamicValue> serial(const std::shared_ptr<DynamicValue>& query);
    std::shared_ptr<DynamicValue> id(const std::shared_ptr<DynamicValue>& query);
    std::shared_ptr<DynamicValue> call_python_function(const std::string& function_name, const std::shared_ptr<DynamicValue>& query);
};

#endif // DEEP_CLIENT_CPP_WRAPPER_H