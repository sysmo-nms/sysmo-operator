from pyasn1.type        import char,univ,namedtype,tag,namedval
from pyasn1.codec.ber   import encoder, decoder

##############################################################################
##############################################################################
#### ENMS PDU DEF ############################################################
##############################################################################
##############################################################################
class EsnmpPDU(univ.Choice):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType(
            'text', char.PrintableString()),
        namedtype.NamedType('id', univ.Integer())
    )

##############################################################################
##############################################################################
#### TRACKER PDU DEF #########################################################
##############################################################################
##############################################################################
" Tracker PDUs are defined here "

class Property(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('key',      char.PrintableString()),
        namedtype.NamedType('value',    char.PrintableString())
    )

class Properties(univ.SequenceOf):
    componentType = Property()

class Bind(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('replacement',  char.PrintableString()),
        namedtype.NamedType('macro',        char.PrintableString())
    )

class Binds(univ.SequenceOf):
    componentType = Bind()

class Graphs(univ.SequenceOf):
    componentType = char.PrintableString()

class LoggerRrd(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('module',   char.PrintableString()),
        namedtype.NamedType('create',   char.PrintableString()),
        namedtype.NamedType('update',   char.PrintableString()),
        namedtype.NamedType('graphs',   Graphs()),
        namedtype.NamedType('binds',    Binds())
    )

class LoggerText(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('module',   char.PrintableString()),
        namedtype.NamedType('conf',     char.PrintableString())
    )

class Logger(univ.Choice):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType(
            'loggerRrd',
            LoggerRrd().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext,
                    tag.tagFormatSimple,
                    0
                )
            )
        ),
        namedtype.NamedType(
            'loggerText',
            LoggerText().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext,
                    tag.tagFormatSimple,
                    1
                )
            )
        )
    )



class Loggers(univ.SequenceOf):
    componentType = Logger()

class Inspector(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('module',   char.PrintableString()),
        namedtype.NamedType('conf',     char.PrintableString())
    )

class Inspectors(univ.SequenceOf):
    componentType = Inspector()

class Groups(univ.SequenceOf):
    componentType = char.PrintableString()

class PermConf(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('read',     Groups()),
        namedtype.NamedType('write',    Groups())
    )

class TargetProperties(univ.SequenceOf):
    componentType = Property()

class TargetProbeReturnKeyVal(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('key',      char.PrintableString()),
        namedtype.NamedType('value',    char.PrintableString())
    )

class TargetProbeReturnKeyVals(univ.SequenceOf):
    componentType = TargetProbeReturnKeyVal()

class ProbeInfoType(univ.Enumerated):
    namedValues = namedval.NamedValues(
        ('create', 0),
        ('delete', 1),
        ('update', 2)
    )

class TargetInfoType(univ.Enumerated):
    namedValues = namedval.NamedValues(
        ('create', 0),
        ('delete', 1),
        ('update', 2)
    )

class TrackerProbeDump(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('channel',  char.PrintableString()),
        namedtype.NamedType('id',       univ.Integer()),
        namedtype.NamedType('module',   char.PrintableString()),
        namedtype.NamedType('data',     univ.OctetString()),
    )

class TrackerProbeInfo(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('channel',  char.PrintableString()),
        namedtype.NamedType('id',       univ.Integer()),
        namedtype.NamedType('name',     char.PrintableString()),
        namedtype.NamedType('perm',     PermConf()),
        namedtype.NamedType('probeMod', char.PrintableString()),
        namedtype.NamedType('probeConf',    char.PrintableString()),
        namedtype.NamedType('status',   char.PrintableString()),
        namedtype.NamedType('timeout',  univ.Integer()),
        namedtype.NamedType('step',     univ.Integer()),
        namedtype.NamedType('inspectors',   Inspectors()),
        namedtype.NamedType('loggers',      Loggers()),
        namedtype.NamedType('properties',   Properties()),
        namedtype.NamedType('active',   univ.Integer()),
        namedtype.NamedType('infoType', ProbeInfoType())
    )

class TrackerProbeActivity(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('channel',  char.PrintableString()),
        namedtype.NamedType('id',       univ.Integer()),
        namedtype.NamedType('timestamp',    univ.Integer()),
        namedtype.NamedType('probeState',   char.PrintableString()),
        namedtype.NamedType('returnStatus', char.PrintableString()),
        namedtype.NamedType('textual',  char.PrintableString())
    )

class TrackerProbeReturn(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('channel',  char.PrintableString()),
        namedtype.NamedType('id',       univ.Integer()),
        namedtype.NamedType('status',   char.PrintableString()),
        namedtype.NamedType('originalReply',    char.PrintableString()),
        namedtype.NamedType('timestamp',        univ.Integer()),
        namedtype.NamedType('keyVals',   TargetProbeReturnKeyVals())
    )

class TrackerProbeModuleInfo(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('name', char.PrintableString()),
        namedtype.NamedType('info', char.PrintableString())
    )

class TrackerTargetInfo(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('channel',     char.PrintableString()),
        namedtype.NamedType('properties',   TargetProperties()),
        namedtype.NamedType('type',         TargetInfoType())
    )

class TrackerPDU_fromClient(char.PrintableString): pass

class TrackerPDU_fromServer(univ.Choice):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType(
            'targetInfo',
            TrackerTargetInfo().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext,
                    tag.tagFormatSimple,
                    1
                )
            )
        ),
        namedtype.NamedType(
            'probeInfo',
            TrackerProbeInfo().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext,
                    tag.tagFormatSimple,
                    2
                )
            )
        ),
        namedtype.NamedType(
            'probeDump',
            TrackerProbeDump().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext,
                    tag.tagFormatSimple,
                    4
                )
            )
        ),
        namedtype.NamedType(
            'probeModInfo',
            TrackerProbeModuleInfo().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext,
                    tag.tagFormatSimple,
                    6
                )
            )
        ),
        namedtype.NamedType(
            'probeActivity',
            TrackerProbeActivity().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext,
                    tag.tagFormatSimple,
                    7
                )
            )
        ),
        namedtype.NamedType(
            'probeReturn',
            TrackerProbeReturn().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext,
                    tag.tagFormatSimple,
                    8
                )
            )
        )
    )

class TrackerPDU(univ.Choice):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType(
            'fromServer',
            TrackerPDU_fromServer().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext,
                    tag.tagFormatSimple,
                    0
                )
            )
        ),
        namedtype.NamedType(
            'fromClient',
            TrackerPDU_fromClient().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext,
                    tag.tagFormatSimple,
                    1
                )
            )
        )
    )


##############################################################################
##############################################################################
#### SUPERCAST PDU DEF #######################################################
##############################################################################
##############################################################################
class SupercastChan(char.PrintableString): pass


class SupercastGroup(char.PrintableString): pass

class SupercastGroups(univ.SequenceOf):
    componentType = SupercastGroup()
    

class SupercastChanInfoType(univ.Enumerated):
    namedValues = namedval.NamedValues(
        ('create', 0),
        ('delete', 1),
        ('update', 2)
    )

class SupercastChanInfo(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('channel',  SupercastChan()),
        namedtype.NamedType('type',     SupercastChanInfoType())
    )

class SupercastChansInfo(univ.SequenceOf):
    componentType = SupercastChanInfo()

class SupercastAuthProto(univ.Enumerated):
    namedValues = namedval.NamedValues(
        ('localFile', 0),
        ('ldap', 1)
    )

class SupercastPDU_fromServer_authAck(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('groups',       char.PrintableString()),
        namedtype.NamedType('staticChans',  char.PrintableString())
    )
    
class SupercastAuthErrorEnumerated(univ.Enumerated):
    namedValues = namedval.NamedValues(
        ('noShuchUser', 0),
        ('badPass', 1),
        ('timeout', 2),
        ('other', 3)
    )

class SupercastAuthError(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('error',    SupercastAuthErrorEnumerated()),
        namedtype.NamedType('userId',  char.PrintableString()),
        namedtype.NamedType('pass',    char.PrintableString())
    )

class SupercastAuthAck(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('groups',       SupercastGroups()),
        namedtype.NamedType('staticChans',  SupercastChansInfo())
    )

class SupercastPDU_fromServer(univ.Choice):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType(
            'chanInfo',
            SupercastChanInfo().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext,
                    tag.tagFormatSimple,
                    1
                )
            )
        ),
        namedtype.NamedType(
            'authReq',
            SupercastAuthProto().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext,
                    tag.tagFormatSimple,
                    2
                )
            )
        ),
        namedtype.NamedType(
            'authAck',
            SupercastAuthAck().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext,
                    tag.tagFormatSimple,
                    3
                )
            )
        ),
        namedtype.NamedType(
            'authError',
            SupercastAuthError().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext,
                    tag.tagFormatSimple,
                    4
                )
            )
        ),
        namedtype.NamedType(
            'subscribeOk',
            SupercastChan().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext,
                    tag.tagFormatSimple,
                    5
                )
            )
        ),
        namedtype.NamedType(
            'subscribeErr',
            SupercastChan().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext,
                    tag.tagFormatSimple,
                    6
                )
            )
        ),
        namedtype.NamedType(
            'unsubscribeOk',
            SupercastChan().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext,
                    tag.tagFormatSimple,
                    7
                )
            )
        ),
        namedtype.NamedType(
            'unsubscribeErr',
            SupercastChan().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext,
                    tag.tagFormatSimple,
                    8
                )
            )
        )
    )

class SupercastAuthResp(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('userId',   char.PrintableString()),
        namedtype.NamedType('pass',     char.PrintableString())
    )


class SupercastPDU_fromClient(univ.Choice):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType(
            'subscribe', 
            SupercastChan().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext,
                    tag.tagFormatSimple,
                    0
                )
            )
        ),
        namedtype.NamedType(
            'unsubscribe', 
            SupercastChan().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext,
                    tag.tagFormatSimple,
                    1
                )
            )
        ),
        namedtype.NamedType(
            'authResp', 
            SupercastAuthResp().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext,
                    tag.tagFormatSimple,
                    4
                )
            )
        )
    )



class SupercastPDU(univ.Choice):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType(
            'fromServer',
            SupercastPDU_fromServer().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext,
                    tag.tagFormatSimple,
                    0
                )
            )
        ),
        namedtype.NamedType(
            'fromClient',
            SupercastPDU_fromClient().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext,
                    tag.tagFormatSimple,
                    1
                )
            )
        )
    )

class NmsPDU(univ.Choice):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType(
            'modSupercastPDU',
            SupercastPDU().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext,
                    tag.tagFormatSimple,
                    0
                )
            )
        ),
        namedtype.NamedType(
            'modTrackerPDU'  , 
            TrackerPDU().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext,
                    tag.tagFormatSimple,
                    2
                )
            )
        )
    )




##############################################################################
##############################################################################
#### EXPORTED FUNCTIONS ######################################################
##############################################################################
##############################################################################
def decode(pdu):
    msg, x = decoder.decode(str(pdu), asn1Spec=NmsPDU())

    msg1        = msg.getComponent()
    msg1_type   = msg.getName()
    if msg1_type == 'modSupercastPDU':
        msg2        = msg1.getComponent()
        msg2_type   = msg1.getName()
        if msg2_type == 'fromServer':
            msg3        = msg2.getComponent()
            msg3_type   = msg2.getName()
            if   msg3_type == 'unsubscribeOk':
                return {
                    'from':     msg1_type,
                    'msgType':  msg3_type,
                    'value':    str(msg3)
                }
            elif msg3_type == 'subscribeOk':
                return {
                    'from':     msg1_type,
                    'msgType':  msg3_type,
                    'value':    str(msg3)
                }
            elif msg3_type == 'subscribeErr':
                return {
                    'from':     msg1_type,
                    'msgType':  msg3_type,
                    'value':    str(msg3)
                }
            elif msg3_type == 'unsubscribeErr':
                return {
                    'from':     msg1_type,
                    'msgType':  msg3_type,
                    'value':    str(msg3)
                }
            elif msg3_type == 'chanInfo':
                channel = msg3.getComponentByName('channel')
                evtype  = msg3.getComponentByName('type')
                if      evtype == 0: eventType = 'create'
                elif    evtype == 1: eventType = 'delete'
                elif    evtype == 2: eventType = 'update'
                return {
                    'from':     msg1_type,
                    'msgType':  msg3_type,
                    'value':    {
                        'channelId':      str(channel),
                        'eventType':    str(eventType)
                    }
                }
            elif msg3_type == 'authReq':
                if      msg3 == 0: authProto = 'localFile'
                elif    msg3 == 1: authProto = 'ldap'
                return {
                    'from':     msg1_type,
                    'msgType':  msg3_type,
                    'value':    str(authProto)
                }
            elif msg3_type == 'authAck':
                groups      = msg3.getComponentByName('groups')
                chans       = msg3.getComponentByName('staticChans')
                group_list  = list()
                chan_list   = list()
                for idx in range(len(groups)):
                    group_list.append(str(groups.getComponentByPosition(idx)))

                for idx in range(len(chans)):
                    i = chans.getComponentByPosition(idx)
                    channel    = str(i.getComponentByName('channel'))
                    evtype     = int(i.getComponentByName('type'))
                    if      evtype == 0: eventType = 'create'
                    elif    evtype == 1: eventType = 'delete'
                    elif    evtype == 2: eventType = 'update'
                    chan_list.append({
                        'channelId': channel,
                        'eventType': eventType
                    })
                return {
                    'from':     msg1_type,
                    'msgType':  msg3_type,
                    'value':    {
                        'groups':   group_list,
                        'chans':    chan_list
                    }
                }
            elif msg3_type == 'authError':
                error  = int(msg3.getComponentByName('error'))
                userId = str(msg3.getComponentByName('userId'))
                passw  = str(msg3.getComponentByName('pass'))
                if      error == 0: errorType = 'noSuchUser'
                elif    error == 1: errorType = 'badPass'
                elif    error == 2: errorType = 'timeout'
                elif    error == 3: errorType = 'other'
                return {
                    'from':     msg1_type,
                    'msgType':  msg3_type,
                    'value':    {
                        'error':    errorType,
                        'userId':   userId,
                        'pass':     passw
                    }
                }
            else:
                print "unknwon message", msg3_type
                return {}
        else: 
            print "unknwon message", msg2_type
            return {}
    elif msg1_type == 'modTrackerPDU':
        msg2        = msg1.getComponent()
        msg2_type   = msg1.getName()
        if msg2_type == 'fromServer':
            msg3        = msg2.getComponent()
            msg3_type   = msg2.getName()
            if msg3_type == 'probeModInfo':
                name = str(msg3.getComponentByName('name'))
                info = str(msg3.getComponentByName('info'))
                return {
                    'from':     msg1_type,
                    'msgType':  msg3_type,
                    'value':    {
                        'name': name,
                        'info': info
                    }
                }
            elif msg3_type == 'targetInfo':
                targetId    = str(msg3.getComponentByName('channel'))
                infoType    = msg3.getComponentByName('type')
                infoProp    = msg3.getComponentByName('properties')
                if      infoType == 0: infoT = 'create'
                elif    infoType == 1: infoT = 'delete'
                elif    infoType == 2: infoT = 'update'
                else:   infoT = 'nothing'
                return {
                    'from':     msg1_type,
                    'msgType':  msg3_type,
                    'value':    {
                        'channel':      targetId,
                        'properties':   infoProp,
                        'infoType':     infoT
                    }
                }
            elif msg3_type == 'probeInfo':
                channel     = str(msg3.getComponentByName('channel'))
                probeId     = msg3.getComponentByName('id')
                name        = str(msg3.getComponentByName('name'))
                perm        = msg3.getComponentByName('perm')
                probeMod    = str(msg3.getComponentByName('probeMod'))
                probeConf   = str(msg3.getComponentByName('probeConf'))
                status      = str(msg3.getComponentByName('status'))
                timeout     = msg3.getComponentByName('timeout')
                step        = msg3.getComponentByName('step')
                inspectors  = msg3.getComponentByName('inspectors')
                loggers     = msg3.getComponentByName('loggers')
                properties  = msg3.getComponentByName('properties')
                active      = msg3.getComponentByName('active')
                infoType    = msg3.getComponentByName('infoType')


                readPerm    = perm.getComponentByName('read')
                writePerm   = perm.getComponentByName('write')
                permDict    = {'read': [], 'write': []}
                for i in range(len(readPerm)):
                    permDict['read'].append(
                        str(readPerm.getComponentByPosition(i))
                    )

                for i in range(len(writePerm)):
                    permDict['write'].append(
                        str(writePerm.getComponentByPosition(i))
                    )

                inspectorsDict = {}
                for i in range(len(inspectors)):
                    ins = inspectors.getComponentByPosition(i)
                    mod  = ins.getComponentByName('module')
                    conf = ins.getComponentByName('conf')
                    inspectorsDict[str(mod)] = str(conf)

                loggersDict = {}
                for i in range(len(loggers)):
                    logger = loggers.getComponentByPosition(i)
                    ltype  = logger.getName()
                    if ltype == 'loggerText':
                        logger2 = logger.getComponent()
                        mod  = logger2.getComponentByName('module')
                        conf = logger2.getComponentByName('conf')
                        loggersDict[str(mod)] = str(conf)
                    elif ltype == 'loggerRrd':
                        logger2 = logger.getComponent()
                        mod     = logger2.getComponentByName('module')

                        create  = logger2.getComponentByName('create')
                        update  = logger2.getComponentByName('update')

                        binds   = logger2.getComponentByName('binds')
                        bindsD = dict()
                        for b in range(len(binds)):
                            bind = binds.getComponentByPosition(b)
                            rep  = bind.getComponentByName('replacement')
                            mac  = bind.getComponentByName('macro')
                            bindsD[str(rep)] = str(mac)

                        graphs  = logger2.getComponentByName('graphs')
                        graphsL = list()
                        for g in range(len(graphs)):
                            graphItem = graphs.getComponentByPosition(g)
                            graphsL.append(str(graphItem))

                        conf   = dict()
                        conf['create'] = str(create)
                        conf['update'] = str(update)
                        conf['graphs'] = graphsL
                        conf['binds']  = str(bindsD)
                        loggersDict[str(mod)] = conf

                propertiesDict = {}
                for i in range(len(properties)):
                    prop    = properties.getComponentByPosition(i)
                    key     = prop.getComponentByName('key')
                    value   = prop.getComponentByName('value')
                    propertiesDict[str(key)] = str(value)

                return {
                    'from': msg1_type,
                    'msgType':  msg3_type,
                    'value':    {
                        'channel':  channel,
                        'id':       int(probeId),
                        'name':     name,
                        'perm':     permDict,
                        'probeMod': probeMod,
                        'probeconf': probeConf,
                        'status':   status,
                        'timeout':  int(timeout),
                        'step':     int(step),
                        'inspectors':   inspectorsDict,
                        'loggers':  loggersDict,
                        'properties':   propertiesDict,
                        'active':   int(active),
                        'infoType': infoType.prettyPrint()
                    }
                }
            elif msg3_type == 'probeDump':
                channel     = str(msg3.getComponentByName('channel'))
                probeId     = msg3.getComponentByName('id')
                module      = msg3.getComponentByName('module')
                binaryData  = msg3.getComponentByName('data')

                return {
                    'from': msg1_type,
                    'msgType':  msg3_type,
                    'value':    {
                        'channel': channel,
                        'id': int(probeId),
                        'logger': module,
                        'data': str(binaryData)
                    }
                }
            elif msg3_type == 'probeActivity':
                channel     = str(msg3.getComponentByName('channel'))
                probeId     = msg3.getComponentByName('id')
                time        = msg3.getComponentByName('timestamp')
                probeState  = str(msg3.getComponentByName('probeState'))
                returnStatus = str(msg3.getComponentByName('returnStatus'))
                textual     = str(msg3.getComponentByName('textual'))
                return {
                    'from': msg1_type,
                    'msgType':  msg3_type,
                    'value':    {
                        'channel':  channel,
                        'id':       int(probeId),
                        'timestamp': int(time),
                        'probeState': probeState,
                        'returnStatus': returnStatus,
                        'textual': textual

                    }
                }
            elif msg3_type == 'probeReturn':
                channel     = str(msg3.getComponentByName('channel'))
                probeId     = msg3.getComponentByName('id')
                status      = str(msg3.getComponentByName('status'))
                original_rep = str(msg3.getComponentByName('originalReply'))
                timestamp   = msg3.getComponentByName('timestamp')
                keyVals     = msg3.getComponentByName('keyVals')

                keyValsDict = dict()
                for i in range(len(keyVals)):
                    keyVal  = keyVals.getComponentByPosition(i)
                    key     = keyVal.getComponentByName('key')
                    value   = keyVal.getComponentByName('value')
                    keyValsDict[str(key)] = str(value)

                return {
                    'from': msg1_type,
                    'msgType':  msg3_type,
                    'value':    {
                        'channel':      channel,
                        'id':           int(probeId),
                        'status':       status,
                        'originalRep':  original_rep,
                        'timestamp':    int(timestamp),
                        'keyVals':      keyValsDict
                    }
                }
            else:
                print "unknwon message", msg3_type
                return {}
        else:
            print "unknwon message", msg2_type
            return {}
        print msg2, msg2_type
    else:
        print "Unknown pdu: ", msg1_type
        return {}


def encode(pduType, chanString=None, userId=None, password=None):
    if   pduType == 'subscribe':
        if chanString != None:
            return encode_subscribe(chanString)
        else:
            return False
    elif pduType == 'unsubscribe':
        if chanString != None: 
            return encode_unsubscribe(chanString)
        else:
            return False
    elif pduType == 'authResp':
        if (userId != None and password != None): 
            return encode_authResp(userId, password)
        else:
            return False
    else:
        return False

def encode_unsubscribe(chanString):
    chan = SupercastChan(chanString).subtype(
        implicitTag=tag.Tag(
            tag.tagClassContext,
            tag.tagFormatSimple,
            1
        )
    )
    fromClient = SupercastPDU_fromClient().subtype(
        implicitTag=tag.Tag(
            tag.tagClassContext,
            tag.tagFormatSimple,
            1
        )
    )
    supercastPDU = SupercastPDU().subtype(
        implicitTag=tag.Tag(
            tag.tagClassContext,
            tag.tagFormatSimple,
            0
        )
    )
    pduDef = NmsPDU()

    fromClient.setComponentByName('unsubscribe', chan)
    supercastPDU.setComponentByName('fromClient', fromClient)
    pduDef.setComponentByName('modSupercastPDU', supercastPDU)
    pdu = encoder.encode(pduDef)
    return pdu

def encode_subscribe(chanString):
    chan = SupercastChan(chanString).subtype(
        implicitTag=tag.Tag(
            tag.tagClassContext,
            tag.tagFormatSimple,
            0
        )
    )
    fromClient = SupercastPDU_fromClient().subtype(
        implicitTag=tag.Tag(
            tag.tagClassContext,
            tag.tagFormatSimple,
            1
        )
    )
    supercastPDU = SupercastPDU().subtype(
        implicitTag=tag.Tag(
            tag.tagClassContext,
            tag.tagFormatSimple,
            0
        )
    )
    pduDef = NmsPDU()

    fromClient.setComponentByName('subscribe', chan)
    supercastPDU.setComponentByName('fromClient', fromClient)
    pduDef.setComponentByName('modSupercastPDU', supercastPDU)
    pdu = encoder.encode(pduDef)
    return pdu

def encode_authResp(userId, password):
    authResp = SupercastAuthResp().subtype(
        implicitTag=tag.Tag(
            tag.tagClassContext,
            tag.tagFormatSimple,
            4
        )
    )
    authResp.setComponentByName('userId', userId)
    authResp.setComponentByName('pass',   password)

    fromClient = SupercastPDU_fromClient().subtype(
        implicitTag=tag.Tag(
            tag.tagClassContext,
            tag.tagFormatSimple,
            1
        )
    )
    fromClient.setComponentByName('authResp', authResp)

    supercastPDU = SupercastPDU().subtype(
        implicitTag=tag.Tag(
            tag.tagClassContext,
            tag.tagFormatSimple,
            0
        )
    )
    supercastPDU.setComponentByName('fromClient', fromClient)

    pduDef = NmsPDU()
    pduDef.setComponentByName('modSupercastPDU', supercastPDU)

    pdu = encoder.encode(pduDef)
    return pdu


#fd = open('/tmp/pdu.bin', 'r')
# fw = open('/tmp/ret.bin', 'w')
#pdu = fd.read(); fd.close()
#print pdu

#a = decoder.decode(pdu, asn1Spec=NmsPDU())
#a = decode(pdu)
#print a
# print "Return is ", a
# x = genPdu_unsubscribe("channel-Xkki")
# 
# fw.write(x); fw.close()
