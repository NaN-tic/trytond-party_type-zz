#This file is part of Tryton.  The COPYRIGHT file at the top level of this
#repository contains the full copyright notices and license terms.

{
    'name':        'Party Types: People and Organizations',
    'name_de_DE':  'Partei Typen: Personen und Organisationen',
    'version':     '1.1.0',
    'author':      'virtual things',
    'email':       'info@virtual-things.biz',
    'website':     'http://www.virtual-things.biz/',
    'description': '''Extend party by the types 'person' or 'organization'.
        Additionally the Party model for type 'person' is extended by
        'pre-name' and 'gender' attributes.
    ''',
    'description_de_DE': '''Erweitert Parteien um die Unterscheidung in
        'Organisation' und 'Person'. Zusätzlich ist das Parteien Modell vom
        Typ 'Person' erweitert mit den Merkmalen 'Vorname' und 'Geschlecht'.
    ''',
    'depends':     ['ir', 'res', 'party',],
    'xml':         ['party.xml',],
    'translation': [#'fr_FR.csv',
                    'de_DE.csv',
                    #'es_ES.csv',],
}
