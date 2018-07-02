#Eric Jacobson
#erjacobs@redhat.com
#29 June 2018
#
#Main Flask application for the watch endpoints service
#
#


import rabbitListener
from yaml import load
from threading import Thread
from flask import Flask
app = Flask(__name__)


@app.route('/')
def main():
    endpoints = readYaml()
    listenerThread = Thread(target = rabbitListener.startListener)


def readYaml():
    """Returns a list of endpoints from config.yml"""
    configData = load(file('config.yml', 'r'))
    return configData['endpoints']


if __name__ == "__main__":
    app.run()
