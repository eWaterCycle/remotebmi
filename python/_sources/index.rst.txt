################
remotebmi Python
################

Welcome to ``remotebmi``'s python documentation!

The `Basic Model Interface (BMI) <https://bmi.readthedocs.io/en/stable/>`_ 
is a standard interface for models. 
The interface is available in different languages and a 
`language agnostic version in SIDL. <https://github.com/csdms/bmi/blob/stable/bmi.sidl>`_

To have a consumer of the model and the provider of the model seperated you
can use `grpc4bmi <https://grpc4bmi.readthedocs.io/>`_, but this only works on
languages that have a grpc implementation.
This repo replaced the gRPC protocol with an REST API.
The `REST API specification <https://github.com/eWaterCycle/remotebmi/blob/main/openapi.yaml>`_
is in the `OpenAPI <https://swagger.io/specification/>`_ format.

Installation
============

.. code-block:: shell

    pip install remotebmi

How to use
==========

There are two parts to remotebmi: the server (which hosts the model) and the 
consumer (who wants to interact with the model).

The server is available for different languages (Julia, R, and Python). Any client
can connect with any server.

Python consumer
---------------

.. code-block:: python

    from remotebmi import RemoteBmiClient

    model = RemoteBmiClient('http://localhost:50051')
    # Now you can use the BMI methods on model
    # for example
    model.initialize('config.file')
    model.update()
    model.get_value('var_name')

A client can also start a `Apptainer <https://apptainer.org/>`_ container 
containing the model and the server:

.. code-block:: python

    from remotebmi import BmiClientApptainer

    model = BmiClientApptainer('my_model.sif', work_dir='/tmp')

The client picks a random port and expects the container to run the BMI web server
on that port. The port is passed to the container using the ``BMI_PORT`` environment
variable.
A client can also start a `Docker <https://docs.docker.com/engine/>`_ container
containing the model and the server.

.. code-block:: python

    from remotebmi import BmiClientDocker

    model = BmiClientDocker('ewatercycle/wflowjl:0.7.3', work_dir='/tmp')

The BMI web server inside the Docker container should be running on port 50051.
If the port is different, you can pass the port as the ``image_port`` argument 
to the ``BmiClientDocker`` constructor.

Python server
-------------

Given you have a model class called ``MyModel`` in a package ``mypackage``
then the web service can be started with the following command.

.. code-block:: shell

    BMI_MODULE=mypackage BMI_CLASS=MyModel run-bmi-server

For example `leakybucket <https://github.com/eWaterCycle/leakybucket-bmi>`_:

.. code-block:: shell

    pip install leakybucket
    BMI_MODULE=leakybucket.leakybucket_bmi BMI_CLASS=LeakyBucketBmi run-bmi-server

and the Python client can connect to it with the following code.

.. code-block:: python

    >>> from remotebmi import RemoteBmiClient
    >>> client = RemoteBmiClient('http://localhost:50051')
    >>> client.get_component_name()

    leakybucket

.. _Docker: https://docs.docker.com/engine/

.. toctree::
    :maxdepth: 3
    :hidden:

    self
    autoapi/index
