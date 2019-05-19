import subprocess
from flask_restful import Resource, Api
from flask import Flask, request, render_template, redirect
from flask_cors import CORS
import sqlite3
import json

# result = subprocess.run(['bitcoin-cli', '-regtest', 'getbalance'], stdout=subprocess.PIPE).stdout.decode('utf-8')
# print(result)
def currentUser():
    return "2MsLZKCD5ZB457EmeZ8ZeXzfsYM1fKzyfYy"

def add_project_db(desc):
    conn = sqlite3.connect('leaderboard.db')
    c = conn.cursor()
    addr = subprocess.run(['bitcoin-cli', "-regtest", "getnewaddress"], stdout=subprocess.PIPE).stdout.decode(
            'utf-8').strip()
    c.execute("INSERT INTO Project VALUES (?, ?, ?)", (desc, 0, addr))
    conn.commit()
    conn.close()
    return addr

def add_project_user(user_adr, project_adr):
    conn = sqlite3.connect('leaderboard.db')
    c = conn.cursor()
    c.execute("INSERT INTO UserProject VALUES (?, ?)", (user_adr, project_adr))
    conn.commit()
    conn.close()

app = Flask(__name__)
api = Api(app)
CORS(app)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world', "foo":"bar", "besedilo":"test"}

class GetBalance(Resource):
    def get(self):
        # result = subprocess.run(['bitcoin-cli', '-regtest', 'getbalance'], stdout=subprocess.PIPE).stdout.decode(
        #     'utf-8').strip()
        conn = sqlite3.connect('leaderboard.db')
        c = conn.cursor()
        c.execute("SELECT balance FROM Balance where address = ?", (currentUser(),))
        return {"balance": f"{c.fetchone()[0]}"}

class GetNewAddress(Resource):
    def get(self):
        result = subprocess.run(['bitcoin-cli', "-regtest", "getnewaddress"], stdout=subprocess.PIPE).stdout.decode(
            'utf-8').strip()
        conn = sqlite3.connect('leaderboard.db')
        c = conn.cursor()
        c.execute("INSERT INTO Balance VALUES (?, ?)", (result, 50))
        conn.commit()
        conn.close()
        return {"new_address": f"{result}"}

class GetCurrentUser(Resource):
    def get(self):
        return {"current_user": currentUser()}

class GetProjects(Resource):
    def get(self):
        conn = sqlite3.connect('leaderboard.db')
        c = conn.cursor()
        c.execute("SELECT * FROM Project")
        projects = []
        for re in c.fetchall():
            projects.append({"description": str(re[0]), "gathered":str(re[1]), "address": str(re[2])})
        #print(json.dumps(projects))
        return json.dumps(projects)

class GetUserProjects(Resource):
    def get(self):
        conn = sqlite3.connect('leaderboard.db')
        c = conn.cursor()
        c.execute("SELECT p.word, p.gathered, p.address FROM UserProject as up, Project as p where user_address = ? and up.project_address = p.address", (currentUser(),))
        projects = []
        for re in c.fetchall():
            projects.append({"description": str(re[0]), "gathered":str(re[1]), "address": str(re[2])})
        #print(json.dumps(projects))
        return json.dumps(projects)

class Donate(Resource):
    def post(self):
        addr = request.json["address"]
        conn = sqlite3.connect('leaderboard.db')
        c = conn.cursor()
        c.execute("UPDATE Balance set balance = balance-1 where address = ?", (currentUser(),))
        c.execute("UPDATE Project set gathered = gathered+1 where address = ?", (addr,))
        c.execute("INSERT INTO Tranzaction VALUES (?, ?)", (currentUser(), addr))
        conn.commit()
        subprocess.run(['bitcoin-cli', "-regtest", "sendtoaddress", addr, "1.0"], stdout=subprocess.PIPE).stdout.decode(
            'utf-8').strip()


class GetTransactions(Resource):
    def get(self):
        conn = sqlite3.connect('leaderboard.db')
        c = conn.cursor()
        c.execute(
            "SELECT * FROM Tranzaction")
        projects = []
        for re in c.fetchall():
            projects.append({"from_address": str(re[0]), "to_address": str(re[1])})
        # print(json.dumps(projects))
        return json.dumps(projects)


#api.add_resource(HelloWorld, '/')
api.add_resource(GetBalance, "/getbalance")
api.add_resource(GetNewAddress, "/getnewaddress")
api.add_resource(GetProjects, "/getprojects")
api.add_resource(GetUserProjects, "/getuserprojects")
api.add_resource(GetCurrentUser, "/getcurrentuser")
api.add_resource(Donate, "/donate")
api.add_resource(GetTransactions, "/gettransactions")

@app.route('/newproject',methods = ['POST', 'GET'])
def result():
    proj_adr = add_project_db(request.form["description"])
    add_project_user(currentUser(), proj_adr)
    return redirect("http://localhost:8080/success.html", code=302)

# @app.route('/donate', methods = ["POST", "GET"])
# def donate():
#     print(request)
#     addr = request.json["address"]
#     conn = sqlite3.connect('leaderboard.db')
#     c = conn.cursor()
#     c.execute("UPDATE Balance set balance = balance-1 where address = ?", (currentUser(),))
#     c.execute("UPDATE Balance set balance = balance+1 where address = ?", (addr,))
#     conn.commit()
#     return redirect("http://localhost:8080/app.html", code=302)

if __name__ == '__main__':
    app.run(host='193.2.179.167', port="8888", debug=True)