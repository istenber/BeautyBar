
var data = {};

data.modify = function(x, y, val) {
    new Ajax.Request('/modify_data', {
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
    data.modify(1, 1, $(val).getValue());
};