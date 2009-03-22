#This file is part of Tryton.  The COPYRIGHT file at the top level of this
#repository contains the full copyright notices and license terms.

{
    'name':        'Party Types',
    'name_de_DE':  'Partei Typen',
    'version':     '0.0.3',
    'author':      'virtual things',
    'email':       'info@virtual-things.biz',
    'website':     'http://www.virtual-things.biz/',
    'description': '''Extend party by the types 'person' or 'organization'
    as described by Len Silverston in "The Data Model
    Resource Book Revised Edition Volume 1" P. 21f''',
    'description_de_DE': '''Erweitert Parteien um die Unterscheidung in 'Organisationen' und 'Personen'
    wie beschrieben in Silverston Len: "The Data Model Resource Book", Revised Edition, Volume 1, S. 21f."
''',
    'depends':     ['ir', 'res', 'party',],
    'xml':         [
                     'party_type.xml',
                   ],
    'translation': [
#        'fr_FR.csv',
        'de_DE.csv',
#        'es_ES.csv',
    ],
}
