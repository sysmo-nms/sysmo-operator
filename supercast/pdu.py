import json

def encode(pyTerm):
    jsonStr = json.dumps(pyTerm)
    jsonBin = jsonStr.encode('utf-8')
    return jsonBin

def decode(jsonBin):
    jsonStr = jsonBin.decode('utf-8')
    pyTerm  = json.loads(jsonStr)
    return pyTerm
