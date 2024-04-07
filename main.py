from flask import Flask, render_template, request, send_file, jsonify
import numpy as np
import matplotlib.pyplot as plt
import tabulate
import io
import base64
import os
import time
# Custom Rule Functions
from GoldenCrossover import isGCS
from GraphGenerator import TwentyByFiftySMAWithGCS

app = Flask(__name__)

@app.route("/")
def index():
    print(time.ctime())
    return render_template("index.html")

@app.route("/GetPossibleStockList",methods=['POST'])
def GetPossibleStockList():
    StockDataDirectory = "./Data/"
    PossibleStockNameList = []
    NotPossibleStockList = []
    WebRequest = request.json
    RuleName = WebRequest.get("RuleName")
    try:
        TimeDelta = int(WebRequest.get("TimeDelta"))
    except Exception as E:
        PossibleStockNameList = "Time must be in Integer"
        return jsonify(PossibleStockNameList)

    if RuleName == "GCS":
        for EachFileName in os.listdir(StockDataDirectory):
            if isGCS(StockDataDirectory,EachFileName,TimeDelta):
                PossibleStockNameList.append(EachFileName.split(".")[0])
            else:
                NotPossibleStockList.append(EachFileName)
    elif RuleName == "RNR":
        PossibleStockNameList = ["New Request Query send to Developer"]
    else:
        PossibleStockNameList = ["No Valid Rule Selects"]
    
    print(len(PossibleStockNameList),len(NotPossibleStockList))
    return jsonify(PossibleStockNameList)

@app.route("/FetchGraph",methods=['POST'])
def FetchGraph():
    WebRequest = request.json
    StockName = WebRequest.get("StockName")
    
    if StockName != "Default":
        try:
           TimeDelta = int(WebRequest.get("TimeDelta"))
           print(StockName,TimeDelta)
           return TwentyByFiftySMAWithGCS(StockName,TimeDelta)
        except Exception as E:
            return jsonify(E)
    else:
        return jsonify("Value Not Selected")
    

if __name__ == '__main__':
    app.run(debug=False,port=7895,host="192.168.100.45")