"""
    domonic.components
    ====================================

    A bit of a dumping ground for components ideas.

    Mainly used by the examples.

"""


import base64
import json

from domonic.html import *
from domonic.events import *


class Websocket(object):
    """[Creates a websocket with listeners for particular events]

    # TODO - collect other or all Window data and pass to a window object

    Args:
        str ([reference]): [the javascript variable name given to the socket]
        str ([address]): [where you want to connect to]
        str ([target]): [the dom element to attach the listeners to]
    """

    @staticmethod
    def get_event(msg):
        evt = None
        try:
            dom_event = json.loads(msg)
        except Exception as e:
            return  # pass on non json message

        # print(msg)
        event_string = dom_event['type']

        if event_string == "keydown" or event_string == "keyup":
            evt = KeyboardEvent(event_string)
            evt.keyCode = dom_event['keyCode']
            evt.charCode = dom_event['charCode']
            evt.code = dom_event['code']
            evt.key = dom_event['key']

        elif event_string == 'mousedown' or event_string == 'mouseup' or event_string == "mousemove":
            evt = MouseEvent(event_string)
            evt.initMouseEvent(_type=event_string, screenX=dom_event['screenX'], screenY=dom_event['screenY'],
                               clientX=dom_event['clientX'], clientY=dom_event['clientY'],
                               ctrlKey=dom_event['ctrlKey'], altKey=dom_event['altKey'], shiftKey=dom_event['shiftKey'])

        elif event_string in ["drag", "dragend", "dragenter", "dragexit", "dragleave", "dragover", "dragstart", "drop"]:
            evt = DragEvent(event_string)
            try:
                evt.dataTransfer = dom_event['dataTransfer']
            except Exception as e:
                pass

        elif event_string == "hashchange":
            # print(dom_event)
            evt = HashChangeEvent(event_string)
            evt.oldURL = dom_event['oldURL']
            evt.newURL = dom_event['newURL']

        elif event_string == 'cut' or event_string == 'copy' or event_string == "paste":
            # print("SUP::",event_string, dom_event)
            evt = ClipboardEvent(event_string)
            evt.clipboardData = dom_event['clipboardData']

        elif event_string == 'wheel':
            evt = WheelEvent(event_string)
            # print(evt)
            # print(dom_event)
            evt.deltaX = dom_event['deltaX']
            evt.deltaY = dom_event['deltaY']
            evt.deltaZ = dom_event['deltaZ']
            evt.deltaMode = dom_event['deltaMode']
            # ?? TODO - no deltaX? - myabe stripped by stringify? was on wrong target

        return evt

    def __init__(self, reference='socket', address='ws://0.0.0.0:5555', target="body",
                 mouse_events=True, keyboard_events=True,
                 ui_events=False, focus_events=False, touch_events=False, wheel_events=False,
                 animation_events=False, clipboard_events=False, error_events=False, submit_events=False,
                 pointer_events=False, before_unload_events=False, SVG_events=False, timer_events=False,
                 drag_events=False, hashchange_events=False, input_events=False, page_transition_events=False,
                 popstate_events=False, storage_events=False, transition_events=False, progress_events=False):

        self.reference = reference
        self.address = address
        self.mouse_events = mouse_events
        self.keyboard_events = keyboard_events
        self.ui_events = ui_events
        self.focus_events = focus_events
        self.touch_events = touch_events
        self.wheel_events = wheel_events
        self.animation_events = animation_events
        self.clipboard_events = clipboard_events
        self.error_events = error_events
        self.submit_events = submit_events
        self.pointer_events = pointer_events
        self.before_unload_events = before_unload_events
        self.SVG_events = SVG_events
        self.timer_events = timer_events
        self.drag_events = drag_events
        self.hashchange_events = hashchange_events
        self.input_events = input_events
        self.page_transition_events = page_transition_events
        self.popstate_events = popstate_events
        self.storage_events = storage_events
        self.transition_events = transition_events
        self.progress_events = progress_events

    def _add_listener(self, event, target='body'):
        return str('''
            $("''' + target + '''").on("''' + event + '''", function(event){
                socket.send( stringify_object(event) );
            });
            ''')
        # TODO - no jquery. detect targets and use # addEventListener

    def __str__(self):
        events = ''
        if self.mouse_events:
            events += self._add_listener('mousedown')
            events += self._add_listener('mousemove')
            events += self._add_listener('mouseup')
        if self.keyboard_events:
            events += self._add_listener('keydown')
            events += self._add_listener('keyup')
        if self.ui_events:  # https://www.w3schools.com/jsref/obj_uievent.asp
            events += self._add_listener('abort')
            events += self._add_listener('beforeunload')
            events += self._add_listener('error')
            events += self._add_listener('load')
            events += self._add_listener('resize')
            events += self._add_listener('scroll')
            events += self._add_listener('select')
            events += self._add_listener('unload')
        if self.focus_events:
            events += self._add_listener('blur')
            events += self._add_listener('focus')
            events += self._add_listener('focusin')
            events += self._add_listener('focusout')
        if self.touch_events:
            events += self._add_listener('touchstart')
            events += self._add_listener('touchend')
            events += self._add_listener('touchmove')
            events += self._add_listener('touchcancel')
        if self.wheel_events:
            # events += self._add_listener('wheel')
            events += '''
            window.addEventListener('wheel', function(){
                socket.send( stringify_object(event) );
            }, false);
            '''
        if self.animation_events:
            events += self._add_listener('animationend')
            events += self._add_listener('animationiteration')
            events += self._add_listener('animationstart')
        if self.clipboard_events:
            # events += self._add_listener('copy')
            # events += self._add_listener('cut')
            # events += self._add_listener('paste')
            events += '''
            window.addEventListener('cut', function(){
                socket.send( stringify_object(event) );
            }, false);
            window.addEventListener('copy', function(){
                socket.send( stringify_object(event) );
            }, false);
            window.addEventListener('paste', function(){
                socket.send( stringify_object(event) );
            }, false);
            '''
        # if self.error_events:
        # events += self._add_listener('')
        if self.submit_events:
            events += self._add_listener('submit')
        # if self.pointer_events:
            # events += '''
            # $("body").on("keydown", function(event){
            #     socket.send( stringify_object(event) );
            # })
            # $("body").on("keyup", function(event){
            #     socket.send( stringify_object(event) );
            # })
            # '''
        # if self.before_unload_events:
            # events += '''
            # $("body").on("keydown", function(event){
            #     socket.send( stringify_object(event) );
            # })
            # $("body").on("keyup", function(event){
            #     socket.send( stringify_object(event) );
            # })
            # '''
        # if self.SVG_events:
            # events += '''
            # $("body").on("keydown", function(event){
            #     socket.send( stringify_object(event) );
            # })
            # $("body").on("keyup", function(event){
            #     socket.send( stringify_object(event) );
            # })
            # '''
        # if self.timer_events:
            # events += '''
            # $("body").on("keydown", function(event){
            #     socket.send( stringify_object(event) );
            # })
            # $("body").on("keyup", function(event){
            #     socket.send( stringify_object(event) );
            # })
            # '''
        if self.drag_events:
            events += self._add_listener('drag')
            events += self._add_listener('dragend')
            events += self._add_listener('dragenter')
            events += self._add_listener('dragleave')
            events += self._add_listener('dragover')
            events += self._add_listener('dragstart')
            events += self._add_listener('drop')
        if self.hashchange_events:
            # events += self._add_listener('hashchange', "window")
            events += '''
            window.addEventListener('hashchange', function(){
                socket.send( stringify_object(event) );
            }, false);
            '''
        if self.input_events:
            events += self._add_listener('input')
        if self.page_transition_events:
            events += self._add_listener('pagehide')
            events += self._add_listener('pageshow')
        if self.popstate_events:
            events += self._add_listener('popstate')
        if self.storage_events:
            events += self._add_listener('storage')
        if self.transition_events:
            events += self._add_listener('transitionend')
        if self.progress_events:
            events += self._add_listener('error')
            events += self._add_listener('loadstart')

        return str(
            script('''
            const socket = new WebSocket("''' + self.address + '''");

            function stringify_object(object, depth=0, max_depth=2) {
                //console.log(object);
                // change max_depth to see more levels, for a touch event, 2 is good
                if (depth > max_depth)
                    return 'Object';

                const obj = {};
                for (let key in object) {
                    let value = object[key];
                    if (value instanceof Node)
                        // specify which properties you want to see from the node
                        value = {id: value.id};
                    else if (value instanceof Window)
                        value = 'Window';
                    else if (value instanceof Object)
                        value = stringify_object(value, depth+1, max_depth);

                    if(key=="originalEvent"){ // note im stripping this one off
                        continue;
                    }
                    obj[key] = value;
                }
                return depth? obj: JSON.stringify(obj);
            }

            $(document).ready(function(){
            ''' + events + """
            });"""
            )
        )


# class Video():
# class Sound():
# def JS(self, thing):
#     	if '.js' in thing[0:15]:
# 		return script( _src=thing )
# 	return script(thing)
# def CSS(self, thing):
# 	if '/' in thing[0:15]:
# 		return link( _rel="stylesheet", _href=f"{thing}" )
# 	return script(thing)


class SpriteCSS(object):
    """ a css sprite sheet.

    this spritesheet works by shifting the position of a bg image
    uses css animation. usage:

    animated_monster = SpriteCSS('monster', 190, 240, 'assets/spritesheets/monster.png', 0.8, 10)

    Args:
        _id - requires an ID which currently becomes a 'css class'
        width
        height
        spritesheet
        time
        steps
        loop
        y_offset - for spritesheets with mulitple rows you can offset the ypos
        bg_color

    Returns:
        str: A HTML rendered string

    """
    STYLE = lambda _id, width, height, spritesheet, time, steps, loop, y_offset, bg_color: """
        .""" + _id + """ {
          background:""" + bg_color + """;
          width:""" + str(width) + """px;
          height:""" + str(height) + """px;
          background: url('""" + spritesheet + """') left center;
          animation:""" + _id + """ """ + str(time) + """s steps(""" + str(steps) + """) infinite;
        }
        /*
        @keyframes """ + _id + """ {
            100% { background-position: -""" + str(steps * width) + """px; }
        }
        */
        @keyframes """ + _id + """ {
            from { background-position:0px -""" + str(y_offset) + """px; }
            to { background-position:-""" + str(steps * width) + """px -""" + str(y_offset) + """px; }
        }
    """

    def __init__(self, id: str, width: int, height: int, spritesheet: str, time, steps: int, loop: bool = True, y_offset: int = 0, bg_color: str = "none"):
        self.id = id
        self.styles = SpriteCSS.STYLE(id, width, height, spritesheet, time, steps, loop, y_offset, bg_color)

    def __str__(self):
        return str(
            span(
                style(self.styles),
                div(_class=self.id)
            )
        )
# _ss = SpriteCSS( path )


# other sprite types may be needed...
# _ss = Sprite()
# _ss = BaseSprite()
# _ss = SpriteJS( path )
# _ss = SpriteSVG( path )
# _ss = SpriteGIF( path )
# _ss = SpriteShader( path )
# _ss = TileSet( path )


class DomonicJS(object):
    def __init__(self):
        pass

    def __str__(self):
        return script("""
            window.domonic = {'version':'0.0.3'}; // || domonic.js
            function print(msg){
                console.log(msg);
            }
            function title(str){
                return str.charAt(0).toUpper();
            }
            function* enumerate(it, start = 0) {
                // i.e. for (const [value, index] of enumerate(word)) {
                let index = start;
                for (const value of it) {
                    yield [value, index++];
                }
            }
            //class list() {
            //    constructor(list) {
            //        this.list = list;
            //    }
            //    append(item) {
            //        this.list.push(item);
            //    }
            //}
            """
        )

# class ImgButton():

#     def __init__(self, up, over=None, down=None, label=None, label_position=None):
#         self.up = up
#         self.over = over
#         self.down = down


# class ImgCheckbox():

#     def __init__(self, up, over=None, down=None, label=None, label_position=None):
#         self.up = up
#         self.over = over
#         self.down = down


class Sound(object):

    def __init__(self, filename):
        self.filename = filename

    def __str__(self):
        return str(
            div(
                audio(source(_src=self.filename, _type="audio/mp3"), _id="sfx", _autoplay="true"),
                script("""
                function play_sound( filename ) {
                let sound = document.getElementById("sfx");
                sound.currentTime = 0;
                sound.src = filename
                sound.play();
                };
                """, _type="text/javascript"
                ),
                _id='sound'
            )
        )


class ProgressBar(object):

    def __init__(self,):
        """
        a progress bar for loading or health / mana etc
        """
        # self.direction # the fill direction for the progress bar.
        # self.max
        # self.min
        self.percent
        self.value
        # self.style =

    def __str__(self):
        # $('#progress_bar span').css('width', somevalue);
        return str(
            div(span(_style="width:100%"), _id="progress_bar", _class="meter")
        )


class Input(object):

    BUTTON = "button"
    CHECKBOX = "checkbox"
    COLOR = "color"
    DATE = "date"
    DATETIME = "datetime-local"
    EMAIL = "email"
    FILE = "file"
    HIDDEN = "hidden"
    IMAGE = "image"
    MONTH = "month"
    NUMBER = "number"
    PASSWORD = "password"
    RADIO = "radio"
    RANGE = "range"
    RESET = "reset"
    SEARCH = "search"
    SUBMIT = "submit"
    TEL = "tel"
    TEXT = "text"
    TIME = "time"
    URL = "url"
    WEEK = "week"

    def __init__(self, _type, _id=None, _name=None, _label=None, *args, **kwargs):
        self._type = _type
        self._label = _label
        self._id = _id
        self._name = _name

    def __str__(self):
        # lab = str(label(self._label, _for=self._name))
        lab = str(label(str(self._label)))
        inp = str(input(_type=self._type, _id=self._id, _name=self._name))
        return str(lab + inp)


# WARNING. What is not documented is subject to lots of change!
# below are just examples of how to build your own components
# they may be removed in future version.
# You should build your own components libaries using domonic


class Modal(object):  # TODO - shouldn't this extend dom?

    def __init__(self, reference=None, content=None):
        self.reference = reference
        self.content = content

    def __str__(self):
        return str(
            div(
                div(
                    span("&times;", _class="close", **{"_data-ref": self.reference}),
                    div(self.content),
                    _class="modal-content",
                    _style="background-color:#fefefe;margin:15% auto;padding:20px;border:1px solid;width:80%;"
                ),
                _class="modal",
                _style="display:none;position:fixed;z-index:1;left:0;top:0;width:100%;height:100%; \
                    overflow:auto;background-color:rgb(0,0,0);background-color:rgba(0,0,0,0.4);",
                _id=self.reference
            )
        )


class Webpage(object):  # TODO - shouldn't this extend html?

    def __init__(self, content=None):
        self.content = content

    def __str__(self):
        classless_css = link(_rel="stylesheet", _href="https://unpkg.com/marx-css/css/marx.min.css")
        jquery = script(_src="https://code.jquery.com/jquery-3.5.1.min.js")
        code = script('''
            $(document).on( "click", ".close", function() {
                var _id = $(this).data('ref');
                $('#'+_id).css("display","none");
            });
            $(document).on( "click", ".open", function() {
                var _id = $(this).data('ref');
                $('#'+_id).css("display","block");
            });

            // When the user clicks anywhere outside of the modal, close it
            //window.onclick = function(event) {
            //    if (event.targeevent_string == modal) {
            //        modal.style.display = "none";
            //    }
            //}

            // pass an ElementID and an endpoint to redraw that div with the endpoints response
            window.redraw = function( _id, endpoint ){
                $.get( endpoint, function( data ) {
                window.console.log(data)
                $( "#"+_id ).html( $(data).html() );
                });
            }

        ''')
        styles = style('''
            .domonic-container {
                padding:20px;
            }
            .modal {
                display: none;
                position: fixed;
                z-index: 1;
                left: 0;
                top: 0;
                width: 100%;
                height: 100%;
                overflow: auto;
                background-color: rgb(0,0,0);
                background-color: rgba(0,0,0,0.4);
            }
            .modal-content {
                background-color: #fefefe;
                margin: 15% auto;
                padding: 20px;
                border: 1px solid #888;
                width: 80%;
            }
            .btn-sm {
                font-size:10px;
                padding: 0px;
                padding-left: 2px;
                padding-right: 2px;
            }
            .del {
                background-color:red;
            }
            .go {
                background-color:green;
            }

        ''')
        return str(
            html(
                '<!DOCTYPE HTML>',
                head(classless_css, jquery, code, styles),
                body(div(self.content, _class="domonic-container"))
            )
        )


# quick templates

webpage_tmpl = lambda content: f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <title>webpage</title>
    </head>
    <body>
    {content}
    </body>
    </html>
    """


# carousel_tmpl = lambda content: f"""
#     <div class="carousel slide" data-ride="carousel">
#         <div class="carousel-inner">
#             {content}
#         </div>
#         <a class="left carousel-control" href="#myCarousel" role="button" data-slide="prev">
#             <span class="glyphicon glyphicon-chevron-left" aria-hidden="true"></span>
#             <span class="sr-only">Previous</span>
#         </a>
#         <a class="right carousel-control" href="#myCarousel" role="button" data-slide="next">
#             <span class="glyphicon glyphicon-chevron-right" aria-hidden="true"></span>
#             <span class="sr-only">Next</span>
#         </a>
#     </div>
#     """

# item_tmpl = lambda content: f"""
#     <div class="item">
#         {content}
#     </div>
#     """
