# DTRACKER
Track k8s deployment

## Deploy service
1. docker-compose
```
docker-compose up -d 
```
2. k8s
still working on helm chart
## Usage:

### Register deployment
pipeline should have a stage that append these info to dtracker through curl

```
curl -H "Content-Type: application/json" -X POST http://localhost:5000 -d '{"svc_name": "summerizer", "developer_name": "dyaa", "commit_id": "commit3", "commit_message": "feature3"}'
```

### Fetch from dtracker

filter by developer name:

```
curl -X GET http://localhost:5000/developer/dyaa
[
    {
        "svc": "summerizer",
        "developer": "dyaa",
        "commit": "commit3",
        "message": "feature3",
        "time": "24/07/2021 22:46:55"
    },
    {
        "svc": "summerizer",
        "developer": "dyaa",
        "commit": "commit3",
        "message": "feature3",
        "time": "24/07/2021 22:51:24"
    }
]
```

filter by service name:

```
curl -X GET http://localhost:5000/svc/summerizer
[
    {
        "svc": "summerizer",
        "developer": "dyaa",
        "commit": "commit3",
        "message": "feature3",
        "time": "24/07/2021 22:46:55"
    },
    {
        "svc": "summerizer",
        "developer": "dyaa",
        "commit": "commit3",
        "message": "feature3",
        "time": "24/07/2021 22:51:24"
    }
]
```

filer by both service and developer

```
curl -X GET http://localhost:5000/both/dyaa,summerizer
[
    {
        "svc": "summerizer",
        "developer": "dyaa",
        "commit": "commit3",
        "message": "feature3",
        "time": "24/07/2021 22:46:55"
    },
    {
        "svc": "summerizer",
        "developer": "dyaa",
        "commit": "commit3",
        "message": "feature3",
        "time": "24/07/2021 22:51:24"
    }
]
```
