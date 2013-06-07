#!/usr/bin/env python

from pyasn1.type import char,univ,namedtype,tag,namedval
from pyasn1.codec.ber import encoder,decoder

" Supercast PDUs are defined here "
class SupercastChan(char.PrintableString): pass

class SupercastGroup(char.PrintableString): pass

class SupercastChanInfoType(univ.Enumerated):
    namedValues = namedval.NamedValues(
        ('create', 0),
        ('delete', 1),
        ('update', 2)
    )

class SupercastChanInfo(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('channel', SupercastChan()),
        namedtype.NamedType('type', SupercastChanInfoType())
    )
    
class SupercastPDU_fromServer_authReq(univ.Enumerated):
    namedValues = namedval.NamedValues(
        ('localfile', 0),
        ('ldap', 1)
    )

class SupercastPDU_fromServer_authAck(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('groups',       char.PrintableString()),
        namedtype.NamedType('staticChans',  char.PrintableString())
    )
    
class SupercastPDU_fromServer_authError_error(univ.Enumerated):
    namedValues = namedval.NamedValues(
        ('noShuchUser', 0),
        ('badPass', 1),
        ('timeout', 2),
        ('other', 3)
    )

class SupercastPDU_fromServer_authError(univ.Sequence):
    #tagSet = univ.Enumerated.tagSet.tagExplicitly(
    #    tag.Tag(
    #        tag.tagClassContext,
    #        tag.tagFormatSimple,
    #        3
    #    )
    #),
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('error', SupercastPDU_fromServer_authError_error()),
        namedtype.NamedType('userId',  char.PrintableString()),
        namedtype.NamedType('pass',    char.PrintableString())
    )

class SupercastPDU_fromServer(univ.Choice):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType(
            'chanInfo',
            char.PrintableString().tagSet.tagExplicitly(
                tag.Tag(
                    tag.tagClassContext,
                    tag.tagFormatSimple,
                    0
                )
            )
        ),
        namedtype.NamedType(
            'authReq',
            SupercastPDU_fromServer_authReq().tagSet.tagExplicitly(
                tag.Tag(
                    tag.tagClassContext,
                    tag.tagFormatSimple,
                    1
                )
            )
        ),
        namedtype.NamedType(
            'authAck',
            SupercastPDU_fromServer_authAck().tagSet.tagExplicitly(
                tag.Tag(
                    tag.tagClassContext,
                    tag.tagFormatSimple,
                    2
                )
            )
        ),
        namedtype.NamedType(
            'authError', 
            SupercastPDU_fromServer_authError().tagSet.tagExplicitly(
                tag.Tag(
                    tag.tagClassContext,
                    tag.tagFormatSimple,
                    3
                )
            )
        )
    )

class SupercastPDU_fromClient(univ.Choice):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('text', char.PrintableString()),
        namedtype.NamedType('id', univ.Integer())
    )

class SupercastPDU(univ.Choice):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('fromServer',SupercastPDU_fromServer()),
        namedtype.NamedType('fromClient', SupercastPDU_fromClient()),
        namedtype.NamedType('testouille', char.PrintableString())
    )



" Esnmp PDUs are defined here "
class EsnmpPDU(univ.Choice):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('text', char.PrintableString()),
        namedtype.NamedType('id', univ.Integer())
    )

" Tracker PDUs are defined here "
class TrackerPDU(univ.Choice):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('text', char.PrintableString()),
        namedtype.NamedType('id', univ.Integer())
    )


class NmsPDU(univ.Choice):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('modSupercastPDU', SupercastPDU()),
        namedtype.NamedType('modEsnmpPDU'    , char.PrintableString()),
        namedtype.NamedType('modTrackerPDU'  , TrackerPDU())
    )

class TestPDU(univ.Choice):
    componentType = namedtype.NamedTypes(
        #namedtype.NamedType('fromServer',SupercastPDU_fromServer()),
        namedtype.NamedType(
            'fromClient',
            SupercastPDU_fromClient().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext,
                    tag.tagFormatSimple,
                    0
                )
            )
        ),
        namedtype.NamedType(
            'testouille1',
            char.PrintableString().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext,
                    tag.tagFormatSimple,
                    1
                )
            )
        ),
        namedtype.NamedType(
            'testouille',  
            char.PrintableString().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext,
                    tag.tagFormatSimple,
                    2
                )
            )
        )
    )

if __name__ == "__main__":
    vPdu = SupercastPDU_fromServer_authError_error('timeout')
    
    wPdu = SupercastPDU_fromServer_authError()
    wPdu.setComponentByName('error', vPdu)
    wPdu.setComponentByName('userId', "user here")
    wPdu.setComponentByName('pass', "pass here")
    
    xPdu = SupercastPDU_fromServer()
    xPdu.setComponentByName('authError', wPdu)
    
    #yPdu = TestPDU()
    #yPdu.setComponentByName('testouille', "hello pdu")
    
    #zPdu = NmsPDU()
    #zPdu.setComponentByName('modSupercastPDU', yPdu)
    #print zPdu.prettyPrint()
    
    encodeTest = wPdu

    pdu = encoder.encode(encodeTest)
    print "encode: ", encodeTest.prettyPrint()
    print "len of pdu:-------> ", len(pdu)
    print "------->", pdu, "<------"
    # XXX Error here
    pduDec, other = decoder.decode(pdu, asn1Spec=encodeTest)
    print "ret -> ", pduDec.prettyPrint(), other
    # XXX Error here
