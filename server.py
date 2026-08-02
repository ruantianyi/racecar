import http.server
import socketserver

PORT = 8000

class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # NOTE: No COOP/COEP here - this WebGL build uses 0 threads and never touches
        # SharedArrayBuffer (verified 0 pthread/SAB refs), so cross-origin isolation buys
        # nothing locally. It would also block CDN fetches (monaco, pyodide, jszip) that
        # lack CORP unless a coi-serviceworker proxy adds it. Simplified build deliberately
        # removed the SW, so we keep only no-store to prevent stale Build/* caching.
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()

socketserver.TCPServer.allow_reuse_address = True
with socketserver.ThreadingTCPServer(('127.0.0.1', PORT), Handler) as httpd:
    print(f"Serving at http://127.0.0.1:{PORT}")
    httpd.serve_forever()
