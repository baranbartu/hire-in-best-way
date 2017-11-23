# I have 3 approaches to be able to make the correct design. 

(RESTful API, Threads/Greenlets, Distributed Task Queue (Celery))

## 1- RESTful API (microservice)

### Prerequisites

```
1- A backend database from AWS
```
* [PostgreSQL(RDS)](https://aws.amazon.com/rds/postgresql/) - RDBMS
```
2- A NoSQL or In-Memory database with TTL support
```
* [ElasticSearch(Amazon ElasticSearch Service)](https://aws.amazon.com/elasticsearch-service/) - NoSQL search engine (exists TTL support for under version <=5.0)
* [Redis(Amazon Elasticache)](https://aws.amazon.com/elasticache/redis/) - In-Memory Database to keep data with TTL
```
3- One Amazon EC2 instance to deploy API
```

### Design

* When the job was created using the endpoint with the necessary information 
(job_id, days_to_stay_online_from_the_creation_date, budget), i would create 
a row on the "jobs" table with the auto sequential primary key (id) and the
auto created_at
* I would call existing distribute_budget service and get the output
* I would calculate TTL for this job as seconds using days_to_stay_online_from_the_creation_date
value and the store with this TTL on the Redis for another services usage.
* Also i would use PgBouncer for connection pooling (transaction pooling mode)
to be able to use PostgreSQL with most efficient way (reduce memory usage,
prevent sessions up and idle), limiting requests on api side(not the DB
side), to be able to make the best load balancing to route request with
RoundRobin
* P.S. Nice to have: I would choose Gunicorn(Python WSGI HTTP Server) with
Async Workers, and trying to use async clients for I/O operations like querying
PostgreSQL or Redis, thus we can be able to handle thousand of requests at a
time. Also we need to observe the bottlenecks on the CPU, always be careful to
prevent GIL disaster.
