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

    def get_rec_name(self, cursor, user, ids, name, context=None):
        """get_rec_name(self, cursor, user, ids, name, context=None)
        This method combines last name and first name for general views.
        The kind of combination of first and last names may vary from
        country to country. The pattern used here is:
        <last_name>, <first_name>
        Overwrite this method for other combinations.
        """
        if not ids:
            return {}
        res = {}
        for employee in self.browse(cursor, user, ids, context=context):
            res[employee.id] = ", ".join(x for x in [employee.name,
                    employee.first_name] if x)
        return res

    def search_rec_name(self, cursor, user, name, args, context=None):
        args2 = []
        i = 0
        while i < len(args):
            ids = self.search(cursor, user, [
                ('name', args[i][1], args[i][2]),
                ], limit=1, context=context)
            if ids:
                args2.append(('name', args[i][1], args[i][2]))
            else:
                ids = self.search(cursor, user, [
                             ('first_name', args[i][1], args[i][2]),
                             ], limit=1, context=context)
                if ids:
                    args2.append(('first_name', args[i][1], args[i][2]))
                else:
                    args2.append((self._rec_name, args[i][1], args[i][2]))
            i += 1
        return args2

Employee()
