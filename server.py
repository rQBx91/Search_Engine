from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
import urllib.parse as url
import os
from QueryRanking import QueryRanking
from Utils import Load, Build, checkIndex
from InMemIndex import InMemIndex

scriptPath = os.getcwd()
N = 1000
Index = []
if checkIndex():
    Index = Load()
else:
    Index = InMemIndex()
    Build(Index)
ranking = QueryRanking(Index, f'{scriptPath}/resources/DocumentStore.json')

def createHTML(ranked: list) -> str:
    with open(scriptPath + '/resources/template.html') as file:
        html = file.read()
        rep = ''
        if ranked == None:
            return html.replace('replacement','')
        for i,ran in enumerate(ranked):
            if i == N:
                break
            if ran[0] == None:
                continue
            rep += f'<div class="p-2 bd-highlight" style="color: #0097e6; font-size: 20px"><a href="{ran[1]}" target="_blank">{ran[0]}</a></div>\n'
        html = html.replace('replacement', rep)
        return html


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

class MyRequestHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('content-type', 'text/html')
            self.end_headers()
            fileContent = ''
            with open(scriptPath + '/resources/index.html' , 'r') as file:
                fileContent = file.read()
            self.wfile.write(fileContent.encode())
        
        elif self.path == '/favicon.ico':
            self.send_response(200)
            self.send_header('content-type', 'image/x-icon')
            self.end_headers()
            with open(scriptPath + '/resources/favicon.ico' , 'rb') as file:
                fileContent = file.read()
            self.wfile.write(fileContent)
        
        elif self.path.split('?')[0] == '/query':
            qeury = url.unquote_plus(self.path.split('?')[1])
            qeury = qeury[2:]
            self.send_response(200)
            self.send_header('content-type', 'text/html')
            self.end_headers()
            result = ranking.rank(qeury)
            html = createHTML(result)
            self.wfile.write(html.encode())
        
        else:
            self.send_response(404)
            self.send_header('content-type', 'text/html')
            self.end_headers()
            response = '<html><body><h1>Not found</h1></body></html>'.encode()
            self.wfile.write(response)


    def do_HEAD(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('content-type', 'text/html')
            self.end_headers()

        elif self.path == '/favicon.ico':
            self.send_response(200)
            self.send_header('content-type', 'image/x-icon')
            self.end_headers()

        else:
            self.send_response(404)
            self.send_header('content-type', 'text/html')
            self.end_headers()


def Run():
    server = ThreadedHTTPServer(('0.0.0.0', 80), MyRequestHandler)
    print(f'Server running on http://0.0.0.0:80')
    server.serve_forever()
    
Run()