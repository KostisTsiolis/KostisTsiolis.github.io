# Local dev server: reachable from your phone on the same Wi-Fi, and tells
# browsers not to cache, so edits show up on a normal refresh.
import http.server

class NoCache(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

http.server.ThreadingHTTPServer(("0.0.0.0", 8000), NoCache).serve_forever()
