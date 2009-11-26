
var attr = {};

attr.set_color = function(val) {
    var color = $(val).getValue();
    var generator = $('generator_name').getValue();
    $('debug').update("set_color(" + val + ", " + color + ")");
    var params = val + "=\"" + color + "\"";
    new Ajax.Request('/set_attr?' + params, {
	    method    : 'get',
	    onSuccess : function(out) {
		start_update_timer();
	    },
	    onFailure : function() { 
		$('debug').update("ajax failed");
	    },
    });
};

attr.set_boolean = function(val, b) {
    var generator = $('generator_name').getValue();
    $('debug').update("set_boolean(" + val + ", " + b + ")");
    var params = val + "=" + b;
    new Ajax.Request('/set_attr?' + params, {
	    method    : 'get',
	    onSuccess : function(out) {
		start_update_timer();
	    },
	    onFailure : function() {
		$('debug').update("ajax failed");
	    },
    });
};

var data = {};

data.modify = function(x, y, val) {
    var params = "x=" + x + "&y=" + y + "&val=" + val;
    new Ajax.Request('/modify_data?' + params, {
	    method    : 'get',
	    onSuccess : function(out) {
		var resp = out.responseText.substr(4);
		$('debug').update("[" + x + "," + y + "]: " + val + 
				  " - " + resp);
		if(x == 1) {
		    $('name' + y).setValue(resp);
		}
		if(x == 2) {
		    $('value' + y).setValue(resp);
		}
		start_update_timer();
	    },
	    onFailure : function() { 
		$('debug').update("ajax failed");
	    },
    });
};

var generator = {};

generator.modify = function(val) {
    new Ajax.Request('/set_generator?name=' + val, {
	    method    : 'get',
	    onSuccess : function(out) {
		update_image();
		update_attribute_table(val);
	    },
	    onFailure : function() { 
		$('debug').update("ajax failed");
	    },
    });
};

fm = function(val) {
    if(val.indexOf("name")!=-1) {
	data.modify(1, val.substr(4), $(val).getValue());
    } else {
	data.modify(2, val.substr(5), $(val).getValue());
    }
};

gen = function(val) {
    $('debug').update("generator: " + val);
    var msg = "<br /><center>Attribute table loading...</center>";
    $('attribute_table').update(msg);
    $('gen_name').update(val);
    generator.modify(val); 
};

set_min = function() {
    $('debug').update("set_min");
    var val = $('r_min').getValue();
    new Ajax.Request('/modify_data?min=' + val, {
	    method    : 'get',
	    onSuccess : function(out) {
		var resp = out.responseText.substr(4);
		$('debug').update("min set to " + resp);
		$('r_min').setValue(resp);
		start_update_timer();
	    },
	    onFailure : function() { 
		$('debug').update("ajax failed");
	    },
    });
};

set_max = function() {
    $('debug').update("set_max");
    var val = $('r_max').getValue();
    new Ajax.Request('/modify_data?max=' + val, {
	    method    : 'get',
	    onSuccess : function(out) {
		var resp = out.responseText.substr(4);
		$('debug').update("max set to " + resp);
		$('r_max').setValue(resp);
		start_update_timer();
	    },
	    onFailure : function() { 
		$('debug').update("ajax failed");
	    },
    });
};

var timer_on = 0;

update_attribute_table = function(generator) {
    new Ajax.Request('/attr_table?gen=' + generator, {
	    method    : 'get',
	    onSuccess : function(out) {
		$('attribute_table').update(out.responseText);
	    },
	    onFailure : function() { 
		$('debug').update("ajax failed");
	    },
    });
};

update_image = function() {
    $('output_image').update(
  "<object data=\"/output_image?" + Math.floor(Math.random() * 1000000) + 
  "\" type=\"image/svg+xml\" height=\"200\" width=\"300\" />");
    timer_on = 0;
    $('debug').update("image updated");
};

start_update_timer = function() {
    if(timer_on == 0) {
	timer_on = 1;
	setTimeout("update_image();", 100);
    }
};

update_part = function(part, params) {
    new Ajax.Request('/main?part=' + part + params, {
	    method    : 'get',
	    onSuccess : function(out) {
		$('part_' + part).update(out.responseText);
	    },
	    onFailure : function() {
		$('debug').update("ajax failed");
	    },
    });
};

var edit = { 
    s : 'data'
};

update_edit = function(s) {
    edit.s = s;
    update_part("edit", "&s=" + edit.s);
    if (edit.s == 'style') { update_attribute_table("session"); }
};

process_button = function(but) {
    update_edit(but);
};

init = function() {
    update_part("list", "");
    update_part("info", "");
    update_edit("data");
    update_image(); // must be last, but why?
};

Event.observe(window, 'load', init, false); 

