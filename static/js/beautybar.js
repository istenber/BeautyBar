
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
	parts.update("info");
	if (editor.current == 'style') { editor.show_attributes(); }
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
	ajaxWrapper("/set_range?" + limit + "=" + $('r_' + limit).getValue(),
		    this._updater, limit);
    },
    set_min: function() {
	this._set_limit("min");
    },
    set_max: function() {
	this._set_limit("max");
    },
    set_name: function(row) {
	var id = "name_" + row;
	ajaxWrapper("/set_name?row=" + row + "&val=\"" +
		    $('r_' + id).getValue() + "\"",
		    this._updater, id);
    },
    set_value: function(row) {
	var id = "value_" + row;
	ajaxWrapper("/set_value?row=" + row + "&val=\"" +
		    $('r_' + id).getValue() + "\"",
		    this._updater, id);
    },
};


var editor = {
    current: 'data',
    _attribute_updater: function(out) {
	$('attribute_table').update(out.responseText);
	jscolor.bind();
    },
    show_attributes: function() {
	ajaxWrapper("/attr_table", this._attribute_updater);
    },
};


var parts = {
    _updater: function(out, part) {
	$('part_' + part).update(out.responseText);
	if(part == "list") {
	    new Carousel('carousel-wrapper',
			 $$('#carousel-content .slide'),
			 $$('a.carousel-control'));
	}
	if(part == "edit" && editor.current == 'style') {
	    editor.show_attributes();
	}
    },
    update: function(part) {
	if(part == "edit") { return this._update_editor(); }
	ajaxWrapper("/main?part=" + part, this._updater, part);
    },
    _update_editor: function() {
	ajaxWrapper("/main?part=edit&s=" + editor.current,
		    this._updater, 'edit');
    }
};


process_button = function(button) {
    editor.current = button;
    parts.update("edit");
};


init = function() {
    preview.init();
    parts.update("list");
    parts.update("info");
    parts.update("edit");
};


Event.observe(window, 'load', init, false); 

