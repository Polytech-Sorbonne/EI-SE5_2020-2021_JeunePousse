![alt text](https://github.com/Polytech-Sorbonne/EI-SE5_2020-2021_JeunePousse/blob/main/Code/Server/Logo_JeunePousse.png)
# EI-SE5_2020-2021_JeunePousse
## SQL database
This solution is represented in a database as follow
Entity | attached to 
---|---
**home**|
**room**| one home
**user**| one home
**reference plant**|
**reference kit**|
**plant**| one room, one reference plant, one reference kit
**sensor or actuator**| one plant
**measure**| one sensor or actuator

Considering that :
1. home
--* represents a home with its address, IP, number of rooms.
3. room
--* represents a room in a home with a name.
5. user
--* represents an user account with a name, an email, a password and linked.
7. reference plant
--* content all the data referred to a plant, with its ideal temperature, humidity, luminosity and soil humidity.
9. reference kit
--* content the description of a "kit" represented by a name. It includes all the name of sensors and actuators and their unities included in the kit.
11. plant
--* represents all the content related to a plant located in a room and the kit used to monitor this one. So it contains links to a reference plant, a reference kit and a room
13. sensor or actuator
--* represents a sensor or actuator which is part of a plant monitoring
15. measure
--* is one measure of a sensor or actuator

INSERER UML DE LA DATABASE

## HTTP python server
The server will have to missions :
1. genrerating the website pages synchronised with database content
2. managing posts from modules linked to plants in a home

