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
            'modTrackerPDU',
            char.PrintableString().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext,
                    tag.tagFormatSimple,
                    2
                )
            )
        ),
        namedtype.NamedType(
            'tt',
            univ.Choice(
                componentType = namedtype.NamedTypes(
                    namedtype.NamedType(
                        'c1',
                        char.PrintableString().subtype(
                            implicitTag=tag.Tag(
                                tag.tagClassContext,
                                tag.tagFormatSimple,
                                4
                            )
                        )
                    ),
                    namedtype.NamedType(
                        'c2',
                        char.PrintableString().subtype(
                            implicitTag=tag.Tag(
                                tag.tagClassContext,
                                tag.tagFormatSimple,
                                5
                            )
                        )
                    )
                )
            ).subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext,
                    tag.tagFormatSimple,
                    3
                )
            )
        )
    )




" read pdu created by erlang asn lib asntest.erl "
sF          = open('ebinary_modTest_choiceOne.bin')
simplePdu   = sF.read(); sF.close()
eF          = open('ebinary_NmsPDU_modTest_choiceOne.bin')
extendedPdu = eF.read(); eF.close()

" OK "
decodedSimplePdu, b = decoder.decode(simplePdu, asn1Spec=TestPDU())
print simplePdu, decodedSimplePdu
print encoder.encode(decodedSimplePdu)

" OK "
decodedExtendedPdu, b = decoder.decode(extendedPdu, asn1Spec=NmsPDU())
print extendedPdu, decodedExtendedPdu
print encoder.encode(decodedExtendedPdu)


" SIMPLE pdu created by pyasnlib "
sPdu = TestPDU()
sPdu.setComponentByName('choiceOne', "YZ")
sEncoded = encoder.encode(sPdu)
sP          = open('pbinary_modTest_choiceOne.bin', 'w')
sP.write(sEncoded); sP.close()

" erlang read OK "
# {ok, B} = file:read_file('pbinary_modTest_choiceOne.bin').
# 'ModTest':decode('TestPDU', B).
# {ok,{choiceOne,"YZ"}}

" pyasn1 read OK "
returnDecoded, b = decoder.decode(sEncoded, asn1Spec=TestPDU())
print returnDecoded



" EXTENDED pdu created by pyasnlib "
" Probleme avec choices ici "
" pyasn1.error.PyAsn1Error: Component type error TestPDU() vs TestPDU() "
" voir http://sourceforge.net/mailarchive/forum.php?thread_name=E1I9I2V-000B1q-Ut%40ffe1.ukr.net&forum_name=pyasn1-users "

workingTuple, a = decoder.decode(extendedPdu, asn1Spec=NmsPDU())
workingData = encoder.encode(workingTuple)
print 
print 
print 
print 

print "----------"

newPdu = NmsPDU()
newPdu.setComponentByName(
    'modTest',
    univ.Choice(
        componentType = namedtype.NamedTypes(
            namedtype.NamedType('c1', "lkj")
        )
    ).subtype(
        implicitTag=tag.Tag(
            tag.tagClassContext,
            tag.tagFormatSimple,
            1
        )
    )
)


#print newPdu

xPdu = encoder.encode(newPdu)
print xPdu
