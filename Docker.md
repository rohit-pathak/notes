## Containers

Define a Dockerfile first

To build (-t is for tag):
docker build -t drfservice .

To run a container:
docker run -p 4000:80 drfservice
This runs a container mapping port 4000 of the host (outer machine) to port 80 of the container 

To associate a local image to one in a repository:
docker tag drfservice rohitpathak/drfservice:v0

To push to registry
docker push rohitpathak/drfservice:v0


## Services

After creating docker-compose.yml, we run
docker swarm init
This makes the current computer a "manager". 

To deploy our "stack"
$ docker stack deploy -c docker-compose.yml drfangularlab
Where drfangularlab then becomes the name of our stack.

where drfangularlab is the name of our "app". App is whole thing (the whole "stack" defined in our docker-compose.yml)

(App = stack? I think yes)

To list created services
docker service ls

A single container running in a service is called a task.
docker service ps drfangularlab_restapi 
lists the tasks for that service

docker container ls 
would include the "tasks"/containers running for drfangularlab_restapi

To redeploy, just run the docker stack deploy command again. Docker performs an in-place update, no need to tear the stack down first or kill any containers.

To take down the stack
docker stack rm drfangularlab

To take down the swarm
docker swarm leave --force


## Swarms
A swarm is a collection of machines running docker. You can think of it as one giant Docker machine.

It has a manager machine and worker machines. We execute commands from the manager machine.

"Enabling swarm mode instantly makes the current machine a swarm manager. From then on, Docker runs the commands you execute on the swarm you’re managing, rather than just on the current machine."

To make a machine a manager (no need for docker-machine if running on pure server):
(venv)  $ docker-machine ssh myvm1 "docker swarm init --advertise-addr 192.168.99.100"

To have another machine join as a worker (see auto generated command when you initialize a manager):
(venv)  $ docker-machine ssh myvm2 "docker swarm join --token SWMTKN-1-3w6khqtw1sgfq2m4xa4w1pis1x94llt3gor1c0u2k047hexlew-8krpt60degbw9c1rdx8ygbhdg 192.168.99.100:2377"

To list nodes (machines in the swarm):
(venv)  $ docker-machine ssh myvm1 "docker node ls"

To have a machine leave a swarm
docker swarm leave

[TODO: Read more about docker-machine and how it may help in automated deployments on cloud servers.]

Miscellaneous docker machine stuff:
eval $(docker-machine env myvm1) # Mac command to connect shell to myvm1
eval $(docker-machine env -u) # Disconnect shell from VMs, use native docker


## Stacks

The top of the hierarchy of distributed applications: the stack. A stack is a group of interrelated services that share dependencies, and can be orchestrated and scaled together. A single stack is capable of defining and coordinating the functionality of an entire application.







