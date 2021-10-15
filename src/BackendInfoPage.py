import logging
import asyncio

from configuration import DefaultConfig
from Backend import Backend
from ListGames import ListGames
from piptools.writer import OutputWriter

class BackendInfoPage():

    async def generatePage(self):
        self.configuration = DefaultConfig()
        self.backend = Backend()
        await self.backend.setup(self.configuration)
        
        logger.info("Loading data:")
        systems = ListGames()
        data_read = await systems.read_from_cache()
        if (len(data_read)>0):
            outputFile = open("cache.html", "w")
            outputFile.write(str(
                "<html>\n\
                <head>\n\
                <meta charset='UTF-8'>\n\
                <title>Cache</title>\n\
                \n\
                <style>\n\
                .axes {\n\
                  padding: 1em;\n\
                }\n\
                \n\
                .buttons {\n\
                  margin-left: 1em;\n\
                }\n\
                \n\
                /*meter*/.axis {\n\
                  min-width: 200px;\n\
                  margin: 1em;\n\
                }\n\
                \n\
                .button {\n\
                  display: inline-block;\n\
                  width: 1em;\n\
                  text-align: center;\n\
                  padding: 1em;\n\
                  border-radius: 20px;\n\
                  border: 1px solid black;\n\
                  background-image: url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAAAXNSR0IArs4c6QAAAAxJREFUCNdjYPjPAAACAgEAqiqeJwAAAABJRU5ErkJggg==);\n\
                  background-size: 0% 0%;\n\
                  background-position: 50% 50%;\n\
                  background-repeat: no-repeat;\n\
                }\n\
                \n\
                .pressed {\n\
                  border: 1px solid red;\n\
                }\n\
                \n\
                .touched::after {\n\
                  content: 'touch';\n\
                  display: block;\n\
                  position: absolute;\n\
                  margin-top: -0.2em;\n\
                  margin-left: -0.5em;\n\
                  font-size: 0.8em;\n\
                  opacity: 0.7;\n\
                }\n\
                </style>\n\
                </head>\n\
                <body>\n\
                <script src='https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js'></script>\n\
                <link rel='stylesheet' type='text/css' href='https://cdn.datatables.net/1.11.0/css/jquery.dataTables.css'>\n\
                <script type='text/javascript' charset='utf8' src='https://cdn.datatables.net/1.11.0/js/jquery.dataTables.js'></script>\n\
                <script type='text/javascript' charset='utf8' src='https://cdn.datatables.net/select/1.3.3/js/dataTables.select.js'></script>\n\
                <link rel='stylesheet' type='text/css' href='https://cdn.datatables.net/select/1.3.3/css/select.dataTables.css'>\n\
                <table id='mytable' class='display'>"
                ))
            outputFile.write(str("<thead><tr>"))
            for headerKey in data_read[0]:
                outputFile.write(str("<th>"+str(headerKey)+"</th>"))
            outputFile.write(str("</tr></thead><tbody>"))
            for entry in data_read:
                logger.info(entry)
                outputFile.write(str("<tr>"))
                for key in entry:
                    if (key=="hash_digest"):
                        outputFile.write(str("<td><a href='https://gamesdb.gog.com/platforms/test/external_releases/"+str(entry[key])+"'>"+str(entry[key])+"</td>"))
                    else:
                        outputFile.write(str("<td>"+str(entry[key])+"</td>"))
                outputFile.write(str("</tr>"))
            outputFile.write(str("</tbody>\n\
            </table>\n\
            <h2 id='start'>Press a button on your controller to start</h2>\n\
            <script type='text/javascript'>$(document).ready( function () {  var myDataTable =  $('#mytable').DataTable({select: {style: 'single'}});} );</script>\n\
            <script type='text/javascript'>\n\
            $.fn.dataTable.Api.register('row().next()', function() {\n\
                // Current row position\n\
                var nrp = this.table().rows()[0].indexOf( this.index() ) + 1;\n\
                // Exists ?\n\
                if( nrp < 0 ) {\n\
                    return null;\n\
                }\n\
                // Next row index by position\n\
                var nri = this.table().rows()[0][ nrp ];\n\
                // Return next row by its index\n\
                return this.table().row( nri );\n\
            });\n\
            $.fn.dataTable.Api.register('row().prev()', function() {\n\
                // Next row position\n\
                var prp = this.table().rows()[0].indexOf( this.index() ) - 1;\n\
                // Exists ?\n\
                if( prp < 0 ) {\n\
                    return null;\n\
                }\n\
                // Previous row index by position\n\
                var pri = ( this.table().rows()[0][ prp ] );\n\
                // Return previous row by its index\n\
                return this.table().row( pri );\n\
            });\n\
            \
            </script>\n\
            <script type='text/javascript'>\n\
                var haveEvents = 'GamepadEvent' in window;\n\
                var haveWebkitEvents = 'WebKitGamepadEvent' in window;\n\
                var controllers = {};\n\
                var rAF = window.mozRequestAnimationFrame ||\n\
                  window.webkitRequestAnimationFrame ||\n\
                  window.requestAnimationFrame;\n\
                \n\
                function connecthandler(e) {\n\
                  addgamepad(e.gamepad);\n\
                }\n\
                function addgamepad(gamepad) {\n\
                  controllers[gamepad.index] = gamepad; var d = document.createElement('div');\n\
                  d.setAttribute('id', 'controller' + gamepad.index);\n\
                  var t = document.createElement('h1');\n\
                  t.appendChild(document.createTextNode('gamepad: ' + gamepad.id));\n\
                  d.appendChild(t);\n\
                  var b = document.createElement('div');\n\
                  b.className = 'buttons';\n\
                  for (var i=0; i<gamepad.buttons.length; i++) {\n\
                    var e = document.createElement('span');\n\
                    e.className = 'button';\n\
                    //e.id = 'b' + i;\n\
                    e.innerHTML = i;\n\
                    b.appendChild(e);\n\
                  }\n\
                  d.appendChild(b);\n\
                  var a = document.createElement('div');\n\
                  a.className = 'axes';\n\
                  for (i=0; i<gamepad.axes.length; i++) {\n\
                    e = document.createElement('meter');\n\
                    e.className = 'axis';\n\
                    //e.id = 'a' + i;\n\
                    e.setAttribute('min', '-1');\n\
                    e.setAttribute('max', '1');\n\
                    e.setAttribute('value', '0');\n\
                    e.innerHTML = i;\n\
                    a.appendChild(e);\n\
                  }\n\
                  d.appendChild(a);\n\
                  document.getElementById('start').style.display = 'none';\n\
                  document.body.appendChild(d);\n\
                  rAF(updateStatus);\n\
                }\n\
                \n\
                function disconnecthandler(e) {\n\
                  removegamepad(e.gamepad);\n\
                }\n\
                \n\
                function removegamepad(gamepad) {\n\
                  var d = document.getElementById('controller' + gamepad.index);\n\
                  document.body.removeChild(d);\n\
                  delete controllers[gamepad.index];\n\
                }\n\
                \n\
                function updateStatus() {\n\
                \
                  scangamepads();\n\
                  for (j in controllers) {\n\
                    var controller = controllers[j];\n\
                    var d = document.getElementById('controller' + j);\n\
                    var buttons = d.getElementsByClassName('button');\n\
                    for (var i=0; i<controller.buttons.length; i++) {\n\
                      var b = buttons[i];\n\
                      var val = controller.buttons[i];\n\
                      var pressed = val == 1.0;\n\
                      var touched = false;\n\
                      if (typeof(val) == 'object') {\n\
                        pressed = val.pressed;\n\
                        if ('touched' in val) {\n\
                          touched = val.touched;\n\
                        }\n\
                        val = val.value;\n\
                      }\n\
                      var pct = Math.round(val * 100) + '%';\n\
                      b.style.backgroundSize = pct + ' ' + pct;\n\
                      b.className = 'button';\n\
                      if (pressed) {\n\
                        b.className += ' pressed';\n\
                      }\n\
                      if (touched) {\n\
                        b.className += ' touched';\n\
                      }\n\
                    }\n\
                \n\
                    var axes = d.getElementsByClassName('axis');\n\
                    for (var i=0; i<controller.axes.length; i++) {\n\
                      var a = axes[i];\n\
                      a.innerHTML = i + ': ' + controller.axes[i].toFixed(4);\n\
                      a.setAttribute('value', controller.axes[i]);\n\
                    }\n\
                  }\n\
                  rAF(updateStatus);\n\
                }\n\
                \n\
                function scangamepads() {\n\
                  var gamepads = navigator.getGamepads ? navigator.getGamepads() : (navigator.webkitGetGamepads ? navigator.webkitGetGamepads() : []);\n\
                  for (var i = 0; i < gamepads.length; i++) {\n\
                    if (gamepads[i] && (gamepads[i].index in controllers)) {\n\
                      controllers[gamepads[i].index] = gamepads[i];\n\
                    }\n\
                  }\n\
                  //Add on to change stuff\n\
                //if (controllers[0].axes[0].toFixed(4)==1)//right\n\
                if (controllers!=null && controllers[0]!=undefined && myStartTime +175 < Date.now()) {\n\
                    if (controllers[0].axes[1].toFixed(4)==1)//down\n\
                    {\n\
                        var nextval = $('#mytable').DataTable().row({ selected: true }).next();\n\
                        if (null!= nextval){\n\
                            nextval.select()\n\
                            var myNodeLocation = $('#mytable').DataTable().rows({order: 'current'}).nodes().indexOf($('#mytable').DataTable().row({ selected: true }).node());\n\
                            var myPage = Math.floor(myNodeLocation/$('#mytable').DataTable().page.len());\n\
                            $('#mytable').DataTable().page(myPage).draw(false);\n\
                            //$('#mytable').DataTable().page( 'next' ).draw( 'page' );\n\
                            myStartTime = Date.now();\n\
                        }\n\
                    }\n\
                    if (controllers[0].axes[1].toFixed(4)==-1)//up\n\
                    {\n\
                        var prevval = $('#mytable').DataTable().row({ selected: true }).prev()\n\
                        if (null!= prevval){\n\
                            prevval.select()\n\
                            var myNodeLocation = $('#mytable').DataTable().rows({order: 'current'}).nodes().indexOf($('#mytable').DataTable().row({ selected: true }).node());\n\
                            var myPage = Math.floor(myNodeLocation/$('#mytable').DataTable().page.len());\n\
                            $('#mytable').DataTable().page(myPage).draw(false);\n\
                            //$('#mytable').DataTable().page( 'previous' ).draw( 'page' );\n\
                            myStartTime = Date.now();\n\
                        }\n\
                    }\n\
                    \n\
                }\n\
                }\n\
                \n\
                var myStartTime = Date.now();\n\
                if (haveEvents) {\n\
                  window.addEventListener('gamepadconnected', connecthandler);\n\
                  window.addEventListener('gamepaddisconnected', disconnecthandler);\n\
                } else if (haveWebkitEvents) {\n\
                  window.addEventListener('webkitgamepadconnected', connecthandler);\n\
                  window.addEventListener('webkitgamepaddisconnected', disconnecthandler);\n\
                } else {\n\
                  setInterval(scangamepads, 500);\n\
                }\n\
                </script>\n\
            </body>\n\
            </html>"))
    
    def main(self):
        asyncio.run(BackendInfoPage.generatePage(self))
        
if __name__ == "__main__":
    logger = logging.getLogger("")
    logger.setLevel(logging.DEBUG)
    runner = BackendInfoPage();
    runner.main()