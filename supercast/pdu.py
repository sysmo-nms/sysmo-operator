from pyasn1.type        import char,univ,namedtype,tag,namedval,constraint
from pyasn1.codec.ber   import encoder, decoder

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

class RrdGraphs(univ.SequenceOf):
    componentType = char.PrintableString()

class RrdIndexes(univ.SequenceOf):
    componentType = univ.Integer()

class LoggerRrd2(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('module',   char.PrintableString()),
        namedtype.NamedType('type',     char.PrintableString()),
        namedtype.NamedType('rrdCreate',char.PrintableString()),
        namedtype.NamedType('rrdUpdate',char.PrintableString()),
        namedtype.NamedType('rrdGraphs',RrdGraphs()),
        namedtype.NamedType('indexes',  RrdIndexes())
    )


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
        ),
        namedtype.NamedType(
            'loggerRrd2',
            LoggerRrd2().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext,
                    tag.tagFormatSimple,
                    3
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

class InfoProbeType(univ.Enumerated):
    namedValues = namedval.NamedValues(
        ('create', 0),
        ('delete', 1),
        ('update', 2)
    )

class InfoTargetType(univ.Enumerated):
    namedValues = namedval.NamedValues(
        ('create', 0),
        ('delete', 1),
        ('update', 2)
    )

class LoggerRrdIdToFile(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('index',   univ.Integer()),
        namedtype.NamedType('fileName',    char.PrintableString())
    )

class LoggerRrdIdToFileSeq(univ.SequenceOf):
    componentType = LoggerRrdIdToFile()

class MonitorLoggerRrdDump(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('target',   char.PrintableString()),
        namedtype.NamedType('probe',    char.PrintableString()),
        namedtype.NamedType('module',   char.PrintableString()),
        namedtype.NamedType('indexes',  LoggerRrdIdToFileSeq()),
        namedtype.NamedType('path',     char.PrintableString())
    )

class LoggerRrdUpdate(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('index',   univ.Integer()),
        namedtype.NamedType('update',  char.PrintableString())
    )

class LoggerRrdUpdates(univ.SequenceOf):
    componentType = LoggerRrdUpdate()

class MonitorLoggerRrdEvent(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('target',       char.PrintableString()),
        namedtype.NamedType('probeName',    char.PrintableString()),
        namedtype.NamedType('updates',      LoggerRrdUpdates())
    )

class MonitorProbeDump(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('channel',  char.PrintableString()),
        namedtype.NamedType('name',     char.PrintableString()),
        namedtype.NamedType('module',   char.PrintableString()),
        namedtype.NamedType('data',     univ.OctetString()),
    )

class MonitorInfoProbe(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('channel',  char.PrintableString()),
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
        namedtype.NamedType('infoType', InfoProbeType())
    )

class MonitorProbeReturn(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('target',       char.PrintableString()),
        namedtype.NamedType('id',           char.PrintableString()),
        namedtype.NamedType('status',       char.PrintableString()),
        namedtype.NamedType('originalReply', char.PrintableString()),
        namedtype.NamedType('timestamp',    univ.Integer()),
        namedtype.NamedType('keyVals',      TargetProbeReturnKeyVals()),
        namedtype.NamedType('nextReturn',   univ.Integer())
    )

class MonitorInfoTarget(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('channel',          char.PrintableString()),
        namedtype.NamedType('properties',       TargetProperties()),
        namedtype.NamedType('sysProperties',    TargetProperties()),
        namedtype.NamedType('type',             InfoTargetType())
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







# extendedquery msg BEGIN
class IpInfo(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('version',      char.PrintableString()),
        namedtype.NamedType('stringVal',    char.PrintableString())
    )


class IfSelection(univ.SequenceOf):
    componentType = univ.Integer()

class SnmpElementCreateQuery(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('ip',           IpInfo()),
        namedtype.NamedType('port',         univ.Integer()),
        namedtype.NamedType('timeout',      univ.Integer()),
        namedtype.NamedType('snmpVer',      char.PrintableString()),
        namedtype.NamedType('community',    char.PrintableString()),
        namedtype.NamedType('v3SecLevel',   char.PrintableString()),
        namedtype.NamedType('v3User',       char.PrintableString()),
        namedtype.NamedType('v3AuthAlgo',   char.PrintableString()),
        namedtype.NamedType('v3AuthKey',    char.PrintableString()),
        namedtype.NamedType('v3PrivAlgo',   char.PrintableString()),
        namedtype.NamedType('v3PrivKey',    char.PrintableString()),
        namedtype.NamedType('ifSelection',  IfSelection()),
    )


class SnmpElementInfoQuery(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('ip',           IpInfo()),
        namedtype.NamedType('port',         univ.Integer()),
        namedtype.NamedType('timeout',      univ.Integer()),
        namedtype.NamedType('snmpVer',      char.PrintableString()),
        namedtype.NamedType('community',    char.PrintableString()),
        namedtype.NamedType('v3SecLevel',   char.PrintableString()),
        namedtype.NamedType('v3User',       char.PrintableString()),
        namedtype.NamedType('v3AuthAlgo',   char.PrintableString()),
        namedtype.NamedType('v3AuthKey',    char.PrintableString()),
        namedtype.NamedType('v3PrivAlgo',   char.PrintableString()),
        namedtype.NamedType('v3PrivKey',    char.PrintableString())
    )

class CreateTargetQuery(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('sysProperties', Properties()),
        namedtype.NamedType('properties',    Properties())
    )

class MonitorExtendedQueryFromClient(univ.Choice):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType(
            'snmpElementInfoQuery',
            SnmpElementInfoQuery().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext,
                    tag.tagFormatSimple,
                    0
                )
            )
        ),
        namedtype.NamedType(
            'snmpElementCreateQuery',
            SnmpElementCreateQuery().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext,
                    tag.tagFormatSimple,
                    1
                )
            )
        ),
        namedtype.NamedType(
            'createTargetQuery',
            CreateTargetQuery().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext,
                    tag.tagFormatSimple,
                    10
                )
            )
        )
    )

class MonitorExtendedQueryFromClientMsg(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('queryId',      univ.Integer()),
        namedtype.NamedType('query',        MonitorExtendedQueryFromClient())
    )
# extendedquery msg END






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

class SnmpSystemInfo(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('sysDescr',     char.PrintableString()),
        namedtype.NamedType('sysObjectId',  char.PrintableString()),
        namedtype.NamedType('sysUpTime',    char.PrintableString()),
        namedtype.NamedType('sysContact',   char.PrintableString()),
        namedtype.NamedType('sysName',      char.PrintableString()),
        namedtype.NamedType('sysLocation',  char.PrintableString()),
        namedtype.NamedType('sysServices',  univ.Integer()),
        namedtype.NamedType('sysORLastChange', char.PrintableString())
    )

class SnmpInterfaceInfo(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('ifIndex',      univ.Integer()),
        namedtype.NamedType('ifDescr',      char.PrintableString()),
        namedtype.NamedType('ifType',       univ.Integer()),
        namedtype.NamedType('ifMTU',        univ.Integer()),
        namedtype.NamedType('ifSpeed',      univ.Integer()),
        namedtype.NamedType('ifPhysAddress',char.PrintableString()),
        namedtype.NamedType('ifAdminStatus',univ.Integer()),
        namedtype.NamedType('ifOperStatus', univ.Integer()),
        namedtype.NamedType('ifLastChange', char.PrintableString())
    )

class SnmpInterfacesInfo(univ.SequenceOf):
    componentType = SnmpInterfaceInfo()

class ReplyChoice(univ.Choice):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType(
            'string',
            char.PrintableString().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext,
                    tag.tagFormatSimple,
                    0
                )
            )
        ),
        namedtype.NamedType(
            'snmpSystemInfo',
            SnmpSystemInfo().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext,
                    tag.tagFormatSimple,
                    1
                )
            )
        ),
        namedtype.NamedType(
            'snmpInterfacesInfo',
            SnmpInterfacesInfo().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext,
                    tag.tagFormatSimple,
                    2
                )
            )
        )
    )

class MonitorExtendedReply(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('queryId',      univ.Integer()),
        namedtype.NamedType('status',       univ.Boolean()),
        namedtype.NamedType('lastPdu',      univ.Boolean()),
        namedtype.NamedType('reply',        ReplyChoice())
    )

class MonitorDeleteProbe(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('target',      char.PrintableString()),
        namedtype.NamedType('probe',       char.PrintableString())
    )

class MonitorPDU_fromClient(univ.Choice):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType(
            'extendedQueryFromClient',
            MonitorExtendedQueryFromClient().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext,
                    tag.tagFormatSimple,
                    20
                )
            )
        )
    )

class MonitorPDU_fromServer(univ.Choice):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType(
            'infoTarget',
            MonitorInfoTarget().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext,
                    tag.tagFormatSimple,
                    1
                )
            )
        ),
        namedtype.NamedType(
            'infoProbe',
            MonitorInfoProbe().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext,
                    tag.tagFormatSimple,
                    2
                )
            )
        ),
        namedtype.NamedType(
            'probeReturn',
            MonitorProbeReturn().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext,
                    tag.tagFormatSimple,
                    3
                )
            )
        ),
        namedtype.NamedType(
            'deleteTarget',
            char.PrintableString().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext,
                    tag.tagFormatSimple,
                    5
                )
            )
        ),
        namedtype.NamedType(
            'deleteProbe',
            MonitorDeleteProbe().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext,
                    tag.tagFormatSimple,
                    6
                )
            )
        ),


       namedtype.NamedType(
            'extendedReply',
            MonitorExtendedReply().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext,
                    tag.tagFormatSimple,
                    12
                )
            )
        ),
        namedtype.NamedType(
            'loggerRrdDump',
            MonitorLoggerRrdDump().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext,
                    tag.tagFormatSimple,
                    20
                )
            )
        ),
        namedtype.NamedType(
            'loggerRrdEvent',
            MonitorLoggerRrdEvent().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext,
                    tag.tagFormatSimple,
                    21
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

class SupercastServerInfo(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('authProto',    char.PrintableString()),
        namedtype.NamedType('dataPort',     univ.Integer()),
        namedtype.NamedType('dataProto',    char.PrintableString())
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
            'serverInfo',
            #SupercastAuthProto().subtype(
            SupercastServerInfo().subtype(
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
            elif msg3_type == 'serverInfo':
                #if      msg3 == 0: authProto = 'localFile'
                #elif    msg3 == 1: authProto = 'ldap'
                authProto   = msg3.getComponentByName('authProto')
                dataPort    = msg3.getComponentByName('dataPort')
                dataProto   = msg3.getComponentByName('dataProto')
                return {
                    'from':     msg1_type,
                    'msgType':  msg3_type,
                    'dataPort': int(dataPort),
                    'dataProto': str(dataProto),
                    'authProto': str(authProto)
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
            if msg3_type == 'infoTarget':
                targetId    = str(msg3.getComponentByName('channel'))
                infoType    = msg3.getComponentByName('type')
                infoProp    = msg3.getComponentByName('properties')
                infoSysProp = msg3.getComponentByName('sysProperties')
                propDict    = dict()
                for i in range(len(infoProp)):
                    prop = infoProp.getComponentByPosition(i)
                    key  = str(prop.getComponentByName('key'))
                    val  = str(prop.getComponentByName('value'))
                    propDict[key] = val
                    
                sysPropDict = dict()
                for i in range(len(infoSysProp)):
                    prop = infoSysProp.getComponentByPosition(i)
                    key  = str(prop.getComponentByName('key'))
                    val  = str(prop.getComponentByName('value'))
                    sysPropDict[key] = val
 

                if      infoType == 0: infoT = 'create'
                elif    infoType == 1: infoT = 'delete'
                elif    infoType == 2: infoT = 'update'
                return {
                    'from':     msg1_type,
                    'msgType':  msg3_type,
                    'value':    {
                        'name':             targetId,
                        'properties':       propDict,
                        'sysProperties':    sysPropDict,
                        'infoType':         infoT
                    }
                }
            elif msg3_type == 'infoProbe':
                target      = str(msg3.getComponentByName('channel'))
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
                    elif ltype == 'loggerRrd2':
                        logger2 = logger.getComponent()
                        mod     = logger2.getComponentByName('module')

                        rtype   = logger2.getComponentByName('type')
                        rcreate = logger2.getComponentByName('rrdCreate')
                        rupdate = logger2.getComponentByName('rrdUpdate')
                        indexes = logger2.getComponentByName('indexes')
                        idxs = []
                        for i in range(len(indexes)):
                            idx = int(indexes.getComponentByPosition(i))
                            idxs.append(idx)

                        rgraphs = logger2.getComponentByName('rrdGraphs')
                        rrdGraphs = dict()
                        for i in range(len(rgraphs)):
                            graph = rgraphs.getComponentByPosition(i)
                            rrdGraphs[i] = str(graph)

                        rrdConfigs = dict()

                        rrdConfigs['type']      = str(rtype)
                        rrdConfigs['rrdCreate'] = str(rcreate)
                        rrdConfigs['rrdUpdate'] = str(rupdate)
                        rrdConfigs['rgraphs']   = rrdGraphs
                        rrdConfigs['indexes']   = idxs

                        loggersDict[str(mod)] = rrdConfigs

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
                    'from':     msg1_type,
                    'msgType':  msg3_type,
                    'value':    {
                        'target':       target,
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
            elif msg3_type == 'loggerRrdDump':
                target      = str(msg3.getComponentByName('target'))
                probeName   = str(msg3.getComponentByName('probe'))
                module      = str(msg3.getComponentByName('module'))
                path        = str(msg3.getComponentByName('path'))
                indexes     = msg3.getComponentByName('indexes')

                indexesDict = dict()
                for i in range(len(indexes)):
                    indexEntry  = indexes.getComponentByPosition(i)
                    index       = int(indexEntry.getComponentByName('index'))
                    fileName    = str(indexEntry.getComponentByName('fileName'))
                    indexesDict[index] = fileName

                return {
                    'from': msg1_type,
                    'msgType': msg3_type,
                    'value': {
                        'target':   target,
                        'id':       probeName,
                        'logger':   module,
                        'data':     None,
                        'path':     path,
                        'indexes':  indexesDict
                    }
                }

            elif msg3_type == 'loggerRrdEvent':
                target      = str(msg3.getComponentByName('target'))
                probeName   = str(msg3.getComponentByName('probeName'))
                updates     = msg3.getComponentByName('updates')

                updatesDict = dict()
                for i in range(len(updates)):
                    rrdUpdate   = updates.getComponentByPosition(i)
                    index       = int(rrdUpdate.getComponentByName('index'))
                    update      = str(rrdUpdate.getComponentByName('update'))
                    updatesDict[index] = update
                
                return {
                    'from':     msg1_type,
                    'msgType':  msg3_type,
                    'value':    {
                        'target':   target,
                        'id':       probeName,
                        'updates':  updatesDict
                    }
                }
            elif msg3_type == 'probeReturn':
                target      = str(msg3.getComponentByName('target'))
                probeId     = str(msg3.getComponentByName('id'))
                status      = str(msg3.getComponentByName('status'))
                original_rep = str(msg3.getComponentByName('originalReply'))
                timestamp   = int(msg3.getComponentByName('timestamp'))
                keyVals     = msg3.getComponentByName('keyVals')
                nextReturn  = int(msg3.getComponentByName('nextReturn'))

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
                        'timestamp':    timestamp,
                        'keyVals':      keyValsDict,
                        'nextReturn':   nextReturn
                    }
                }

            elif msg3_type == 'deleteTarget':
                target = str(msg3)
                return {
                    'from': msg1_type,
                    'msgType':  msg3_type,
                    'value':    {
                        'name': target
                    }
                }
            elif msg3_type == 'deleteProbe':
                probe = str(msg3.getComponentByName('probe'))
                target = str(msg3.getComponentByName('target'))
                return {
                    'from': msg1_type,
                    'msgType':  msg3_type,
                    'value':    {
                        'name': probe,
                        'target': target
                    }
                }

            elif msg3_type == 'extendedReply':
                queryId = int(msg3.getComponentByName('queryId'))
                status  = bool(msg3.getComponentByName('status'))
                lastPdu = bool(msg3.getComponentByName('lastPdu'))

                reply   = msg3.getComponentByName('reply')
                rep     = reply.getComponent()
                repType = reply.getName()

                if repType == 'string':
                    replyPayload = str(rep)
                elif repType == 'snmpSystemInfo':
                    replyPayload = dict()
                    replyPayload['sysDescr']        = str(rep.getComponentByName('sysDescr'))
                    replyPayload['sysObjectId']     = str(rep.getComponentByName('sysObjectId'))
                    replyPayload['sysUpTime']       = str(rep.getComponentByName('sysUpTime'))
                    replyPayload['sysContact']      = str(rep.getComponentByName('sysContact'))
                    replyPayload['sysName']         = str(rep.getComponentByName('sysName'))
                    replyPayload['sysLocation']     = str(rep.getComponentByName('sysLocation'))
                    replyPayload['sysServices']      = int(rep.getComponentByName('sysServices'))
                    replyPayload['sysORLastChange'] = str(rep.getComponentByName('sysORLastChange'))
                elif repType == 'snmpInterfacesInfo':
                    replyPayload = list()
                    for i in range(len(rep)):
                        element = rep.getComponentByPosition(i)
                        anIf = dict()
                        anIf['ifIndex'] = int(element.getComponentByName('ifIndex'))
                        anIf['ifDescr'] = str(element.getComponentByName('ifDescr'))
                        anIf['ifType']  = int(element.getComponentByName('ifType'))
                        anIf['ifMTU']   = int(element.getComponentByName('ifMTU'))
                        anIf['ifSpeed'] = int(element.getComponentByName('ifSpeed'))
                        anIf['ifPhysaddress'] = str(element.getComponentByName('ifPhysAddress'))
                        anIf['ifAdminStatus'] = int(element.getComponentByName('ifAdminStatus'))
                        anIf['ifOperStatus'] = int(element.getComponentByName('ifOperStatus'))
                        anIf['ifLastChange'] = str(element.getComponentByName('ifLastChange'))
                        replyPayload.append(anIf)

                return {
                    'from':     'extendedReply',
                    'queryId':  queryId,
                    'lastPdu':  lastPdu,
                    'value': {
                            'status':       status,
                            'lastPdu':      lastPdu,
                            'replyType':    repType,
                            'reply':        replyPayload
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
    elif pduType == 'monitorSnmpElementInfoQuery':
        (queryId, args) = payload
        return encode_monitorSnmpElementInfoQuery(queryId, args)
    elif pduType == 'monitorSnmpElementCreateQuery':
        (queryId, args) = payload
        return encode_monitorSnmpElementCreateQuery(queryId, args)
    elif pduType == 'monitorCreateTargetQuery':
        (queryId, args) = payload
        return encode_monitorCreateTargetQuery(queryId, args)
    else:
        print "Cannont encode PDU: ", pduType
        return False

def encode_monitorSnmpElementCreateQuery(queryId, args):
    (ipv, ip, port, timeout, snmpVer, community, v3SecL, v3User, 
            v3AuthAlg, v3AuthKey, v3PrivAlg, v3PrivKey,ifSelection) = args
    ipinfo = IpInfo()
    ipinfo.setComponentByName('version', ipv)
    ipinfo.setComponentByName('stringVal', ip)

    snmpElementCreateQuery = SnmpElementCreateQuery().subtype(
        implicitTag=tag.Tag(
            tag.tagClassContext,
            tag.tagFormatSimple,
            1
        )
    )
    snmpElementCreateQuery.setComponentByName('ip',         ipinfo)
    snmpElementCreateQuery.setComponentByName('port',       int(port))
    snmpElementCreateQuery.setComponentByName('timeout',    int(timeout))
    snmpElementCreateQuery.setComponentByName('snmpVer',    snmpVer)
    snmpElementCreateQuery.setComponentByName('community',  community)
    snmpElementCreateQuery.setComponentByName('v3SecLevel', v3SecL)
    snmpElementCreateQuery.setComponentByName('v3User',     v3User)
    snmpElementCreateQuery.setComponentByName('v3AuthAlgo', v3AuthAlg)
    snmpElementCreateQuery.setComponentByName('v3AuthKey',  v3AuthKey)
    snmpElementCreateQuery.setComponentByName('v3PrivAlgo', v3PrivAlg)
    snmpElementCreateQuery.setComponentByName('v3PrivKey',  v3PrivKey)
    ifSel = IfSelection()
    for i in range(len(ifSelection)):
        ifSel.setComponentByPosition(i, ifSelection[i])
    snmpElementCreateQuery.setComponentByName('ifSelection',    ifSel)

    extendedQuery   = MonitorExtendedQueryFromClient()
    extendedQuery.setComponentByName('snmpElementCreateQuery', snmpElementCreateQuery)

    extendedQueryFromClient = MonitorExtendedQueryFromClientMsg().subtype(
        implicitTag=tag.Tag(
            tag.tagClassContext,
            tag.tagFormatSimple,
            20
        )
    )
    extendedQueryFromClient.setComponentByName('queryId', queryId)
    extendedQueryFromClient.setComponentByName('query',   extendedQuery)

    fromClient = MonitorPDU_fromClient().subtype(
        implicitTag=tag.Tag(
            tag.tagClassContext,
            tag.tagFormatSimple,
            1
        )
    )
    fromClient.setComponentByName('extendedQueryFromClient', extendedQueryFromClient)

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

def encode_monitorCreateTargetQuery(queryId, args):
    (sysProps, props) = args
    createQuery = CreateTargetQuery().subtype(
        implicitTag=tag.Tag(
            tag.tagClassContext,
            tag.tagFormatSimple,
            10
        )
    )

    propList  = Properties()
    i = 0
    for key in props.keys():
        p = Property()
        p.setComponentByName('key', key)
        p.setComponentByName('value', props[key])
        propList.setComponentByPosition(i, p)
        i = i+1

    spropList = Properties()
    i = 0
    for key in sysProps.keys():
        p = Property()
        p.setComponentByName('key', key)
        p.setComponentByName('value', sysProps[key])
        spropList.setComponentByPosition(i, p)
        i = i+1

    createQuery.setComponentByName('sysProperties',   spropList)
    createQuery.setComponentByName('properties',      propList)

    extendedQuery = MonitorExtendedQueryFromClient()
    extendedQuery.setComponentByName('createTargetQuery', createQuery)

    extendedQueryFromClient = MonitorExtendedQueryFromClientMsg().subtype(
        implicitTag=tag.Tag(
            tag.tagClassContext,
            tag.tagFormatSimple,
            20
        )
    )
    extendedQueryFromClient.setComponentByName('queryId', queryId)
    extendedQueryFromClient.setComponentByName('query',   extendedQuery)

    fromClient = MonitorPDU_fromClient().subtype(
        implicitTag=tag.Tag(
            tag.tagClassContext,
            tag.tagFormatSimple,
            1
        )
    )
    fromClient.setComponentByName('extendedQueryFromClient', extendedQueryFromClient)

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




def encode_monitorSnmpElementInfoQuery(queryId, args):
    (ipv, ip, port, timeout, snmpVer, community, v3SecL, v3User, 
            v3AuthAlg, v3AuthKey, v3PrivAlg, v3PrivKey) = args
    ipinfo = IpInfo()
    ipinfo.setComponentByName('version', ipv)
    ipinfo.setComponentByName('stringVal', ip)

    snmpElementInfoQuery = SnmpElementInfoQuery().subtype(
        implicitTag=tag.Tag(
            tag.tagClassContext,
            tag.tagFormatSimple,
            0
        )
    )
    snmpElementInfoQuery.setComponentByName('ip',       ipinfo)
    snmpElementInfoQuery.setComponentByName('port',     int(port))
    snmpElementInfoQuery.setComponentByName('timeout',  int(timeout))
    snmpElementInfoQuery.setComponentByName('snmpVer',  snmpVer)
    snmpElementInfoQuery.setComponentByName('community',community)
    snmpElementInfoQuery.setComponentByName('v3SecLevel',   v3SecL)
    snmpElementInfoQuery.setComponentByName('v3User',       v3User)
    snmpElementInfoQuery.setComponentByName('v3AuthAlgo',   v3AuthAlg)
    snmpElementInfoQuery.setComponentByName('v3AuthKey',    v3AuthKey)
    snmpElementInfoQuery.setComponentByName('v3PrivAlgo',   v3PrivAlg)
    snmpElementInfoQuery.setComponentByName('v3PrivKey',    v3PrivKey)

    extendedQuery   = MonitorExtendedQueryFromClient()
    extendedQuery.setComponentByName('snmpElementInfoQuery', snmpElementInfoQuery)

    extendedQueryFromClient = MonitorExtendedQueryFromClientMsg().subtype(
        implicitTag=tag.Tag(
            tag.tagClassContext,
            tag.tagFormatSimple,
            20
        )
    )
    extendedQueryFromClient.setComponentByName('queryId', queryId)
    extendedQueryFromClient.setComponentByName('query',   extendedQuery)

    fromClient = MonitorPDU_fromClient().subtype(
        implicitTag=tag.Tag(
            tag.tagClassContext,
            tag.tagFormatSimple,
            1
        )
    )
    fromClient.setComponentByName('extendedQueryFromClient', extendedQueryFromClient)

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
