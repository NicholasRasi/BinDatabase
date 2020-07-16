# BinDatabase
A minimal lightweight thread-safe bin database with REST interface (Flask + TinyDB)

## Usage
```python
# init
virtualenv env
source env/bin/activate
pip install -r requirements.txt
# run
python main.py --host "0.0.0.0" --port 8080
```
### Usage
Push JSON documents into a bin

1. post data to bin, if the bin does not exist it will be created
```
POST http://localhost:8080/bin_name
Content-Type: application/json

{
  "bench_1": 1000,
  "bench_2": 200
}

```

2. get bin data
```
GET http://localhost:8080/bin_name
Accept: application/json
```

3. get all bins data
```
GET http://localhost:8080//all
Accept: application/json
```