# Deep Client PHP extension implemented in C++

Deep Client - a way to connect your favourite language with Deep.

## Quick Start
```php
extension_loaded('deep_client_php_extension') or dl('deep_client_php_extension.so');

function test_client($client) {
    $new_record = array(
        "type_id" => 58,
        "from_id" => 0,
        "to_id" => 0
    );
    return $client->insert($new_record);
}

$client = new DeepClientPhpWrapper(
	'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJodHRwczovL2hhc3VyYS5pby9qd3QvY2xhaW1zIjp7IngtaGFzdXJhLWFsbG93ZWQtcm9sZXMiOlsiYWRtaW4iXSwieC1oYXN1cmEtZGVmYXVsdC1yb2xlIjoiYWRtaW4iLCJ4LWhhc3VyYS11c2VyLWlkIjoiMzgwIn0sImlhdCI6MTY5NDcxMTk1NX0.4m8VCpSXxe2JS0sxSk9vkESCK0T2qOV18U8276VfUk0',
	'https://3007-deepfoundation-dev-4lq4ij4517x.ws-eu104.gitpod.io/api/gql'
);
var_dump($client);


var_dump(test_client($client));
```

## Examples

```php
$client->select(1);
```

```php
$new_record = array(
    "type_id" => 58,
    "from_id" => 0,
    "to_id" => 0
);
$client->insert($new_record);
```


## Install/Build Deep Client PHP extension implemented in C++
```bash
pip install -r requirements.txt
apt-get install autoconf cmake make automake libtool git libboost-all-dev libssl-dev g++
cmake .
make
```
