
var data = {};

data.modify = function(x, y, val) {
    var params = "x=" + x + "&y=" + y + "&val=" + val;
    new Ajax.Request('/modify_data?' + params, {
	    method    : 'get',
	    onSuccess : function(out) {
		$('debug').update("[" + x + "," + y + "]: " + val + 
				  " - " + out.responseText);
		start_update_timer();
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

var timer_on = 0;

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
	setTimeout("update_image();", 1000);
    }
};

