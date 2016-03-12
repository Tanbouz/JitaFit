function BasicMenu(element, item_size, orientation) {
  this.element = element;
  this.item_size = item_size;
  this.items = [];

  if (orientation == "vertical") {
    this.orientation = "Y";
  } else {
    this.orientation = "X";
  }

  this.focus = null;
}

BasicMenu.prototype.Init = function() {
  var menu = this;
  this.element.children().each(
    function(index, value) {
      menu.items.push(this.id);
    }
  )
  menu.Animate();
  menu.SelectEvent();
  $('.menu-image').on('dragstart', function(event) {
    event.preventDefault();
  });
};

BasicMenu.prototype.SelectEvent = function(callback) {
  var menu = this;
  this.element.on("click", "> .menu-item", function(event) {
    var pos = menu.items.indexOf(event.currentTarget.id);
    for (var i = 0; i < pos; i++) {
      menu.Shift();
    }
    menu.Animate();
    menu.element.trigger("select", [event.currentTarget.id]);
  });
}

BasicMenu.prototype.Shift = function() {
  this.items.push(this.items.shift());
}

BasicMenu.prototype.Animate = function() {
  for (var i = 0; i < this.items.length; i++) {
    var shift = i * this.item_size;
    $("#" + this.items[i]).css("transform", "translate" + this.orientation + "(" + shift + "px)");
  }
}

function ScrollMenu(item_size) {
  this.clicked = false;
  this.scroll = true;

  // Scroll direction
  this.pre = 0;
  this.delta = 0;

  this.element = null;
  this.item_size = item_size;
  this.items = [];

  this.submenu = null;
}

ScrollMenu.prototype.init = function() {
  var menu = this;
  this.items = [];
  this.element.children().each(
    function(index, value) {
      menu.items.push(this.id);
    }
  )
  this.Animate();
  this.DragStart();
  this.DragEnd();
  this.SelectEvent();
  $('.menu-image').on('dragstart', function(event) {
    event.preventDefault();
  });
};

// Events
// -------------------------------------------
// User selects an item. Load next submenu or functionality.
ScrollMenu.prototype.SelectEvent = function() {
  var menu = this;

  this.element.one("click", "> .menu-item", function(event) {
    menu.scroll = false;
    menu.element.off("mousedown mouseup mousemove");
    var choice = event.currentTarget.id;
    menu.Collapse(choice);
    menu.ExpandEvent(choice);
    menu.element.trigger("select", [choice]);
  });
}

// Go back to this menu. Expand and remove all childern.
ScrollMenu.prototype.ExpandEvent = function(focus) {
  var menu = this;
  $("#" + focus).one("click", function(event) {
    menu.Animate();
    menu.element.trigger('expand');
    menu.focus = null;
    menu.submenu.delete();
    setTimeout(function() {
      menu.DragStart();
      menu.DragEnd();
      menu.SelectEvent();
    }, 100);
  });
}

ScrollMenu.prototype.Collapse = function(target) {
  var pos = this.items.indexOf(target);
  for (var i = 0; i < this.items.length; i++) {
    var item = $("#" + this.items[i]);
    item.css("transform", "translateY(" + 0 + "px)");
    item.addClass("hidden");
  }
  $("#" + this.items[pos]).removeClass("hidden");
};

ScrollMenu.prototype.delete = function(target) {
  var menu = this;

  if (menu.submenu) {
    menu.submenu.delete();
  }
  if (menu.element) {
    menu.element.remove();
  }
};

// Scroll and Drag functionality
// -------------------------------------------
ScrollMenu.prototype.DragStart = function() {
  var menu = this;
  this.element.on("mousedown", function(event) {
    menu.DragDirection();
    menu.scroll = true;
    setTimeout(function() {
      if (menu.scroll) {
        menu.Scroll();
      }
    }, 200);
  });
};

ScrollMenu.prototype.DragEnd = function() {
  var menu = this;
  this.element.on("mouseup mouseleave", function(event) {
    menu.scroll = false;
    setTimeout(function() {
      this.pre = 0;
      this.delta = 0;
    }, 200);
  });
};

// Detect mouse direction
ScrollMenu.prototype.DragDirection = function() {
  var menu = this;
  // Limit mousemove to once per unit time otherwise it will fire too many events
  setTimeout(function() {
    menu.element.one("mousemove", function(event) {
      var current = event.clientY;
      var delta = current - menu.pre;
      // Limit deltas to allow quick switch in direction anywhere on the page
      menu.delta = Math.max(Math.min(delta + menu.delta, 10), -10);
      menu.pre = current;
    });
    if (menu.scroll) {
      menu.DragDirection();
    }
  }, 100);
};

ScrollMenu.prototype.Scroll = function() {
  var menu = this;
  if (this.delta < 0) {
    this.Shift();
  } else {
    this.UnShift();
  }
  this.Animate();

  setTimeout(function() {
    if (menu.scroll) {
      menu.Scroll();
    }
  }, 250);
};

ScrollMenu.prototype.Shift = function() {
  this.items.unshift(this.items.pop());
}

ScrollMenu.prototype.UnShift = function() {
  this.items.push(this.items.shift());
}

ScrollMenu.prototype.Animate = function() {
  for (var i = 0; i < this.items.length; i++) {
    // Always hide one item in front to be ready to appear while scrolling.
    var shift = (i * this.item_size) - this.item_size;
    var item = $("#" + this.items[i]);
    item.css("transform", "translateY(" + shift + "px)");

    var last_position = ((this.items.length - 1) * this.item_size) - this.item_size;

    if (shift < 0 || shift == last_position) {
      // Hide elements on the edge so they won't appear to the user
      // when they switch places on the loop edge
      item.addClass("hidden");
    } else {
      item.removeClass("hidden");
    }
  }
}
