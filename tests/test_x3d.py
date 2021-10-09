"""
    test_collada
    ~~~~~~~~~~~~
"""

import unittest
# import requests
# from mock import patch

from domonic import domonic

from domonic.dom import *
from domonic.html import *
from domonic.xml.x3d import *
from domonic.decorators import silence


class TestCase(unittest.TestCase):

    # @silence
    def test_domonic_x3dom(self):
    	x3dom_test = html(
			head(
			    meta(**{"_http-equiv": "X-UA-Compatible"}, _content="IE=edge"),
			    title("My first X3DOM page"),
			    script(_type='text/javascript', _src='https://www.x3dom.org/download/x3dom.js'),
			    script(
		    	"""
				$(document).ready(function(){
				    var screenshotCount = 0;

				    //Every time the user clicks on the 'take screenhot' button
				    $("#btnTakeScreenshot").on("click", function() {
				        //Get data url from the runtime
				        var imgUrl = document.getElementById("canvas").runtime.getScreenshot();

				        //Create preview image...
				        var newScreenshotImage = document.createElement('img');
				        newScreenshotImage.src = imgUrl;
				        newScreenshotImage.id = "screenshot_" + screenshotCount;
				        $('#screenshotPreviews').append(newScreenshotImage);

				        //...and download link
				        var newScreenshotDownloadLink = document.createElement('a');
				        newScreenshotDownloadLink.href = imgUrl;
				        newScreenshotDownloadLink.download = "screenshot_" + screenshotCount + ".png";
				        newScreenshotDownloadLink.innerHTML = "Speichern";
				        $('#screenshotPreviews').append(newScreenshotDownloadLink);

				        screenshotCount++;
				        $('#screenshotCount').html(screenshotCount);
				    });
				});
		    	"""
			    ),
			    link(_rel='stylesheet', _type='text/css', _href='https://www.x3dom.org/download/x3dom.css')
			),
			body(
				h1("Animate Objects with X3DOM!"),
				p("Learn how to animate objects."),
				x3d(_width='500px', _height='400px').append(
			    	scene(
				        transform(_DEF="ball").append(
					        shape(
					            appearance(
					                material(_diffuseColor='1 0 0')
					            ),
					            sphere()
					        )
				        ),
			        	timeSensor(_DEF="time", _cycleInterval="2", _loop="true"),
			        	PositionInterpolator(_DEF="move", _key="0 0.5 1", _keyValue="0 0 0  0 3 0  0 0 0"),
			        	Route(_fromNode="time", _fromField ="fraction_changed", _toNode="move", _toField="set_fraction"),
			        	Route(_fromNode="move", _fromField ="value_changed", _toNode="ball", _toField="translation")
			        )
			    )
			)
		)

    	render( str(x3dom_test) )#, "sphere_test.html" )


	# def test_aframe(self):
    # 		pass


if __name__ == '__main__':
    unittest.main()
