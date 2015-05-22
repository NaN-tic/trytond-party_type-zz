# The COPYRIGHT file at the top level of this repository
#repository contains the full copyright notices and license terms.

from trytond.pool import Pool
from .party import Party


def register():
    Pool.register(
        Party,
        module='party_type', type_='model')
