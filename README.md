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
..* represents a home with its address, IP, number of rooms.
3. room
..* represents a room in a home with a name.
5. user
..* represents an user account with a name, an email, a password and linked.
7. reference plant
..* content all the data referred to a plant, with its ideal temperature, humidity, luminosity and soil humidity.
9. reference kit
..* content the description of a "kit" represented by a name. It includes all the name of sensors and actuators and their unities included in the kit.
11. plant
..* represents all the content related to a plant located in a room and the kit used to monitor this one. So it contains links to a reference plant, a reference kit and a room
13. sensor or actuator
..* represents a sensor or actuator which is part of a plant monitoring
15. measure
..* is one measure of a sensor or actuator

INSERER UML DE LA DATABASE


## HTTP python server
The server will have to missions :
1. genrerating the responsive website pages synchronised with database content
2. managing posts from modules linked to plants in a home

### Website and server
#### Sign up and sign in
Before using a module, you need to create an user account. By creating this, you also indicates all the data related to your home including your home's room. After signing up, home, room, and user sql database's tables will be upgraded by the server from the website REST posted data.

INSERER 1 IMAGE PAGE CONNEXION & 2 IMAGES CREATION COMPTE

Then, you will be able to connect to your account by indicating your email and password.

#### Dashboard page

INSERER IMAGE DASHBOARD

After connecting, the server handles a REST GET request from the connection website page and it loads your dashboard page by getting your home's room and all the plant in each room from the databse.
A navigation bar allows the user to move to the option page of to log out. To do this, REST GET requests are send from the navigation bar to the server.
On the dashboard, the data are organised as follow :
1. a sidebar menu allow the user to move from home's rooms to an other.
2. for each room, the server lists for each plant in a room, for all sensors and actuoators linked to a plant its last measure.
3. an information table also indicates the ideal measures referred to this plant.

#### Option page

INSERER IMAGE OPTION

The option page offers the user's data :
..* about him
..* of plants home
..* of plants rooms
..* of his plants

As a consequence whren the server received REST GET request defined as getting the option page, it loads all the data mentionned above from the sql database. Moreover, this website page, allows the user to indicates if his attend to be on vacation but also he can add a room in its home or add a plant to a room.
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


