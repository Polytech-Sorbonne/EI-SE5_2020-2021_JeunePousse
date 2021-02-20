![alt text](https://github.com/Polytech-Sorbonne/EI-SE5_2020-2021_JeunePousse/blob/main/Code/Server/Logo_JeunePousse.png "Logo JeunePousse")

# EI-SE5_2020-2021_JeunePousse
## SQL database

This solution is represented in a database as follows :

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
* represents a home with its address, IP, number of rooms.
3. room
* represents a room in a home with a name.
5. user
* represents an user account with a name, an email, a password and linked.
7. reference plant
* content all the data referred to a plant, with its ideal temperature, humidity, luminosity and soil humidity.
9. reference kit
* content the description of a "kit" represented by a name. It includes all the name of sensors and actuators and their unities included in the kit.
11. plant
* represents all the content related to a plant located in a room and the kit used to monitor this one. So it contains links to a reference plant, a reference kit and a room
13. sensor
* represents a sensor which is part of a plant monitoring
15. measure
* is one measure of a sensor


![alt text](https://github.com/Polytech-Sorbonne/EI-SE5_2020-2021_JeunePousse/blob/main/Datasheets/Database_and_server_flowcharts/UML_JeunePousse.png "UML of the database")

## HTTP python server
The server has two objectives :

1. Generating the responsive website pages synchronised with the database content,
2. Managing POST requests from modules linked to the plants

---

### Website and server
#### Sign up and sign in
Before using a module, you need to create an user account. By creating this, you will also indicate all the data related to your home including your rooms. After signing up, the tables home, room, and user will be updated by the server from the website REST posted data.

![alt text](https://github.com/Polytech-Sorbonne/EI-SE5_2020-2021_JeunePousse/blob/main/Resources/Connexion_page.png "Connexion Page screenshot")

![alt text](https://github.com/Polytech-Sorbonne/EI-SE5_2020-2021_JeunePousse/blob/main/Resources/Inscription_partie1.png "Subcription part 1 Page screenshot")

![alt text](https://github.com/Polytech-Sorbonne/EI-SE5_2020-2021_JeunePousse/blob/main/Resources/inscription_partie2.png "Subcription part 2 Page screenshot")


Then, you will be able to connect to your account with your email and password.

#### Dashboard page

![alt text](https://github.com/Polytech-Sorbonne/EI-SE5_2020-2021_JeunePousse/blob/main/Resources/Dashboard.png "Dashboard")

![alt text](https://github.com/Polytech-Sorbonne/EI-SE5_2020-2021_JeunePousse/blob/main/Resources/Dashboard_2.png "Dashboard 2")

After connecting, the server handles a REST GET request from the connection website page and it loads your dashboard by getting your various rooms and all the plants in each room from the database.
A navigation bar allows the user to move to the option page and to log out.

On the dashboard, the data are organised as follows :

1. A sidebar menu allowing the user to move from one room to another.
2. For each room, the server lists for each plant in a room, and for all sensors linked to a plant, their last measurement.
3. An information table also indicates the ideal values for each particular plant.

#### Option page

![alt text](https://github.com/Polytech-Sorbonne/EI-SE5_2020-2021_JeunePousse/blob/main/Resources/Options.png "Options")

The option page offers the user's data :
* about him
* of his home
* of his rooms
* of his plants

As a consequence when the server received REST GET request defined as getting the option page, it loads all the data mentionned above from the sql database. Moreover, this website page, allows the user to indicates if his attend to be on vacation but also he can add a room in its home or add a plant to a room.
##### Changing plants functionnal mode
The performance form on this page allows the user to define if if is far from his home for a long time or not. In fact, plants have 2 modes :
1. Performance
2. Vacation
These modes will be explained after in the document.

To change this functionnal mode, the user selects which mode he wants to apply from the website page. Then, the website sends a REST POST request to the server indicating that all plant tables linked to rooms attached to the user's home must be updated in the sql database about this caracteristic.
##### Adding a room
In order to add a room, the user selects the room type and write the name. This method allows to keep a standardized room name composed of :
1. A predefined room type (kitchen, bedroom, ..)
2. A user's choice additionnal name
It allows to have for example : "Tom bedroom" where the user selects "bedroom" and writes "Tom".
After this, the user clicks on the button and the website sends to the server a REST POST with these data. Finally, the server add these data by creating a new table in "room" table.
##### Adding a plant
When a user get a kit (module composed of a microcontroller, sensors and actuators), the module's screen will display the reference module. Then, the user have just to write this reference, he selects in which of his rooms the plant is located and he also selects the type of plant that the module will monitor. By clicking on the button, the serer receives a REST POST request from the website with these data. Then the server updates the plant's database identified by this reference. It updates the fields related to the type of plant and the plant location in the house.



#### Website role
The website is here to display user's modules measures, to aware the user of the ideal constants for his plants, to have a look of the data the sql database have about him. This is also the place where the user can configure a new module he bought. Finally, the only one action that the user can have on its modules is to indicates he will be far from home for a long time (on vacation for example). By indicating this to the website, its modules bahvior will be able to adapt their monitoring to this. The user does not have more to care about. In fact, the server and the modules do everything else for him.


---

### Server for plant monitoring
In addition to website generating, the server also monitor all plants.
The server receives 2 differents POST from modules. Each module discuss with the server through an unique communication port in order to allow multiple threaded connections from the server.
#### First connection POST
When a module is connected to the current, it connects to the internet and directly sends a REST POST request to the server on a general communication port.
It sends its module's unique reference and the kit name which composed it.
By receiving this REST POST request, the server will check in the sql database if a "plant" with the same unique reference exists.
1. If it exists, the server responds to this REST POST request with the communication port already affected to this "plant" before.
2. If it is not in the sql databse, the server will create a "plant" table for this new module by affecting a unique new communication port. It also creates all sensors and actuators related to the kit mentionned by the module. The added "plant" table, will be initialized as a "non user affected" plant. In fact, room reference, functionnal mode and plant reference are initialized at '-1'. These fields are updated when the user add the plant from its reference on the option website page. Then th server responds to the module by sending it a REST POST request with the new affected unique communication port.

By receiving the server's response, the module redefined its communication port as the one returns by the server.

#### Measure POST
After doing the previous step, the module get measures from all its sensors and actuators and then send these to the server as a REST POST request. By receiving this, the server get all the ideal constants related to this plant in "reference plant" table. Then it compares module's sended measures to these ideal constants and defined "corrections" for the module. As a response, the server sends a REST POST request to the module with these corrections.
These are about indications for the module to dispaly on its screen about the temperature, the humidity and the soil humidity. It also indicated if lights need to be switch on by the module or how much it have to irrigates.



## Hardware part
