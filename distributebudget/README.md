# I have 3 approaches to be able to make the correct design. 

(RESTful API, Threads/Greenlets, Distributed Task Queue (Celery))

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

## 1- RESTful API (microservice)

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
prevent GIL disasters.

## 2- Threads/Greenlets

### Design
* I am assuming that this service will be calling at the end of the days
* I would try to code my service as I/O bound, not CPU. Of course CPU will be
  used in any way, but i would try to find C/Rust bindings for python to prevent GIL
* Because Threads or Greenlets will be executing on the one process and one
  sharing CPU core.
* I would prefer to choose Greenlets because threads are expensive in terms of
  virtual memory and kernel overhead because they are still OS threads, not
  native python threads. But greenlets will be working their own context and
  they will provide us the concurrency. If most of the things would be I/O
  bound, then we would get best efficiency.
* I am again assuming a bulk job creation at a day (100, 1000 or more), parsing
  some csv files or ETL task from another database.
* I would write a create_job, distribute_budget and store_result functions.
* After parsing the bulk result i would spawn a greenlet and each function
  would callback(spawn another greenlet) to other functions respectively. And
  it makes our service quite fast.


## 3- Distributed Task Queue (Celery)

We can use either Redis or RabbitMQ as a message broker.

### Design

* I am assuming we have an ETL job for the bulk jobs and a task will be spawn
  for making the necessary duties for each job.
* We have three task: create_job, distribute_budget and store_result
* Also we have three separated message queues and three workers which consuming
  regarding tasks from their queues.
* Each create_job task will spawn distibute_budget subtask and each
  distribute_budget task will spawn store_results subtask.
* We can benchmarking for the 3 tasks to measure CPU bottlenecks using cProfile
  or something else. If one task's CPU usage more than the others, then we
  can tune process counts on the workers according to CPU load.
* For example: We have 16 core server and the create_job function uses %50 of
  CPU resource. Then we can give 8 process to create_job function and give 4
  processes for the other two subtasks.
