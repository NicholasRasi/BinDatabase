# bin-database
A simple bin database with REST interface

### Usage
Push JSON documents into a bin

1. create a bin
```
POST http://localhost:8080/new
Content-Type: application/json

{
  "id": "bin_name",
  "desc": "bin description"
}
``` 

2. post data to bin
```
POST http://localhost:8080/bin_name
Content-Type: application/json

{
  "bench_1": 1000,
  "bench_2": 200
}

```

3. get bin data
```
GET http://localhost:8080/bin_name
Accept: application/json
```

3. get all bins data
```
GET http://localhost:8080//all
Accept: application/json
```