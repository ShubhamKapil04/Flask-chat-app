from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import join_room, leave_room, send, SocketIO
import random
from string import ascii_uppercase

app = Flask(__name__)
app.config["SECRET_KEY"] = "abcdefgh"
# socketIO integration
socketio = SocketIO(app)

# Created Dictionary for different rooms    
rooms = {}

# Generate for the room 
def generate_unique_code(length):
    while True:
        code = ""
        # Generating the Code Randomly
        for _ in range(length):
            code += random.choice(ascii_uppercase)
        
         # Checking if the code already exist in the Dictionary
        # if it did exist then will generate another Code
        if code not in rooms:
            break
    
    return code

# Home page
@app.route("/", methods=["POST", "GET"])
def home():
    # clearing the session
    session.clear()
    if request.method == "POST":
        name = request.form.get("name")
        code = request.form.get("code")
        # they both have empty values
        join = request.form.get("join", False)
        create = request.form.get("create", False)

        # If they don't have name
        if not name:
            return render_template("home.html", error="Please enter a name.", code=code, name=name)
        
        # if user trying to join but not inserted the code then we have to give him error
        if join != False and not code:
            return render_template("home.html", error="Please enter a room code.", code=code, name=name)
        
        # if they generated a room
        room = code
        if create != False:
            room = generate_unique_code(4)
            # Number of the members in the Room 
            # The message also storing  in the list
            rooms[room] = {"members": 0, "messages": []}
        elif code not in rooms:
            return render_template("home.html", error="Room does not exist.", code=code, name=name)
        
        # Storing the data in server for temporary
        # We can Manipulate by the sever and also secure way to store the data 
        # Semi permanent
        session["room"] = room
        session["name"] = name
        return redirect(url_for("room"))

    return render_template("home.html")

@app.route("/room")
def room():
    room = session.get("room")
    if room is None or session.get("name") is None or room not in rooms:
        return redirect(url_for("home"))

    return render_template("room.html", code=room, messages=rooms[room]["messages"])

@socketio.on("message")
def message(data):
    room = session.get("room")
    if room not in rooms:
        return 
    
    # content that going to send to the room
    content = {
        "name": session.get("name"),
        "message": data["data"]
    }
    # sending to this content to the room
    send(content, to=room)
    rooms[room]["messages"].append(content)
    print(f"{session.get('name')} said: {data['data']}")

#connecting to the roomv
@socketio.on("connect")
def connect(auth):
    room = session.get("room")
    name = session.get("name")
    if not room or not name:
        return
    
    # room does't exist
    if room not in rooms:
        leave_room(room)
        return
    
    join_room(room)
    send({"name": name, "message": "has entered the room"}, to=room)
    rooms[room]["members"] += 1  # how many room member in the room
    print(f"{name} joined room {room}")

# Leaving the room
@socketio.on("disconnect")
def disconnect():
    room = session.get("room")
    name = session.get("name")
    leave_room(room)

    if room in rooms:
        rooms[room]["members"] -= 1  # decrementing the Members those who leaving
        if rooms[room]["members"] <= 0:  # if in room there are no member the delete that room
            del rooms[room]
    
    send({"name": name, "message": "has left the room"}, to=room)
    print(f"{name} has left the room {room}")

if __name__ == "__main__":
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)