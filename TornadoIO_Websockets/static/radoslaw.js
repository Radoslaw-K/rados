$(function(){
		var ws;
		var logger = function(msg){
		var now = new Date();
		var sec = now.getSeconds();
		var min = now.getMinutes();
		var hr = now.getHours();

		$("#log").html($("#log").html() + "<br/>" + hr + ":" + min + ":" + sec + " ___ " +  msg);
		//$("#log").animate({ scrollTop: $('#log')[0].scrollHeight}, 100);
		$('#log').scrollTop($('#log')[0].scrollHeight);
		}
 
        var sender = function() {
		var msg = $("#msg").val();
		if (msg.length > 0)
		ws.send(msg);
		$("#msg").val('');
		}
 
		var temp_updater = function(temperature) {
		$("#thermometer").text(temperature + "\u00B0"+"C");
		}
		
        var sbrd_sender = function() {
		var sbrd_msg = $("#sbrd_message").val();
		if (sbrd_msg.length > 0) ws.send("sbrd_" + sbrd_msg);
        $("#sbrd_message").val('');
        }

        ws = new WebSocket("wss://7c7a6577.dataplicity.io/ws");

        ws.onmessage = function(evt) {
		if(evt.data[0] === '{'){
			if(evt.data[1] === 't' ){
			temp_updater(evt.data.slice(6,10) );
			}
				
			logger(evt.data.slice(1));
			}
		
		var canvas = document.getElementById('canvas_image');
		var context = canvas.getContext('2d');
		var imageObj = new Image();
		imageObj.onload = function () {
			context.drawImage(imageObj, 0, 0, 640, 480);
			};
		imageObj.src = 'data:image/jpg;base64,'+evt.data; 
		};

        ws.onclose = function(evt) { 
		$("#log").text("...Connection was closed..."); 
		$("#thebutton #msg").prop('disabled', true);
		};

        ws.onopen = function(evt) {
		$("#log").text("Opening socket..."); 
		};
 
        $("#msg").keypress(function(event) {
		if (event.which == 13) {
			sender();
			}
		});

        $("#sbrd_message").keypress(function(event) {
		if (event.which == 13) {
			sbrd_sender();
			}
        });
 
        $("#thebutton").click(function(){
		sender();
		});

        $("#green_on").click(function(){
		ws.send("on_g");
		});

        $("#green_off").click(function(){
		ws.send("off_g");
		});

        $("#red_on").click(function(){
		ws.send("on_r");
		});

        $("#red_off").click(function(){
		ws.send("off_r");
		});

       $("#video_on").click(function(){
		ws.send("on_vid");
		});
	
	   $("#sbrd_button").click(function(){
		sbrd_sender();
        });
	
	   

      });
