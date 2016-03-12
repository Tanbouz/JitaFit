from django.core.management.base import BaseCommand, CommandError
from fitapp.models import *
import pymssql
import sys

class Command(BaseCommand):
    args = None
    help = 'Populate database with data from EVE Static Data Export'

    def handle(self, *args, **options):
        app_name = 'fitapp'
        tables = [
            # ---- Characters -----------------------------------
            BasicTable(
                name = CharacterAttributes,
                fields = ('attribute_id', 'name'),
                query = """ SELECT
                    chrAttributes.attributeID,
                    chrAttributes.attributeName
                    FROM chrAttributes """,
                foreign_keys = []
            ),

            BasicTable(
                name = CharacterFactions,
                fields = ('faction_id', 'name'),
                query = """ SELECT
                    chrFactions.factionID,
                    chrFactions.factionName
                    FROM chrFactions """,
                foreign_keys = []
            ),
            # ---- General -----------------------------------

            BasicTable(
                name = Units,
                fields = ('unit_id', 'name', 'display', 'description'),
                query = """ SELECT
                    eveUnits.unitID,
                    eveUnits.unitName,
                    eveUnits.displayName,
                    eveUnits.description
                    FROM eveUnits """,
                foreign_keys = []
            ),
            # ---- Attributes -----------------------------------

            BasicTable(
                name = AttributeCategories,
                fields = ('category_id', 'name'),
                query = """ SELECT
                    dgmAttributeCategories.categoryID,
                    dgmAttributeCategories.categoryName
                    FROM dgmAttributeCategories """,
                foreign_keys = []
            ),

            BasicTable(
                name = Attributes,
                fields = ('attribute_id', 'name', 'defaultvalue', 'display',
                          'stackable', 'highisgood', 'unit_fk', 'category_fk'),
                query = """ SELECT
                    dgmAttributeTypes.attributeID,
                    dgmAttributeTypes.attributeName,
                    dgmAttributeTypes.defaultValue,
                    dgmAttributeTypes.displayName,
                    dgmAttributeTypes.stackable,
                    dgmAttributeTypes.highIsGood,
                    dgmAttributeTypes.unitID,
                    dgmAttributeTypes.categoryID
                    FROM dgmAttributeTypes """,
                foreign_keys = [(Units, 'unit_fk'),
                                (AttributeCategories, 'category_fk')]
            ),

            BasicTable(
                name = Categories,
                fields = ('category_id', 'name', 'description'),
                query = """ SELECT
                    invCategories.categoryID,
                    invCategories.categoryName,
                    invCategories.description
                    FROM invCategories """,
                foreign_keys = []
            ),

            BasicTable(
                name = Groups,
                fields = ('group_id', 'category_fk', 'name'),
                query = """ SELECT
                    invGroups.groupID,
                    invGroups.categoryID,
                    invGroups.groupName
                    FROM invGroups """,
                foreign_keys = [(Categories, 'category_fk')]
            ),

            BasicTable(
                name = MetaGroups,
                fields = ('metagroup_id', 'name'),
                query = """ SELECT
                    invMetaGroups.metaGroupID,
                    invMetaGroups.metaGroupName
                    FROM invMetaGroups """,
                foreign_keys = []
            ),
            TreeTable(
                name = MarketGroups,
                fields = ('marketgroup_id', 'parent_fk', 'name'),
                query = """ SELECT
                    invMarketGroups.marketGroupID,
                    invMarketGroups.parentGroupID,
                    invMarketGroups.marketGroupName
                    FROM invMarketGroups
                    WHERE invMarketGroups.parentGroupID {0} """,
                primary_key = 'marketgroup_id',
                foreign_keys = [(MarketGroups, 'parent_fk')]
            ),
            BasicTable(
                name = Types,
                fields = ('type_id', 'name', 'description' , 'mass', 'volume',
                'capacity', 'portionsize' , 'price' , 'faction_fk', 'group_fk',
                'marketgroup_fk'),
                query = """ SELECT
                    invTypes.typeID,
                    invTypes.typeName,
                    invTypes.description,
                    invTypes.mass,
                    invTypes.volume,
                    invTypes.capacity,
                    invTypes.portionSize,
                    invTypes.basePrice,
                    invTypes.raceID,
                    invTypes.groupID,
                    invTypes.marketGroupID
                    FROM invTypes
                    JOIN invGroups
                    ON invGroups.groupID = invTypes.groupID
                    WHERE invGroups.categoryID IN (6,7,8,16,18,20,32) """,
                foreign_keys = [(CharacterFactions, 'faction_fk'),
                                (Groups,'group_fk'),
                                (MarketGroups, 'marketgroup_fk')]
            ),
            BasicTable(
                name = MetaTypes,
                fields = ('type_fk', 'parent_fk', 'metagroup_fk'),
                query = """ SELECT
                    invMetaTypes.typeID,
                    invMetaTypes.parentTypeID,
                    invMetaTypes.metaGroupID
                    FROM invMetaTypes """,
                foreign_keys = [(Types, 'type_fk'), (Types,'parent_fk'),
                                (MetaGroups, 'metagroup_fk')]
            ),
            BasicTable(
                name = TypeAttributes,
                fields = ('type_fk', 'attribute_fk', 'value'),
                query = """ SELECT
                    dgmTypeAttributes.typeID,
                    dgmTypeAttributes.attributeID,
                    coalesce(valueInt, valueFloat)
                    FROM dgmTypeAttributes
                    JOIN invTypes ON invTypes.typeID = dgmTypeAttributes.typeID
                    JOIN invGroups ON invGroups.groupID = invTypes.groupID
                    WHERE invGroups.categoryID IN (6,7,8,16,18,20,32)
                    AND invTypes.published = 1 """,
                foreign_keys = [(Types, 'type_fk'), (Attributes,'attribute_fk')]
            ),
            # ---- Effects ---------------------------------------
            BasicTable(
                name = Effects,
                fields = ('effect_id', 'name'),
                query = """ SELECT DISTINCT
                    dgmEffects.effectID,
                    dgmEffects.effectName
                    FROM dgmTypeEffects
                    JOIN invTypes ON invTypes.typeID = dgmTypeEffects.typeID
                    JOIN invGroups ON invGroups.groupID = invTypes.groupID
                    JOIN dgmEffects ON dgmEffects.effectID = dgmTypeEffects.effectID
                    WHERE invGroups.categoryID IN (6,7,8,16,18,20,32)
                    AND invTypes.published = 1
                    AND dgmEffects.published = 1 """,
                foreign_keys = []
            ),
            BasicTable(
                name = TypeEffects,
                fields = ('type_fk', 'effect_fk'),
                query = """ SELECT DISTINCT
                    dgmTypeEffects.typeID,
                    dgmTypeEffects.effectID
                    FROM dgmTypeEffects
                    JOIN invTypes
                    ON invTypes.typeID = dgmTypeEffects.typeID
                    JOIN invGroups
                    ON invGroups.groupID = invTypes.groupID
                    JOIN dgmEffects
                    ON dgmEffects.effectID = dgmTypeEffects.effectID
                    WHERE invGroups.categoryID IN (6,7,8,16,18,20,32)
                    AND invTypes.published = 1
                    AND dgmEffects.published = 1 """,
                foreign_keys = [(Types, 'type_fk'), (Effects,'effect_fk')]
            ),
        ]


        connection = pymssql.connect(server = '',
                                    port=1433,
                                    user = '',
                                    password = '',
                                    database = '')
        cursor = connection.cursor()


        switches = {
            'CharacterAttributes' :
                {'clean': True,'populate': True},
            'CharacterFactions' :
                {'clean': True,'populate': True},
            'Units' :
                {'clean': True,'populate': True},
            'AttributeCategories' :
                {'clean': True,'populate': True},
            'Attributes' :
                {'clean': True,'populate': True},
            'Categories' :
                {'clean': True,'populate': True},
            'Groups' :
                {'clean': True,'populate': True},
            'MetaGroups' :
                {'clean': True,'populate': True},
            'MarketGroups' :
                {'clean': True,'populate': True},
            'Types' :
                {'clean': True,'populate': True},
            'MetaTypes' :
                {'clean': True,'populate': True},
            'TypeAttributes' :
                {'clean': True,'populate': True},
            'Effects' :
                {'clean': True,'populate': True},
            'TypeEffects' :
                {'clean': True,'populate': True},
        }


        try:
            for table in tables:
                table_name = table.table_name.__name__
                self.stdout.write("> " + table_name)
                switch = switches[table_name]
                if( switch['clean'] ):
                    table.clean()
                if( switch['populate'] ):
                    table.populate(cursor)

        except KeyboardInterrupt:
            self.stdout.write("\nStopped")
        else:
            self.stdout.write("Done!")





class Table():

    def __init__(self, name, fields):
        self.table_name = name
        self.fields = fields

    def populate(self):
        pass

    def convert_strings(self, row):
        # Convert to UTF-8
        for field in row.items():
            if type(field[1]) is bytes:
                # Decode bytes as latin1 to default python str which is utf-8
                row[field[0]] = field[1].decode('latin_1')

    def link_foreign_keys(self, row):
        # Process foreign keys
        for key in self.foreign_keys:
            foreign_table = key[0]
            key_value = key[1]
            key_obj = None
            try:
                key_obj = foreign_table.objects.get(pk=row[key_value])
            except foreign_table.DoesNotExist:
                continue
            finally:
                row[key_value] = key_obj

    def clean(self):
        self.table_name.objects.all().delete()

class BasicTable(Table):

    def __init__(self, name, fields, query, foreign_keys = []):
        Table.__init__(self, name, fields)
        self.query = query
        self.foreign_keys = foreign_keys

    def populate(self, cursor):

        cursor.execute(self.query)

        for row in cursor:
            row = dict(zip(self.fields, row))

            self.link_foreign_keys(row)
            self.convert_strings(row)

            try:
                self.table_name.objects.update_or_create(**row)
            except ValueError:
                print("Value error: row %s skipped." % row)


class TreeTable(Table):

    def __init__(self, name, fields, query, primary_key, foreign_keys = []):
        Table.__init__(self, name, fields)
        self.query = query
        self.primary_key = primary_key
        self.foreign_keys = foreign_keys

    def populate(self, cursor):
        self._populate(None, cursor)

    def _populate(self, parent, cursor):
        if parent is None:
            query = self.query.format('IS NULL')
        else:
            query = self.query.format('= ' + str(parent))

        cursor.execute(query)
        parents = []

        for row in cursor:
            row = dict(zip(self.fields, row))
            self.convert_strings(row)
            self.link_foreign_keys(row)

            try:
                self.table_name.objects.update_or_create(**row)
            except ValueError:
                print("Value error: row %s skipped." % row)
            else:
                parents.append(row[self.primary_key])

        for parent in parents:
            self._populate(parent, cursor)
