
var preview = {
    init: function() {
	preview.preload();
	preview.f = $('preview_show');
	preview.l = $('preview_load');
	svgweb.appendChild(preview._output_img, preview.f);
	preview.processing = false;
    },
    preload: function() {
	if(Prototype.Browser.IE) {
	    preview._load_image = preview._load_image_ie;
	    preview.use_load_image = false;
	} else if(Prototype.Browser.Opera) {
	    preview._load_image = preview._load_image_others;
	    preview.use_load_image = false;
	} else {
	    preview._load_image = preview._load_image_others;
	    preview.use_load_image = true;
	}
	preview._output_img = preview._load_image();
    },
    _load_image_ie: function() {
	var svg_image = document.createElement('object', true);
	svg_image.setAttribute('classid', 'image/svg+xml');
	svg_image.setAttribute('src', '/preview');
	svg_image.setAttribute('width', '300');
	svg_image.setAttribute('height', '200');
	svg_image.setAttribute('id', 'preview_image');
	svg_image.addEventListener('load', function(evt) {
		preview._image_loaded(); }, false);
	return svg_image;
    },
    _load_image_others: function() {
	var svg_image = document.createElement('object', true);
	svg_image.setAttribute('type', 'image/svg+xml');
	svg_image.setAttribute('data', '/preview');
	svg_image.setAttribute('width', '300');
	svg_image.setAttribute('height', '200');
	svg_image.setAttribute('id', 'preview_image');
	svg_image.addEventListener('load', function(evt) {
		preview._image_loaded(); }, false);
	return svg_image;
    },
    update: function() {
	if(preview.processing == true) { return false; }
	preview.processing = true;
	svgweb.removeChild(preview._output_img, preview.f);
	preview._output_img = preview._load_image();
	svgweb.appendChild(preview._output_img, preview.f);
	if(preview.use_load_image) {
	    preview.f.hide();
	    preview.l.show();
	}
	return true;
    },
    _image_loaded: function() {
	if(preview.use_load_image) {
	    preview.f.show();
	    preview.l.hide();
	}
	preview.processing = false;
    }
};


var ajaxWrapper = function(url, postprocessor, data) {
    var ajax_request = new Ajax.Request(url, {
	    method    : 'get',
	    onSuccess : function(out) {
		postprocessor(out, data);
	    },
	    onFailure : function() { 
	    }
	});
    ajax_request = ajax_request;
};


var editor = {
    current: 'style',
    init: function() {
	this.buttons = {'style': [true, "style_img", this.load_images("style")],
			'data': [false, "data_img", this.load_images("data")],
			'file': [false, "file_img", this.load_images("file")]};
    },
    load_images: function(name) {
	var on = new Image();
	on.src = "/images/" + name + "_on.png";
	var off = new Image();
	off.src = "/images/" + name + "_off.png";
	return [on, off];
    },
    set_state: function(struct, state) {
	if(struct[0] == state) { return; }
	struct[0] = state;
	$(struct[1]).src = struct[2][struct[0] ? 0 : 1].src;
    },
    set_active: function(name) {
	if(name == this.current) { return; }
	this.set_state(this.buttons[this.current], false);
	this.set_state(this.buttons[name], true);
	this.current = name;
    },
    _attribute_updater: function(out) {
	$('attribute_table').update(out.responseText);
	jscolor.bind();
    },
    show_attributes: function() {
	ajaxWrapper('/attr_table', this._attribute_updater);
    }
};


var parts = {
    _updater: function(out, part) {
	$('part_' + part).update(out.responseText);
	if(part == 'info') {
	    new lightbox($('lightbox_preview'));
	}
	if((part == 'edit') && (editor.current == 'style')) {
	    editor.show_attributes();
	}
    },
    update: function(part) {
	if(part == 'edit') { return this._update_editor(); }
	ajaxWrapper('/main?part=' + part, this._updater, part);
    },
    _update_editor: function() {
	ajaxWrapper('/main?part=edit&s=' + editor.current,
		    this._updater, 'edit');
    }
};


var file = {
    clean: function() {
	file.enable_edit();
	$('f_savefile').setValue('');
	$('f_loadfile').setValue('');
	$('load_span').innerHTML = '';
	$('save_span').innerHTML = '';
    },
    disable_edit: function() {
	$('f_save').disabled = true;
	$('f_savefile').disabled = true;
	$('f_load').disabled = true;
	$('f_loadfile').disabled = true;
    },
    enable_edit: function() {
	$('f_save').disabled = false;
	$('f_savefile').disabled = false;
	$('f_load').disabled = false;
	$('f_loadfile').disabled = false;
    },
    _save_updater: function(out) {
	var resp = out.responseText;
	$('save_span').innerHTML = resp;
	file.clean_timer();
    },
    _load_updater: function(out) {
	var resp = out.responseText;
	$('load_span').innerHTML = resp;
	preview.update();
	parts.update('info');
	file.clean_timer();
    },
    save: function() {
	var val = $('f_savefile').getValue();
	$('save_span').innerHTML = 'Processing...';
	$('f_loadfile').setValue('');
	this.disable_edit();
	ajaxWrapper('/save?name=' + val, this._save_updater);
    },
    load: function() {
	var val = $('f_loadfile').getValue();
	$('load_span').innerHTML = 'Processing...';
	$('f_savefile').setValue('');
	this.disable_edit();
	ajaxWrapper('/load?name=' + val, this._load_updater);
    },
    clean_timer: function() {
	if(this._timer) {
	    clearTimeout(this._timer);
	}
	this._timer = setTimeout('file.clean()', 3000);
    }
};

var attr = {
    _updater: function(out) {
	preview.update();
    },
    set_value: function(val) {
	ajaxWrapper('/set_attr?' + val + '=\"' + $(val).getValue() + '\"',
		    this._updater);
    },
    set_random: function(val) {
	ajaxWrapper('/set_attr?' + val + '=\"random\"',
		    this._updater);
    },
    set_boolean: function(val, r) {
	ajaxWrapper('/set_attr?' + val + '=\"' + r + '\"',
		    this._updater);
    },
    set_choice: function(val, c) {
	ajaxWrapper('/set_attr?' + val + '=\"' + c + '\"',
		    this._updater);
    },
    set_color: function(val) {
	this.set_value(val);
    },
    set_float: function(val, min, max) {
	var v = $(val).getValue();
	if (!parseFloat(v)) { $(val).setValue(1.0); return; }
	if (v > max) { $(val).setValue(max); return; }
	if (v < min) { $(val).setValue(min); return; }
	this.set_value(val);
    },
    _generator_updater: function(out) {
	preview.update();
	parts.update('info');
	if (editor.current == 'style') { editor.show_attributes(); }
    },
    set_generator: function(val) {
	ajaxWrapper('/set_generator?name=' + val, this._generator_updater);
    }
};


var data = {
    _updater: function(out, limit) {
	var resp = out.responseText.substr(4);
	$('r_' + limit).setValue(resp);
	preview.update();
    },
    _set_limit: function(limit) {
	ajaxWrapper('/set_range?' + limit + '=' + $('r_' + limit).getValue(),
		    this._updater, limit);
    },
    set_min: function() {
	this._set_limit('min');
    },
    set_max: function() {
	this._set_limit('max');
    },
    set_name: function(row) {
	var id = 'name_' + row;
	ajaxWrapper('/set_name?row=' + row + '&val=\"' +
		    $('r_' + id).getValue() + '\"',
		    this._updater, id);
    },
    set_value: function(row) {
	var id = 'value_' + row;
	ajaxWrapper('/set_value?row=' + row + '&val=\"' +
		    $('r_' + id).getValue() + '\"',
		    this._updater, id);
    }
};


process_button = function(button) {
    editor.set_active(button);
    parts.update('edit');
};


init = function() {
    preview.init();
    editor.init();
    parts.update('info');
    parts.update('edit');
    var carousel_attributes = { duration: 0.1, visibleSlides: 3}
    var carousel = new Carousel('carousel-wrapper',
				$$('.slide'),
				$$('a.carousel-control'),
				carousel_attributes);
};


Event.observe(window, 'load', init, false); 

