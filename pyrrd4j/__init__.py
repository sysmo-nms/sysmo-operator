import pyrrd4j.pipe

def init(parent=None):
    return pipe.Rrd4jAsync(parent)

def call(command, callback):
    command['callback'] = callback
    pipe.Rrd4jAsync.singleton.execute(command)
