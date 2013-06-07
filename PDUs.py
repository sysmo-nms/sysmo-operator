#!/usr/bin/env python

from pyasn1.type import char,univ,namedtype,tag,namedval
from pyasn1.codec.ber import encoder,decoder

" Supercast PDUs are defined here "
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
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('error', SupercastPDU_fromServer_authError_error()),
        namedtype.NamedType('userId',  char.PrintableString()),
        namedtype.NamedType('pass',    char.PrintableString())
    )

class SupercastPDU_fromServer(univ.Choice):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('chanInfo', char.PrintableString()),
        namedtype.NamedType('authReq', SupercastPDU_fromServer_authReq()),
        namedtype.NamedType('authAck', SupercastPDU_fromServer_authAck()),
        namedtype.NamedType('authError', SupercastPDU_fromServer_authError())
    )

class SupercastPDU_fromClient(univ.Choice):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('text', char.PrintableString()),
        namedtype.NamedType('id', univ.Integer())
    )

class SupercastPDU(univ.Choice):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('fromServer',SupercastPDU_fromServer()),
        namedtype.NamedType('fromClient', SupercastPDU_fromClient())
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
        namedtype.NamedType('modEsnmpPDU'    , EsnmpPDU()),
        namedtype.NamedType('modTrackerPDU'  , TrackerPDU())
    )

if __name__ == "__main__":
    vPdu = SupercastPDU_fromServer_authError_error('timeout')
    
    wPdu = SupercastPDU_fromServer_authError()
    wPdu.setComponentByName('error', vPdu)
    wPdu.setComponentByName('userId', "user here")
    wPdu.setComponentByName('pass', "pass here")
    
    xPdu = SupercastPDU_fromServer()
    xPdu.setComponentByName('authError', wPdu)
    
    yPdu = SupercastPDU()
    yPdu.setComponentByName('fromServer', xPdu)
    
    zPdu = NmsPDU()
    zPdu.setComponentByName('modSupercastPDU', yPdu)
    print zPdu.prettyPrint()
    
    #encodeTest = xPdu
    #pdu = encoder.encode(encodeTest)
    #print encodeTest.prettyPrint, pdu
    #pduDec, other = decoder.decode(pdu, asn1Spec=encodeTest)
    
