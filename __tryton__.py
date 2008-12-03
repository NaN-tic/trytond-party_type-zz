#This file is part of Tryton.  The COPYRIGHT file at the top level of this
#repository contains the full copyright notices and license terms.

{
    'name':        'Party Types for People and Organisations',
    'name_de_DE':  "Geschäftsparteitypen 'Person' und 'Organisation'",
    'version':     '0.0.3',
    'author':      'Udo Spallek',
    'email':       'udono@virtual-things.biz',
    'website':     'http://www.virtual-things.biz/',
    'description': '''Extend party by the types 'person' or
        'organization' as described by Len Silverston in "The Data Model
        Resource Book Revised Edition Volume 1" P. 21f''',
    'description_de_DE': '''Erweitert Geschäftsparteien um die
        Unterscheidung in 'Organisationen' und 'Personen' wie in
        Silverston Len:"The Data Model Resource Book", Revised Edition,
        Volume 1, S. 21f, beschrieben.''',
    'depends':     ['ir', 'res', 'party'],
    'xml':         [
                     'party_type.xml',
                   ],
    'translation': [
#        'fr_FR.csv',
        'de_DE.csv',
#        'es_ES.csv',
    ],
}
