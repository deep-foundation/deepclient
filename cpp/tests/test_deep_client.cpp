#include "../DeepClientCppWrapper.h"

auto fn(auto deep) {
    std::cout << "\ntest deep.select:" << std::endl;
    std::cout << deep.select(IntValue::make(1))->toJson() << std::endl;
    std::cout << "\ntest deep.insert:" << std::endl;
    return deep.insert(AssociativeArray::make({
                                                      {"type_id", 58},
                                                      {"from_id", 0},
                                                      {"to_id", 0}
                                              }))->toJson();
}

int main() {
    try {
        std::cout << fn(DeepClientCppWrapper("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJodHRwczovL2hhc3VyYS5pby9qd3QvY2xhaW1zIjp7IngtaGFzdXJhLWFsbG93ZWQtcm9sZXMiOlsiYWRtaW4iXSwieC1oYXN1cmEtZGVmYXVsdC1yb2xlIjoiYWRtaW4iLCJ4LWhhc3VyYS11c2VyLWlkIjoiMzgwIn0sImlhdCI6MTY5MTkxMTQxM30.W0GOuqOvRZrgrVZkLaceKTPBitXwR-1WlxLgxUZXOnY",
                                             "http://192.168.0.135:3006/gql")) << std::endl;
        return 0;
    } catch (const std::exception& e) {
        std::cout << e.what() << std::endl;
        return 1;
    }
}