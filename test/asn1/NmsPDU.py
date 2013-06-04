#!/usr/bin/env python2

from pyasn1.type import char, univ, namedtype, tag
from pyasn1.codec.ber import encoder, decoder

class NmsPDU_TrackerPDU_FromServer_CmdResp(univ.Sequence):
    compenentType = namedtype.NamedTypes(
        namedtype.NamedType('cmdId', univ.Integer()),
        namedtype.NamedType('cmdMsg', char.PrintableString())
    )

class NmsPDU_TrackerPDU_FromServer(univ.Choice):
    compenentType = namedtype.NamedTypes(
        namedtype.NamedType('targetInfo', univ.Integer()),
        namedtype.NamedType('probeInfo', univ.Integer()),
        namedtype.NamedType('probeFetch', univ.Integer()),
        namedtype.NamedType('probeDump', univ.Integer()),
        namedtype.NamedType('cmdResp', NmsPDU_TrackerPDU_FromServer_CmdResp()),
        namedtype.NamedType('probeModInfo', univ.Integer())
    )

class NmsPDU_TrackerPDU(univ.Choice):
    compenentType = namedtype.NamedTypes(
        namedtype.NamedType('fromServer', NmsPDU_TrackerPDU_FromServer()),
        namedtype.NamedType('fromClient', univ.Integer()),
    )

class NmsPDU(univ.Choice):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('modSupercastPDU', univ.Integer()),
        namedtype.NamedType('modEsnmpPDU', univ.Integer()),
        namedtype.NamedType('modTrackerPDU', NmsPDU_TrackerPDU())
    )

print "hello"
