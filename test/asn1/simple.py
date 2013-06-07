#!/usr/bin/env python

from pyasn1.type import char,univ,namedtype,tag
from pyasn1.codec.ber import encoder,decoder




class Choice1(univ.Choice):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('text1',   char.PrintableString()),
        namedtype.NamedType('text2',   char.PrintableString()),
        namedtype.NamedType('text3',   char.PrintableString())
    )
    
class Choice2(univ.Choice):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('text1',   char.PrintableString()),
        namedtype.NamedType('text2',   char.PrintableString()),
        namedtype.NamedType('text2',   char.PrintableString())
    )

class SimpleChoice(univ.Choice):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('c1',   Choice1()),
        namedtype.NamedType('c2',   Choice2())
    )

y = Choice1()
y.setComponentByName('text1', "hello C1")
y.setComponentByName('text2', "hello C1")

z = SimpleChoice()
z.setComponentByName('c1', y)
#z.setComponentByName('text2', "hello")

print z.prettyPrint()
