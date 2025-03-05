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
        <select id='ping_type' name='ping_type'>
        <option value='ping'>Ping</option>
        <option value='blind_ping'>Blind Ping</option>
        </select>
        <input type='text' name='user_input'>
        <input type='submit' value='Send'>
        </form>
        """
        self.wfile.write(html.encode())

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode()
        #post_data="ping_type=ping&user_input=8.8.8.8"
        pairs = post_data.split('&')

        parsed_data = {pair.split('=')[0]: pair.split('=')[1] for pair in pairs}

        ping_type = parsed_data.get('ping_type', '')
        user_input = parsed_data.get('user_input', '')

        print(ping_type)
        user_input = urllib.parse.unquote_plus(user_input)
        print(user_input)
        ping="ping -c 4 " if os.name!="nt" else "ping "
        if ping_type=="ping":
            print(ping+user_input)
            response=os.popen(ping+user_input).read()
        else :
            os.system(ping+user_input)
            response="Ping Ping Ping"
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(response.encode())

with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print(f"Server is running at  http://127.0.0.1:{PORT}")
    httpd.serve_forever()
