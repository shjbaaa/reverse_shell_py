import http.server
import socketserver
import urllib.parse
import os

PORT = 8000

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):      
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        html = """
        <form method='POST' action='/'>
            <input type='submit' value='Ping'>
            <input type='text' name='user_input'>
        </form>
        """
        self.wfile.write(html.encode())

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode()
        text = urllib.parse.parse_qs(post_data)['user_input'][0]
        
        ping="ping -c 4 " if os.name!="nt" else "ping "
        response=os.popen(ping+text).read()
       
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(response.encode())

with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print(f"Server is running at  http://127.0.0.1:{PORT}")
    httpd.serve_forever()
