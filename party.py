#This file is part of Tryton.  The COPYRIGHT file at the top level of this
#repository contains the full copyright notices and license terms.
from trytond.model import ModelView, ModelSQL, fields

_STATES_PERSON = {
    "readonly": "active == False or party_type != 'person'",
    "invisible": "party_type != 'person'",
}

class Party(ModelSQL, ModelView):
    """Class: Party(ModelSQL, ModelView)
    This class inherits party.party model and adds the types 'person' and
    'organization'. A party with the type 'Person' has the basic
    attributes firstname and gender.
    A party with the type 'Organization' has no additional attributes.
    """
    _name = "party.party"

    party_type = fields.Selection(
            [("organization", "Organization"), ("person", "Person")],
            "Party Type", select=1, readonly=False,
            on_change=['party_type'],
            states={"readonly": "active == False"})
    first_name = fields.Char("First Name", size=None,
            states=_STATES_PERSON)
    gender = fields.Selection(
            [("male", "Male"),
             ("female", "Female"),
             ("", "")], "Gender", select=1, sort=False,
             readonly=False, states=_STATES_PERSON)

    def default_party_type(self, cursor, user, context=None):
        """default_party_type(self, cursor, user, context=None)
        This method sets the default for field type, depending on the context
        defined in party_type.xml.
        """
        if context is None:
            context = {}
        return context.get('party_type', 'organization')

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
        for party in self.browse(cursor, user, ids, context=context):
            res[party.id] = ", ".join(x for x in [party.name,
                                                  party.first_name] if x)
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

    def on_change_party_type(self, cursor, user, ids, values, context=None):
        res = {}
        party_type = values.get('party_type', 'organization')
        if party_type == 'organization':
            res['party_type'] = party_type
            res['first_name'] = False
            res['gender'] = False
        return res


    def get_full_name(self, cursor, user, ids, name, context=None):
        """get_full_name(self, cursor, user, ids, name, context=None)
        This method overwrites the standard full name as used in letters or
        reports to call the name of a personal party.  The kind of
        combination of first and last names may vary from country to country.
        The pattern used here is:
        <first_name> <last_name>
        Overwrite this method for other combinations.
        """
        if not ids:
            return {}
        res = {}
        for party in self.browse(cursor, user, ids, context=context):
            res[party.id] = " ".join(x for x in [party.first_name,
                                                  party.name] if x)
        return res

Party()
