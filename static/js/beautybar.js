
var preview = {
    init: function() {
	this.preload();
	this.f = $('preview_show');
	this.l = $('preview_load');
	svgweb.appendChild(this._output_img, this.f);
	this.processing = false;
    },
    preload: function() {
	this.use_load_image = false;
	if(Prototype.Browser.Gecko) {
	    this.use_load_image = true;
	}
	this._output_img = this._load_image();
    },
    _load_image: function() {
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
	if(this.processing == true) { return false; }
	this.processing = true;
	if(Prototype.Browser.IE) {
	    this._output_img = $('preview_image');
	}
	svgweb.removeChild(this._output_img, this.f);
	this._output_img = this._load_image();
	svgweb.appendChild(this._output_img, this.f);
	if(this.use_load_image) {
	    this.f.hide();
	    this.l.show();
	}
	return true;
    },
    _image_loaded: function() {
	if(this.use_load_image) {
	    this.f.show();
	    this.l.hide();
	}
	this.processing = false;
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
    _set_state: function(name) {
	if(name == this.current) {
	    $('mbut_' + name + '_on').show();
	    $('mbut_' + name + '_off').hide();
	} else {
	    $('mbut_' + name + '_off').show();
	    $('mbut_' + name + '_on').hide();
	}
    },
    set_active: function(name) {
	if(name == this.current) { return; }
	this.current = name;
	this._set_state('style');
	this._set_state('data');
	this._set_state('file');
	parts.update('edit');
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
	this.enable_edit();
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
	ajaxWrapper('/save?name="' + val + '"', this._save_updater);
    },
    load: function() {
	var val = $('f_loadfile').getValue();
	$('load_span').innerHTML = 'Processing...';
	$('f_savefile').setValue('');
	this.disable_edit();
	ajaxWrapper('/load?name="' + val + '"', this._load_updater);
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
    set_num: function(name, val) {
	ajaxWrapper('/set_attr?' + name + '=\"' + val + '\"',
		    this._updater);
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
    _dataset_updater: function(out, limit) {
	parts.update('edit');
	preview.update();
    },
    dataset: function(name) {
	ajaxWrapper('/dataset?name=' + name,
		    this._dataset_updater);
    },
    add_row: function() {
	ajaxWrapper('/add_row', this._dataset_updater);
    },
    del_row: function() {
	ajaxWrapper('/del_row', this._dataset_updater);
    },
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


init = function() {
    preview.init();
    parts.update('info');
    parts.update('edit');
    var carousel_attributes = { duration: 0.1, visibleSlides: 3}
    var carousel = new Carousel('carousel-wrapper',
				$$('.slide'),
				$$('a.carousel-control'),
				carousel_attributes);
};


Event.observe(window, 'load', init, false); 

