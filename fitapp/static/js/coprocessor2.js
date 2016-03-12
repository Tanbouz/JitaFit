$(document).ready(main);

function main() {
  var jita = new Jita();
  jita.init();
}

function Jita() {
  this.menu_main = null;
  this.active = null;

  this.ships = new ShipsSelect();
  this.market = null;
  this.characters = null;
  this.fits = null;
}

Jita.prototype.init = function() {
  jita = this;
  var menu_main = new BasicMenu($('#menu-main'), 55, 'horizontal');
  menu_main.Init();

  $('#menu-main').on('select', function(event, focus) {
    url = $('#' + focus).data('url');
    func = $('#' + focus).data('func');

    if (jita.active) {
      jita.active.unload();
    }

    if (jita[func]) {
      jita[func].load();
      jita.active = jita[func];
    }
  })
};

function ShipsSelect() {
  this.shiptypes_menu = null;
  this.ship_menu = null;
  this.factions = null;

  this.selected_faction = null;
  this.selected_shiptypes = null;
  this.selected_ship = null;
}

ShipsSelect.prototype.load = function() {
  this.shiptypes_menu = new ScrollMenu(55);
  this.factions_menu = new ScrollMenu(55);
  this.ships_menu = new ScrollMenu(55);

  this.shiptypes_menu.submenu = this.factions_menu;
  this.factions_menu.submenu = this.ships_menu;

  this.load_shiptypes();
};


ShipsSelect.prototype.unload = function() {
  this.shiptypes_menu.delete();
};

ShipsSelect.prototype.load_shiptypes = function() {
  var self = this;
  url = 'igb/menu/shiptypes';

  $.get(url).done(function(data, status) {
    $("#fit-market").append(data);
    self.shiptypes_menu.element = $('#menu-shiptypes');

    setTimeout(function() {
      self.shiptypes_menu.init();
    }, 100)

    $('#menu-shiptypes').on('select', function(event, focus) {
      self.selected_shiptype = focus;
      self.load_factions();
    })
  });
};

ShipsSelect.prototype.load_factions = function() {
  var self = this;
  url = 'igb/menu/factions';

  $.get(url).done(function(data, status) {
    $("#fit-market").append(data);
    self.factions_menu.element = $('#menu-factions');

    setTimeout(function() {
      self.factions_menu.init();
    }, 100)

    $('#menu-factions').on('select', function(event, focus) {
      self.selected_faction = focus;
      self.load_ships();
    })
  });
};

ShipsSelect.prototype.load_ships = function() {
  var self = this;
  url = "igb/menu/getships/" + self.selected_shiptype + "/" + this.selected_faction

  $.get(url).done(function(data, status) {
    $("#fit-market").append(data);
    self.ships_menu.element = $('#menu-ships');

    setTimeout(function() {
      self.ships_menu.init();
    }, 100)

    $('#menu-ships').on('select', function(event, focus) {

    })
  });
};
