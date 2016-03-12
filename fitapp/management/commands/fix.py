from django.core.management.base import BaseCommand, CommandError
from fitapp.models import *
import pymssql
import yaml

class Command(BaseCommand):
    args = None
    help = 'DB fixes'

    def handle(self, *args, **options):
        app_name = 'fitapp'

        self.factions()
        self.ships_factions()

    # Fix ship factions. Factions are in a yaml file provided in SDE.
    def ships_factions(self):

        with open('/opt/jita/jitafit/dev/typeIDs.yaml') as f:
            data = yaml.load(f)

            for typeid in data:
                # Only process type ids that have a faction id defined
                if 'factionID' in data[typeid]:
                    the_type = Types.objects.filter(pk=typeid)
                    if(len(the_type) > 0):
                        # Get faction model object so as to use for the foriegn key
                        chr_faction = CharacterFactions.objects.filter(pk=data[typeid]['factionID'])
                        if(len(chr_faction) > 0):
                            the_type[0].faction_fk = chr_faction[0]
                            the_type[0].save()

    def factions(self):
        published = [
            "Caldari State",
            "Minmatar Republic",
            "Amarr Empire",
            "Gallente Federation",
            "Guristas Pirates",
            "Angel Cartel",
            "Blood Raider Covenant",
            "ORE",
            "Servant Sisters of EVE",
            "Mordu's Legion Command",
            "Sansha's Nation",
            "Serpentis",
        ]

        factions = CharacterFactions.objects.all()

        for faction in factions:
            if(faction.name in published):
                faction.published = True
            else:
                faction.published = False

            faction.save()
