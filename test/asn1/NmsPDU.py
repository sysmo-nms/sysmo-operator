#!/usr/bin/env python2

from pyasn1.type import char, univ, namedtype, tag
from pyasn1.codec.ber import encoder, decoder

class NmsPDU_TrackerPDU_FromServer_CmdResp(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('cmdId', univ.Integer()),
        namedtype.NamedType('cmdMsg', char.PrintableString())
    )

class NmsPDU_TrackerPDU_FromServer(univ.Choice):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('targetInfo', univ.Integer()),
        namedtype.NamedType('probeInfo', univ.Integer()),
        namedtype.NamedType('probeFetch', univ.Integer()),
        namedtype.NamedType('probeDump', univ.Integer()),
        namedtype.NamedType('cmdResp', NmsPDU_TrackerPDU_FromServer_CmdResp()),
        namedtype.NamedType('probeModInfo', univ.Integer())
    )

class NmsPDU_TrackerPDU(univ.Choice):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('fromServer', NmsPDU_TrackerPDU_FromServer()),
        namedtype.NamedType('fromClient', univ.Integer()),
    )

class NmsPDU(univ.Choice):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('modSupercastPDU', univ.Integer()),
        namedtype.NamedType('modEsnmpPDU', univ.Integer()),
        namedtype.NamedType('modTrackerPDU', NmsPDU_TrackerPDU())
    )

a = NmsPDU()
b = NmsPDU_TrackerPDU()
c = NmsPDU_TrackerPDU_FromServer()
d = NmsPDU_TrackerPDU_FromServer_CmdResp()

d.setComponentByName('cmdId', 34)
d.setComponentByName('cmdMsg', "hello")

c.setComponentByName('cmdResp', d)
b.setComponentByName('fromServer', c)
a.setComponentByName('modTrackerPDU', b)

fd  = open("NmsPDU_modTrackerPDU_fromServer_cmdResp_CmdResponce.bin")
modTrackerPdu = fd.read()

x = encoder.encode(d)
print x
w, y = decoder.decode(x, asn1Spec=NmsPDU_TrakcerPDU_FromServer_CmdResp())
print y 

# VOIR PYASN1 Example Modules
