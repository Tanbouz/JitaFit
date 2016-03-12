from django.db import models

class CharacterAttributes(models.Model):
    attribute_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'fitapp'

class CharacterFactions(models.Model):
    faction_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    published = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'fitapp'

# -------------------------------------------------
class AttributeCategories(models.Model):
    category_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'fitapp'

class Attributes(models.Model):
    attribute_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    defaultvalue = models.FloatField(blank=True, null=True)
    display = models.CharField(max_length=100, blank=True, null=True)
    stackable = models.BooleanField(default=False)
    highisgood = models.BooleanField(default=False)
    unit_fk = models.ForeignKey('Units', blank=True, null=True)
    category_fk = models.ForeignKey('AttributeCategories', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'fitapp'

class TypeAttributes(models.Model):
    type_fk = models.ForeignKey('Types')
    attribute_fk = models.ForeignKey('Attributes')
    value = models.FloatField()

    def __str__(self):
        return self.type_fk

    class Meta:
        app_label = 'fitapp'

# -------------------------------------------------
class Units(models.Model):
    unit_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    display = models.CharField(max_length=50, blank=True, null=True)
    description = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'fitapp'

class Categories(models.Model):
    category_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=3000, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'fitapp'

class Groups(models.Model):
    group_id = models.IntegerField(primary_key=True)
    category_fk = models.ForeignKey('Categories', blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'fitapp'

class MarketGroups(models.Model):
    marketgroup_id = models.IntegerField(primary_key=True)
    parent_fk = models.ForeignKey('self', blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'fitapp'

class MetaGroups(models.Model):
    metagroup_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'fitapp'

class MetaTypes(models.Model):
    type_fk = models.OneToOneField('Types', blank=True, null=True)
    parent_fk = models.ForeignKey('Types', related_name='parent_type_id', blank=True, null=True)
    metagroup_fk = models.ForeignKey('MetaGroups', blank=True, null=True)

    def __str__(self):
        return self.type_fk

    class Meta:
        app_label = 'fitapp'

class Traits(models.Model):
    trait_fk = models.ForeignKey('Types')
    bonus = models.FloatField(blank=True, null=True)
    bonustext = models.TextField(blank=True, null=True)
    skill_fk = models.ForeignKey('Types', related_name='skill_id', blank=True, null=True)
    unit_fk = models.ForeignKey('Units', blank=True, null=True)

    def __str__(self):
        return self.bonus

    class Meta:
        app_label = 'fitapp'

class Types(models.Model):
    type_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=3000, blank=True, null=True)
    mass = models.FloatField(blank=True, null=True)
    volume = models.FloatField(blank=True, null=True)
    capacity = models.FloatField(blank=True, null=True)
    portionsize = models.IntegerField(blank=True, null=True)
    price = models.BigIntegerField(blank=True, null=True)

    faction_fk = models.ForeignKey('CharacterFactions', blank=True, null=True)
    group_fk = models.ForeignKey('Groups', blank=True, null=True)
    marketgroup_fk = models.ForeignKey('MarketGroups', blank=True, null=True)

    attributes = models.ManyToManyField('Attributes', through='TypeAttributes')
    effects = models.ManyToManyField('Effects', through='TypeEffects')

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'fitapp'

# ---- Effects ---------------------------------------

class Effects(models.Model):
    effect_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'fitapp'

class TypeEffects(models.Model):
    type_fk = models.ForeignKey('Types', blank=True, null=True)
    effect_fk = models.ForeignKey('Effects', blank=True, null=True)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.effect_fk

    class Meta:
        app_label = 'fitapp'
