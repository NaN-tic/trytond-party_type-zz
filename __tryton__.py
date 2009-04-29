#This file is part of Tryton.  The COPYRIGHT file at the top level of this
#repository contains the full copyright notices and license terms.

{
    'name':        'BETA: Distinguish Parties between People and Organizations.',
    'name_de_DE':  'BETA: Parteien in Personen und Organisationen unterscheiden.',
    'version':     '1.1.0',
    'author':      'virtual things',
    'email':       'info@virtual-things.biz',
    'website':     'http://www.virtual-things.biz/',
    'description': '''
    WARNING: BETA STATUS
This module is in public testing phase and not yet released.
Never use this module in productive environment. You can not
uninstall this module once it is installed. Watch
www.tryton.org/news.html for release announcements.

Use this module only for testing purposes and submit your issues to
http://bugs.tryton.org. Please note your testing results on
http://code.google.com/p/tryton/wiki/Testing1_2_0#External_Modules.


    Extend party model by the types 'person' or 'organization'. Additionally
    parties with type 'person' are extended by 'pre-name' and 'gender'
    attributes.
    ''',
    'description_de_DE': '''
WARNUNG: BETA STATUS
Dieses Modul befindet sich momentan in der Testphase und ist noch nicht
veröffentlicht. Dieses Modul ist nicht für Produktivumgebungen
geeignet. Es ist nicht möglich dieses Modul zu deinstallieren. Achten Sie
auf Neuigkeiten unter www.tryton.org/news.html.

Helfen Sie bitte dieses Modul zu testen. Eigenarten können unter
http://bugs.tryton.org gemeldet werden. Bitte vermerken Sie ihre
Testergebnisse unter
http://code.google.com/p/tryton/wiki/Testing1_2_0#External_Modules.



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
