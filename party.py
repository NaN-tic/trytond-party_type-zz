#This file is part party_type module for Tryton.
#The COPYRIGHT file at the top level of this repository contains 
#the full copyright notices and license terms.
from trytond.model import fields
from trytond.pyson import Equal, Eval, Not, Or, Bool
from trytond.transaction import Transaction
from trytond.pool import PoolMeta

__all__ = ['Party']
__metaclass__ = PoolMeta

_STATES_PERSON = {
    "readonly": Or(Not(Bool(Eval('active'))),
            Not(Equal(Eval('party_type'), 'person'))),
    "invisible": Not(Equal(Eval('party_type'), 'person')),
}
_STATES_PERSON_DEPENDS = ['active', 'party_type']


class Party:
    """trytond.model.Party()
    This class inherits party.party model and adds a type attribute with
    'person' and 'organization' as values. A party with the type
    'Person' has the additional attributes firstname and gender.
    A party with the type 'Organization' has no additional attributes.
    """
    __name__ = "party.party"

    party_type = fields.Selection([
            ("organization", "Organization"),
            ("person", "Person"),
            ], "Party Type", select=1, readonly=False, on_change=['party_type'],
            states={
                'readonly': Not(Bool(Eval('active'))),
            }, depends=['active'])
    first_name = fields.Char("First Name", size=None, states=_STATES_PERSON,
        depends=_STATES_PERSON_DEPENDS)
    gender = fields.Selection([
                ("male", "Male"),
                ("female", "Female"),
                (None, ""),
            ], "Gender", select=1, sort=False, readonly=False,
            states=_STATES_PERSON, depends=_STATES_PERSON_DEPENDS)

    @staticmethod
    def default_party_type():
        """Party.default_party_type()
        This method sets the default value for field type, depending
        on the context defined in party_type.xml.
        """
        return Transaction().context.get('party_type', 'organization')

    @classmethod
    def get_rec_name(cls, records, name):
        """Party.get_rec_name(records, name)
        This method combines last and first name for views.
        The kind of combination of first and last names may vary from
        country to country. The pattern used here is::

            <last_name>, <first_name>

        Overwrite this method for other conventions of person names.
        """
        if not records:
            return {}
        res = {}
        for party in records:
            res[party.id] = ", ".join(x for x in [
                    party.name, party.first_name] if x)
        return res

    @classmethod
    def search_rec_name(cls, name, clause):
        """Party.search_rec_name(name, clause)
        This method adds the first name to search clause for searching persons.
        """
        ids = cls.search([('name',) + tuple(clause[1:])], limit=1)
        if ids:
            return [('name',) + tuple(clause[1:])]
        else:
            ids = cls.search([('first_name',) + tuple(clause[1:])], limit=1)
            if ids:
                return [('first_name',) + tuple(clause[1:])]
        return super(Party, cls).search_rec_name(name, clause)

    def on_change_party_type(self):
        '''Party.on_change_party_type(values)
        Method to clear party attributes, when changing a party with
        party type 'person' to type 'organization'.
        '''
        res = {}
        party_type = self.party_type or  'organization'
        if party_type == 'organization':
            res['party_type'] = party_type
            res['first_name'] = None
            res['gender'] = None
        return res

    @classmethod
    def get_full_name(cls, records, name):
        """Party.get_full_name(records, name)
        This method overwrites the standard full name as used in reports
        to call the name of a person party. The kind of combination of
        first and last names may vary from country to country.
        The pattern used here is::

        <first_name> <last_name>

        Overwrite this method for other conventions of person names.
        """
        if not records:
            return {}
        res = {}
        for party in records:
            res[party.id] = " ".join(x for x in [
                    party.first_name, party.name] if x)
        return res
