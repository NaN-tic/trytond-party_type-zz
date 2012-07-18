#This file is part party_type module for Tryton.
#The COPYRIGHT file at the top level of this repository contains 
#the full copyright notices and license terms.
{
    'name': 'Party Type',
    'name_ca_ES': 'Tipus de tercers',
    'name_de_DE': 'Parteien Typ',
    'name_es_ES': 'Tipos de terceros',
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
    'description_es_ES': '''
        Diferencia en los terceros según personas físicas i organizaciones
        - Amplia el modelo de tercero y añade el tipos 'personas' y 'organización'
        - Añade el atributo 'firts name' y 'gender' a los terceros'
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
        'locale/es_ES.po',
        ],
}
