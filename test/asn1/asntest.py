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

" OK "
decodedExtendedPdu, b = decoder.decode(extendedPdu, asn1Spec=NmsPDU())
print extendedPdu, decodedExtendedPdu




" SIMPLE pdu created by pyasnlib "
simplePdu = TestPDU()
simplePdu.setComponentByName('choiceOne', "YZ")
simpleEncoded = encoder.encode(simplePdu)
sP          = open('pbinary_modTest_choiceOne.bin', 'w')
sP.write(simpleEncoded); sP.close()

" erlang read OK "
# {ok, B} = file:read_file('pbinary_modTest_choiceOne.bin').
# 'ModTest':decode('TestPDU', B).
# {ok,{choiceOne,"YZ"}}

" pyasn1 read OK "
returnDecoded, b = decoder.decode(simpleEncoded, asn1Spec=TestPDU())
print returnDecoded



" EXTENDED pdu created by pyasnlib "
" Probleme avec choices ici "
" pyasn1.error.PyAsn1Error: Component type error TestPDU() vs TestPDU() "

" voir http://sourceforge.net/mailarchive/forum.php?thread_name=E1I9I2V-000B1q-Ut%40ffe1.ukr.net&forum_name=pyasn1-users "
extendedPdu = NmsPDU()
msgTest = char.PrintableString().subtype(
    explicitTag=tag.Tag(
        tag.tagClassContext,
        tag.tagFormatSimple,
        1
    )
)

extendedPdu.setComponentByName('modTest', TestPDU(msgTest))

print extendedPdu
print simplePdu

print str(simplePdu)
