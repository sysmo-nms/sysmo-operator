#!/usr/bin/env python2

from pyasn1.type import char, univ, namedtype, tag
from pyasn1.codec.ber import encoder, decoder

" decode and encode asn1 terms "



" encode "
class CommandResponce(univ.Choice):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('aab', univ.Integer()),
        namedtype.NamedType('bbc', univ.OctetString())
    )

c = CommandResponce()
c.setComponentByName('aab', 123)
c.setComponentByName('bbc', 'hello jojo')
# print "initial value!!!!!!!!!!!!!!! ", c

# binPdu = encoder.encode(c)
# print "value encoded!!!!!!!!!!!!!!! ", binPdu

# test = decoder.decode(binPdu)
# print "value decoded!!!!!!!!!!!!!!! ", test


" decode "
fd  = open("NmsPDU_modTrackerPDU_fromServer_cmdResp_CmdResponce.bin")
modTrackerPdu = fd.read()

# print "hello pyasn1", pdu
i_integer   = encoder.encode(univ.Integer(999))
i_return    = decoder.decode(i_integer)
print i_integer, " --> ",  i_return

p_string    = encoder.encode(char.PrintableString("hello world"))
p_return    = decoder.decode(p_string)
print p_string, " --> ",  p_return

arghh = decoder.decode(modTrackerPdu)

# voir http://pyasn1.sourceforge.net/codecs.html#2.1
# "decoding untagged types" (any and choice)
#rtt, modTrackerPdu = decoder.decode(modTrackerPdu, asn1Spec=univ.Choice())

print "!!!!! ->>>> ", arghh, " <<<<<<<<<- !!!!!!!!!"

# create a choice of 2 things

class NmsPDU(univ.Choice):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('modSupercastPDU', univ.Integer()),
        namedtype.NamedType('modEsnmpPDU', univ.Integer()),
        namedtype.NamedType('modTrackerPDU', NmsPDU_TrackerPDU())
    )

class NmsPDU_TrackerPDU(univ.Choice):
    compenentType = namedtype.NamedTypes(
        namedtype.NamedType('fromServer', NmsPDU_TrackerPDU_FromServer()),
        namedtype.NamedType('fromClient', univ.Integer()),
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

class NmsPDU_TrackerPDU_FromServer_CmdResp(univ.Sequence):
    compenentType = namedtype.NamedTypes(
        namedtype.NamedType('cmdId', univ.Integer()),
        namedtype.NamedType('cmdMsg', char.PrintableString())
    )

c = TChoice()
c.setComponentByName('message', 'hello')

print c.prettyPrint()
a = encoder.encode(c)








