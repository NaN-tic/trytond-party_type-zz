#This file is part of Tryton.  The COPYRIGHT file at the top level of this
#repository contains the full copyright notices and license terms.
from trytond.model import ModelView, ModelSQL, fields
import copy

class Company(ModelSQL, ModelView):
    _name = 'company.company'

    def default_party_type(self):
        """
        This method sets the default for field type to organization
        for companies.
        """
        return 'organization'

    def on_change_party_type(self, values):
        res = {}
        res['party_type'] = 'organization'
        res['first_name'] = False
        res['gender'] = False
        return res

Company()


class Employee(ModelSQL, ModelView):
    _name = 'company.employee'

    def default_party_type(self):
        """
        This method sets the default for field type to organization
        for companies.
        """
        return 'person'

    def on_change_party_type(self, values):
        res = {}
        res['party_type'] = 'person'
        return res

    def get_rec_name(self, ids, name):
        """get_rec_name(ids, name)
        This method combines last name and first name for general views.
        The kind of combination of first and last names may vary from
        country to country. The pattern used here is:
        <last_name>, <first_name>
        Overwrite this method for other combinations.
        """
        if not ids:
            return {}
        res = {}
        for employee in self.browse(ids):
            res[employee.id] = ", ".join(x for x in [employee.name,
                    employee.first_name] if x)
        return res

    def search_rec_name(self, name, clause):
        ids = self.search([
            ('name',) + tuple(clause[1:]),
            ], limit=1)
        if ids:
            return [('name',) + tuple(clause[1:])]
        else:
            ids = self.search([
                ('first_name',) + tuple(clause[1:]),
                ], limit=1)
            if ids:
                return [('first_name',) + tuple(clause[1:])]
        return [(self._rec_name,) + tuple(clause[1:])]

Employee()
