#!/usr/bin/python3
# PGO training for webkitgtk: serves <root> on 127.0.0.1 and loads each page in
# a WebKitGTK 6.0 view until the page reports that it has finished.
# Usage: pgo-train.py <root>; exits non-zero if a page times out or a web
# process dies, so a broken training run cannot silently produce no profile.
import functools, http.server, sys, threading, time
import gi
gi.require_version("Gtk", "4.0")
gi.require_version("WebKit", "6.0")
from gi.repository import Gio, GLib, Gtk, WebKit

# (path, JavaScript that is true once the page is done, timeout in seconds)
PAGES = [
    ("render.html?reps=3", "document.title.startsWith('done')", 1800),
    ("Speedometer2.1/InteractiveRunner.html?startAutomatically",
     "!!document.querySelector('pre')", 3600),
    # report=true starts the run without a click; the report POST is ignored.
    ("JetStream2/index.html?report=true",
     "document.getElementById('result-summary').textContent.trim().length > 0", 7200),
]


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        self.rfile.read(int(self.headers.get("Content-Length", 0)))
        self.send_response(204)
        self.end_headers()

    def log_message(self, *args):
        pass


server = http.server.ThreadingHTTPServer(
    ("127.0.0.1", 0), functools.partial(Handler, directory=sys.argv[1]))
threading.Thread(target=server.serve_forever, daemon=True).start()
base = "http://127.0.0.1:%d/" % server.server_address[1]
state = {"page": -1, "start": 0.0, "failed": False}


def fail(message):
    print("pgo-train: " + message, flush=True)
    state["failed"] = True
    app.quit()


def next_page(view):
    state["page"] += 1
    if state["page"] == len(PAGES):
        app.quit()
        return
    state["start"] = time.monotonic()
    print("pgo-train: loading " + PAGES[state["page"]][0], flush=True)
    view.load_uri(base + PAGES[state["page"]][0])
    GLib.timeout_add_seconds(5, poll, view, state["page"])


def poll(view, page):
    path, done, timeout = PAGES[page]
    elapsed = time.monotonic() - state["start"]
    if elapsed > timeout:
        fail("%s did not finish in %d seconds" % (path, timeout))
        return False

    def finished(view, result):
        try:
            value = view.evaluate_javascript_finish(result).to_boolean()
        except GLib.Error:
            value = False
        if value:
            print("pgo-train: %s done in %.0f seconds" % (path, elapsed), flush=True)
            next_page(view)
        else:
            GLib.timeout_add_seconds(5, poll, view, page)

    view.evaluate_javascript(done, -1, None, None, None, finished)
    return False


def activate(app):
    window = Gtk.ApplicationWindow(application=app)
    window.set_default_size(1400, 900)
    view = WebKit.WebView()
    view.connect("web-process-terminated", lambda view, reason: fail("web process terminated: %s" % reason.value_nick))
    window.set_child(view)
    window.present()
    next_page(view)


# Non-unique, so a leftover instance cannot take over the run and exit 0.
app = Gtk.Application(application_id="org.webkitgtk.PgoTrain", flags=Gio.ApplicationFlags.NON_UNIQUE)
app.connect("activate", activate)
app.run(None)
sys.exit(0 if state["page"] == len(PAGES) and not state["failed"] else 1)
