import sys
from g_python.gextension import Extension
from g_python.hmessage import Direction, HMessage

extension_info = {
    "title": "RMimic",
    "description": ":rmimic x",
    "version": "2.0",
    "author": "Lande"
}

ext = Extension(extension_info, sys.argv)
ext.start()

def on_connection_start():
    print('Connected with: {}:{}'.format(ext.connection_info['host'], ext.connection_info['port']))
    if ext.harble_api: print("Harble API :" + ext.harble_api)
    else: print("No Harble API detected")
    print(space)

ext.on_event('connection_start', on_connection_start)


space = "-----------------------"
players = {}

def userjoin(message):

    nombre = message.packet.read_int()

    for i in range(nombre):
        message.packet.read_int()  # id entité
        pseudo = message.packet.read_string() # pseudo
        message.packet.read_string()  # humeur
        skin = message.packet.read_string()  # skin
        index = message.packet.read_int()  # index de l'entité dans la salle
        message.packet.read_int() # x
        message.packet.read_int() # y
        message.packet.read_string()  # z | La hauteur sous forme de string genre "2.5"
        message.packet.read_int()  # rotation
        typee = message.packet.read_int()  # type de l'entité

        if(typee == 1):
            genre = message.packet.read_string()

            players[index] = pseudo, skin, genre
            print(players[index][0], "join")
            print(players)
            print(space)
            
            message.packet.read_int()
            message.packet.read_int()
            message.packet.read_string()
            message.packet.read_string()
            message.packet.read_int()
            message.packet.read_bool()

        if(typee == 2):
            message.packet.read_int()
            message.packet.read_int()
            message.packet.read_string()
            message.packet.read_int()
            message.packet.read_bool()
            message.packet.read_int()
            message.packet.read_int()
            message.packet.read_string()
            message.packet.read_bool()

        if(typee == 4):
            message.packet.read_string()
            message.packet.read_int()
            message.packet.read_string()
            message.packet.read_int()
            message.packet.read_bool()
            message.packet.read_bool()
            message.packet.read_int()
            message.packet.read_int()


def leave(message):
    user = message.packet.read_string()
    index = int(user)
    
    if index in players:
        print(players[index][0], "leave")
        del players[index]
    print(players)
    print(space)


def clear_user(message):
    players.clear()
    print("room changed")


def change_skin(message):
    (index, skin, _, _, _) = message.packet.read("isssi")
    if index != -1:
        pseudo = players[index][0]
        genre = players[index][2]
        players[index] = pseudo, skin, genre
        print("skin changed | id: {}, pseudo: {}".format(index, players[index][0]))
        print(space)


def speech(message):
    (text, color, index) = message.packet.read('sii')
    if text.startswith(":rmimic"):
        message.is_blocked = True
        if players:
            name = text[8:]
            for j in players:
                if (players[j][0] == name):
                    look = players[j][1]
                    genre = players[j][2]
                    ext.send_to_server("{l}{h:2730}{s:\""+genre+"\"}{s:\""+look+"\"}")
                    ext.send_to_client("{l}{h:1446}{i:0}{s:\"Look changed to: "+name+"\"}{i:0}{i:1}{i:0}{i:0}")
                    break
            else: ext.send_to_client("{l}{h:1446}{i:0}{s:\"I don't found: "+name+"\"}{i:0}{i:1}{i:0}{i:0}")
        else: ext.send_to_client("{l}{h:1446}{i:0}{s:\"Pls reload the room\"}{i:0}{i:1}{i:0}{i:0}")


ext.intercept(Direction.TO_CLIENT, userjoin, 374)
ext.intercept(Direction.TO_CLIENT, leave, 2661)
ext.intercept(Direction.TO_CLIENT, clear_user, 1301)
ext.intercept(Direction.TO_SERVER, speech, 1314)
ext.intercept(Direction.TO_CLIENT, change_skin, 3920)
