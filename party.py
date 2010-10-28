#This file is part of Tryton.  The COPYRIGHT file at the top level of this
#repository contains the full copyright notices and license terms.
from trytond.model import ModelView, ModelSQL, fields
from trytond.pyson import Equal, Eval, Not, Or, Bool


_STATES_PERSON = {
    "readonly": Or(Not(Bool(Eval('active'))),
            Not(Equal(Eval('party_type'), 'person'))),
    "invisible": Not(Equal(Eval('party_type'), 'person')),
}


class Party(ModelSQL, ModelView):
    """trytond.model.Party()
    This class inherits party.party model and adds a type attribute with
    'person' and 'organization' as values. A party with the type
    'Person' has the additional attributes firstname and gender.
    A party with the type 'Organization' has no additional attributes.
    """
    _name = "party.party"

    party_type = fields.Selection([
                ("organization", "Organization"),
                ("person", "Person"),
            ], "Party Type", select=1, readonly=False, on_change=[
                'party_type',
            ], states={
                'readonly': Not(Bool(Eval('active'))),
            })
    first_name = fields.Char("First Name", size=None, states=_STATES_PERSON)
    gender = fields.Selection([
                ("male", "Male"),
                ("female", "Female"),
                ("", ""),
            ], "Gender", select=1, sort=False, readonly=False,
            states=_STATES_PERSON)

    def default_party_type(self, cursor, user, context=None):
        """Party.default_party_type(cursor, user[, context])
        This method sets the default value for field type, depending
        on the context defined in party_type.xml.
        """
        if context is None:
            context = {}
        return context.get('party_type', 'organization')

    def get_rec_name(self, cursor, user, ids, name, context=None):
        """Party.get_rec_name(cursor, user, ids, name[, context])
        This method combines last and first name for views.
        The kind of combination of first and last names may vary from
        country to country. The pattern used here is::

            <last_name>, <first_name>

        Overwrite this method for other conventions of person names.
        """
        if not ids:
            return {}
        res = {}
        for party in self.browse(cursor, user, ids, context=context):
            res[party.id] = ", ".join(x for x in [
                    party.name, party.first_name] if x)
        return res

    def search_rec_name(self, cursor, user, name, clause, context=None):
        """Party.search_rec_name(cursor, user, name, clause[, context=None])
        This method adds the first name to search clause for searching persons.
        """
        ids = self.search(cursor, user, [
                    ('name',) + clause[1:],
                ], limit=1, context=context)
        if ids:
            return [('name',) + clause[1:]]
        else:
            ids = self.search(cursor, user, [
                        ('first_name',) + clause[1:],
                    ], limit=1, context=context)
            if ids:
                return [('first_name',) + clause[1:]]
        return [(self._rec_name,) + clause[1:]]

    def on_change_party_type(self, cursor, user, values, context=None):
        '''Party.on_change_party_type(cursor, user, values[, context])
        Method to clear party attributes, when changing a party with
        party type 'person' to type 'organization'.
        '''
        res = {}
        party_type = values.get('party_type', 'organization')
        if party_type == 'organization':
            res['party_type'] = party_type
            res['first_name'] = False
            res['gender'] = False
        return res

    def get_full_name(self, cursor, user, ids, name, context=None):
        """Party.get_full_name(cursor, user, ids, name[, context=None])
        This method overwrites the standard full name as used in reports
        to call the name of a person party. The kind of combination of
        first and last names may vary from country to country.
        The pattern used here is::

        <first_name> <last_name>

        Overwrite this method for other conventions of person names.
        """
        if not ids:
            return {}
        res = {}
        for party in self.browse(cursor, user, ids, context=context):
            res[party.id] = " ".join(x for x in [
                    party.first_name, party.name] if x)
        return res

Party()

