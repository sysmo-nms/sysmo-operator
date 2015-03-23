import pyrrd4j.pipe

def init(parent=None):
    return pipe.Rrd4jAsync(parent)

def graph(graph, callback):
    cmd = "%s;%s;%s;%s;%s;%i;%i;%s;%i;%i;" % (
        graph['title'],
        graph['name'],
        graph['vlabel'],
        graph['rrdSrc'],
        graph['pngDst'],
        graph['spanBegin'],
        graph['spanEnd'],
        graph['consolFun'],
        graph['width'],
        graph['height'])
    for g in graph['DS']:
        cmd += g
        cmd += '@'
    # remove last pipe character
    cmd = cmd[:-1]
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
