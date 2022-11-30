
import gc
import os, signal, threading
import RobotStateFetcherBasics as RSF
from waitress import serve
from flask import jsonify, request, render_template, Flask, make_response
from flask_restful import Resource, Api

#app = Flask("getRobotStateAPI")
app = Flask(__name__)
api = Api(app)

robotStateInfo = {}

print("start of App")

#@app.route('/', methods=['GET', 'POST'])

#def data_server():
#    return ("success")

class robotState(Resource): 
    def get(self, ipAddr): #, robotStateInfo):
    #def get(ipAddr):

        #response = RSF.main({"10.100.247.191"})
        if ipAddr == "187":

            pid = os.getpid()

            os.kill(pid, signal.SIGINT)
        
        response = RSF.main({ipAddr})

        return(response)

api.add_resource(robotState,'/<ipAddr>')

if __name__ == "__main__":
    #app.run()
    serve(app)
