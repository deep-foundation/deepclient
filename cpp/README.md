# Deep Client implemented in C++

Deep Client - a way to connect your favourite language with Deep.


## Quick Start
```cpp
#include "DeepClientCppWrapper.h"

auto fn(auto deep) {
    //your code
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
```


## Examples
```cpp
auto fn(auto deep) {
    return deep.select(IntValue::make(1))->toJson();
}
```

```cpp
auto fn(auto deep) {
    return deep.insert(AssociativeArray::make({
        {"type_id", 58},
        {"from_id", 0},
        {"to_id", 0}
    }))->toJson();
}
```


## Install/Build
```bash
pip install -r requirements.txt

apt-get install autoconf cmake make automake libtool git libboost-all-dev libssl-dev g++
cmake .
make
./test_deep_client
```
