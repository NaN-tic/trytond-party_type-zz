#This file is part of Tryton.  The COPYRIGHT file at the top level of this
#repository contains the full copyright notices and license terms.

{
    'name':        'Distinguish Parties between People and Organizations.',
    'name_de_DE':  'Parteien in Personen und Organisationen unterscheiden.',
    'version':     '1.2.0',
    'author':      'virtual things',
    'email':       'info@virtual-things.biz',
    'website':     'http://www.virtual-things.biz/',
    'description': '''
    Extend party model by the types 'person' or 'organization'. Additionally
    parties with type 'person' are extended by 'pre-name' and 'gender'
    attributes.
    ''',
    'description_de_DE': '''
    Erweitert das Modell von Parteien um die Typen 'Person' und
    'Organisation'. Zusätzlich werden Parteien vom Typ 'Person' erweitert
    um die Merkmale 'Vorname' und 'Geschlecht'.
    ''',
    'depends':     ['ir', 'res', 'party',],
    'xml':         ['party.xml',],
    'translation': [#'fr_FR.csv',
                    #'es_ES.csv',
                    'de_DE.csv',],
}
