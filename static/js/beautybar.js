
var preview = {
    init: function() {
	this._frame = $('preview_frame');
	svgweb.appendChild(this._output_img, this._frame);
	this._timer_on = false;
    },

    preload: function() {
	if(Prototype.Browser.IE) {
	    this._load_image = this._load_image_IE;
	} else {
	    this._load_image = this._load_image_others;
	}
	this._load_image();
    },

    _load_image_IE: function() {
	console.log("TODO: IE not supported yet.");
    },

    _load_image_others: function() {
	var rnd = Math.floor(Math.random() * 1000000);
	var svg_image = document.createElement('object', true);
	svg_image.setAttribute('type', 'image/svg+xml');
	svg_image.setAttribute('data', '/output_image?' + rnd);
	svg_image.setAttribute('width', '300');
	svg_image.setAttribute('height', '200');
	svg_image.setAttribute('id', 'o_img');
	this._output_img = svg_image;
    },

    update: function() {
	if(this._timer_on) { return; }
	this._timer_on = true;
	this._loading();
	setTimeout("preview._update_image();", 100);
	return;
    },

    _loading : function() {
	svgweb.removeChild(this._output_img, this._frame);
    },

    _update_image : function() {
        this._load_image();
	svgweb.appendChild(this._output_img, this._frame);
	this._timer_on = false;
    },

};
preview.preload();

var attr = {};

attr.set_color = function(val) {
    var color = $(val).getValue();
    var generator = $('generator_name').getValue();
    var params = val + "=\"" + color + "\"";
    new Ajax.Request('/set_attr?' + params, {
	    method    : 'get',
	    onSuccess : function(out) {
		preview.update();
	    },
	    onFailure : function() { 
	    },
    });
};

attr.set_boolean = function(val, b) {
    var generator = $('generator_name').getValue();
    var params = val + "=" + b;
    new Ajax.Request('/set_attr?' + params, {
	    method    : 'get',
	    onSuccess : function(out) {
		preview.update();
	    },
	    onFailure : function() {
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
		if(x == 1) {
		    $('name' + y).setValue(resp);
		}
		if(x == 2) {
		    $('value' + y).setValue(resp);
		}
		preview.update();
	    },
	    onFailure : function() { 
	    },
    });
};

var generator = {};

generator.modify = function(val) {
    new Ajax.Request('/set_generator?name=' + val, {
	    method    : 'get',
	    onSuccess : function(out) {
		preview.update();
		update_part("info", "");
		if (edit.s == 'style') { update_attribute_table("session"); }
	    },
	    onFailure : function() { 
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
    var msg = "<br /><center>Attribute table loading...</center>";
    generator.modify(val); 
};

set_min = function() {
    var val = $('r_min').getValue();
    new Ajax.Request('/modify_data?min=' + val, {
	    method    : 'get',
	    onSuccess : function(out) {
		var resp = out.responseText.substr(4);
		$('r_min').setValue(resp);
		preview.update();
	    },
	    onFailure : function() { 
	    },
    });
};

set_max = function() {
    var val = $('r_max').getValue();
    new Ajax.Request('/modify_data?max=' + val, {
	    method    : 'get',
	    onSuccess : function(out) {
		var resp = out.responseText.substr(4);
		$('r_max').setValue(resp);
		preview.update();
	    },
	    onFailure : function() { 
	    },
    });
};

var timer_on = false;

update_attribute_table = function(generator) {
    new Ajax.Request('/attr_table?gen=' + generator, {
	    method    : 'get',
	    onSuccess : function(out) {
		$('attribute_table').update(out.responseText);
		jscolor.bind();
	    },
	    onFailure : function() { 
	    },
    });
};

update_part = function(part, params) {
    new Ajax.Request('/main?part=' + part + params, {
	    method    : 'get',
	    onSuccess : function(out) {
		$('part_' + part).update(out.responseText);
		if(part == "list") {
		    new Carousel('carousel-wrapper',
				 $$('#carousel-content .slide'),
				 $$('a.carousel-control'));
		}
	    },
	    onFailure : function() {
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
    preview.init();
    update_part("list", "");
    update_part("info", "");
    update_edit("data");
};

Event.observe(window, 'load', init, false); 

