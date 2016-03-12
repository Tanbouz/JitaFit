from django.conf.urls import patterns, include, url
from django.contrib import admin
from fitapp import views

igb = [
    url(r'menu/shiptypes', views.menu_shiptypes,
        {'template': 'igb/menu_shiptypes.html'}),
    url(r'menu/factions', views.menu_factions,
        {'template': 'igb/menu_factions.html'}),
    url(r'menu/getships/(?P<shiptype>.+)/(?P<faction>.+)',
        views.get_ships, {'template': 'igb/menu_ships.html'}),
    url(r'menu/getslots/(?P<ship_id>.+)', views.get_slots),
    url(r'menu/fit',      views.menu_fit),
    url(r'menu/market',   views.menu_market),
    url(r'menu/character', views.menu_character),
    url(r'^$', views.igb_home)
]

res = [
    url(r'menu/shiptypes', views.menu_shiptypes,
        {'template': 'res/menu_shiptypes.html'}),
    url(r'menu/factions', views.menu_factions,
        {'template': 'res/menu_factions.html'}),
    url(r'menu/getships/(?P<shiptype>.+)/(?P<faction>.+)',
        views.get_ships, {'template': 'res/menu_ships.html'}),
    url(r'menu/getslots/(?P<ship_id>.+)', views.get_slots),
    url(r'menu/fit',      views.menu_fit),
    url(r'menu/market',   views.menu_market),
    url(r'menu/character', views.menu_character),
    url(r'^$', views.res_home)
]

urlpatterns = [
    url(r'jitafit/igb', include(igb)),
    url(r'jitafit/res', include(res))
]
