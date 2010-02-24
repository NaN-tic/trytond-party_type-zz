#This file is part of Tryton.  The COPYRIGHT file at the top level of this
#repository contains the full copyright notices and license terms.
from trytond.model import ModelView, ModelSQL, fields
import copy

class Company(ModelSQL, ModelView):
    _name = 'company.company'

    def default_party_type(self, cursor, user, context=None):
        """
        This method sets the default for field type to organization
        for companies.
        """
        if context is None:
            context = {}
        return 'organization'

    def on_change_party_type(self, cursor, user, ids, values, context=None):
        res = {}
        res['party_type'] = 'organization'
        res['first_name'] = False
        res['gender'] = False
        return res

Company()


class Employee(ModelSQL, ModelView):
    _name = 'company.employee'

    def default_party_type(self, cursor, user, context=None):
        """
        This method sets the default for field type to organization
        for companies.
        """
        if context is None:
            context = {}
        return 'person'

    def on_change_party_type(self, cursor, user, ids, values, context=None):
        res = {}
        res['party_type'] = 'person'
        return res

Employee()
