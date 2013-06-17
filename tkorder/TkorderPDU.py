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

class TargetProperty(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('name',     char.PrintableString()),
        namedtype.NamedType('value',    univ.OctetString())
    )

class TargetProperties(univ.SequenceOf):
    componentType = TargetProperty()

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

class ProbeType(univ.Enumerated):
    namedValues = namedval.NamedValues(
        ('fetch', 0),
        ('status', 1)
    )

class TrackerProbeInfo(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('channel',  char.PrintableString()),
        namedtype.NamedType('id',       univ.Integer()),
        namedtype.NamedType('name',     char.PrintableString()),
        namedtype.NamedType('type',     ProbeType()),
        namedtype.NamedType('probeMod', char.PrintableString()),
        namedtype.NamedType('status',   char.PrintableString()),
        namedtype.NamedType('step',     univ.Integer()),
        namedtype.NamedType('timeout',  univ.Integer()),
        namedtype.NamedType('infoType', ProbeInfoType())
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
            'probeModInfo',
            TrackerProbeModuleInfo().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext,
                    tag.tagFormatSimple,
                    6
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
                print "unsubscribeOk message", msg3
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
                infoType    = str(msg3.getComponentByName('type'))
                infoProp    = msg3.getComponentByName('properties')
                return {
                    'from':     msg1_type,
                    'msgType':  msg3_type,
                    'value':    {
                        'channel': targetId,
                        'properties': infoProp,
                        'infoType': infoType
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
            return encode_subscribe(chanString)
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
#print a
# print "Return is ", a
# x = genPdu_unsubscribe("channel-Xkki")
# 
# fw.write(x); fw.close()
