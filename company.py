#This file is part party_type module for Tryton.
#The COPYRIGHT file at the top level of this repository contains 
#the full copyright notices and license terms.
from trytond.model import ModelView, ModelSQL, fields
from trytond.pool import PoolMeta
import copy

__all__ = ['Company', 'Employee']
__metaclass__ = PoolMeta

class Company:
    __name__ = 'company.company'

    @staticmethod
    def default_party_type():
        """
        This method sets the default for field type to organization
        for companies.
        """
        return 'organization'

    def on_change_party_type(self):
        res = {}
        res['party_type'] = 'organization'
        res['first_name'] = False
        res['gender'] = False
        return res


class Employee:
    __name__ = 'company.employee'

    @staticmethod
    def default_party_type():
        """
        This method sets the default for field type to organization
        for companies.
        """
        return 'person'

    def on_change_party_type(self):
        res = {}
        res['party_type'] = 'person'
        return res

    @classmethod
    def get_rec_name(cls, records, name):
        """get_rec_name(records, name)
        This method combines last name and first name for general views.
        The kind of combination of first and last names may vary from
        country to country. The pattern used here is:
        <last_name>, <first_name>
        Overwrite this method for other combinations.
        """
        if not records:
            return {}
        res = {}
        for employee in records:
            res[employee.id] = ", ".join(x for x in [employee.name,
                    employee.first_name] if x)
        return res

    @classmethod
    def search_rec_name(cls, name, clause):
        ids = cls.search([
            ('name',) + tuple(clause[1:]),
            ], limit=1)
        if ids:
            return [('name',) + tuple(clause[1:])]
        else:
            ids = cls.search([
                ('first_name',) + tuple(clause[1:]),
                ], limit=1)
            if ids:
                return [('first_name',) + tuple(clause[1:])]
        return [(cls._rec_name,) + tuple(clause[1:])]
