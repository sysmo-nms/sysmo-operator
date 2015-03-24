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
    cmd = "CONFIG:" + cfg
    return pipe.Rrd4jAsync(parent, cmd)

def graph(graph, callback):
    cmd = "%s;%s;%s;%s;%s;%i;%i;%i;%i;" % (
        graph['title'],
        graph['name'],
        graph['vlabel'],
        graph['rrdSrc'],
        graph['pngDst'],
        graph['spanBegin'],
        graph['spanEnd'],
        graph['width'],
        graph['height'])
    for g in graph['DS']:
        cmd += g
        cmd += '@'
    # remove last separator character
    cmd     = cmd[:-1]
    command = dict()
    command['string'] = 'GRAPH:' + cmd
    command['callback'] = callback
    print("command is" + cmd)
    pipe.Rrd4jAsync.singleton.execute(command)

def update(command, callback):
    command['string'] = 'UPDATE:' + command['string']
    call(command, callback)

def call(command, callback):
    command['callback'] = callback
    pipe.Rrd4jAsync.singleton.execute(command)
## __init__ api end
