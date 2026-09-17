from http.server import HTTPServer, BaseHTTPRequestHandler
import datetime, json, threading

LOG_FILE = "honeypot_log.jsonl"
LOG = []
lock = threading.Lock()

class HoneyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        entry = {
            "time": datetime.datetime.now().isoformat(),
            "ip": self.client_address[0],
            "path": self.path,
            "agent": self.headers.get("User-Agent", "?"),
            "referer": self.headers.get("Referer", "-"),
        }
        with lock:
            LOG.append(entry)
            with open(LOG_FILE, "a") as f:
                f.write(json.dumps(entry) + "\n")
        print(json.dumps(entry))

        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        # Bait payload: looks like a normal download/confirmation page.
        # In a real red-team exercise this would NOT deliver any executable —
        # it only proves the link was clicked.
        self.wfile.write(b"<html><body><h3>Thanks for visiting!</h3>"
                          b"<p>Your request has been logged for security awareness testing.</p>"
                          b"</body></html>")

    def log_message(self, *args):
        pass  # suppress default stderr logging; we log structured JSON instead


def run(port=8080):
    print(f"Honeypot bait link live on http://localhost:{port}")
    HTTPServer(("", port), HoneyHandler).serve_forever()


if __name__ == "__main__":
    run()
