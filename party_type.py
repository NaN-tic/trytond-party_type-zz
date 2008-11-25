#This file is part of Tryton.  The COPYRIGHT file at the top level of this
#repository contains the full copyright notices and license terms.

from trytond.osv import fields, OSV

_STATES_PERSON = {
    "readonly": "active == False",
    "readonly": "type != 'person'",
}

_CHANGE_NAME_FIELDS = [
    "type",
    "person_name",
    "name_order",
    "first_name",
    "last_name",
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
    person_name = fields.Function("get_person_name", type="char",
            string="Name", required=False, states={
                    "readonly": "active == False",
                    "invisible": "type != 'person'"})
    last_name = fields.Char("Last Name", size=None,
            on_change=_CHANGE_NAME_FIELDS, states={
                    "readonly": "active == False",
                    "readonly": "type != 'person'",
                    "required": "first_name == False and type == 'person'"})
    first_name = fields.Char("First Name", size=None,
            on_change=_CHANGE_NAME_FIELDS, states={
                    "readonly": "active == False",
                    "readonly": "type != 'person'",
                    "required": "last_name == False and type == 'person'"})
    name_order = fields.Property(type="selection", selection=
            [("first_last", "<First-Name> <Last-Name>"),
             ("last_first", "<Last-Name> <First-Name>"),
             ("last_comma_first", "<Last-Name>, <First-Name>")
            ], string="Order", on_change=_CHANGE_NAME_FIELDS, required=True,
            states=_STATES_PERSON, help="The order of the name parts which " \
                    "build the party name of a person.")
    gender = fields.Selection(
            [("male", "Male"),
             ("female", "Female"),
            ], "Gender", select=1, readonly=False, states=_STATES_PERSON)

    def __init__(self):
        super(PartyType, self).__init__()

    def default_active(self, cursor, user, context=None):
        return True

    def default_type(self, cursor, user, context=None):
        return "organization"

    def default_name_order(self, cursor, user, context=None):
        return "last_first"

    def default_gender(self, cursor, user, context=None):
        return "male"

    def get_person_name(self, cursor, user, ids, name, args, context=None):
        res={}
        for item in self.browse(cursor, user, ids, context=context):
            res[item.id] = item.name
        return res

    def write(self, cursor, user, ids, vals, context=None):
        # Reset all person data for type organization:
        if vals["type"] == "organization":
            vals["last_name"] = False
            vals["first_name"] = False
            vals["name_order"] = None
            vals["gender"] = None
        return super(PartyType, self).write(cursor, user, ids, vals,
                context=context)

    # This method (re-)build the name attribute for the records
    def _build_name(self, cursor, user, ids, vals, context=None):
        if context is None:
            context = {}
        if isinstance(ids, (int, long)):
            ids = [ids]
        res = {}
        res["name"] = ""
        if vals["type"] == "person":
            first_name = vals["first_name"] or ''
            last_name = vals["last_name"] or ''
            if vals["name_order"] == "first_last":
                res["name"] = \
                        first_name \
                        + (last_name and first_name and ' ' or '') \
                        + last_name
            elif vals["name_order"] == "last_first":
                res["name"] = \
                        last_name \
                        + (last_name and first_name and ' ' or '') \
                        + first_name
            elif vals["name_order"] == "last_comma_first":
                res["name"] = \
                        last_name \
                        + (last_name and first_name and ', ' or '') \
                        + first_name
            else:
                pass
        res["person_name"] = res["name"]
        return res

    def on_change_type(self, cursor, user, ids, vals, context=None):
        # On change of the type from 'person' to 'organization' or reversed,
        # we need to delete all the opposide type fields
        if not "type" in vals:
            return {}
        res = {}
        # Reset all organization data:
        if vals["type"] == "person":
            res["name"] = False
        # Reset all person data:
        if vals["type"] == "organization":
            res["last_name"] = False
            res["first_name"] = False
            res["name_order"] = None
            res["gender"] = None
        return res

    def on_change_last_name(self, cursor, user, ids, vals, context=None):
        return self._build_name(cursor, user, ids, vals, context=None)

    def on_change_first_name(self, cursor, user, ids, vals, context=None):
        return self._build_name(cursor, user, ids, vals, context=None)

    def on_change_name_order(self, cursor, user, ids, vals, context=None):
        return self._build_name(cursor, user, ids, vals, context=None)

PartyType()
