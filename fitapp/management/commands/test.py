from django.core.management.base import BaseCommand, CommandError
from fitapp.models import *
import pymssql
import sys

class Command(BaseCommand):
    args = None
    help = 'Populate database with data from EVE Static Data Export'

    def handle(self, *args, **options):
        app_name = 'fitapp'

        ship_id = 603

        shiptype = Types.objects.get(pk = ship_id)

        slots = {
            'upgradeSlotsLeft': 0,
            'lowSlots': 0,
            'medSlots': 0,
            'hiSlots': 0,
        }

        attributes = shiptype.attributes.filter(name__in = list(slots.keys()))

        slot_ids = [attribute.attribute_id for attribute in attributes]

        slot_numbers = TypeAttributes.objects.filter(type_fk = ship_id, attribute_fk__in = slot_ids)

        for slot in slot_numbers:
            slots[slot.attribute_fk.name] = int(slot.value)

        print(slots)
