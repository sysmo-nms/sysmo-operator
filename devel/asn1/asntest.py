#!/usr/bin/env python2

from pyasn1.type        import char, univ, namedtype, tag
from pyasn1.codec.ber   import encoder, decoder

from pprint import pprint

class ArrgPDU(char.PrintableString): pass

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
        ),
        namedtype.NamedType(
            'choiceThree',
            ArrgPDU().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext,
                    tag.tagFormatSimple,
                    3
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

# print "----------------------------------------------------------------------"
# print "----------------------------------------------------------------------"
# print "----------------------------------------------------------------------"

" OK "
decodedSimplePdu, b = decoder.decode(simplePdu, asn1Spec=TestPDU())
# print "-> read simple pdu from erlang asn lib: "
# print simplePdu, decodedSimplePdu
# print encoder.encode(decodedSimplePdu)
# print "----------------------------------------------------------------------"

" OK "
decodedExtendedPdu, b = decoder.decode(extendedPdu, asn1Spec=NmsPDU())
# print "-> read extended pdu from erlang asn lib: "
# print extendedPdu, decodedExtendedPdu
# print encoder.encode(decodedExtendedPdu)
# print "----------------------------------------------------------------------"


" SIMPLE pdu created by pyasnlib "
sPdu = TestPDU()
sPdu.setComponentByName('choiceOne', "YZ")
sEncoded = encoder.encode(sPdu)
sP          = open('pbinary_modTest_choiceOne.bin', 'w')
sP.write(sEncoded); sP.close()
# print "-> create simple pdu with pyasn1"
# print sEncoded

" erlang read OK "
# {ok, B} = file:read_file('pbinary_modTest_choiceOne.bin').
# 'ModTest':decode('TestPDU', B).
# {ok,{choiceOne,"YZ"}}

" pyasn1 read OK "
returnDecoded, b = decoder.decode(sEncoded, asn1Spec=TestPDU())
# print "-> decode simple pdu created with with pyasn1"
# print returnDecoded
# print "----------------------------------------------------------------------"



" EXTENDED pdu created by pyasnlib "
" Probleme avec CHOICE ici "
" pyasn1.error.PyAsn1Error: Component type error TestPDU() vs TestPDU() "
" voir http://sourceforge.net/mailarchive/forum.php?thread_name=E1I9I2V-000B1q-Ut%40ffe1.ukr.net&forum_name=pyasn1-users "
" la valeur decodee plus haut extendedPdu est correctement decodee en"
" workingTuple. Le tuple est ensuite encode en workingData. workingData"
" est ensuite ecrit dans pbinary_NmsPDU_modTest_choiceOne.bin et est "
" identique a extendedPdu d'origine. WTF"

" pyasn encode correctement son tuple tire du pdu de la lib erlang "
workingTuple, a = decoder.decode(extendedPdu, asn1Spec=NmsPDU())
workingData = encoder.encode(workingTuple)
eP          = open('pbinary_NmsPDU_modTest_choiceOne.bin', 'w')
eP.write(workingData); eP.close()

print "here is: ", workingTuple
print
pprint (vars(workingTuple))
print
pprint (vars(NmsPDU()))
print

xpdu = NmsPDU()
zpdu = TestPDU()

print "xpdu component: ", xpdu

ko = zpdu.setComponentByName('choiceOne', "XY")
ok = workingTuple.getComponentByName('modTest')
xpdu.setComponentByName('modTest', ok)

" TestPDU extrait du working tuple peut etre correctement assigne au "
" NmsPDU() ??? "

print "xpdu component: ", xpdu



print
print
print
print

" voir diference entre les deux concerne les tags "
pprint(vars(ok))
pprint(vars(ko))

" ... "
koo = TestPDU().subtype(
    implicitTag=tag.Tag(
        tag.tagClassContext,
        tag.tagFormatSimple,
        1
    )
)

koo.setComponentByName('choiceTwo', "UU")
ultimate = NmsPDU()
ultimate.setComponentByName('modTest', koo)
print ultimate
print encoder.encode(ultimate)

" SUCCESS "
" voir ce que ca change de subtyper TestPDU() avec un autre tag, "
" et de koo.setComponentByName avec un autre choice "
