#!/usr/bin/env python2

from pyasn1.type        import char, univ, namedtype, tag
from pyasn1.codec.ber   import encoder, decoder

class TestPDU(univ.Choice):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType(
            'choiceOne',
            char.PrintableString().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext,
                    tag.tagFormatSimple,
                    1
                )
            )
        ),
        namedtype.NamedType(
            'choiceTwo',
            char.PrintableString().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext,
                    tag.tagFormatSimple,
                    2
                )
            )
        )
    )

class NmsPDU(univ.Choice):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType(
            'modTest',
            TestPDU().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext,
                    tag.tagFormatSimple,
                    1
                )
            )
        ),
        namedtype.NamedType(
            'modTest2',
            char.PrintableString().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext,
                    tag.tagFormatSimple,
                    2
                )
            )
        )
    )


" DECODE EXAMPLE "
eF = open('ebinary_NmsPDU_modTest_choiceOne.bin')
extendedPdu = eF.read(); eF.close()
decodedExtendedPdu, b = decoder.decode(extendedPdu, asn1Spec=NmsPDU())
print "-> ", decodedExtendedPdu
# -> NmsPDU().setComponentByPosition(0, TestPDU().setComponentByPosition(0, PrintableString('hello')))

" ENCODE EXAMPLE "
aPdu = TestPDU()
aPdu.setComponentByName('choiceOne', "hello")

bPdu = NmsPDU()
bPdu.setComponentByName('modTest', aPdu)

# ->  NmsPDU().setComponentByPosition(0, TestPDU().setComponentByPosition(0, PrintableString('AB')))
# Traceback (most recent call last):
#   File "./asntest.py", line 65, in <module>
#     bPdu.setComponentByName('modTest', aPdu)
#   File "/usr/lib/python2.7/dist-packages/pyasn1/type/univ.py", line 429, in setComponentByName
#     self._componentType.getPositionByName(name), value
#   File "/usr/lib/python2.7/dist-packages/pyasn1/type/univ.py", line 585, in setComponentByPosition
#     self._verifyComponent(idx, value)
#   File "/usr/lib/python2.7/dist-packages/pyasn1/type/univ.py", line 421, in _verifyComponent
#     (repr(t), repr(value)))
# pyasn1.error.PyAsn1Error: Component type error TestPDU() vs TestPDU().setComponentByPosition(0, PrintableString('hello'))
# 
