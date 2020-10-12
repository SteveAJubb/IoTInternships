# Guide for Setup of Node Red inside Docker

Node-Red is a great tool for accessing the data from TheThingsNetwork and utilising it. 

To make the process of setting up a application of Node-Red we will use Docker. Docker is a system that allows os-level virtualisation similar to virtual machines but with significantly less hardware demand. 


## Installing Docker

The easiest way to install and setup your first docker container if on a windows machine is to install Docker Desktop.

[Instructions and Download Links](https://docs.docker.com/docker-for-windows/install-windows-home/)

## Installing Node-Red

Inside Command Prompt use the command:

    docker run -it -p 1880:1880 --name mynodered nodered/node-red

This will create a container with the nodered application running. You can then access this application on a web browser using your local machine and the port 1880.

[http://127.0.0.1:1880/](http://127.0.0.1:1880/)

## Installing Additional Palletes
Two additional palletes are used to for the example code given. Firstly the TTN pallette which allows you to import the messages from the TTN network.

node-red-contrib-ttn  

Secondly the Email palette which allows you to send emails as part of flows. 
node-red-node-emai

To install these palletes click in the top right corner for settings and then manage palletes. Click on the install tab and then search for the palettes given above.

## Importing Code
With the additional palletes installed you will be able to succesfully import the example code provided. This is done by clicking settings and then import. Then paste in the example code.
