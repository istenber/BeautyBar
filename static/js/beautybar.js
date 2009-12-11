
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


var ajaxWrapper = function(url, postprocessor, data) {
    new Ajax.Request(url, {
	    method    : 'get',
	    onSuccess : function(out) {
		postprocessor(out, data);
	    },
	    onFailure : function() { 
	    },
	});
};


var attr = {
    _updater: function(out) {
	preview.update();
    },
    set_value: function(val) {
	ajaxWrapper("/set_attr?" + val + "=\"" + $(val).getValue() + "\"",
		    this._updater);
    },
    set_boolean: function(val) {
	this.set_value(val);
    },
    set_color: function(val) {
	this.set_value(val);
    },
    _generator_updater: function(out) {
	preview.update();
	update_part("info", "");
	if (edit.s == 'style') { update_attribute_table("session"); }
    },
    set_generator: function(val) {
	ajaxWrapper("/set_generator?name=" + val, this._generator_updater);
    },
};


var data = {
    _updater: function(out, limit) {
	var resp = out.responseText.substr(4);
	$('r_' + limit).setValue(resp);
	preview.update();
    },
    _set_limit: function(limit) {
	ajaxWrapper("/modify_data?" + limit + "=" + $('r_' + limit).getValue(),
		    this._updater, limit);
    },
    set_min: function() {
	this._set_limit("min");
    },
    set_max: function() {
	this._set_limit("max");
    },
};

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

fm = function(val) {
    if(val.indexOf("name")!=-1) {
	data.modify(1, val.substr(4), $(val).getValue());
    } else {
	data.modify(2, val.substr(5), $(val).getValue());
    }
};


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

