### A demo of Luigi getting started example with dockerized setup

I am using Luigi for the first time and was trying to set it up using docker. Taking help from https://github.com/axiom-data-science/docker-luigi and https://github.com/lucrussell/docker-luigi I managed to get the top_artists example working with dockerized setup of luigi.


__Note:__

The `docker-compose.yml` file has 3 services:

- luigi (this is the central scheduler for running tasks)
- postgres (database used by luigi for storing task and event related information)
- demo (this is the container where we run the top_artists process)

The `docker-compose.yml` file expects one environment variable __DATE_INTERVAL__.

To run this process locally, make sure you have both `docker` and `docker-compose` installed and also make sure the `docker` service is running. Then provide a value for __DATE_INTERVAL__:

For example:

```
export DATE_INTERVAL=2019-12

```

Then create the directories for volumes:

```
mkdir docker-volumes
mkdir docker-volumes/data
mkdir docker-volumes/luigistate
```

Then bring up the docker setup by running:

```
docker-compose up -d
```

It will take some time to build all the containers and start them


You can check the logs using:


```
docker-compose logs -f
```

Once the containers are up and running, if you visit the `http://localhost:8082` on your browser, you will see the Luigi's interface


In the docker-compose logs if you see the following line it means the process ran successfully:

```
luigi-getting-started-docker_demo_1 exited with code 0
```

And the details should be available at `http://localhost:8082`

To run the task for a different date, you do

```
docker-compose down
export DATE_INTERVAL=<some other date interval of your choice>
docker-compose up -d
```

