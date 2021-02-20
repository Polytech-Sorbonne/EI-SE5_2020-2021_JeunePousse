import http.server, urllib.parse, sqlite3, requests, threading,  socketserver, cgi, random
from urllib.parse import urlparse
from math import *
import json
import datetime as dt

port = []

email_root = "root@root.root"
password_root = "root@root.root"

OK = 200
KO = 404
REDIRECTION = 301

colors = ['#007bff', '#ff00ff', '#7570E3', '#64E2B6', '#64E268', '#F98151', '#DEC61D', '#DE1D72']

#Donnee temporaire le temps de la configuration d'un compte
#home
AddNumber_t = ""
Street_t = ""
City_t = ""
PostalCode_t = ""
Country_t = ""
NumberOfRooms_t = ""
ip_t = ""
#user
Name_t = ""
Email_t = ""
Password_t = ""
#room
room_t = []
piece_type = ["salon", "salle à manger", "chambre", "salle de bain", "cuisine", "garage"]
############################################################
html_start = '<!DOCTYPE html><html lang="fr"><head><title>Jeune Pousse</title><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css"> <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script><script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script><script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script><style type="text/css" media="screen"></head>'
html_body = '<body>'
html_end = '</body>\n</html>'
icone_house = '<svg xmlns="http://www.w3.org/2000/svg" width="40%" height="40%" fill="currentColor" class="bi bi-house-fill" viewBox="0 0 16 16"><path fill-rule="evenodd" d="M8 3.293l6 6V13.5a1.5 1.5 0 0 1-1.5 1.5h-9A1.5 1.5 0 0 1 2 13.5V9.293l6-6zm5-.793V6l-2-2V2.5a.5.5 0 0 1 .5-.5h1a.5.5 0 0 1 .5.5z"/><path fill-rule="evenodd" d="M7.293 1.5a1 1 0 0 1 1.414 0l6.647 6.646a.5.5 0 0 1-.708.708L8 2.207 1.354 8.854a.5.5 0 1 1-.708-.708L7.293 1.5z"/></svg>'
icone_user= '<svg xmlns="http://www.w3.org/2000/svg" width="40%" height="40%" fill="currentColor" class="bi bi-person-square" viewBox="0 0 16 16"><path d="M11 6a3 3 0 1 1-6 0 3 3 0 0 1 6 0z"/><path d="M2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2zm12 1a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1v-1c0-1-1-4-6-4s-6 3-6 4v1a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1h12z"/></svg>'

no_data = 1000000

temp_email = ''
temp_password = ''

icone_3_traits = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-border-width" viewBox="0 0 16 16"><path d="M0 3.5A.5.5 0 0 1 .5 3h15a.5.5 0 0 1 .5.5v2a.5.5 0 0 1-.5.5H.5a.5.5 0 0 1-.5-.5v-2zm0 5A.5.5 0 0 1 .5 8h15a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5H.5a.5.5 0 0 1-.5-.5v-1zm0 4a.5.5 0 0 1 .5-.5h15a.5.5 0 0 1 0 1H.5a.5.5 0 0 1-.5-.5z"/></svg>'
icone_graphe = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-bar-chart-line-fill" viewBox="0 0 16 16"><path d="M11 2a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v12h.5a.5.5 0 0 1 0 1H.5a.5.5 0 0 1 0-1H1v-3a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v3h1V7a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v7h1V2z"/></svg>'
icone_question = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-question-square-fill" viewBox="0 0 16 16"><path d="M2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2zm3.496 6.033a.237.237 0 0 1-.24-.247C5.35 4.091 6.737 3.5 8.005 3.5c1.396 0 2.672.73 2.672 2.24 0 1.08-.635 1.594-1.244 2.057-.737.559-1.01.768-1.01 1.486v.105a.25.25 0 0 1-.25.25h-.81a.25.25 0 0 1-.25-.246l-.004-.217c-.038-.927.495-1.498 1.168-1.987.59-.444.965-.736.965-1.371 0-.825-.628-1.168-1.314-1.168-.803 0-1.253.478-1.342 1.134-.018.137-.128.25-.266.25h-.825zm2.325 6.443c-.584 0-1.009-.394-1.009-.927 0-.552.425-.94 1.01-.94.609 0 1.028.388 1.028.94 0 .533-.42.927-1.029.927z"/></svg>'


bdd_user_capt = ["Name", "Unit", "PlantReference", "DateInsertion"]
bdd_user_plant_fields = ["id", "PlantReference", "RoomReference", "PortCOM", "Reference SN", "Performance"]
bdd_home_fields = ["id", "Location", "Ip", "Number Of Rooms", "Insertion Date", ""]
bdd_room_fields = ["", "id", "Name", "Home Reference", "Insertion Date", ""]
bdd_user_fields = ["id", "Name", "Email", "Password", "Home Reference", "Insertion Date"]
bdd_plant_fields = ["Name", "Origin", "Temperature", "Humidity", "Luminosity", "GroundQuality"]
bdd_kit_fields = ["Name", "SensoractionNames", "SensoractionUnits", "Insertion Date"]
img_dashboard = ['https://www.wallpaperup.com/uploads/wallpapers/2017/04/22/1086857/48df69b50d7601215c6509cb7bd6ab69-1000.jpg'
    , 'https://www.wallpaperup.com/uploads/wallpapers/2016/06/24/991640/24d24526389da7b23e893cb4cc5a69bc-1000.jpg'
    , 'https://s2.best-wallpaper.net/wallpaper/1920x1080/1707/Insect-plant-green-blurry_1920x1080.jpg'
    , 'https://www.wallpaperup.com/uploads/wallpapers/2013/07/21/121843/baaf1f0c61e2e12f49136ea2d01a2e08-1400.jpg'
    , 'https://www.wallpaperup.com/uploads/wallpapers/2014/04/17/335836/3ee55c99a9d557242d54cc4ac40863d7-1400.jpg']

sensor_type = ["Temperature", "Humidity", "Luminosity", "Ground quality", "Water tank"]

def add_nav_bar(activ_num, id_user, active_room, performance, fixe):
    if fixe == 1:
        content = '<nav class="navbar navbar-inverse navbar-fixed-top"><div class="container-fluid"><div class="navbar-header"><a class="navbar-brand">Jeune Pousse</a></div><ul class="nav navbar-nav">'
    else:
        content = '<nav class="navbar navbar-inverse"><div class="container-fluid"><div class="navbar-header"><a class="navbar-brand">Jeune Pousse</a></div><ul class="nav navbar-nav">'
    if activ_num == 1:
        content += '<li class="active"><a href="/dashboard/{}/{}/{}">Dashboard</a></li>'.format(str(id_user), str(active_room), str(performance))
    else :
        content += '<li><a href="/dashboard/{}/{}/{}">Dashboard</a></li>'.format(str(id_user), str(active_room), str(performance))
    if activ_num == 2:
        content += '<li class="active"><a href="/option/{}/{}/{}">Configure</a></li>'.format(str(id_user), str(active_room), str(performance))
    else :
        content += '<li><a href="/option/{}/{}/{}">Configure</a></li>'.format(str(id_user), str(active_room), str(performance))
    content += '</ul>'
    content += '<ul class="nav navbar-nav navbar-right"><li><a href="/home"><span class="glyphicon glyphicon-user"></span> Log Out</a></li></ul>'
    content += '</div>\n</nav>'
    return content

def get_room_image(room_name):
    path = 'site/pictures/'
    room = ''
    if('salle de bain' in room_name):
        room = 'salle_de_bain'
    elif('salle à manger' in room_name):
        room = 'salle_a_manger'
    else:
        room_category = room_name.split(' ')
        room = room_category[0]
    f = open(path + room + '.txt', 'r')
    content = f.read()
    f.close()
    return content

def construct_dashboard(home, user_list, room_list, user_plant_list, kitreference_list, reference_plant_list, user_sensor, user_measure, performance, active_room):
    user = user_list
    user_home = home[0]
    user_room = []
    user_plant = []
    global colors
    #on recupere la home, la room et les plantes de l'utilisateur

    for h in home:
        if h[0] == user[4]:
            user_home = h
    first_room = room_list[0]
    is_active_room_user_s = False
    for p in room_list:
        if p[2] == user_home[0]:
            user_room.append(p)
            if int(p[0]) == int(active_room):
                is_active_room_user_s = True
    first_room = user_room[0]
    if not is_active_room_user_s:
        print("not in room")
        active_room = first_room[0]
    for pl in user_plant_list:
        if int(pl[2]) == int(active_room):
            user_plant.append(pl)
    nb_of_plants = len(user_plant)
    nb_of_rooms = len(user_room)

    f = open('site/header_dashboard.html', 'r')
    content = f.read()
    f.close()
    #on extrait les mesures
    for p in user_plant:
      colo = 0
      sensor = []
      unite = []
      data = []
      for s in user_sensor:
          if s[3] == p[0]:
              value = []
              i = 50
              print(user_measure)
              for m in reversed(user_measure):
                  if m[2] == s[0]:
                      if i > 0:
                          print("MESUREEEE")
                          value.append((m[1], convert_time(m[3])))
                          i -= 1
              sensor.append((s[1], value, s[2])) #nom du capteur, liste (valeurs, dateinsertion), unite
      #content += create_one_chart(sensor, p[0])
    content += html_body
    content += add_nav_bar(1, user[0], active_room, performance, 1) #ajout de la navbar

    content += '<div class="sidebar">'

    content += '<div class="sidebar-header text-center">'
    content += '<legend><h3 style="color: white;">Mes pièces</h3></legend>'
    content += '</div>'
    i = 1
    nom_room_active = ''
    for r in user_room:
        if int(active_room) == int(r[0]):
            content += '<a href="/dashboard/{}/{}/{}" class="active" >{}</a>'.format(str(user[0]), str((r[0])), str(performance), r[1])
            nom_room_active = r[1]
        else:
            content += '<a href="/dashboard/{}/{}/{}">{}</a>'.format(str(user[0]), str((r[0])), str(performance), r[1])
        i += 1
    content += '</div>'

    content += '<div class="main container-fluid">'
    #content += '<div class="col-sm-2">' #colonne vide

    content += '<div class="col-sm-12" style="background-color:#E1D5C8;">'#debut colonne donnees
    url = random.choice(img_dashboard)
    color = 'white'
    #if url == img_dashboard[3]:
    #    color = '#93A6C5'
    content += '<div class="row text-center" style="background-image:url(\'{}\'); background-repeat:no-repeat;background-size:cover;">'.format(url)
    content += '<h1 class="sticky" style="color:{};"><b><br>Mon dashboard de<br>{}</b></h1>'.format(color, nom_room_active)
    content += '<h1><br><br><br><br><br><br><br><br><br><br><br></h1>'
    content += '</div>'
    for p in user_plant:
        good = 0
        nom = ''
        temperature = ''
        humidity = ''
        luminosity = ''
        groundquality = ''
        img_url = ''
        for p_r in reference_plant_list:
            if p[1] == p_r[0]:
                nom = p_r[1]
                temperature = p_r[3]
                humidity = p_r[4]
                luminosity = p_r[5]
                groundquality = p_r[6]
                img_url = p_r[7]
        sensor = []
        if (len(user_measure) != 0) & (len(user_sensor) != 0):
            for s in user_sensor:
                if s[3] == p[0]:
                    value = user_measure[0]
                    for m in user_measure:
                        if m[2] == s[0]:
                            value = m
                    sensor.append((s[1], value[1], s[2], value[-1])) #nom du capteur, valeur, unite, date de la mesure
        #content += '<div class="row">' #debut ligne => plante
        #content += '<img src="{}" class="img-fluid" alt="Responsive image" >'.format(img_dashboard) #width="40" height="40"
        #content += '</div>'
        content += '<div class="row" style="background-color:#E1D5C8;">' #debut ligne => plante

        content += '<div class="row text-left" >' #debut ligne nom plante
        content += '<div class="col-sm-6"><ul><h2 style="color:#7386D5;">Données de ma plante : <b>{}</b></h2></div></ul>'.format(nom)
        content += '<div class="col-sm-3"><h2 class="text-center" style="color:#7386D5;">'
        content += '<svg onclick="display_graph{}() "'.format(p[0])
        content += ' xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-bar-chart-line-fill" viewBox="0 0 16 16"><path d="M11 2a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v12h.5a.5.5 0 0 1 0 1H.5a.5.5 0 0 1 0-1H1v-3a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v3h1V7a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v7h1V2z"/></svg>'
        content += ' '
        content += icone_question
        content += '</h2></div>'
        content += '<div class="col-sm-3">'
        maj = ''
        for s in sensor:
            maj = s[3]
        content += '<p class="text-center"><br>Dernière mise à jour {}</p>'.format(maj)
        content += '</div>'
        content += '</div>'
        content += '<legend>'
        content += '</legend>' #fin ligne nom plante

        #content += '<legend style="background-color:#E1D5C8;"><p></p></legend>'
        #content += '<div class="row text-left">' #debut ligne donnees plante
        content += '<div class="col-sm-9" >' #debut ligne donnees brutes
        i = 0
        for s in sensor:
            if i == 0:
                content += '<div class= "row text-center">'
            content += '<div class="col-sm-5">'
            name = s[0]
            if name == 'GroundQuality':
                name = 'Soil humidity'
            content += '<h3>{}</h3><h4> {} {}</h4>'.format(name, s[1], s[2])
            content += '</div>'
            i += 1
            if i == 2:
                content += '</div>'
                i = 0
        #content += '</ul>'
        content += '</div>'#fin ligne donnees brutes
        content += '<div class="col-sm-3" style="background-color:white;">' #debut colonne plante reference
        content += '<div class="row text-left">'
        content += '<div class="col-sm-8">'
        content += '<h4> Informations sur les {}s'.format(nom)
        content += '</div>'
        content += '<div class="col-sm-4">'
        content += '<img src="{}" class="img-fluid" alt="Responsive image" width="65" height="65">'.format(img_url)
        content += '</div>'
        content += '</div>'
        content += '<div class="row text-left">'
        content += '<div class="col-sm-6">'
        f = open('site/pictures/temperature.txt')
        url = f.read()
        f.close()
        content += '<h4 style="color:#7386D5;"><img src="{}" class="img-fluid" alt="Responsive image" width="40" height="40">{}°C</h4>'.format(url, str(temperature))
        #content += '</div>'
        #content += '<div class="col-sm-2">'
        #content += '<h4 style="color:#7386D5;">{}°C</h4>'.format(str(temperature))
        content += '</div>'
        #content += '<div class="col-sm-1">'
        content += '<div class="col-sm-6">'
        f = open('site/pictures/humidity.txt')
        url = f.read()
        f.close()
        content += '<h4 style="color:#7386D5;"><img src="{}" class="img-fluid" alt="Responsive image" width="40" height="40">{}%</h4>'.format(url, str(humidity))
        content += '</div>'
        content += '</div>'
        #content += '<div class="col-sm-2">'
        #content += '<h4 style="color:#7386D5;">{}%</h4>'.format(str(humidity))
        #content += '</div>'
        #content += '</div>'
        content += '<div class="row text-left">'
        content += '<div class="col-sm-6">'
        f = open('site/pictures/luminosity.txt')
        url = f.read()
        f.close()
        content += '<h4 style="color:#7386D5;"><img src="{}" class="img-fluid" alt="Responsive image" width="40" height="40">{}L</h4>'.format(url, str(luminosity))
        content += '</div>'
        content += '<div class="col-sm-6">'
        f = open('site/pictures/qualite_sol.txt')
        url = f.read()
        f.close()
        content += '<h4 style="color:#7386D5;"><img src="{}" class="img-fluid" alt="Responsive image" width="40" height="40">{}%</h4>'.format(url, str(groundquality))
        content += '</div>'
        content += '</div>' #fin colonne plante reference
        content += '<div class="row" style="background-color:#E1D5C8;"><div class="col-sm-12" style="background-color:#E1D5C8;"><h3></h3></div></div>'
        content += '</div>'#fin ligne donnees plante
        content += '</div>'#fin colonne donnees
        content += '<div class="row" id="graph{}" style="background-color:#F5CB9E;display: none;">'.format(p[0]) #debut graphe
        content += '<canvas class="my-4 w-100" id="chart_div{}"></canvas>'.format(p[0])
        content += '</div>' #fin graphe
        #content += '</div>'#fin ligne => plante
        content += '<div class="row" style="background-color:#fafafa;">'
        content += '<h3><br></h3>'
        content += '</div>'
    content += '</div>'
    content += '</div>'

    content += '<script>'
    for p in user_plant:
      content += 'function display_graph{}() '.format(p[0])
      content += ' {var x = document.getElementById("graph'
      content += '{}");'.format(p[0])
      content += 'if (x.style.display === "none") {x.style.display = "block"; drawChart{};} else {x.style.display = "none";}}'
    content += '</script>'



    content += html_end

    return content

def convert_time(time):
    list_ = time.split("-", 1)
    year = list_[0]
    month = list_[1]

    print(month)
    list_ = month.split("-",1)
    month_ = list_[0]
    month_int = ((int)(month_)) - 1
    month = str(month_int)
    print(month)
    day = list_[1]
    list_ = day.split(" ",1)
    day = list_[0]
    hour = list_[1]
    list_ = hour.split(":", 1)
    hour = list_[0]
    min = list_[1]
    list_ = min.split(":", 1)
    min = list_[0]
    return year, month, day, hour, min

def construct_option_page(home, user_list, room_list, user_plant_list, kitreference_list, reference_plant_list, performance, active_room):
    user = user_list
    user_home = home[0]
    user_room = []
    user_plant = []

    #on recupere la home, la room et les plantes de l'utilisateur

    for h in home:
        if h[0] == user[4]:
            print(h)
            user_home = h
    for p in room_list:
        if p[2] == user_home[0]:
            user_room.append(p)
    if len(user_plant_list) != 0:
        for p in user_plant_list:
            for r in user_room:
                if p[2] == r[0]:
                    user_plant.append(p)
    nb_of_plants = len(user_plant)
    nb_of_rooms = len(user_room)

    f = open('site/header_options.html', 'r')
    content = f.read()
    f.close()
    content += html_body
    content += add_nav_bar(2, user[0], active_room, performance, 0) #ajout de la navbar
    content += '<div id="div_img"></div>'
    content += '<div class="col-sm-12">'
    content += '<div class="row content">'

    content += '<div class="col-sm-8">'
    content += '<div class="row text-center">'

    content += '<h1 class="h1 mb-1 font-weight-bold text-center"><b><br><br>Configurez votre logement</b></h1>'
    content += '<h3 class="h3 mb-1 font-weight-normal text-center">Constuler les données liées à votre logement et ajoutez une pièce ou une plante</h3>'
    content += '</div>'

    content += '</div>'
    content += '<div class="col-sm-4 text-center" style="background:#f5f5f5;background:rgba(255,255,255,0.8);border: none;">'
    content += '<div class="row text-center">'
    content += '<legend class="col-form-label">Mode des modules</legend>'
    content += '</div>'
    content += '<div class="row text-center">'
    content += '<form class="form-signin" action="/performance_mode/{}/{}/{}/{}" method="post">'.format(str(user_home[0]), str(user[0]), str(active_room), str(performance))
    content += '<select class="form-control m-3" id="performance" name="performance" placeholder="Mode" onchange="this.form.submit()">'
    if int(performance) == 1:
        content += '<option selected="selected" class="text-center" value="1">Performance</option>'
        content += '<option class="text-center" value="0">Vacances</option>'
    else:
        content += '<option class="text-center" value="1">Performance</option>'
        content += '<option selected="selected" class="text-center" value="0">Vacances</option>'
    content += '</select>'
    content += '</form>'
    content += '</div>'
    content += '<div class="row text-justify">'
    content += '<div class="col-sm-1 text-center">'
    content += '</div>'
    content += '<div class="col-sm-10 text-justify">'
    content += '<p><br><b>Performance : </b>Vos kits échangent fréquemment avec notre service et son contrôlés par ce dernier<br><br><b>Vacance : </b>Utile quand vous êtes loin de chez vous, la main est laissée à votre module qui s\'adapte à votre absence<p>'
    content += '</div>'
    content += '<div class="col-sm-1 text-center">'
    content += '</div>'
    content += '</div>'
    content += '</div>'
    content += '</div>'

    content += '<div class="row content mb-3">'
    content += '<h1><br><br><br></h1>'
    content += '<div class="col-sm-4 text-center">'
    content += '<div class="col-sm-12 text-center" style="background:#000;background:rgba(255,255,255,0.6);">'
    content += '<div class="row content">'
    content += '<div class="col-sm-4">'
    content += '<br>'
    content += icone_user
    content += '</div>'
    content += '<div class="col-sm-8 text-center">'
    content += '<div class="row content">'
    content += '<p><b><br>Nom </b>{}</p>'.format(user[1])
    content += '</div>'
    content += '<div class="row content">'
    content += '<p><b>E-mail </b>{}</p>'.format(user[2])
    content += '</div>'
    content += '</div>'
    content += '</div>'
    content += '<div class="row content">'
    content += '<div class="col-sm-4">'
    content += '<br><br>'
    content += icone_house
    content += '</div>'
    content += '<div class="col-sm-8 text-center">'
    content += '<br>'
    content += '<div class="row content">'
    content += '<p>{}</p>'.format(user_home[1] + " rue " + user_home[2])
    content += '</div>'
    content += '<div class="row content">'
    content += '<p>{}</p>'.format(user_home[3])
    content += '</div>'
    content += '<div class="row content">'
    content += '<p>{}</p>'.format(user_home[4] + ", " + user_home[5])
    content += '</div>'
    content += '</div>'

    content += '</div>'
    content += '</div>'
    content += '<div class="row content">'
    content += '<div class="col-sm-12 text-center">'
    content += '<p></p>'
    content += '</div>'
    content += '</div>'
    content += '<div class="row content">'
    content += '<div class="col-sm-12 text-center">'
    content += '<div class="col-sm-12 text-center" style="background:#000;background:rgba(255,255,255,0.6);">'
    content += '<h4 class="h4 mb-2 font-weight-normal text-center"><b><br>Nombre de pièces enregistrées </b>{}<br><br><b>Nombre de plantes enregistrées</b> {}</h4>'.format(str(nb_of_rooms), str(nb_of_plants))
    content += '<h5 class="h5 mb-2 font-weight-normal text-center"><br><b>Dernière mise à jour </b>{}</h5>'.format("a completer")
    content += '</div>'
    content += '</div>'
    content += '</div>'
    content += '</div>'


    content += '<div class="col-sm-8 text-center">'
    content += '<h1><br></h1>'
    content += '<div class="col-sm-1 text-center">'
    content += '</div>'
    content += '<div class="col-sm-4 text-center">'
    content += '<ul class="list-group">'
    content += '<li class="list-group-item" style="background:#000;background:rgba(255,255,255,0.0);border: none;">'
    content += '<div>'
    content += '<form class="form-signin" action="/add_room/{}/{}/{}" method="post">'.format(str(user_home[0]), str(user[0]), str(active_room), str(performance))
    content += '<div class="row">'
    content += '<select class="form-control m-3" id="room_type" name="Nom" placeholder="Type de la pièce">'
    for p in piece_type:
        content += '<option class="text-center" value="{}">{}</option>'.format(p, p)
    content += '</select>'
    content += '</div>'
    content += '<br>'
    content += '<div class="row">'
    content += '<div><input name="Nomf" id="room_name" class="form-control" placeholder="Nom de la pièce à ajouter" required autofocus></div>'
    content += '<br>'
    content += '<button class="btn btn-lg btn-primary btn-block" type="submit">Ajouter une pièce</button>'
    content += '</div>'
    content += '</form>'
    content += '</div>'
    content += '</li>'
    content += '</ul>'
    content += '</div>'

    content += '<div class="col-sm-6 text-center">'
    content += '<ul class="list-group">'
    content += '<li class="list-group-item" style="background:#000;background:none;border: none;">'
    content += '<div>'
    content += '<form class="form-signin" action="/add_plant/{}/{}/{}" method="post">'.format(str(user_home[0]), str(user[0]), str(active_room), str(performance))
    content += '<div class="row">'
    content += '<div class="col-sm-6 text-center">'
    content += '<label class="mt-2" for="plant_name">Nom de la plante</label>'
    content += '<select class="form-control m-3" id="plant_name" name="plant_id" placeholder="Nom de la plante">'
    for p in reference_plant_list:
        content += '<option class="text-center" value="{}">{}</option>'.format(p[0], p[1])
    content += '</select>'
    content += '</div>'
    content += '<div class="col-sm-6 text-center">'
    #content += '<label class="mt-2" for="kit_name">Nom du kit</label>'
    #content += '<select class="form-control m-3" id="kit_name" name="kit_id" placeholder="Nom du kit">'
    content += '<label class="mt-2" for="module_reference">Référence du kit</label>'
    content += '<div><input class="form-control m-3" id="module_reference" name="module_reference" placeholder="Numéro affiché sur votre module" required autofocus></div>'

    #for p in kitreference_list:
    #    content += '<option class="text-center" value="{}">{}</option>'.format(p[0], p[1])
    #content += '</select>'
    content += '</div>'
    content += '</div>'
    content += '<div class="row">'
    content += '<div class="col-sm-6 text-center">'
    content += '<label class="mt-2" for="room_name">Pièce où est la plante</label>'
    content += '<select class="form-control m-3" id="room_name" name="room_id" placeholder="Type de la pièce">'
    for p in user_room:
        content += '<option class="text-center" value="{}">{}</option>'.format(p[0], p[1])
    content += '</select>'
    content += '</div>'
    content += '<div class="col-sm-6 text-center">'
    content += '<br>'
    content += '<button class="btn btn-lg btn-primary btn-block" type="submit">Ajouter une plante</button>'
    content += '</div>'
    content += '</div>'
    content += '</form>'
    content += '</div>'
    content += '</li>'
    content += '</ul>'
    content += '</div>'
    content += '</div>'


    content += '</div>'
    content += '<div class="col-sm-1 text-center">'
    content += '</div>'

    content += '</div>'
    content += '</div>'


    content += '<div class="row content">'
    content += '<div class="col-sm-12 text-center">'
    content += '<h1><br><br><br></h1>'
    content += '<div class="row content">'
    content += '<div class="col-sm-6 text-center">'
    content += '<div class="row content">'
    content += '<h1 class="text-center">Mes pièces</h1>'
    content += '</div>'
    content += '<div class="row content text-center">'
    if len(user_room) == 0:
        content += '<div class="row content">'
        content += '<p></p>'
        content += '</div>'
        ontent += '<div class="col-sm-12" style="background:white;">'
        content += '<h4><br><br> Aucune pièce dans le logement !<br> Vous pouvez en ajouter une !<br><br></h4>'
        content += '</div>'
    else :
        i = 0
        for r in user_room:
            if i == 0:
                content += '<div class="row content">'
                content += '<p></p>'
                content += '</div>'
                content += '<div class="row content">'

            content += '<div class="col-sm-6" style="background:white;">'
            content += '<div class="col-sm-2" style="border: solid #555;">'
            content += '<img src="{}" class="img-fluid" alt="Responsive image" width="65" height="65">'.format(get_room_image(r[1]))
            content += '</div>'
            content += '<div class="col-sm-10 text-center">'
            content += '<p><br>{}</p>'.format(r[1])
            content += '</div>'
            content += '</div>'
            i += 1
            if i == 2:
                content += '</div>'
                i = 0
        if i != 0:
            content += '</div>'
    content += '</div>'
    content += '</div>'
    content += '<div class="col-sm-6 text-center">'
    content += '<div class="row content">'
    content += '<h1 class="text-center">Mes plantes</h1>'
    content += '</div>'
    content += '<div class="row content">'
    content += '<div class="col-sm-1 text-center">'

    content += '</div>'
    content += '<div class="col-sm-11 text-center">'
    if len(user_plant) == 0:
        content += '<div class="row content">'
        content += '<p></p>'
        content += '</div>'
        content += '<div class="col-sm-12" style="background:white;">'
        content += '<h4><br><br> Aucune plante dans le logement !<br> Vous pouvez en ajouter une !<br><br></h4>'
        content += '</div>'
    else :
        for p in user_plant:
            content += '<div class="row content">'
            content += '<p></p>'
            content += '</div>'
            content += '<div class="row content" style="background:white;>'
            nom = ''
            origin = ''
            room = ''
            img_url = ''
            kit = ''
            date = str(p[-1])
            for p_r in reference_plant_list:
                if p[1] == p_r[0]:
                    nom = p_r[1]
                    origin = p_r[2]
                    img_url = p_r[7]
            for r in user_room:
                if p[2] == r[0]:
                    room = r[1]
            for k in kitreference_list:
                if p[3] == k[0]:
                    print("kit trouvé")
                    kit = k[1]

            content += '<div class="col-sm-12" style="background:white;">'
            content += '<div class="row content text-left">'
            content += '<div class="col-sm-12" style="background:white;">'
            content += '<ul><p><b>{}</b><br><br></p></ul>'.format(nom)
            content += '</div>'
            content += '</div>'
            content += '<div class="row content" style="background:white;">'
            content += '<div class="col-sm-7" style="background:white;">'
            content += '<ul><p class="text-left">Origine : {}<br>Piece : {}<br>Kit : {}<br>Date d\'ajout : {}</p></ul>'.format(origin, room, kit, date)
            content += '</div>'
            content += '<div class="col-sm-4" style="background:white;">'
            content += '<img src="{}" class="img-fluid" alt="Responsive image" width="65" height="65">'.format(img_url)
            content += '</div>'
            content += '</div>'
            content += '</div>'

    content += '</div>'

    content += '</div>'
    content += '</div>'
    content += '</div>'
    content += '</div>'
    content += '</div>'

    content += '</div>'
    content += html_end
    return content

#permet d'ajouter une piece lors de la creation d'un compte
def create_account_add_rooms():
    global room_t
    global NumberOfRooms_t
    content = ''
    destination_final = ''
    f = open('site/header_create_account.html', 'r')
    content = f.read()
    f.close()

    content += '<div class="col-sm-12">'
    content += '<h1 class="h3 mb-3 font-weight-normal">Indiquez les pièces du logement</h1>'
    if len(room_t) != 0:
        for p in room_t:
            content += '<div class="container-fluid text-center"><div class="row content">'
            content += '<div class="col-sm-2 sidenav">'
            content += icone_3_traits
            content += '</div>'
            content += '<div class="col-sm-8 text-left">'
            content += '<h4>{}</h4>'.format(p)
            content += '</div></div></div>'

    for p in piece_type :
        content += '<div class="row text-center">\n'
        content += '<div class="col-sm-4">'
        content += '</div>'
        content += '<div id = "icone"  class="col-sm-4">'
        content += '<div class="dropdown">\n'
        content += '<button id = "icone" class="btn btn-default dropdown-toggle input-block-level" type="button" data-toggle="dropdown">'
        content += '<h4>{}</h4>'.format(p)
        content += '\n<span class="caret"></span></button>'
        content += '<iframe id="invisible" name="invisible" style="display:none;"></iframe>'
        content += '<div class="dropdown-menu center">'
        if len(room_t) == int(NumberOfRooms_t) - 1:
            content += '<form class="form-signin" action="/end_config" method="post">'
        else :
            content += '<form class="form-signin" action="/add_next_room_config" method="post">'
        content += '<div><input name="Nom" id="Nom" value="{}" readonly="readonly" class="form-control" hidden></div>'.format(p)
        content += '<div><input name="Nomf" id="Nomf" class="form-control" placeholder="Nommer cette pièce" required autofocus></div>'
        content += '<div> <button type="submit" class="btn btn-secondary ">Ajouter une pièce</button></div></form>'
        content += '</div></div></div></div>'
        content += '<div class="col-sm-4">'
        content += '</div>'
    content += '</div>'
    content += '<div class="col-sm-12">'
    content += '<progress id="prog" max="100" value="100"> 100% </progress>'
    pourcentage = 100 * (len(room_t) + 1) / int(NumberOfRooms_t)
    content += '<progress id="prog" max="100" value="{}"> {}% </progress>'.format(str(pourcentage), str(pourcentage))
    content += '</div>'
    content += '<footer class="container-fluid text-center">'
    content += '<p class="mt-5 mb-3 text-muted">&copy; 2021 JeunePousse</p>'
    content += '</footer>'
    content += '</div>'
    content += html_end
    return content

def add_nav_bar_root(activ_num):
    content = '<nav class="navbar navbar-inverse"><div class="container-fluid"><div class="navbar-header"><a class="navbar-brand">Jeune Pousse Root</a></div><ul class="nav navbar-nav">'
    if activ_num == 1:
        content += '<li class="active"><a href="/root_home">homes</a></li>'
    else :
        content += '<li><a href="/root_home">homes</a></li>'
    if activ_num == 2:
        content += '<li class="active"><a href="/root_room">rooms</a></li>'
    else :
        content += '<li><a href="/root_room">rooms</a></li>'
    if activ_num == 3:
        content += '<li class="active"><a href="/root_user">users</a></li>'
    else :
        content += '<li><a href="/root_user">users</a></li>'
    if activ_num == 4:
        content += '<li class="active"><a href="/root_plant">plants</a></li>'
    else :
        content += '<li><a href="/root_plant">plants</a></li>'
    if activ_num == 5:
        content += '<li class="active"><a href="/root_kit">kits</a></li>'
    else :
        content += '<li><a href="/root_kit">kits</a></li>'
    if activ_num == 6:
        content += '<li class="active"><a href="/root_user_plant">modules</a></li>'
    else :
        content += '<li><a href="/root_user_plant">modules</a></li>'
    if activ_num == 7:
        content += '<li class="active"><a href="/root_user_capt">capteurs</a></li>'
    else :
        content += '<li><a href="/root_user_capt">capteurs</a></li>'
    content += '</ul>'
    content += '<ul class="nav navbar-nav navbar-right"><li><a href="/home"><span class="glyphicon glyphicon-user"></span> Root Log Out</a></li></ul>'
    content += '</div>\n</nav>'
    return content

def root_access(type_to_display, home_list, user_list, room_list, plant_list, kit_list, user_plant_list, user_sensor_list):

    #content = html_start #ajout DOCTYPE html lang title meta head
    #content += html_body
    f = open('site/root_header.html', 'r')
    content = f.read()
    f.close()
    legend = []
    data = []

    if(type_to_display == '/root_home'):
        content += add_nav_bar_root(1)
        legend = bdd_home_fields
        for d in home_list:
            data.append([d[0], d[1] + " " + d[2] + ", " + d[3] + ", " + d[4] + ", " + d[5], d[6], str(d[7]), d[8], ""])
    elif type_to_display == '/root_room':
        content += add_nav_bar_root(2)
        legend = bdd_room_fields
        for d in room_list:
            data.append(["", d[0], d[1], d[2], d[3], ""])
    elif type_to_display == '/root_user':
        content += add_nav_bar_root(3)
        legend = bdd_user_fields
        for d in user_list:
            data.append([d[0], d[1], d[2], d[3], d[4], d[6]])
    elif type_to_display == '/root_plant':
        content += add_nav_bar_root(4)
        legend = bdd_plant_fields
        for d in plant_list:
            data.append([d[1], d[2], d[3], d[4], d[5], d[6]])
    elif type_to_display == '/root_kit':
        content += add_nav_bar_root(5)
        legend = bdd_kit_fields
        for d in kit_list:
            data.append([d[1], d[2], d[3], d[4]])
    elif type_to_display == '/root_user_plant':
        content += add_nav_bar_root(6)
        legend = bdd_user_plant_fields
        for d in user_plant_list:
            data.append([d[0], d[1], d[2], d[4], d[5], d[6]])
    elif type_to_display == '/root_user_capt':
        content += add_nav_bar_root(7)
        legend = bdd_user_capt
        for d in user_sensor_list:
            data.append(["", d[1], d[2], d[3], d[4], ""])

    if(type_to_display == '/root_kit'):
        content += '<div class="row">'
        content += '<div class="col-sm-12">'
        content += '<form class="form-signin" action="/root_add_kit" method="post">'
        content += '<h1 class="h3 mb-3 font-weight-normal">ROOT ACCESS : ajouter un kit</h1>'
        content += '<label for="Name" class="sr-only">Name</label>'
        content += '<input id="Name" name="Name" class="form-control" placeholder="Name" required autofocus>'
        content += '<h4>Rensigner la liste des capteurs et actionneurs composants le kit de la sorte : \'capteur,capteur,....\'</h4>'
        content += '<label for="SensorAction" class="sr-only">Capteurs & Actionneurs</label>'
        content += '<input id="SensorAction" name="SensorAction" class="form-control" placeholder="Capteurs & Actionneurs" required autofocus>'
        content += '<h4>Rensigner la liste des unités de chaque capteur/actionneur (attention à l\'ordre) de la sorte : \'unite,unite,....\'</h4>'
        content += '<label for="Units" class="sr-only">Units</label>'
        content += '<input id="Units" name="Units" class="form-control" placeholder="Units" required autofocus>'
        content += '<button class="btn btn-secondary btn-lg btn-block" type="submit">Ajouter le kit</button>'
        content += '</form>'
        content += '</div>'
        content += '</div>'
    if(type_to_display == '/root_user_plant'):
        print('test ajout plante')
        content += '<div class="row">'
        content += '<div class="col-sm-12">'
        content += '<form class="form-signin" action="/kit_connexion" method="post">'
        content += '<h1 class="h3 mb-3 font-weight-normal">ROOT ACCESS : ajouter un module</h1>'
        content += '<label for="Reference" class="sr-only">Reference</label>'
        content += '<input id="Reference" name="Reference" class="form-control" placeholder="Reference" required autofocus>'
        content += '<label for="kit_name" class="sr-only">Nom du kit</label>'
        content += '<input id="kit_name" name="kit_name" class="form-control" placeholder="Nom du kit" required autofocus>'
        content += '<button class="btn btn-secondary btn-lg btn-block" type="submit">Ajouter le kit</button>'
        content += '</form>'
        content += '</div>'
        content += '</div>'
        print(user_plant_list)
    if type_to_display == '/root_plant':
        content += '<div class="row">'
        content += '<div class="col-sm-12">'
        content += '<form class="form-signin" action="/root_add_plant" method="post">'
        content += '<h1 class="h3 mb-3 font-weight-normal">ROOT ACCESS : ajouter une référence de plante</h1>'
        content += '<label for="Name" class="sr-only">Name</label>'
        content += '<input id="Name" name="Name" class="form-control" placeholder="Name" required autofocus>'
        content += '<label for="Origin" class="sr-only">Origine</label>'
        content += '<input id="Origin" name="Origin" class="form-control" placeholder="Origine" required autofocus>'
        content += '<label for="Temperature" class="sr-only">Temperature</label>'
        content += '<input id="Temperature" name="Temperature" class="form-control" placeholder="Temperature" required autofocus>'
        content += '<label for="Humidity" class="sr-only">Humidity</label>'
        content += '<input id="Humidity" name="Humidity" class="form-control" placeholder="Humidity" required autofocus>'
        content += '<label for="Luminosity" class="sr-only">Luminosity</label>'
        content += '<input id="Luminosity" name="Luminosity" class="form-control" placeholder="Luminosity" required autofocus>'
        content += '<label for="GroundQuality" class="sr-only">Ground quality</label>'
        content += '<input id="GroundQuality" name="GroundQuality" class="form-control" placeholder="Ground quality" required autofocus>'
        content += '<label for="PictureUrl" class="sr-only">Plant picture URL</label>'
        content += '<input id="PictureUrl" name="PictureUrl" class="form-control" placeholder="Plant picture URL" required autofocus>'

        content += '<button class="btn btn-secondary btn-lg btn-block" type="submit">Ajouter la plante</button>'
        content += '</form>'
        content += '</div>'
        content += '</div>'

    content += '<div class="container">'
    content += '<div class="row">'

    if type_to_display == '/root_kit':
        content += '<div class="col-sm-2 border">'
        content += '<h3 class="bg-light border">'
        content += legend[0]
        content += '</h3>'
        content += '</div>'
        content += '<div class="col-sm-4 border">'
        content += '<h3 class="bg-light border">'
        content += legend[1]
        content += '</h3>'
        content += '</div>'
        content += '<div class="col-sm-4 border">'
        content += '<h3 class="bg-light border">'
        content += legend[2]
        content += '</h3>'
        content += '</div>'
        content += '<div class="col-sm-2 border">'
        content += '<h3 class="bg-light border">'
        content += legend[3]
        content += '</h3>'
        content += '</div>'
    else :
        for l in legend:
            content += '<div class="col-sm-2 border">'
            content += '<h3 class="bg-light border">'
            content += l
            content += '</h3>'
            content += '</div>'
    content += '</div>'

    for d in data:
        content += '<div class="row">'
        if type_to_display == '/root_kit':
            content += '<div class="col-sm-2 border">'
            content += '<p class="bg-light border">'
            content += d[0]
            content += '</p>'
            content += '</div>'
            content += '<div class="col-sm-4 border">'
            content += '<p class="bg-light border">'
            content += d[1]
            content += '</p>'
            content += '</div>'
            content += '<div class="col-sm-4 border">'
            content += '<p class="bg-light border">'
            content += d[2]
            content += '</p>'
            content += '</div>'
            content += '<div class="col-sm-2 border">'
            content += '<p class="bg-light border">'
            content += d[3]
            content += '</p>'
            content += '</div>'
        else:
            for e in d:
                content += '<div class="col-sm-2 border">'
                content += '<p class="bg-light border">'
                content += str(e)
                content += '</p>'
                content += '</div>'
        content += '</div>'
    content += '</div>'

    content += html_end
    return content

def get_user(user_bdd, user_id):
    for u in user_bdd:
        if int(u[0]) == int(user_id):
            return u
    return []

def get_home(home_bdd, home_id):
    for u in home_bdd:
        if int(u[0]) == int(home_id):
            return u
    return []

def serve_on_port(port):
    #server = ThreadingHTTPServer(("localhost",port), MyHandler)
    #server.serve_forever()
    return

class MyHandler(http.server.BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.mysql = MySQL('../BDD/jeunepousse.db')
        super(MyHandler, self).__init__(*args, **kwargs)

    def do_GET(self):
        """Respond to a GET request."""
        res = urllib.parse.urlparse(self.path)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        content = ''
        #pour site web
        if(res.path == '/home'):
            f = open('site/identification.html', 'r')
            content = f.read()
            f.close()
        elif('/dashboard' in res.path):
            room_list = self.mysql.select('/room')
            user_list = self.mysql.select('/user')
            user_plant_list = self.mysql.select('/plant')
            sensor_list = self.mysql.select('/sensoraction')
            measure_list = self.mysql.select('/measure')
            home = self.mysql.select('/home')
            kitreference_list = self.mysql.select('/kitreference') #a supp
            reference_plant_list = self.mysql.select('/plantreference')
            split_path = self.path.lower().split("/")
            performance = split_path[-1]
            active_room = split_path[-2]
            user_t = split_path[-3]
            user = get_user(user_list, user_t)
            content = construct_dashboard(home, user, room_list, user_plant_list, kitreference_list, reference_plant_list, sensor_list, measure_list, performance, active_room)

        elif('/option' in res.path):
            room_list = self.mysql.select('/room')
            user_list = self.mysql.select('/user')
            user_plant_list = self.mysql.select('/plant')
            home = self.mysql.select('/home')
            kitreference_list = self.mysql.select('/kitreference')
            reference_plant_list = self.mysql.select('/plantreference')
            split_path = self.path.lower().split("/")
            performance = split_path[-1]
            active_room = split_path[-2]
            user_t = split_path[-3]
            user = get_user(user_list, user_t)
            content = construct_option_page(home, user, room_list, user_plant_list, kitreference_list, reference_plant_list, performance, active_room)

        elif '/root_' in res.path:
            room_list = self.mysql.select('/room')
            user_list = self.mysql.select('/user')
            plant_list = self.mysql.select('/plantreference')
            home_list = self.mysql.select('/home')
            kit_list = self.mysql.select('/kitreference')
            user_plant_list = self.mysql.select('/plant')
            user_sensor_list = self.mysql.select('/sensoraction')
            content = root_access(res.path, home_list, user_list, room_list, plant_list, kit_list, user_plant_list, user_sensor_list)

        if(content == ''):
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
        else:
            self.wfile.write(bytes(content, 'UTF-8'))

    def do_POST(self):
        """Respond to a POST request."""
        global AddNumber_t
        global Street_t
        global City_t
        global PostalCode_t
        global Country_t
        global Name_t
        global Email_t
        global Password_t
        global NumberOfRooms_t
        global room_t
        global ip_t
        global email_root
        global password_root
        data_type = ""

        content = ''
        res = urllib.parse.urlparse(self.path)
        print(res)
        if res.query != '':
            query = urllib.parse.parse_qs(res.query)
        elif self.path.lower() == "/root_add_kit":
            temp = self.rfile.read(int(self.headers['Content-Length']))
            data = dict(urllib.parse.parse_qs(temp.decode('UTF-8')))
            Name = "{}".format(data.get('Name')[0])
            SensorAction = "{}".format(data.get('SensorAction')[0])
            Units = "{}".format(data.get('Units')[0])
            kit_bdd = self.mysql.select('/kitreference')
            does_not_exist = True
            for e in kit_bdd:
                if Name == e[1]:
                    does_not_exist = False
            if does_not_exist:
                data = {'Name': [Name], 'SensoractionNames': [SensorAction], 'SensoractionUnits':[Units]}
                self.mysql.insert('/kitreference', data)
            room_list = self.mysql.select('/room')
            user_list = self.mysql.select('/user')
            plant_list = self.mysql.select('/plantreference')
            home_list = self.mysql.select('/home')
            kit_list = self.mysql.select('/kitreference')
            user_plant_list = self.mysql.select('/plant')
            user_sensor_list = self.mysql.select('/sensoraction')
            content = root_access('/root_add_kit', home_list, user_list, room_list, plant_list, kit_list, user_plant_list, user_sensor_list)
            self.send_response(REDIRECTION)

        elif self.path.lower() == "/root_add_plant":
            temp = self.rfile.read(int(self.headers['Content-Length']))
            data = dict(urllib.parse.parse_qs(temp.decode('UTF-8')))
            Name = "{}".format(data.get('Name')[0])
            Origin = "{}".format(data.get('Origin')[0])
            Temperature = "{}".format(data.get('Temperature')[0])
            Humidity = "{}".format(data.get('Humidity')[0])
            Luminosity = "{}".format(data.get('Luminosity')[0])
            GroundQuality = "{}".format(data.get('GroundQuality')[0])
            PictureUrl = "{}".format(data.get('PictureUrl')[0])
            kit_bdd = self.mysql.select('/plantreference')
            does_not_exist = True
            for e in kit_bdd:
                if Name == e[1]:
                    does_not_exist = False
            if does_not_exist:
                data = {'Name': [Name], 'Origin': [Origin], 'Temperature':[Temperature], 'Humidity': [Humidity], 'Luminosity': [Luminosity], 'GroundQuality':[GroundQuality], 'PictureUrl':[PictureUrl]}
                self.mysql.insert('/plantreference', data)
            room_list = self.mysql.select('/room')
            user_list = self.mysql.select('/user')
            plant_list = self.mysql.select('/plantreference')
            home_list = self.mysql.select('/home')
            kit_list = self.mysql.select('/kitreference')
            user_plant_list = self.mysql.select('/plant')
            user_sensor_list = self.mysql.select('/sensoraction')
            content = root_access('/root_user_plant', home_list, user_list, room_list, plant_list, kit_list, user_plant_list, user_sensor_list)
            self.send_response(REDIRECTION)

        elif self.path.lower() == "/connexion":
            table = self.mysql.select('/user')
            temp = self.rfile.read(int(self.headers['Content-Length']))
            data = dict(urllib.parse.parse_qs(temp.decode('UTF-8')))
            email = "{}".format(data.get('Email')[0])
            password = "{}".format(data.get('Password')[0])
            if (email == email_root) & (password == password_root):
                room_list = self.mysql.select('/room')
                user_list = self.mysql.select('/user')
                plant_list = self.mysql.select('/plant')
                home_list = self.mysql.select('/home')
                kit_list = self.mysql.select('/kitreference')
                user_plant_list = self.mysql.select('/plant')
                user_sensor_list = self.mysql.select('/sensoraction')
                content = root_access('/root_home', home_list, user_list, room_list, plant_list, kit_list, user_plant_list, user_sensor_list)
                self.send_response(REDIRECTION)
            else :
                user_not_found = True
                for user in table:
                    if (user[2] == email) & (user[3] == password):
                        user_not_found = False
                        room_list = self.mysql.select('/room')
                        user_plant_list = self.mysql.select('/plant')
                        sensor_list = self.mysql.select('/sensoraction')
                        measure_list = self.mysql.select('/measure')
                        home = self.mysql.select('/home')
                        kitreference_list = self.mysql.select('/kitreference') #a supp
                        reference_plant_list = self.mysql.select('/plantreference')
                        performance = '1'
                        active_room = '1'
                        content = construct_dashboard(home, user, room_list, user_plant_list, kitreference_list, reference_plant_list, sensor_list, measure_list, performance, active_room)
                        #content = construct_option_page(home, user, room_list, user_plant_list, kitreference_list, reference_plant_list, performance)
                        self.send_response(REDIRECTION)
                if user_not_found:
                    f = open('site/identification.html', 'r')
                    content = f.read()
                    f.close()
                    self.send_response(REDIRECTION)

        elif self.path.lower() == "/option":
            table = self.mysql.select('/user')
            temp = self.rfile.read(int(self.headers['Content-Length']))
            data = dict(urllib.parse.parse_qs(temp.decode('UTF-8')))
            room_list = self.mysql.select('/room')
            user_list = self.mysql.select('/user')
            user_plant_list = self.mysql.select('/plant')
            home = self.mysql.select('/home')
            kitreference_list = self.mysql.select('/kitreference')
            reference_plant_list = self.mysql.select('/plantreference')
            performance = '1'
            active_room = '1'
            content = construct_option_page(home, user_list, room_list, user_plant_list, kitreference_list, reference_plant_list, performance, active_room)
            self.send_response(REDIRECTION)

        elif self.path.lower() == "/add_account":
            temp = self.rfile.read(int(self.headers['Content-Length']))
            data = dict(urllib.parse.parse_qs(temp.decode('UTF-8')))
            AddNumber_t = "{}".format(data.get('AddNumber')[0])
            Street_t = "{}".format(data.get('Street')[0])
            City_t = "{}".format(data.get('City')[0])
            PostalCode_t = "{}".format(data.get('PostalCode')[0])
            Country_t = "{}".format(data.get('Country')[0])
            f = open('site/ajout_compte.html', 'r')
            content = f.read()
            f.close()
            self.send_response(REDIRECTION)

        elif self.path.lower() == "/add_room_config":
            temp = self.rfile.read(int(self.headers['Content-Length']))
            data = dict(urllib.parse.parse_qs(temp.decode('UTF-8')))
            Name_t = "{}".format(data.get('Name')[0])
            Email_t = "{}".format(data.get('Email')[0])
            Password_t = "{}".format(data.get('Password')[0])
            NumberOfRooms_t = "{}".format(data.get('NumberOfRooms')[0])
            content = create_account_add_rooms()
            self.send_response(REDIRECTION)

        elif self.path.lower() == "/add_next_room_config":
            temp = self.rfile.read(int(self.headers['Content-Length']))
            data = dict(urllib.parse.parse_qs(temp.decode('UTF-8')))
            Nom = "{}".format(data.get('Nom')[0])
            Nomf = "{}".format(data.get('Nomf')[0])
            Name = Nom + " " + Nomf
            if(Name not in room_t):
                room_t.append(Name)
            content = create_account_add_rooms()
            self.send_response(REDIRECTION)

        elif self.path.lower() == "/end_config":
            temp = self.rfile.read(int(self.headers['Content-Length']))
            data = dict(urllib.parse.parse_qs(temp.decode('UTF-8')))
            Nom = "{}".format(data.get('Nom')[0])
            Nomf = "{}".format(data.get('Nomf')[0])
            Name = Nom + " " + Nomf
            if(Name not in room_t):
                room_t.append(Name)
                ip_t = self.client_address[0]
                #on ajoute le logement (on est sur qu'il n'existe pas dans la bdd)
                home = {'AddressNumber':[AddNumber_t], 'Street': [Street_t], 'City': [City_t], 'PostalCode': [PostalCode_t], 'Country': [Country_t], 'Ip':[ip_t], 'NumberOfRooms':[NumberOfRooms_t]}
                self.mysql.insert('/home', home)
                home_bdd = self.mysql.select('/home')
                home_id = -1
                for h in home_bdd:
                    if (h[1] == AddNumber_t) & (h[2] == Street_t) & (h[3] == City_t) & (h[4] == PostalCode_t) & (h[5] == Country_t):
                        id = h[0]
                if id == -1:
                    print('Error !!!!')
                user = {'Name': [Name_t], 'Email':[Email_t], 'Password':[Password_t], 'HomeReference': [id]}
                self.mysql.insert('/user', user)
                user_list = self.mysql.select('/user')
                user = user_list[-1]
                for r in room_t:
                    room = {'Name': [r], 'HomeReference':[id]}
                    self.mysql.insert('/room', room)
                #home
                AddNumber_t = ""
                Street_t = ""
                City_t = ""
                PostalCode_t = ""
                Country_t = ""
                NumberOfRooms_t = ""
                ip_t = ""
                #user
                Name_t = ""
                Email_t = ""
                Password_t = ""
                #room
                room_t = []
                room_list = self.mysql.select('/room')
                user_plant_list = self.mysql.select('/plant')
                sensor_list = self.mysql.select('/sensoraction')
                measure_list = self.mysql.select('/measure')
                home = self.mysql.select('/home')
                kitreference_list = self.mysql.select('/kitreference') #a supp
                reference_plant_list = self.mysql.select('/plantreference')
                performance = '1'
                active_room = '1'
                content = construct_dashboard(home, user, room_list, user_plant_list, kitreference_list, reference_plant_list, sensor_list, measure_list, performance, active_room)
                #content = construct_option_page(home, user, room_list, user_plant_list, kitreference_list, reference_plant_list, performance)
                self.send_response(REDIRECTION)

            else :
                content = create_account_add_rooms()
            self.send_response(REDIRECTION)

        elif "/performance_mode" in self.path.lower():
            print( self.path.lower())
            temp = self.rfile.read(int(self.headers['Content-Length']))
            data = dict(urllib.parse.parse_qs(temp.decode('UTF-8')))

            split_path = self.path.lower().split("/")
            active_room = split_path[-2]
            user_t = split_path[-3]
            HomeReference = split_path[-4]

            performance = "{}".format(data.get('performance')[0])
            user_bdd = self.mysql.select('/user')
            user = get_user(user_bdd, user_t)


            room_list = self.mysql.select('/room')
            user_plant_list = self.mysql.select('/plant')
            reference_plant_list = self.mysql.select('/plantreference')
            for r in room_list:
                if int(r[2]) == int(HomeReference):
                    for p in user_plant_list:
                        if p[2] == r[0]:
                            self.mysql.update("plant", "Performance", performance, str(p[0]) ) #on met a jour le mode

            home = self.mysql.select('/home')
            kitreference_list = self.mysql.select('/kitreference')
            content = construct_option_page(home, user, room_list, user_plant_list, kitreference_list, reference_plant_list, performance, active_room)
            self.send_response(REDIRECTION)


        elif "/add_plant" in self.path.lower():
            print( self.path.lower())
            temp = self.rfile.read(int(self.headers['Content-Length']))
            data = dict(urllib.parse.parse_qs(temp.decode('UTF-8')))

            split_path = self.path.lower().split("/")

            performance = split_path[-1]
            active_room = split_path[-2]
            user_t = split_path[-3]

            room_id = "{}".format(data.get('room_id')[0])
            module_reference = "{}".format(data.get('module_reference')[0])
            plant_id = "{}".format(data.get('plant_id')[0])

            user_plant_list = self.mysql.select('/plant')
            for p in user_plant_list:
                if p[5] == module_reference: #reference du module
                    self.mysql.update("plant", "PlantReference", str(plant_id), str(p[0]) )
                    self.mysql.update("plant", "RoomReference", str(room_id), str(p[0]) )
                    self.mysql.update("plant", "Performance", '1', str(p[0]) ) #on met a jour le mode

            user_bdd = self.mysql.select('/user')
            user = get_user(user_bdd, user_t)
            room_list = self.mysql.select('/room')
            user_plant_list = self.mysql.select('/plant')
            home = self.mysql.select('/home')
            reference_plant_list = self.mysql.select('/plantreference')
            kitreference_list = self.mysql.select('/kitreference')

            content = construct_option_page(home, user, room_list, user_plant_list, kitreference_list, reference_plant_list, performance, active_room)
            self.send_response(REDIRECTION)

        elif "/add_room" in self.path.lower():
            temp = self.rfile.read(int(self.headers['Content-Length']))
            data = dict(urllib.parse.parse_qs(temp.decode('UTF-8')))

            split_path = self.path.lower().split("/")
            performance = split_path[-1]
            active_room = split_path[-2]
            user_t = split_path[-3]

            Nom = "{}".format(data.get('Nom')[0])
            Nomf = "{}".format(data.get('Nomf')[0])
            Name = Nom + " " + Nomf
            HomeReference = split_path[-3]
            room = {'Name': [Name], 'HomeReference':[HomeReference]}

            user_bdd = self.mysql.select('/user')
            room_bdd = self.mysql.select('/room')

            user = get_user(user_bdd, user_t)

            not_in_room = True
            for r in room_bdd:
                if (int(r[2]) == int(HomeReference)) & (r[1] == Name):
                    not_in_room = False
            if not_in_room:
                self.mysql.insert('/room', room)
            room_list = self.mysql.select('/room')
            user_plant_list = self.mysql.select('/plant')
            home = self.mysql.select('/home')
            kitreference_list = self.mysql.select('/kitreference')
            reference_plant_list = self.mysql.select('/plantreference')
            performance = split_path[-1]
            content = construct_option_page(home, user, room_list, user_plant_list, kitreference_list, reference_plant_list, performance, active_room)
            self.send_response(REDIRECTION)

        elif "/kit_connexion" == self.path.lower():
            print("Serveur kit connexion")

            # data = dict(urllib.parse.parse_qs(temp.decode('UTF-8')))
            q = self.rfile.read(int(self.headers['content-length'])).decode(encoding="utf-8")
            query = urllib.parse.parse_qs(q,keep_blank_values=1,encoding='utf-8')

            #print(q)
            # data = query[''] #TODO
            #data = json.loads(q)
            #temporary_reference = data['Reference']
            #nom_du_kit = data['kit_name']

            obj = json.loads(q)
            temporary_reference = obj['Reference']
            nom_du_kit = obj['kit_name']

            print("Temporary reference :")
            print(temporary_reference)

            print("Nom kit :")
            print(nom_du_kit)

            user_plant_list = self.mysql.select('/plant')

            already_in_database = False
            portCOM = 0
            capteurs = []
            for p in user_plant_list:
                if p[5] == temporary_reference:
                    portCOM = int(p[4])
            if portCOM == 0 :
                if len(user_plant_list) > 0:
                    last_p = user_plant_list[-1]
                    portCOM = int(last_p[4]) + 10
                else :
                    portCOM = 8890
                kitreference_list = self.mysql.select('/kitreference')
                kit_id = ''
                for k in kitreference_list:
                    if k[1] == nom_du_kit:
                        kit_id = k[0]
                if kit_id != '':
                    plant = {'PlantReference': ['-1'], 'RoomReference': ['-1'], 'KitReference': [kit_id], 'PortCOM': [str(portCOM)], 'ReferenceProductNumber': [temporary_reference], 'Performance': ['-1']}
                    self.mysql.insert('/plant', plant)
                    plant_id = len(self.mysql.select('/plant'))

                    kitreference_list = self.mysql.select('/kitreference')

                    for k in kitreference_list:
                        #if k[0] == p[3]: #kit de la plante
                        capteurs_comma = k[2]
                        unites_comma = k[3]
                        #on retire les virgules
                        capteurs = capteurs_comma.split(",")
                        unites = unites_comma.split(",")
                        print("CAPTEURS !!!!")
                        print(capteurs)
                        #on cree les capteurs
                        i = 0
                        for c in capteurs:
                            unit_ = unites[i]
                            capteur = {'Name': [c], 'Unit': [unit_], 'PlantReference': [str(plant_id)]}
                            capt = self.mysql.select('/sensoraction')
                            sensor_already_add = False
                            for ca in capt:
                                if (ca[1] == c) & (ca[2] == unit_) & (ca[3] == str(plant_id)):
                                    sensor_already_add = True
                            if not sensor_already_add:
                                self.mysql.insert('/sensoraction', capteur)
                            i += 1
                        #on cree un thread pour ecouter sur ce port
                        threading.Thread(target=serve_on_port, args=[portCOM]).start()

                else :
                    portCOM = -1

            obj['PortCOM'] = str(portCOM)

            data_type = "json"
            content = obj


        elif "/add_measure" == self.path.lower():
            q = self.rfile.read(int(self.headers['content-length'])).decode(encoding="utf-8")
            query = urllib.parse.parse_qs(q,keep_blank_values=1,encoding='utf-8')

            obj = json.loads(q)
            print(obj)

            # obj = query[''] #TODO
            Reference = obj['Reference']
            Temperature = obj['Temperature']
            Humidity = obj['Humidity']
            GroundQuality = obj['GroundQuality']
            WaterLevel = obj['WaterLevel']
            print(Reference)
            print(Temperature)
            print(Humidity)
            print(GroundQuality)
            print(WaterLevel)
            print("-----------------------------------")

            plants = self.mysql.select('/plant')
            reference_plant_list = self.mysql.select('/plantreference')
            sensors = self.mysql.select('/sensoraction')

            for p in plants:
                if p[-3] == Reference: #on a trouve la plante
                   print("Référence trouvée")
                   performance = p[-2]
                   temperature_ref = 0.0
                   humidity_ref = 0.0
                   luminosity_ref = 0.0
                   groundquality_ref = 0.0
                   light_ref = 0
                   water_level_ref = 1
                   irrigation_score = 0
                   for p_r in reference_plant_list:
                    if p[1] == p_r[0]:
                          temperature_ref = float(p_r[3])
                          humidity_ref = float(p_r[4])
                          luminosity_ref = float(p_r[5])
                          groundquality_ref = float(p_r[6])
                   if (performance == '1'): #mode performance
                    delay = 30000 #ms = 30s
                    ratio_temp = float(Temperature) / temperature_ref
                    if ( ratio_temp < 0.8 ): #trop froid
                        temperature_ref = -1
                    elif ratio_temp > 1.2 : #trop chaud
                        temperature_ref = 1
                    else :
                        temperature_ref = 0 #bonne temperature
                    ratio_hum = float(Humidity) / humidity_ref
                    if ratio_hum < 0.85: #trop sec
                        humidity_ref = -1
                        irrigation_score = 1
                        if ratio_hum < 0.5:
                            irrigation_score += 1
                    elif ratio_hum > 1.25 : #trop humide
                        humidity_ref = 1
                    else :
                        humidity_ref = 0 #bonne humiditee
                    ratio_hum_sol = float(GroundQuality) / groundquality_ref
                    if ratio_hum_sol < 0.7: #sol trop sec
                        groundquality_ref = -1
                        irrigation_score += 1
                        if ratio_hum < 0.6:
                            irrigation_score += 1
                            if ratio_hum < 0.3:
                                irrigation_score += 1
                    elif ratio_hum_sol > 1.5 : #sol trop humide
                        groundquality_ref = 1
                    else :
                        groundquality_ref = 0 #bonne humiditee du sol
                    light_ref = 0
                    heure = dt.datetime.now().hour
                    if (heure > 6) & (heure < 20):
                        light_ref = 1
                    if WaterLevel < 20:
                        water_level_ref = 0 #attention, surveiller le niveau d'eau
                    elif WaterLevel < 5:
                        water_level_ref = -1 #urgent, rservoir quasi vide
                   else : #mode vacance
                    delay = 60000 #ms = 1min

                   obj['mode'] = int(performance), #1 performance, 0 vacances
                   obj['delay'] = delay,
                   obj['temp_indicator'] = temperature_ref,
                   obj['hum_indicator'] = humidity_ref,
                   obj['lum_indicator'] = luminosity_ref,
                   obj['grnd_indicator'] = groundquality_ref,
                   obj['water_indicator'] = water_level_ref,
                   obj['light_power'] = light_ref,
                   obj['irrig_score'] = irrigation_score

                   #on ajoute les mesures dans la bdd
                   for s in sensors:
                       if s[3] == p[0]:
                           print("Capteur trouvé !")
                           print(Reference)
                           print(Temperature)
                           print(Humidity)
                           print(GroundQuality)
                           print(WaterLevel)
                           print("-----------------------------------")
                           if s[1] == 'Temperature':
                               print("Capteur Temperature")
                               mesure = {'Value': [str(Temperature)], 'SensoractionReference': [str(s[0])]}
                               print(mesure)
                               self.mysql.insert('/measure', mesure)
                           if s[1] == 'Humidity':
                               print("Capteur Humidity")
                               mesure = {'Value': [str(Humidity)], 'SensoractionReference': [str(s[0])]}
                               self.mysql.insert('/measure', mesure)
                           if s[1] == 'GroundQuality':
                               print("Capteur GroundQuality")
                               mesure = {'Value': [str(GroundQuality)], 'SensoractionReference': [str(s[0])]}
                               self.mysql.insert('/measure', mesure)
                           if s[1] == 'WaterLevel':
                               print("Capteur WaterLevel")
                               mesure = {'Value': [str(WaterLevel)], 'SensoractionReference': [str(s[0])]}
                               self.mysql.insert('/measure', mesure)
                           if s[1] == 'Light':
                               print("Capteur Light")
                               mesure = {'Value': [str(Light)], 'SensoractionReference': [str(s[0])]}
                               self.mysql.insert('/measure', mesure)

            data_type = "json"
            content = obj

        if content == '': #compte non trouve
            self.send_response(REDIRECTION)
            self.send_header('Location', '/')
            self.end_headers()

        elif data_type == "json":
            self.send_response(200)
            # body = str(content).encode("utf8")
            self.send_header("Content-type", "application/json")
            #self.send_header("Content-Length", len(content))
            self.end_headers()
            body = json.dumps(content).encode("utf8")
            print(body)
            self.wfile.write(body)

        else :
            self.send_response(200)
            body = content.encode("utf8")
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
		#self.send_header("Content-type", "text/html")



class MySQL():
	def __init__(self, name):
		self.c = None
		self.req = None
		self.conn = sqlite3.connect(name)
		self.c = self.conn.cursor()

	def __exit__(self, exc_type, exc_value, traceback):
		self.conn.close()

	def select(self,path):
		elem = path.split('/')
		if len(elem) == 2:
			req = "select * from %s" %(elem[1])
		else:
			req = "select %s from %s where id=%s" %(elem[3],elem[1],elem[2])
		return self.c.execute(req).fetchall()

	def insert(self,path,query):
		attr = ', '.join(query.keys())
		val = ', '.join('"%s"' %v[0] for v in query.values())
		print(attr,val)
		req = "insert into %s (%s) values (%s)" %(path.split('/')[1], attr, val)
		print(req)
		self.c.execute(req)
		self.conn.commit()
	def update(self, nom_table, nom_colonne, valeur, condition_value):
		req = "update %s set %s = %s where id=%s"%(nom_table, nom_colonne, valeur, condition_value)
		self.c.execute(req)
		self.conn.commit()

class ThreadingHTTPServer (socketserver . ThreadingMixIn ,http . server . HTTPServer):
	pass

def serve_on_port(port_) :
    global port
    server = ThreadingHTTPServer (("", port_) , MyHandler)
    server.serve_forever()
    port.append(server)
    print("port OPEN")
    print(port_)

if __name__ == '__main__':
	# start_capteur_threads()
	#On ouvre un 4e thread pour toutes les autres requêtes
    threading.Thread(target=serve_on_port, args=[7777]).start()
    threading.Thread(target=serve_on_port, args=[8888]).start()
    print("Divers : 8888");
