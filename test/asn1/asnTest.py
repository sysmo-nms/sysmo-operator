#!/usr/bin/env python2

from pyasn1.type import univ, namedtype
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
print "initial value!!!!!!!!!!!!!!! ", c

binPdu = encoder.encode(c)
print "value encoded!!!!!!!!!!!!!!! ", binPdu

test = decoder.decode(binPdu)
print "value decoded!!!!!!!!!!!!!!! ", test


" decode "
fd  = open("pdu.bin")
pdu = fd.read()
print "hello pyasn1", pdu
