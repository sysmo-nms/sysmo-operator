import pyrrd4j.pipe


## __init__ api begin
def init(colorDict, parent=None):
    cfg = "%s;%s;%s;%s;%s;%s;%s;%s;%s;%s" % (
        colorDict['BACK'],
        colorDict['CANVAS'],
        colorDict['SHADEA'],
        colorDict['SHADEB'],
        colorDict['GRID'],
        colorDict['MGRID'],
        colorDict['FONT'],
        colorDict['FRAME'],
        colorDict['ARROW'],
        colorDict['XAXIS']
    )
    cmd = "CONFIG|" + cfg
    return pipe.Rrd4jAsync(parent, cmd)

def graph(graph, callback):
    cmd = "%s;%s;%s;%s;%s;%i;%i;%i;%i;%s;%s;%s;%s;%s;%s;" % (
        graph['title'],
        graph['name'],
        graph['vlabel'],
        graph['filenameRrd'],
        graph['filenamePng'],
        graph['spanBegin'],
        graph['spanEnd'],
        graph['width'],
        graph['height'],

        graph['minValue'],
        graph['maxValue'],
        graph['rigid'],
        graph['base'],
        graph['unit'],
        graph['unitExponent']
)
    for g in graph['DS']:
        cmd += g
        cmd += '@'
    # remove last pipe character
    cmd = cmd[:-1]
    command = dict()
    command['string'] = 'GRAPH|' + cmd
    command['callback'] = callback
    pipe.Rrd4jAsync.singleton.execute(command)

def update(update, callback):
    updates = update['updates']
    cmd     = "%s;%i;" % (update['file'], update['timestamp'])
    for k in updates.keys():
        cmd += "%s,%i" % (k, updates[k])
        cmd += '@'
    cmd = cmd[:-1]
    command = dict() 
    command['string'] = 'UPDATE|' + cmd
    command['callback'] = callback
    call(command, callback)

def call(command, callback):
    command['callback'] = callback
    pipe.Rrd4jAsync.singleton.execute(command)
## __init__ api end
