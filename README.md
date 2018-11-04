# Nameko simple storage #

Provides a small and simple micro-service for storing data into a Redis
backend.

You can use it to store non-sensitive or temporary data for exchanging 
between micro-services.

## Configuration

Before launch the installation of that micro-service, you must edit the
docker-compose.yml file to adapt some variables, IP addresses for instance.

## Installation

You can install this project by using the docker-compose file in the root
folder:

``docker-compose up -d``

## Usage

Once the service up and running, you can test it by connecting on it and run
a Nameko shell:

```
    nameko-simple-storage $ docker exec -it nameko-simple-storage /bin/sh
    /nameko/nameko-simple-storage #
    /nameko/nameko-simple-storage # nameko shell --config ../config.yml
    Nameko Python 3.6.7 (default, Oct 24 2018, 22:57:42)
    [GCC 6.4.0] shell on linux
    Broker: amqp://guest:guest@192.168.1.90 (from --config)
    >>>
``` 

Then, you can store and retrieve data:

```
    >>> my_data = {'project': 'nameko-simple-storage', 'version': '0.2.0'}
    >>> n.rpc.simple_storage.put_item(data=my_data, my_metadata='Use kwargs to store them')
    'ba1b03719b0e8f3aef2b9ea129b87e6bc6bdf668023d2800b35d87536a7aad2d'
    >>>
    >>> data, metadata = n.rpc.simple_storage.get_item('ba1b03719b0e8f3aef2b9ea129b87e6bc6bdf668023d2800b35d87536a7aad2d')
    >>> data
    {'project': 'nameko-simple-storage', 'version': '0.2.0'}
    >>> metadata
    {'my_metadata': 'Use kwargs to store them'}
    >>>
``` 

You can delete data by using get_item method with 'delete_after_read' 
argument at True.

## LICENSE

This project is under MIT license.
