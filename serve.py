import http.server
import socketserver
import os

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def directory_listing(self, path):
        if path == '/':
            self.path = '/index.html'
        return super().directory_listing(path)

PORT = 8080
Handler = CustomHandler
os.chdir(r"C:\Users\ranja\OneDrive\Desktop\learn1\ecom\Gumroad_product_digital\Ai-toolkit\AI data quality analyzer")

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"AI Data Quality Analyzer serving at http://localhost:{PORT}")
    httpd.serve_forever()
