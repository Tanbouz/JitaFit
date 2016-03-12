from django.shortcuts import render
from django.template import RequestContext
from fitapp.models import *
from django.http import JsonResponse

ships_list = {
    'mining':       'Mining Barges',
    'frigates':     'Frigates',
    'destroyers':   'Destroyers',
    'cruisers':     'Cruisers',
    'battlecruisers': 'Battlecruisers',
    'battleships':  'Battleships',
    'capital':      'Capital Ships',
    'industrial':   'Industrial Ships',
}

faction_list = {
    '500003': 'Amarr Empire',
    '500001': 'Caldari State',
    '500004': 'Gallente Federation',
    '500002': 'Minmatar Republic',
    '500000': 'Faction',
}


def igb_home(request):
    return render(request, 'igb/igb.html')


def res_home(request):
    return render(request, 'res/res.html', {'stdslots': [1, 2, 3, 4, 5, 6, 7, 8]})


def menu_shiptypes(request, template):
    return render(request, template, {'ships': ships_list})


def menu_fit(request, template):
    return JsonResponse({'name': 'Fit'})


def menu_market(request):
    return JsonResponse({'name': 'Market'})


def menu_character(request):
    return JsonResponse({'name': 'Character'})


def menu_factions(request, template):
    return render(request, template, {'factions': faction_list})


def get_ships(request, shiptype, faction, template):
    factions = [faction]

    # Expand faction into rest of the factions
    if(faction == '500000'):
        factions.remove('500000')
        exclude_list = list(faction_list.keys())
        queryset = CharacterFactions.objects.filter(
            published=True).exclude(pk__in=exclude_list)
        for result in queryset:
            factions.append(result.pk)

    s1 = set()

    ships_market_group = MarketGroups.objects.filter(parent_fk__exact=4)
    ship_type = ships_market_group.filter(name__exact=ships_list[shiptype])
    tree(ship_type[0].pk, s1)

    ships = Types.objects.filter(faction_fk__in=factions)

    faction_ships = []

    for ship in ships:
        if(ship.marketgroup_fk and (ship.marketgroup_fk.pk in s1)):
            faction_ships.append(ship)

    return render(request, template, {'ships': faction_ships, })


def tree(parent, result):
    items = MarketGroups.objects.filter(parent_fk__exact=parent)

    if len(items) == 0:
        return False
    else:
        for item in items:
            result.add(item.marketgroup_id)
            tree(item.marketgroup_id, result)
        return True


def get_slots(request, ship_id):

    shiptype = Types.objects.get(pk=ship_id)

    slots = {
        'upgradeSlotsLeft': 0,
        'lowSlots': 0,
        'medSlots': 0,
        'hiSlots': 0,
    }

    attributes = shiptype.attributes.filter(name__in=list(slots.keys()))

    slot_ids = [attribute.attribute_id for attribute in attributes]

    slot_numbers = TypeAttributes.objects.filter(
        type_fk=ship_id, attribute_fk__in=slot_ids)

    for slot in slot_numbers:
        slots[slot.attribute_fk.name] = int(slot.value)

    return JsonResponse(slots)
