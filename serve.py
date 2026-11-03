# Local dev server, only reachable from this Mac (localhost). Tells
# browsers not to cache, so edits show up on a normal refresh.
import http.server

class NoCache(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

http.server.ThreadingHTTPServer(("127.0.0.1", 8000), NoCache).serve_forever()
