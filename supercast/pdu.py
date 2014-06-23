from pyasn1.type        import char,univ,namedtype,tag,namedval,constraint
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
#### MONITOR PDU DEF #########################################################
##############################################################################
##############################################################################
" Monitor PDUs are defined here "

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

class LoggerRrdConfig(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('file',     char.PrintableString()),
        namedtype.NamedType('create',   char.PrintableString()),
        namedtype.NamedType('update',   char.PrintableString()),
        namedtype.NamedType('graphs',   Graphs()),
        namedtype.NamedType('binds',    Binds())
    )

class LoggerRrdConfigs(univ.SequenceOf):
    componentType = LoggerRrdConfig()

class LoggerRrd(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('module',   char.PrintableString()),
        namedtype.NamedType('config',   LoggerRrdConfigs())
    )

class LoggerText(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('module',   char.PrintableString()),
        namedtype.NamedType('conf',     char.PrintableString())
    )

class LoggerEvents(univ.Sequence):
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
        ),
        namedtype.NamedType(
            'loggerEvents',
            LoggerEvents().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext,
                    tag.tagFormatSimple,
                    2
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


class MonitorRrdFileDump(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('target',       char.PrintableString()),
        namedtype.NamedType('probeName',    char.PrintableString()),
        namedtype.NamedType('module',       char.PrintableString()),
        namedtype.NamedType('fileId',       char.PrintableString()),
        namedtype.NamedType('bin',          univ.OctetString())
    )

class MonitorProbeEvent(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('probeName',    char.PrintableString()),
        namedtype.NamedType('eventId',      univ.Integer()),
        namedtype.NamedType('insertTs',     univ.Integer()),
        namedtype.NamedType('ackTs',        univ.Integer()),
        namedtype.NamedType('status',       char.PrintableString()),
        namedtype.NamedType('textual',      char.PrintableString()),
        namedtype.NamedType('ackNeeded',    univ.Boolean()),
        namedtype.NamedType('ackValue',     char.PrintableString()),
        namedtype.NamedType('groupOwner',   char.PrintableString()),
        namedtype.NamedType('userOwner',    char.PrintableString()),
    )

class MonitorProbeEvents(univ.SequenceOf):
    componentType = MonitorProbeEvent()

class MonitorEventProbeDump(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('target',   char.PrintableString()),
        namedtype.NamedType('probe',    char.PrintableString()),
        namedtype.NamedType('module',   char.PrintableString()),
        namedtype.NamedType('events',   MonitorProbeEvents()),
    )

class MonitorProbeDump(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('channel',  char.PrintableString()),
        namedtype.NamedType('name',     char.PrintableString()),
        namedtype.NamedType('module',   char.PrintableString()),
        namedtype.NamedType('data',     univ.OctetString()),
    )

class MonitorProbeInfo(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('channel',  char.PrintableString()),
        namedtype.NamedType('id',       univ.Integer()),
        namedtype.NamedType('name',     char.PrintableString()),
        namedtype.NamedType('descr',    char.PrintableString()),
        namedtype.NamedType('info',     char.PrintableString()),
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

class MonitorProbeActivity(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('target',       char.PrintableString()),
        namedtype.NamedType('probeName',    char.PrintableString()),
        namedtype.NamedType('timestamp',    univ.Integer()),
        namedtype.NamedType('probeState',   char.PrintableString()),
        namedtype.NamedType('returnStatus', char.PrintableString()),
        namedtype.NamedType('textual',  char.PrintableString())
    )

class MonitorProbeReturn(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('target',  char.PrintableString()),
        namedtype.NamedType('id',      char.PrintableString()),
        namedtype.NamedType('status',   char.PrintableString()),
        namedtype.NamedType('originalReply',    char.PrintableString()),
        namedtype.NamedType('timestamp',        univ.Integer()),
        namedtype.NamedType('keyVals',   TargetProbeReturnKeyVals())
    )

class MonitorProbeModuleInfo(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('name', char.PrintableString()),
        namedtype.NamedType('info', char.PrintableString())
    )

class MonitorTargetInfo(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('channel',      char.PrintableString()),
        namedtype.NamedType('properties',   TargetProperties()),
        namedtype.NamedType('type',         TargetInfoType())
    )

class MonitorCreateTarget(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('ipAdd',        char.PrintableString()),
        namedtype.NamedType('permConf',     PermConf()),
        namedtype.NamedType('staticName',   char.PrintableString()),
        namedtype.NamedType('snmpv2ro',     char.PrintableString()),
        namedtype.NamedType('snmpv2rw',     char.PrintableString()),
        namedtype.NamedType('template',     char.PrintableString()),
        namedtype.NamedType('queryId',      univ.Integer())
    )

class MonitorCreateSimpleProbe(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('target',       char.PrintableString()),
        namedtype.NamedType('name',         char.PrintableString()),
        namedtype.NamedType('description',  char.PrintableString()),
        namedtype.NamedType('permConf',     PermConf()),
        namedtype.NamedType('template',     char.PrintableString()),
        namedtype.NamedType('timeout',      univ.Integer()),
        namedtype.NamedType('step',         univ.Integer()),
        namedtype.NamedType('flags',        Properties()),
        namedtype.NamedType('exe',          char.PrintableString()),
        namedtype.NamedType('queryId',      univ.Integer())
    )

class MonitorQuery(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('queryId',      univ.Integer()),
        namedtype.NamedType('query',        char.PrintableString())
    )


class MonitorReply(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('queryId',      univ.Integer()),
        namedtype.NamedType('status',       univ.Boolean()),
        namedtype.NamedType('info',         char.PrintableString())
    )

class CheckArg(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('flag',         char.PrintableString()),
        namedtype.NamedType('value',        char.PrintableString())
    )
class CheckArgs(univ.SequenceOf):
    componentType = CheckArg()

class MonitorSimulateCheck(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('queryId',      univ.Integer()),
        namedtype.NamedType('executable',   char.PrintableString()),
        namedtype.NamedType('args',         CheckArgs())
    )

class CheckInfos(univ.SequenceOf):
    componentType = univ.OctetString()

class GetCheckReply(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('queryId',      univ.Integer()),
        namedtype.NamedType('status',       univ.Boolean()),
        namedtype.NamedType('infos',        CheckInfos())
    )

class MonitorPDU_fromClient(univ.Choice):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType(
            'createTarget',
            MonitorCreateTarget().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext,
                    tag.tagFormatSimple,
                    1
                )
            )
        ),
        namedtype.NamedType(
            'createSimpleProbe',
            MonitorCreateSimpleProbe().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext,
                    tag.tagFormatSimple,
                    4
                )
            )
        ),
        namedtype.NamedType(
            'simulateCheck',
            MonitorSimulateCheck().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext,
                    tag.tagFormatSimple,
                    7
                )
            )
        ),
        namedtype.NamedType(
            'query',
            MonitorQuery().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext,
                    tag.tagFormatSimple,
                    10
                )
            )
        )
    )

class MonitorPDU_fromServer(univ.Choice):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType(
            'targetInfo',
            MonitorTargetInfo().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext,
                    tag.tagFormatSimple,
                    1
                )
            )
        ),
        namedtype.NamedType(
            'probeInfo',
            MonitorProbeInfo().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext,
                    tag.tagFormatSimple,
                    2
                )
            )
        ),
        namedtype.NamedType(
            'probeDump',
            MonitorProbeDump().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext,
                    tag.tagFormatSimple,
                    4
                )
            )
        ),
        namedtype.NamedType(
            'probeModInfo',
            MonitorProbeModuleInfo().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext,
                    tag.tagFormatSimple,
                    6
                )
            )
        ),
        namedtype.NamedType(
            'probeActivity',
            MonitorProbeActivity().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext,
                    tag.tagFormatSimple,
                    7
                )
            )
        ),
        namedtype.NamedType(
            'probeReturn',
            MonitorProbeReturn().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext,
                    tag.tagFormatSimple,
                    8
                )
            )
        ),
        namedtype.NamedType(
            'rrdFileDump',
            MonitorRrdFileDump().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext,
                    tag.tagFormatSimple,
                    9
                )
            )
        ),
        namedtype.NamedType(
            'eventProbeDump',
            MonitorEventProbeDump().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext,
                    tag.tagFormatSimple,
                    10 
                )
            )
        ),
        namedtype.NamedType(
            'probeEventMsg',
            MonitorProbeEvent().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext,
                    tag.tagFormatSimple,
                    11 
                )
            )
        ),
        namedtype.NamedType(
            'monitorReply',
            MonitorReply().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext,
                    tag.tagFormatSimple,
                    12
                )
            )
        ),
        namedtype.NamedType(
            'getCheckReply',
            GetCheckReply().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext,
                    tag.tagFormatSimple,
                    13
                )
            )
        )
    )

class MonitorPDU(univ.Choice):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType(
            'fromServer',
            MonitorPDU_fromServer().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext,
                    tag.tagFormatSimple,
                    0
                )
            )
        ),
        namedtype.NamedType(
            'fromClient',
            MonitorPDU_fromClient().subtype(
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

# subscribe messages
# from client
class SupercastSubscribe(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('queryId',  univ.Integer()),
        namedtype.NamedType('channel',  SupercastChan())
    )

class SupercastUnsubscribe(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('queryId',  univ.Integer()),
        namedtype.NamedType('channel',  SupercastChan())
    )

# from server
class SupercastUnsubscribeOk(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('queryId',  univ.Integer()),
        namedtype.NamedType('channel',  SupercastChan())
    )

class SupercastUnsubscribeErr(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('queryId',  univ.Integer()),
        namedtype.NamedType('channel',  SupercastChan())
    )

class SupercastSubscribeOk(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('queryId',  univ.Integer()),
        namedtype.NamedType('channel',  SupercastChan())
    )

class SupercastSubscribeErr(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('queryId',  univ.Integer()),
        namedtype.NamedType('channel',  SupercastChan())
    )



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
            SupercastSubscribeOk().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext,
                    tag.tagFormatSimple,
                    5
                )
            )
        ),
        namedtype.NamedType(
            'subscribeErr',
            SupercastSubscribeErr().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext,
                    tag.tagFormatSimple,
                    6
                )
            )
        ),
        namedtype.NamedType(
            'unsubscribeOk',
            SupercastUnsubscribeOk().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext,
                    tag.tagFormatSimple,
                    7
                )
            )
        ),
        namedtype.NamedType(
            'unsubscribeErr',
            SupercastUnsubscribeErr().subtype(
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
            SupercastSubscribe().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext,
                    tag.tagFormatSimple,
                    0
                )
            )
        ),
        namedtype.NamedType(
            'unsubscribe', 
            SupercastUnsubscribe().subtype(
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
            'modMonitorPDU'  , 
            MonitorPDU().subtype(
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
                queryId = msg3.getComponentByName('queryId')
                channel = msg3.getComponentByName('channel')
                return {
                    'from':     msg1_type,
                    'msgType':  msg3_type,
                    'queryId':  int(queryId),
                    'value':    str(channel)
                }
            elif msg3_type == 'subscribeOk':
                queryId = msg3.getComponentByName('queryId')
                channel = msg3.getComponentByName('channel')
                return {
                    'from':     msg1_type,
                    'msgType':  msg3_type,
                    'queryId':  int(queryId),
                    'value':    str(channel)
                }
            elif msg3_type == 'subscribeErr':
                queryId = msg3.getComponentByName('queryId')
                channel = msg3.getComponentByName('channel')
                return {
                    'from':     msg1_type,
                    'msgType':  msg3_type,
                    'queryId':  int(queryId),
                    'value':    str(channel)
                }
            elif msg3_type == 'unsubscribeErr':
                queryId = msg3.getComponentByName('queryId')
                channel = msg3.getComponentByName('channel')
                return {
                    'from':     msg1_type,
                    'msgType':  msg3_type,
                    'queryId':  int(queryId),
                    'value':    str(channel)
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
    elif msg1_type == 'modMonitorPDU':
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
                propDict    = dict()
                for i in range(len(infoProp)):
                    prop = infoProp.getComponentByPosition(i)
                    key  = str(prop.getComponentByName('key'))
                    val  = str(prop.getComponentByName('value'))
                    propDict[key] = val
                    

                if      infoType == 0: infoT = 'create'
                elif    infoType == 1: infoT = 'delete'
                elif    infoType == 2: infoT = 'update'
                else:   infoT = 'nothing'
                return {
                    'from':     msg1_type,
                    'msgType':  msg3_type,
                    'value':    {
                        'name':         targetId,
                        'properties':   propDict,
                        'infoType':     infoT
                    }
                }
            elif msg3_type == 'probeInfo':
                target      = str(msg3.getComponentByName('channel'))
                probeId     = msg3.getComponentByName('id')
                name        = str(msg3.getComponentByName('name'))
                descr       = str(msg3.getComponentByName('descr'))
                info        = str(msg3.getComponentByName('info'))
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
                        mod     = logger2.getComponentByName('module')
                        conf    = logger2.getComponentByName('conf')
                        loggersDict[str(mod)] = str(conf)
                    elif ltype == 'loggerEvents':
                        logger2 = logger.getComponent()
                        mod     = logger2.getComponentByName('module')
                        conf    = logger2.getComponentByName('conf')
                        loggersDict[str(mod)] = str(conf)
                    ####################
                    # IF LOGGER IS RRD #
                    ####################
                    elif ltype == 'loggerRrd':
                        logger2 = logger.getComponent()
                        mod     = logger2.getComponentByName('module')
                        rrdConfig = logger2.getComponentByName('config')

                        rrdConfigs = dict()
                        for confId in range(len(rrdConfig)):
                            rrdConf = rrdConfig.getComponentByPosition(confId)
                            rrdFileId = rrdConf.getComponentByName('file')
                            rrdCreate = rrdConf.getComponentByName('create')
                            rrdUpdate = rrdConf.getComponentByName('update')
                            rrdGraphs = rrdConf.getComponentByName('graphs')
                            rrdBinds  = rrdConf.getComponentByName('binds')
                            bindsD = dict()
                            for b in range(len(rrdBinds)):
                                bind = rrdBinds.getComponentByPosition(b)
                                rep  = bind.getComponentByName('replacement')
                                mac  = bind.getComponentByName('macro')
                                bindsD[str(rep)] = str(mac)

                            graphsL = list()
                            for g in range(len(rrdGraphs)):
                                graphItem = rrdGraphs.getComponentByPosition(g)
                                graphsL.append(str(graphItem))

                            rrdKey = str(rrdFileId)
                            rrdConfigs[rrdKey] = dict()
                            rrdConfigs[rrdKey]['create'] = str(rrdCreate)
                            rrdConfigs[rrdKey]['update'] = str(rrdUpdate)
                            rrdConfigs[rrdKey]['graphs'] = graphsL
                            rrdConfigs[rrdKey]['binds']  = bindsD

                        loggersDict[str(mod)] = rrdConfigs
                    ##########
                    # END IF #
                    ##########

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
                        'target':       target,
                        'id':           int(probeId),
                        'name':         name,
                        'descr':        descr,
                        'info':         info,
                        'perm':         permDict,
                        'probeMod':     probeMod,
                        'probeconf':    probeConf,
                        'status':       status,
                        'timeout':      int(timeout),
                        'step':         int(step),
                        'inspectors':   inspectorsDict,
                        'loggers':      loggersDict,
                        'properties':   propertiesDict,
                        'active':       int(active),
                        'infoType':     infoType.prettyPrint()
                    }
                }
            elif msg3_type == 'probeDump':
                channel     = str(msg3.getComponentByName('channel'))
                probeId     = str(msg3.getComponentByName('name'))
                module      = msg3.getComponentByName('module')
                binaryData  = msg3.getComponentByName('data')

                return {
                    'from': msg1_type,
                    'msgType':  msg3_type,
                    'value':    {
                        'target': channel,
                        'id':     probeId,
                        'logger': module,
                        'data':   str(binaryData)
                    }
                }
            elif msg3_type == 'probeEventMsg':
                probeName   = msg3.getComponentByName('probeName')
                eventId     = msg3.getComponentByName('eventId')
                insertTs    = msg3.getComponentByName('insertTs')
                ackTs       = msg3.getComponentByName('ackTs')
                status      = str(msg3.getComponentByName('status'))
                textual     = str(msg3.getComponentByName('textual'))
                ackNeeded   = msg3.getComponentByName('ackNeeded')
                ackValue    = str(msg3.getComponentByName('ackValue'))
                groupOwner  = str(msg3.getComponentByName('groupOwner'))
                userOwner   = str(msg3.getComponentByName('userOwner'))

                return {
                    'from': msg1_type,
                    'msgType':  msg3_type,
                    'value':    {
                        'id':           probeName,
                        'data': {
                            'eventId':      eventId,
                            'insertTs':     int(insertTs),
                            'ackTs':        int(ackTs),
                            'status':       status,
                            'textual':      textual,
                            'ackNeeded':    ackNeeded,
                            'ackValue':     ackValue,
                            'groupOwner':   groupOwner,
                            'userOwner':    userOwner
                        }
                    }
                }
            elif msg3_type == 'eventProbeDump':
                target      = str(msg3.getComponentByName('target'))
                probe       = str(msg3.getComponentByName('probe'))
                module      = str(msg3.getComponentByName('module'))
                events      = msg3.getComponentByName('events')
                
                eventsList = list()
                for i in range(len(events)):
                    anEvent     = events.getComponentByPosition(i)
                    eventId     = anEvent.getComponentByName('eventId')
                    insertTs    = anEvent.getComponentByName('insertTs')
                    ackTs       = anEvent.getComponentByName('ackTs')
                    status      = str(anEvent.getComponentByName('status'))
                    textual     = str(anEvent.getComponentByName('textual'))
                    ackNeeded   = anEvent.getComponentByName('ackNeeded')
                    ackValue    = str(anEvent.getComponentByName('ackValue'))
                    groupOwner  = str(anEvent.getComponentByName('groupOwner'))
                    userOwner   = str(anEvent.getComponentByName('userOwner'))
                    eventDict = {
                        'eventId':      eventId,
                        'insertTs':     int(insertTs),
                        'ackTs':        int(ackTs),
                        'status':       status,
                        'textual':      textual,
                        'ackNeeded':    ackNeeded,
                        'ackValue':     ackValue,
                        'groupOwner':   groupOwner,
                        'userOwner':    userOwner}
                    eventsList.append(eventDict)
                return {
                    'from': msg1_type,
                    'msgType':  msg3_type,
                    'value':    {
                        'target': target,
                        'id':     probe,
                        'logger': module,
                        'data':   eventsList
                    }
                }
            elif msg3_type == 'rrdFileDump':
                target      = str(msg3.getComponentByName('target'))
                probeName   = str(msg3.getComponentByName('probeName'))
                fileId      = str(msg3.getComponentByName('fileId'))
                module      = str(msg3.getComponentByName('module'))
                binFile     = msg3.getComponentByName('bin')

                return {
                    'from':     msg1_type,
                    'msgType':  msg3_type,
                    'value':    {
                        'target':   target,
                        'id':       probeName,
                        'logger':   module,
                        'fileId':   fileId,
                        'data':     binFile
                    }
                }
            elif msg3_type == 'probeActivity':
                target      = str(msg3.getComponentByName('target'))
                probeName   = msg3.getComponentByName('probeName')
                time        = msg3.getComponentByName('timestamp')
                probeState  = str(msg3.getComponentByName('probeState'))
                returnStatus = str(msg3.getComponentByName('returnStatus'))
                textual     = str(msg3.getComponentByName('textual'))
                return {
                    'from': msg1_type,
                    'msgType':  msg3_type,
                    'value':    {
                        'target':       target,
                        'name':         probeName,
                        'timestamp':    int(time),
                        'probeState':   probeState,
                        'returnStatus': returnStatus,
                        'textual':      textual

                    }
                }
            elif msg3_type == 'probeReturn':
                target      = str(msg3.getComponentByName('target'))
                probeId     = str(msg3.getComponentByName('id'))
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
                        'target':       target,
                        'id':           probeId,
                        'status':       status,
                        'originalRep':  original_rep,
                        'timestamp':    int(timestamp),
                        'keyVals':      keyValsDict
                    }
                }
            elif msg3_type == 'monitorReply':
                queryId = int(msg3.getComponentByName('queryId'))
                status  = bool(msg3.getComponentByName('status'))
                info    = str(msg3.getComponentByName('info'))
                return {
                    'from':     'monitorReply',
                    'queryId':  queryId,
                    'value': {
                        'status':   status,
                        'info':     info
                    }
                }
            elif msg3_type == 'getCheckReply':
                queryId = int(msg3.getComponentByName('queryId'))
                status  = bool(msg3.getComponentByName('status'))
                infos   = msg3.getComponentByName('infos')
                infoList = list()
                for i in range(len(infos)):
                    info = str(infos.getComponentByPosition(i))
                    infoList.append(info)

                return {
                    'from':     'getCheckReply',
                    'queryId':  queryId,
                    'value': {
                        'status':   status,
                        'infos':    infoList
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


def encode(pduType, payload):
    if   pduType == 'subscribe':
        (queryId, channel) = payload
        return encode_subscribe(queryId, channel)
    elif pduType == 'unsubscribe':
        (queryId, channel) = payload
        return encode_unsubscribe(queryId, channel)
    elif pduType == 'authResp':
        (userId, password) = payload
        return encode_authResp(userId, password)
    elif pduType == 'monitorCreateTarget':
        (queryId, msg)          = payload
        (ip, perms, n, ro, rw, tpl) = msg
        return encode_create_target(ip, perms, n, ro, rw, tpl, queryId)
    elif pduType == 'query':
        (queryId, queryString) = payload
        return encode_query(queryId, queryString)
    elif pduType == 'monitorSimulateCheck':
        (queryId, checkConf) = payload
        return encode_simulateCheck(queryId, checkConf)
    elif pduType == 'monitorCreateSimpleProbe':
        (queryId, args) = payload
        return encode_createSimpleProbe(queryId, args)
    else:
        return False


def encode_simulateCheck(queryId, checkConfig):
    (path, args) = checkConfig
    argsP  = CheckArgs()
    for i in range(len(args)):
        (flag, val) = args[i]
        argP = CheckArg()
        argP.setComponentByName('flag',   flag)
        argP.setComponentByName('value', val)
        argsP.setComponentByPosition(i, argP)

    checkP = MonitorSimulateCheck().subtype(
        implicitTag=tag.Tag(
            tag.tagClassContext,
            tag.tagFormatSimple,
            7
        )
    )
    checkP.setComponentByName('queryId',    queryId)
    checkP.setComponentByName('executable', path)
    checkP.setComponentByName('args',       argsP)

    fromClient = MonitorPDU_fromClient().subtype(
        implicitTag=tag.Tag(
            tag.tagClassContext,
            tag.tagFormatSimple,
            1
        )
    )

    fromClient.setComponentByName('simulateCheck', checkP)

    monitorPDU = MonitorPDU().subtype(
        implicitTag=tag.Tag(
            tag.tagClassContext,
            tag.tagFormatSimple,
            2
        )
    )
    monitorPDU.setComponentByName('fromClient', fromClient)

    pduDef = NmsPDU()
    pduDef.setComponentByName('modMonitorPDU', monitorPDU)

    pdu = encoder.encode(pduDef)
    return pdu

def encode_query(queryId, queryString):
    query = MonitorQuery().subtype(
        implicitTag=tag.Tag(
            tag.tagClassContext,
            tag.tagFormatSimple,
            10
        )
    )
    query.setComponentByName('queryId', queryId)
    query.setComponentByName('query',   queryString)

    fromClient = MonitorPDU_fromClient().subtype(
        implicitTag=tag.Tag(
            tag.tagClassContext,
            tag.tagFormatSimple,
            1
        )
    )
    fromClient.setComponentByName('query', query)

    monitorPDU = MonitorPDU().subtype(
        implicitTag=tag.Tag(
            tag.tagClassContext,
            tag.tagFormatSimple,
            2
        )
    )
    monitorPDU.setComponentByName('fromClient', fromClient)

    pduDef = NmsPDU()
    pduDef.setComponentByName('modMonitorPDU', monitorPDU)

    pdu = encoder.encode(pduDef)
    return pdu

def encode_createSimpleProbe(queryId, args):
    (tname, pname, descr, perms, tpl, timeout, step, flags, exe) = args

    (read, write)   = perms
    readGroups      = Groups()
    for i in range(len(read)):
        readGroups.setComponentByPosition(i, read[i])
    writeGroups     = Groups()
    for i in range(len(write)):
        writeGroups.setComponentByPosition(i, write[i])

    permConf      = PermConf()
    permConf.setComponentByName('read',         readGroups)
    permConf.setComponentByName('write',        writeGroups)

    fprops = Properties()
    for i in range(len(flags)):
        (f, v) = flags[i]
        fprop = Property()
        fprop.setComponentByName('key', f)
        fprop.setComponentByName('value', v)
        fprops.setComponentByPosition(i, fprop)


    createSP = MonitorCreateSimpleProbe().subtype(
        implicitTag=tag.Tag(
            tag.tagClassContext,
            tag.tagFormatSimple,
            4
        )
    )

    createSP.setComponentByName('target',   tname)
    createSP.setComponentByName('name',     pname)
    createSP.setComponentByName('description',  descr)
    createSP.setComponentByName('permConf', permConf)
    createSP.setComponentByName('template', tpl)
    createSP.setComponentByName('timeout',  int(timeout))
    createSP.setComponentByName('step',     int(step))
    createSP.setComponentByName('flags',    fprops)
    createSP.setComponentByName('exe',      exe)
    createSP.setComponentByName('queryId',  queryId)

    fromClient = MonitorPDU_fromClient().subtype(
        implicitTag=tag.Tag(
            tag.tagClassContext,
            tag.tagFormatSimple,
            1
        )
    )
    fromClient.setComponentByName('createSimpleProbe', createSP)

    monitorPDU = MonitorPDU().subtype(
        implicitTag=tag.Tag(
            tag.tagClassContext,
            tag.tagFormatSimple,
            2
        )
    )
    monitorPDU.setComponentByName('fromClient', fromClient)

    pduDef = NmsPDU()
    pduDef.setComponentByName('modMonitorPDU', monitorPDU)

    pdu = encoder.encode(pduDef)
    return pdu

def encode_create_target(ip, perms, name, ro, rw, tpl, queryId):
    (read, write)   = perms
    readGroups      = Groups()
    for i in range(len(read)):
        readGroups.setComponentByPosition(i, read[i])
    writeGroups     = Groups()
    for i in range(len(write)):
        writeGroups.setComponentByPosition(i, write[i])

    targetConf      = PermConf()
    targetConf.setComponentByName('read',         readGroups)
    targetConf.setComponentByName('write',        writeGroups)

    targetCreate = MonitorCreateTarget().subtype(
        implicitTag=tag.Tag(
            tag.tagClassContext,
            tag.tagFormatSimple,
            1
        )
    )
    targetCreate.setComponentByName('ipAdd',    ip)
    targetCreate.setComponentByName('permConf', targetConf)
    targetCreate.setComponentByName('staticName', name)
    targetCreate.setComponentByName('snmpv2ro', ro)
    targetCreate.setComponentByName('snmpv2rw', rw)
    targetCreate.setComponentByName('template', tpl)
    targetCreate.setComponentByName('queryId',  queryId)

    fromClient = MonitorPDU_fromClient().subtype(
        implicitTag=tag.Tag(
            tag.tagClassContext,
            tag.tagFormatSimple,
            1
        )
    )
    fromClient.setComponentByName('createTarget', targetCreate)

    monitorPDU = MonitorPDU().subtype(
        implicitTag=tag.Tag(
            tag.tagClassContext,
            tag.tagFormatSimple,
            2
        )
    )
    monitorPDU.setComponentByName('fromClient', fromClient)

    pduDef = NmsPDU()
    pduDef.setComponentByName('modMonitorPDU', monitorPDU)

    pdu = encoder.encode(pduDef)
    return pdu


def encode_unsubscribe(queryId, chanString):
    #chan = SupercastChan(chanString).subtype(
        #implicitTag=tag.Tag(
            #tag.tagClassContext,
            #tag.tagFormatSimple,
            #1
        #)
    #)
    unsubscribe = SupercastUnsubscribe().subtype(
        implicitTag=tag.Tag(
            tag.tagClassContext,
            tag.tagFormatSimple,
            1
        )
    )
    unsubscribe.setComponentByName('queryId', univ.Integer(queryId))
    unsubscribe.setComponentByName('channel', char.PrintableString(chanString))

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

    fromClient.setComponentByName('unsubscribe', unsubscribe)
    supercastPDU.setComponentByName('fromClient', fromClient)
    pduDef.setComponentByName('modSupercastPDU', supercastPDU)
    pdu = encoder.encode(pduDef)
    return pdu

def encode_subscribe(queryId, chanString):
    subscribe = SupercastSubscribe().subtype(
        implicitTag=tag.Tag(
            tag.tagClassContext,
            tag.tagFormatSimple,
            0
        )
    )
    subscribe.setComponentByName('queryId', univ.Integer(queryId))
    subscribe.setComponentByName('channel', char.PrintableString(chanString))

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

    fromClient.setComponentByName('subscribe', subscribe)
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
