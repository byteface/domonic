import sys, os
sys.path.insert(0,'../..')

from domonic.javascript import Math
from domonic.html import *
from domonic.components import SpriteCSS


classless_css = link(_rel="stylesheet", _href="https://unpkg.com/marx-css/css/marx.min.css")
jquery = script(_src="https://code.jquery.com/jquery-3.5.1.min.js")

code = div(
		audio(_id="myAudio", _autoplay="true").html(
			source("Your browser does not support the audio element.",
				_src="ken.mp3",
				# dl the mp3, call it ken.mp3. then click on ken
				# http://www.gamethemesongs.com/Hyper_Street_Fighter_II_-_CPS2_-_Ken_Stage.html
				# be nice to convert this one.. https://www.youtube.com/watch?v=zFYK8sL5BHI&t
				_type="audio/mp3")
		),
    	script(_type="text/javascript").html(
	    '''    
	    $( document ).ready(function() {
	        $( '.ken' ).on('click', function() {
	            let sound = document.getElementById("myAudio");
	            sound.currentTime = 0;
	            sound.play();

	            // goFullScreen();
	        });
	    });
	    '''
	))

level = div(
	style("""
	.bg {
	  background-image: url("bg.png");
	  height: 100%;
	  background-position: center;
	  background-repeat: no-repeat;
	  background-size: cover;
	}
	"""),
	div(_class="bg")
)

game = article(
  div( 
  	level,
  	span(SpriteCSS('ken', 70, 80, 'ken.png', 0.8, 4, True, 80), _style="position:absolute; top:70%; left:10%;", _id="moveMe")
  ),

  script("""

		var p1 = document.getElementById('moveMe'),
		keyCodes = { left: 37, up: 38, right: 39, down: 40 },
		keys = [];

		window.addEventListener('keydown', function (evt) {
		    keys[evt.keyCode] = true;
		});

		window.addEventListener('keyup', function (evt) {
		    keys[evt.keyCode] = false;
		});

		setInterval(function () {
		    
		    // get position of div
		    var x = parseInt(p1.style.left, 10),
		        y = parseInt(p1.style.top, 10);
		    
		    // update position
		    // left/right
		    if (keys[keyCodes.left]) {
		        x -= 1;
		    } else if (keys[keyCodes.right]) {
		        x += 1;
		    }
		    // up/down
		    if (keys[keyCodes.up]) {
		        y -= 1;
		    } else if (keys[keyCodes.down]) {
		        y += 1;
		    }
		    
		    // set div position
		    p1.style.left = x + 'px';
		    p1.style.top = y + 'px';
		    
		}, 1/30);


		""")

)

render( html(head(classless_css, jquery, code), body(game)), 'sf2.html' )
