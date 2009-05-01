#This file is part of Tryton.  The COPYRIGHT file at the top level of this
#repository contains the full copyright notices and license terms.
from trytond.model import ModelView, ModelSQL, fields

_STATES_PERSON = {
    "readonly": "active == False or party_type != 'person'",
    "invisible": "party_type != 'person'",
}

class Party(ModelSQL, ModelView):
    """Class: Party(ModelSQL, ModelView)
    This class inherits party.party model and add the types 'person' and
    'organization'. A party with the type 'person' has the basic
    attributes firstname and gender.
    A party with the type 'Organization' has no additional attributes.
    """
    _name = "party.party"

    party_type = fields.Selection(
            [("organization", "Organization"), ("person", "Person")],
            "Party Type", select=1, readonly=False,
            states={"readonly": "active == False"})
    first_name = fields.Char("First Name", size=None, states=_STATES_PERSON)
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

    def _name_get(self, cursor, user, ids, name, arg, delimiter=' ',
            context=None):
        """_name_get(self, cursor, user, ids, name, arg, delimiter,
                     context=None)
        This method combines last name and first name with a delimiter.
        The kind of combination of first and last names may vary from
        country to country. The general pattern used here is:
        <last_name><delimiter><first_name>
        Overwrite this method for other combinations.
        """
        if not ids:
            return {}
        res = {}
        for party in self.browse(cursor, user, ids, context=context):
            res[party.id] = party.name + delimiter + party.first_name
        return res

    def get_rec_name(self, cursor, user, ids, name, arg, context=None):
        """get_rec_name(self, cursor, user, ids, name, arg, context=None)
        This method combines last name and first name for general views.
        """
        delimiter = ", "
        return self._name_get(cursor, user, ids, name, arg, delimiter,
                context=None)

    def get_full_name(self, cursor, user, ids, name, arg, context=None):
        """get_full_name(self, cursor, user, ids, name, arg, context=None)
        This method overwrite the standard full name as used in letters or
        reports to call the name of a party.
        """
        delimiter = " "
        return self._name_get(cursor, user, ids, name, arg, delimiter,
                context=None)
Party()
