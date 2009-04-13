#This file is part of Tryton.  The COPYRIGHT file at the top level of this
#repository contains the full copyright notices and license terms.
from trytond.model import ModelView, ModelSQL, fields

_STATES_PERSON = {
    "readonly": "active == False or party_type != 'person'",
    "invisible": "party_type != 'person'",
}

class Party(ModelSQL, ModelView):
    """Class: Party(OSV)
    This class inherits party.party model and add the types 'person' and
    'organization'. A party with the type 'person' has the basic
    attributes firstname and gender.
    A party with the type 'Organization' has no additional attributes.
    """
    _description = "PartyType"
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
        """
        This method sets the default for field type, depending on the context
        defined in party_type.xml
        """
        if context is None:
            context = {}
        return context.get('party_type', 'organization')

    def get_rec_name(self, cursor, user, ids, name, arg, context=None):
        if not ids:
            return {}
        res = {}
        for party in self.browse(cursor, user, ids, context=context):
            res[party.id] = ", ".join(x for x in [party.name,
                party.first_name] if x)
        return res

Party()
