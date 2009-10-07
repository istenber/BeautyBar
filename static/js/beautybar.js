
var data = {};

data.modify = function(x, y, val) {
    params = "x=" + x + "&y=" + y + "&val=" + val;
    new Ajax.Request('/modify_data?' + params, {
	    method    : 'get',
	    onSuccess : function(out) {
		$('debug').update("[" + x + "," + y + "]: " + val + 
				  " - " + out.responseText);
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