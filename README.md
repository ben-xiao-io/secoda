# Requirements

The requirements are in `requirements.txt`

1. Create a virtual python environment `python -m venv env`
2. Activate environment. See details [here](https://docs.python.org/3/library/venv.html)
3. Do `pip install -r requirements.txt`


# Launching

1. Django files are stored in `/secoda_assessment`
2. Run `python manage.py runserver`
3. There are two endpoints that you can use. `http://127.0.0.1:8000/api/get-table-metadata/` and `http://127.0.0.1:8000/api/get-table-metadata-from-str/`


# Endpoint details

### http://127.0.0.1:8000/api/get-table-metadata/

The end point is expecting a JSON body of the following format from a POST method in the following format:

```
{
    'host': 'host_url', 
    'db_name': 'name', 
    'username': 'username', 
    'password': 'password', 
    'port': 123
}
```

With the provided test, this is an example with credentials omitted:    
`{'host': 'secoda-demo-postgres.caymkhepkkox.us-east-1.rds.amazonaws.com', 'db_name': 'postgres', 'username': 'USERNAME OMITTED', 'password': 'PASSWORD OMITTED', 'port': PORT_OMITTED}`

### http://127.0.0.1:8000/api/get-table-metadata-from-str/

The endpoint is expecting a connection string in the form of `{'conn_str' : 'postgresql://username:password@host:port/database'}` from a POST method