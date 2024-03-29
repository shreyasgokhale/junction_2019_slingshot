from flask import Flask, render_template
from flask_socketio import SocketIO, join_room, emit
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
from game import GameState
import json
#import shoot-action


# initialize Flask
app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates')
GoogleMaps(
    app,
    key="AIzaSyBmm32aJXraStLKXAG0J3rpyWIDOSM0w2E"
)

socketio = SocketIO(app)

#game_state = GameState()

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('join')
def handle_joined(data):
    print ("data nickname" + data['nickname'])
    nickname = data['nickname']
    print (game_state.add_player(nickname))


@socketio.on('update_position')
def handle_update_position(data):
    print ("update_position data ", data)
    game_state.update_player_position(data['nickname'], data['position'])


@socketio.on('shoot')
def handle_shoot(data):
    print ("handle_shoot data", data)
    nickname = data['nickname']
    game_state.toggle_player_is_shooting(nickname)


@app.route("/map")
def mapview():
    # creating a map in the view
    movingmap = Map(
        identifier="movingmap",
        varname="movingmap",
        lat=60.185509859,
        lng=24.824594148,
        markers=[],
    )
    return render_template('map.html', movingmap=movingmap)


# # Function to make MongoDBAPI object
# def makeObject(link=link, dbName = "LocalDB", dbCollection="LocalCollection"):
#     mdbobject = MongoDBDriver.MongoDBAPI(link)
#     mdbobject.defineDB(dbName)
#     mdbobject.defineCollection(dbCollection)
#     return mdbobject


class Thread(object):
    def __init__(self):
        self.thread = None

    def start_server(self):
        socketio.run(app, debug=True, use_reloader=False)

    def start(self):
        self.thread = socketio.start_background_task(self.start_server)

    def wait(self):
        self.thread.join()


if __name__ == '__main__':
    t = Thread()
    t.start()
    game_state = GameState()


    while True:
        socketio.sleep(1)
        game_state.update()
        socketio.emit('state_update', game_state.get_json(), scope='/map')
        print('Sent updated state')

    socketio.wait()
