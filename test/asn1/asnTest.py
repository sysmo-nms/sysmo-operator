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
#print i_integer, " --> ",  i_return

p_string    = encoder.encode(char.PrintableString("hello world"))
p_return    = decoder.decode(p_string)
#print p_string, " --> ",  p_return

arghh = decoder.decode(modTrackerPdu)

# voir http://pyasn1.sourceforge.net/codecs.html#2.1
# "decoding untagged types" (any and choice)
#rtt, modTrackerPdu = decoder.decode(modTrackerPdu, asn1Spec=univ.Choice())

#print "!!!!! ->>>> ", arghh, " <<<<<<<<<- !!!!!!!!!"

# create a choice of 2 things


class NmsPDU_TrackerPDU_FromServer_CmdResp(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('cmdId', univ.Integer()),
        namedtype.NamedType('cmdMsg', char.PrintableString())
    )

class NmsPDU_TrackerPDU_FromServer(univ.Choice):
    componentType = namedtype.NamedTypes(
#        namedtype.NamedType('tragetInfo', univ.Integer()),
#        namedtype.NamedType('probeInfo', char.PrintableString()),
#        namedtype.NamedType('probeFetch', char.PrintableString()),
        namedtype.NamedType('probeDump', char.PrintableString()),
        namedtype.NamedType('cmdResp', NmsPDU_TrackerPDU_FromServer_CmdResp()),
#        namedtype.NamedType('probeModInfo', char.PrintableString())
    )

# class NmsPDU_TrackerPDU_FromServer(univ.Choice):
#     componentType = namedtype.NamedTypes(
#         namedtype.NamedType('targetInfo', univ.Integer()),
#         namedtype.NamedType('probeInfo', univ.Integer()),
#         namedtype.NamedType('probeFetch', univ.Integer()),
#         namedtype.NamedType('probeDump', univ.Integer()),
#         namedtype.NamedType('cmdResp', NmsPDU_TrackerPDU_FromServer_CmdResp()),
#         namedtype.NamedType('probeModInfo', univ.Integer())
#     )

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

cmdResp = NmsPDU_TrackerPDU_FromServer_CmdResp()
cmdResp.setComponentByName('cmdId', 23)
cmdResp.setComponentByName('cmdMsg', "hello")

#fromSrv = NmsPDU_TrackerPDU_FromServer()
#fromSrv.setComponentByName('cmdResp', cmdResp)

#trackerPdu = NmsPDU_TrackerPDU()
#trackerPdu.setComponentByName('fromServer', fromSrv)

#nmsPdu = NmsPDU()
#nmsPdu.setComponentByName('modTrackerPDU', trackerPdu)



testC = NmsPDU_TrackerPDU_FromServer()
#testC.setComponentByName('choix1', 234)
#testC.setComponentByName('choix2', "hello")
testC.setComponentByName('cmdResp', cmdResp)



encodeTest = testC
print  encodeTest.getName()
print  encodeTest.getComponent()
print "pdu is: ", encodeTest
data = encoder.encode(encodeTest)
print "data is: ", data
dataDec, other = decoder.decode(data, asn1Spec=encodeTest)
print "dataDec is: ", dataDec

