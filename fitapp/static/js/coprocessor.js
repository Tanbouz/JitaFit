$(document).ready(main);

function main() {
  var jita = new Jita();
  jita.init();
}

function Jita() {
  this.active = null;

  this.slots = [
    // High slots
    233, 243, 254, 265, 276, 287, 297, 308,
    // Med slots
    323, 333, 344, 355, 6, 16, 26, 37,
    // Low slots
    53, 63, 73, 83, 94, 104, 115, 126,
    // Sub slots
    141, 151, 162, 173, 184,
    // Rig slots
    197, 208, 218
  ];
}

Jita.prototype.init = function() {
  var jita = this;
  jita.circle();

  $('#jita-menu-ships').on('click', function() {

    var url = 'res/menu/shiptypes';

    $.get(url).done(function(data, status) {
      // Remove previous active menu if exists
      if (jita.active) {
        $('#' + jita.active.id).remove();
      }

      // Set new active menu and append content
      jita.active = $(data).filter('div')[0];
      $('#jita-sidebar').after(data);

      $('#' + jita.active.id).children().each(function() {
        $('#' + this.id).on('click', function() {
          $('#jita-factions').remove();
          jita.factions(this.id);
        })
      })
    });
  })

  // $('#jita-menu-market').on('click', function(){
  //     var url = 'res/menu/market';
  //     $.get(url).done(function(data, status){
  //
  //         if(jita.active){
  //             $('#'+jita.active.id).remove();
  //         }
  //         jita.active = $(data).filter('div')[0];
  //         $('#jita-sidebar').after(data);
  //     });
  // })
  //
  // $('#jita-menu-character').on('click', function(){
  //     var url = 'res/menu/character';
  //
  //     $.get(url).done(function(data, status){
  //
  //         if(jita.active){
  //             $('#'+jita.active.id).remove();
  //         }
  //         jita.active = $(data).filter('div')[0];
  //         $('#jita-sidebar').after(data);
  //     });
  // })
  //
  // $('#jita-menu-fits').on('click', function(){
  //     var url = 'res/menu/fit';
  //
  //     $.get(url).done(function(data, status){
  //
  //         if(jita.active){
  //             $('#'+jita.active.id).remove();
  //         }
  //         jita.active = $(data).filter('div')[0];
  //         $('#jita-sidebar').after(data);
  //     });
  // })

  $('#ship-center').on('shipselected', function(event, ship_id) {
    $('#ship-center > img').remove();
    $('#ship-center').append('<img class="ship-image img-responsive" src="https://image.eveonline.com/Render/' + ship_id + '_512.png">');
    jita.update_slots(ship_id);
  });
};

Jita.prototype.circle = function() {
  var jita = this;

  var process = function() {
    var x = $('#fit-circle').width();
    var i = 0;
    $('#fit-center').children().each(function() {
      var element = $('#' + this.id);
      element.children().width(x / 11).height(x / 11);

      element.css({
        transform: 'rotate(' + jita.slots[i] + 'deg)'
      });

      var y = element.children('.slot').width();
      element.children().css({
        transform: 'translateX(' + x / 2.75 + 'px) translateY(' + -y / 2 + 'px)'
      });

      i++;
    });
  }

  process();

  $(window).on('resize', function() {
    process();
  });
}


Jita.prototype.factions = function(shiptypes) {
  var jita = this;
  var url = 'res/menu/factions';

  $.get(url).done(function(data, status) {
    $('#' + shiptypes).append(data);

    $('#jita-factions').children().each(function() {
      $('#' + this.id).on('click', function() {
        var faction = this.id;
        jita.getships(this.id, shiptypes);
      })
    })
  });

}

// Get all ships with the specified faction and ship type
Jita.prototype.getships = function(faction, shiptype) {
  var jita = this;
  var url = "res/menu/getships/" + shiptype + "/" + faction;

  $.get(url).done(function(data, status) {
    $('#' + faction).append(data);
    var root_div = $(data).filter('div')[0].id;

    $('#' + root_div).children().on('click', function(event) {
      var ship_id = event.currentTarget.id;
      $('#ship-center').trigger('shipselected', [ship_id]);
    })

  });
}


Jita.prototype.update_slots = function(ship_id) {
  var url = "res/menu/getslots/" + ship_id;

  $.get(url).done(function(data, status) {

    $('.slots > .slot').addClass('inactive');

    for (var i = 0; i < data['hiSlots']; i++) {
      $('#highslot-' + i + ' > .slot').removeClass('inactive');
    }

    for (var i = 0; i < data['medSlots']; i++) {
      $('#medslot-' + i + ' > .slot').removeClass('inactive');
    }

    for (var i = 0; i < data['lowSlots']; i++) {
      $('#lowslot-' + i + ' > .slot').removeClass('inactive');
    }
  });

}
