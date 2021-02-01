-- effacement des tables
DROP TABLE IF EXISTS home; --data related to a home
DROP TABLE IF EXISTS room; --data related to a room
DROP TABLE IF EXISTS user; --data related to an user
DROP TABLE IF EXISTS plantreference; --reference data related to plants
DROP TABLE IF EXISTS plant; --data related to one plant in a room
DROP TABLE IF EXISTS kitreference; --data related to the sensor in one kit => allow to easily add sensors in database by the user
DROP TABLE IF EXISTS sensoraction; --sensor & actionners
DROP TABLE IF EXISTS measure; --measure related to one sensor/action

CREATE TABLE home (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  AddressNumber TEXT NOT NULL,
  Sreet TEXT NOT NULL,
  City TEXT NOT NULL,
  PostalCode TEXT NOT NULL,
  Country TEXT NOT NULL,
  Ip TEXT NOT NULL,
  NumberOfRooms INTEGER NOT NULL,
  DateInsertion TIMESTAMP DEFAULT CURRENT_TIMESTAMP);

CREATE TABLE room (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  Name TEXT NOT NULL,
  HomeReference INTEGER,
  DateInsertion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (HomeReference) REFERENCES logement(id));

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  Name TEXT NOT NULL, --user name
  Email TEXT NOT NULL, --email address
  Password TEXT NOT NULL, --user password
  HomeReference INTEGER, --link to one home
  LastConnection TIMESTAMP DEFAULT CURRENT_TIMESTAMP, --date of last user connection
  DateInsertion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (HomeReference) REFERENCES logement(id));

CREATE TABLE plantreference (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  Name TEXT NOT NULL, --plant name
  Origin TEXT NOT NULL, --country origin of the plant
  Temperature INTEGER, --best temperature for the plant
  Humidity INTEGER, --best Humidity for the plant
  Luminosity INTEGER, --best Luminosity for the plant
  GroundQuality NUMBER, --best ground quality for the plant
  DateInsertion TIMESTAMP DEFAULT CURRENT_TIMESTAMP);

CREATE TABLE plant (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  PlantReference INTEGER,
  RoomReference INTEGER,
  KitReference INTEGER,
  DateInsertion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (PlantReference) REFERENCES plantreference(id),
  FOREIGN KEY (RoomReference) REFERENCES room(id),
  FOREIGN KEY (KitReference) REFERENCES kitreference(id));

CREATE TABLE kitreference (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  Name TEXT NOT NULL,
  SensoractionNames TEXT NOT NULL, --all sensor and action's name related to this kit
  SensoractionUnits TEXT NOT NULL, --all sensor and action's unit related to this kit
  DateInsertion TIMESTAMP DEFAULT CURRENT_TIMESTAMP);

CREATE TABLE sensoraction (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  Name TEXT NOT NULL, --sensor name
  Unit TEXT NOT NULL, --sensor measure unit
  PlantReference INTEGER, --link to one room
  DateInsertion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (PlantReference) REFERENCES plant(id));

CREATE TABLE measure (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  Value REAL,
  SensoractionReference INTEGER,
  DateInsertion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (SensoractionReference) REFERENCES sensoraction(id));
