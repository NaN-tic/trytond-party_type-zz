#This file is part of Tryton.  The COPYRIGHT file at the top level of this
#repository contains the full copyright notices and license terms.

{
    'name': 'Party Type',
    'name_ca_ES': 'Tipus de tercers',
    'name_de_DE': 'Parteien Typ',
    'version': '2.1.2',
    'author': 'virtual things',
    'email': 'info@virtual-things.biz',
    'website': 'http://www.virtual-things.biz/',
    'description': '''
        Distinction of Parties between people and organization
        - Extends the party model by the types 'person' or 'organization'
        - Adds attributes 'first name' and 'gender' for parties of
          type 'person'
    ''',
    'description_ca_ES': '''
        Diferenciació de tercers segons persones físiques i organització
        - Amplia el model de tercer per afegir els tipus 'persones' i 'organització'
        - Afegeix l'atribut 'first name' i 'gender' als tercers'
    ''',
    'description_de_DE': '''
        Unterscheidung von Parteien nach Person oder Organisation
        - Erweitert das Modell von Parteien um die Typen 'Person'
          und 'Organisation'.
        - Fügt die Merkmale 'Vorname' und 'Geschlecht' zu Parteien des Typs
         'Person' hinzu.
    ''',
    'depends': [
        'party',
        'company',
        ],
    'xml': [
        'party.xml',
        'company.xml'
        ],
    'translation': [
        'locale/ca_ES.po',
        'locale/de_DE.po',
        ],
}
