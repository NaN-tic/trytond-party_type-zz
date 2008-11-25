#This file is part of Tryton.  The COPYRIGHT file at the top level of this
#repository contains the full copyright notices and license terms.

from trytond.osv import fields, OSV

_STATES_PERSON = {
    "readonly": "active == False",
    "invisible": "type != 'person'",
}
_STATES_PARTY = {
    "readonly": "active == False",
}
_CHANGE_NAME_FIELDS = [
    "type",
    "name_order",
    "person_first_name",
    "person_last_name",
]


class PartyType(OSV):
    """Class: PartyType(OSV)
    This class inherits party.pary model and add the types 'person' and
    'organization'. A party with the type 'person' has the
    attributes firstname, lastname and gender.
    A party with the type 'Orgaization' has no additional attributes.
    """
    _description = __doc__
    _name = "party.party"

    type = fields.Selection(
            [("organization", "Organization"), ("person", "Person")],
            "Type", on_change=['type'], select=1, readonly=False,
            states={"readonly": "active == False"})
    name = fields.Char("Name", size=None, required=True, select=1,
            states={"readonly": "active == False",
                    "invisible": "type == 'person'"})
    complete_person_name = fields.Function("get_complete_person_name",
            type="char", string="Name",
            states={"readonly": "active == False",
                    "invisible": "type != 'person'"})
    person_gender = fields.Selection(
            [("male", "Male"),
             ("female", "Female"),
            ], "Gender", select=1, readonly=False, states=_STATES_PERSON)
    person_last_name = fields.Char("Last Name", size=None,
            required=False, on_change=_CHANGE_NAME_FIELDS,
            states=_STATES_PERSON)
    person_first_name = fields.Char("First Name", size=None,
            required=False, on_change=_CHANGE_NAME_FIELDS,
            states=_STATES_PERSON)
    name_order = fields.Property(type="selection", selection=
            [("first_last", "Firstname Lastname"),
             ("last_first", "Lastname, Firstname")
            ], string="Order", on_change=_CHANGE_NAME_FIELDS, required=True,
            states=_STATES_PERSON, help="The order of the name parts which " \
                    "build the party name of a person.")

    def __init__(self):
        super(PartyType, self).__init__()

    def default_active(self, cursor, user, context=None):
        return True

    def default_type(self, cursor, user, context=None):
        return "organization"

    def default_name_order(self, cursor, user, context=None):
        return "last_first"

    def default_person_gender(self, cursor, user, context=None):
        return "male"

    # This method (re-)build the name attribute for the records
    def _build_name(self, cursor, user, ids, vals, context=None):
        if context is None:
            context = {}
        if isinstance(ids, (int, long)):
            ids = [ids]
        res = {}

        if vals["type"] == "person":
            # TODO: Make an config for the party module where the user can flexible provide
            # python-code to generate the partyname entry
            print "vals:", vals
            first_name = vals["person_first_name"] or ''
            last_name = vals["person_last_name"] or ''
            if vals["name_order"] == "first_last":
                res["name"] = res["complete_person_name"] = \
                        first_name \
                        + (last_name and first_name and ' ' or '') \
                        + last_name
            elif vals["name_order"] == "last_first":
                res["name"] = res["complete_person_name"] = \
                        last_name \
                        + (last_name and first_name and ', ' or '') \
                        + first_name
            else:
                pass
        return res

    #### Object Methods
    def on_change_type(self, cursor, user, ids, vals, context=None):
        # On change of the type from person to organization or reversed,
        #  we need to delete all the other types data to prevent errors
        #  mainly caused by just hidden and not destroied data
        if not "type" in vals:
            return {}
        res = {}
        # Reset all organization data:
        if vals["type"] == "person":
            res["name"] = False
        # Reset all person data:
        if vals["type"] == "organization":
            res["person_last_name"] = False
            res["person_first_name"] = False
            res["name_order"] = None
        return res

    # Here we take care to resample the name attribute when a name part changes
    def on_change_person_last_name(self, cursor, user, ids, vals, context=None):
        return self._build_name(cursor, user, ids, vals, context=None)

    def on_change_person_first_name(self, cursor, user, ids, vals, context=None):
        return self._build_name(cursor, user, ids, vals, context=None)

    def on_change_name_order(self, cursor, user, ids, vals, context=None):
        return self._build_name(cursor, user, ids, vals, context=None)

    def get_complete_person_name(self, cursor, user, ids, name, args, context=None):
        res={}
        for item in self.browse(cursor, user, ids, context=context):
            res[item.id] = item.name
        return res

PartyType()
