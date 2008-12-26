#This file is part of Tryton.  The COPYRIGHT file at the top level of this
#repository contains the full copyright notices and license terms.

from trytond.osv import fields, OSV

_STATES_PERSON = {
    "readonly": "active == False or party_type != 'person'",
}

_CHANGE_NAME_FIELDS = [
    "party_type",
    "party_name",
    "first_name",
    "last_name",
]


class Party(OSV):
    """Class: Party(OSV)
    This class inherits party.party model and add the types 'person' and
    'organization'. A party with the type 'person' has the basic
    attributes firstname, lastname and gender.
    A party with the type 'Organization' has no additional attributes.
    """
    _description = "PartyType"
    _name = "party.party"

    party_type = fields.Selection(
            [("organization", "Organization"), ("person", "Person")],
            "Party Type", on_change=['party_type'], select=1, readonly=False,
            states={"readonly": "active == False"})
    party_name = fields.Function("get_party_name", type="char",
            fnct_inv='set_party_name', on_change=_CHANGE_NAME_FIELDS,
            string="Name", required=True,
            states={"readonly": "active == False or party_type != 'organization'"})
    last_name = fields.Char("Last Name", size=None,
            on_change=_CHANGE_NAME_FIELDS, states={
                    "readonly": "active == False or party_type != 'person'",
                    "required": "first_name == False and party_type == 'person'"})
    first_name = fields.Char("First Name", size=None,
            on_change=_CHANGE_NAME_FIELDS, states={
                    "readonly": "active == False or party_type != 'person'",
                    "required": "last_name == False and party_type == 'person'"})
    gender = fields.Selection(
            [("male", "Male"),
             ("female", "Female")], "Gender", select=1, sort=False,
             readonly=False, states=_STATES_PERSON)

    def __init__(self):
        super(Party, self).__init__()

    def default_active(self, cursor, user, context=None):
        return True

    def default_party_type(self, cursor, user, context=None):
        """
        This method sets the default for field type, depending on the context
        defined in party_type.xml
        """
        if context is None:
            context = {}
        return context.get('party_type', 'organization')


    def default_gender(self, cursor, user, context=None):
        return "male"

    def get_party_name(self, cursor, user, ids, name, args, context=None):
        """
        This method gets the name from party and put it into function field
        party_name.
        """
        if context is None:
            context = {}
        if isinstance(ids, (int, long)):
            ids = [ids]
        res={}
        for item in self.browse(cursor, user, ids, context=context):
            res[item.id] = item.name
        return res

    def set_party_name(self, cursor, user, id, name, value, arg, context=None):
        """
        This dummy method make the function field party_name "writable".
        In real the entry is handled before via the on_change_party_name,
        which copies this party.party_name entry into the party.name entry.
        """
        return

    def create(self, cursor, user, vals, context=None):
        print "create vals:", vals
        if context is None:
            context = {}
        vals = self._cleanup_organization_vals(vals)
        if "party_name" in vals:
            vals["name"] = vals["party_name"] or vals["name"]
        return super(Party, self).create(cursor, user, vals,
               context=context)

    def write(self, cursor, user, ids, vals, context=None):
        if context is None:
            context = {}
        if isinstance(ids, (int, long)):
            ids = [ids]
        vals = self._cleanup_organization_vals(vals)
        return super(Party, self).write(cursor, user, ids, vals,
                context=context)

    def _cleanup_organization_vals(self, vals):
        """
        This private method resets all person data for type organization.
        """
        if "party_type" in vals:
            if vals["party_type"] == "organization":
                vals["last_name"] = False
                vals["first_name"] = False
                vals["gender"] = None
        return vals

    def _build_name(self, cursor, user, ids, vals, context=None):
        """
        This method (re-)build the name and party_name attribute following
        name_order rules.
        """
        if context is None:
            context = {}
        if isinstance(ids, (int, long)):
            ids = [ids]
        res = {}
        #Get the name order from users company object.
        user_obj = self.pool.get('res.user')
        user = user_obj.browse(cursor, user, user, context=context)
        vals['name_order'] = user.company.name_order

        if vals["party_type"] == "person":
            res["name"] = ""
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
        elif vals["party_type"] == "organization":
            if "name" in vals:
                res["name"] = vals["name"]
        else:
            res["name"] = None
        if "name" in res:
            res["party_name"] = res["name"]
        else:
            res["party_name"] = None
        return res

    def on_change_party_type(self, cursor, user, ids, vals, context=None):
        """
        This method deletes the opposide related fields, when changeing from
        'person' to 'organization' or vice versa.
        """
        if context is None:
            context = {}
        if isinstance(ids, (int, long)):
            ids = [ids]
        if not "party_type" in vals:
            return {}
        res = {}
        # Reset person data:
        res = self._cleanup_organization_vals(vals)
        # Reset names:
        res["name"] = res["party_name"] = False
        return res

    def on_change_last_name(self, cursor, user, ids, vals, context=None):
        return self._build_name(cursor, user, ids, vals, context=None)

    def on_change_first_name(self, cursor, user, ids, vals, context=None):
        return self._build_name(cursor, user, ids, vals, context=None)

    def on_change_party_name(self, cursor, user, ids, vals, context=None):
        if context is None:
            context = {}
        if isinstance(ids, (int, long)):
            ids = [ids]
        if not "type" in vals:
            return {}
        vals["name"] = vals["party_name"]
        return self._build_name(cursor, user, ids, vals, context=None)

Party()

class Company(OSV):
    """Class: Company(OSV)
    This class adds preferences
    <Last-Name>, <First-Name>
    <First-Name> <Last-Name>
    <Last-Name> <First-Name>
    for party type Person to the company.
    """
    _description = "Company"
    _name = "company.company"

    name_order = fields.Selection(
            [("last_comma_first", "<Last-Name>, <First-Name>"),
             ("first_last", "<First-Name> <Last-Name>"),
             ("last_first", "<Last-Name> <First-Name>"),], "Order",
            required=True, sort=False, help="The order of the name parts " \
                    "which build the party name of type person.")

    def __init__(self):
        super(Company, self).__init__()

    def default_name_order(self, cursor, user, context=None):
        return "last_comma_first"

    def on_change_party_type(self, cursor, user, ids, vals, context=None):
        # TODO: This method makes problems. It needed to be called on
        # party_type object. But how to?
        # The same is TODO with module party_bank. It even needed to be inherited
        # in a class
        # and depended in __tryton__.py.
        party_obj = self.pool.get('party.party')
        return party_obj.on_change_party_type(cursor, user, ids, vals,
                context=context)
Company()
