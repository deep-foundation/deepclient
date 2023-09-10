# cpp-docker-isolation-provider

## Quick Start
```cpp
auto fn(auto params) {
    //your code
}
```
#### or install @archer-lotos/cpp-tests package in deep


## Information about handler parameters
- `/healthz` - GET - 200 - Health check endpoint
    - Response:
        - `{}`
- `/init` - GET - 200 - Initialization endpoint
    - Response:
        - `{}`
- `/call` and `/http-call` - GET - 200 - Call executable code of handler in this isolation provider
    - Request:
        - body:
            - params:
                - jwt: STRING - Deeplinks send this token, for create gql and deep client
                - code: STRING - Code of handler
                - data: {} - Data for handler execution from deeplinks
                  > If this is type handler
                    - oldLink - from deeplinks, link before transaction
                    - newLink - from deeplinks, link after transaction
                    - promiseId - from deeplinks, promise id
    - Response:
        - `{ resolved?: any; rejected?: any; }` - If resolved or rejected is not null, then it's result of execution


## Information about params in function fn

- `params.deep` - Deep Client instance
- `params.data` - Data for handler execution from deeplinks
```cpp
class HandlerParameters {
public:
    DeepClientCppWrapper* deep = nullptr;
    json data;
    HandlerParameters(DeepClientCppWrapper* deepClient, const std::string &jsonData) {
        deep = deepClient;
        data = json::parse(jsonData);
    }
};
```


## Examples
```cpp
auto fn(auto params) {
    return params.data;
}
```

```cpp
auto fn(auto params) {
    return params.deep.select(IntValue::make(1))->toJson();
}
```

```cpp
auto fn(auto params) {
    return params.deep.insert(AssociativeArray::make({
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
#apt-get install libboost-python1.74-dev
cmake .
make
```

#### Or Local restart docker
```bash
docker build -t cpp-docker-isolation-provider .
docker run -d -p 39100:39100 -e PORT=39100 cpp-docker-isolation-provider
docker ps
```


## Check open ports
```bash
netstat -tuln
curl http://localhost:39100
```