#!/usr/bin/env python3
"""
JobFlow Local Server
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Saves all job data to jobflow_data.json on your Mac.
Data survives browser clears, cache wipes, and browser changes.

HOW TO USE:
  1. Put this file in the SAME folder as JobSearch_System_enhanced.html
  2. Open Terminal
  3. cd to that folder:  cd ~/Desktop/JobFlow
  4. Run:               python3 jobflow_server.py
  5. Dashboard opens automatically at http://localhost:8765

TO STOP:   Press Ctrl+C in Terminal
DATA FILE: jobflow_data.json  (in the same folder — back this up!)
"""

import http.server, json, os, sys, webbrowser

PORT      = 8765
BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, 'jobflow_data.json')
HTML_FILE = os.path.join(BASE_DIR, 'JobSearch_System_enhanced.html')


def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


class Handler(http.server.BaseHTTPRequestHandler):

    def log_message(self, fmt, *args):
        pass  # keep terminal clean

    def cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def do_OPTIONS(self):
        self.send_response(200)
        self.cors()
        self.end_headers()

    def do_GET(self):
        path = self.path.split('?')[0]

        if path in ('/', '/index.html'):
            if not os.path.exists(HTML_FILE):
                self.send_error(404, 'Dashboard not found. Make sure both files are in the same folder.')
                return
            with open(HTML_FILE, 'rb') as f:
                body = f.read()
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.cors()
            self.end_headers()
            self.wfile.write(body)

        elif path == '/api/load':
            body = json.dumps(load_data()).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.cors()
            self.end_headers()
            self.wfile.write(body)

        else:
            self.send_error(404)

    def do_POST(self):
        if self.path == '/api/save':
            length = int(self.headers.get('Content-Length', 0))
            raw = self.rfile.read(length)
            try:
                incoming = json.loads(raw.decode('utf-8'))
                incoming_jobs = incoming.get('jobflow_v3_jobs', [])
                force_sync = incoming.get('_forceSync', False)

                if force_sync:
                    # Sync button: what you see is what gets saved — full overwrite
                    save_data(incoming)
                    print(f'  SYNC: {len(incoming_jobs)} job(s) force-written → jobflow_data.json')
                else:
                    # Normal save: merge incoming with existing disk jobs
                    existing = load_data()
                    existing_jobs = existing.get('jobflow_v3_jobs', [])
                    existing_ids = {j['id'] for j in existing_jobs}
                    new_jobs = [j for j in incoming_jobs if j['id'] not in existing_ids]
                    updated = {j['id']: j for j in incoming_jobs}
                    merged = [updated.get(j['id'], j) for j in existing_jobs] + new_jobs
                    incoming['jobflow_v3_jobs'] = merged
                    save_data(incoming)
                    print(f'  Saved {len(merged)} job(s)  →  jobflow_data.json  (+{len(new_jobs)} new)')

                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.cors()
                self.end_headers()
                self.wfile.write(json.dumps({'ok': True}).encode())
            except Exception as e:
                self.send_response(500)
                self.cors()
                self.end_headers()
                self.wfile.write(json.dumps({'ok': False, 'error': str(e)}).encode())
        else:
            self.send_error(404)


def main():
    if not os.path.exists(HTML_FILE):
        print(f'\n  Cannot find: {HTML_FILE}')
        print('  Make sure jobflow_server.py and JobSearch_System_enhanced.html')
        print('  are in the same folder.\n')
        sys.exit(1)

    existing = load_data()
    job_count = len(existing.get('jobflow_v3_jobs', []))

    print(f"""
  JobFlow Local Server
  ─────────────────────────────────────────
  Dashboard  →  http://localhost:{PORT}
  Data file  →  jobflow_data.json
  Stop       →  Ctrl+C in this Terminal
  Jobs       →  {job_count} existing job(s) found
  ─────────────────────────────────────────
""")

    webbrowser.open(f'http://localhost:{PORT}')
    server = http.server.HTTPServer(('localhost', PORT), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\n  Server stopped. Your data is safe in jobflow_data.json\n')


if __name__ == '__main__':
    main()
