import sys
import threading
import json
from SocketServer import ThreadingMixIn
from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
from HTTPWebSocketsHandler import HTTPWebSocketsHandler
from mouseUtils import move, position, click

last = {u'x' : 0, u'z' : 0}

class MouseHandler(HTTPWebSocketsHandler):
    def on_ws_message(self, message):
        if message is None:
            message = ''
        
        # 0 - Sending a ping to the server to validate that we are connected ('Ahoy')
        # 1 - Signal for left click request
        # 2 - Signal for right click request
        if message == '0':
            self.log_message('Ahoy recived')
        elif message == '1':
            click(1)
        elif message == '2':
            click(2)
        # Anything else is data from the accelometer
        else:
            # Get the average (X, Y) coordinates
            try:
                msg = json.loads(message)
            except Exception, e:
                self.log_message('Error in reading data, will ignore this packet.')
                return
            frst = msg[0]
            avgX = frst[u'y']
            avgY = frst[u'x']
            for data in msg:
                avgX += data[u'y']
                avgY += data[u'x']
            avgX = avgX // len(msg)
            avgY = avgY // len(msg)
            avgX /= -40
            avgY /= 40
            # Get mouse position and new position
            pos = position()
            x = pos[0] + avgX
            y = pos[1] + avgY
            # Set the mouse to the new position
            move(x, y)
            # Log the mouse's position and save the it as the last one
            last = msg[-1]
            self.log_message(str((avgX, avgY)))

    def on_ws_connected(self):
        self.log_message('%s','websocket connected')

    def on_ws_closed(self):
        self.log_message('%s','websocket closed')

# ---- Main Server ---- #

if len(sys.argv) > 1:
    port = int(sys.argv[1])
else:
    port = 8000

class WSThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""
    
def _ws_main():
    try:
        server = WSThreadedHTTPServer(('', port), MouseHandler)
        server.daemon_threads = True
        print('started httpserver at port %d' % (port,))
        server.serve_forever()
    except KeyboardInterrupt:
        print('^C received, shutting down server')
        server.socket.close()

if __name__ == '__main__':
    _ws_main()        