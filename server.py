from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import os
import json

class SimpleHandler(BaseHTTPRequestHandler):
    def load_template(self, name):
        with open(f'templates/{name}', encoding='utf-8') as f:
            return f.read()

    def load_test(self, test_id):
        with open(f'data/{test_id}.json', encoding='utf-8') as f:
            return json.load(f)

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == '/':
            html = self.load_template("index.html")
            self.respond(html)
        elif path.startswith("/static/"):
            self.serve_static()
        elif path.startswith("/test/"):
            test_id = path.split("/")[-1]
            try:
                test = self.load_test(test_id)
                form_html = self.render_test_form(test, test_id)
                self.respond(form_html)
            except:
                self.send_error(404)
        else:
            self.send_error(404)

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path.startswith("/submit/"):
            test_id = parsed.path.split("/")[-1]
            length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(length).decode()
            data = parse_qs(post_data)

            test = self.load_test(test_id)
            score = 0
            for i, q in enumerate(test["questions"]):
                user_answer = data.get(f"q{i}", [""])[0]
                if user_answer == q["correct"]:
                    score += 1

            result = self.load_template("result.html")
            result = result.replace("{{score}}", str(score))
            result = result.replace("{{total}}", str(len(test["questions"])))
            self.respond(result)
        else:
            self.send_error(404)

    def render_test_form(self, test, test_id):
        html = self.load_template("test.html")
        q_html = ""
        for i, q in enumerate(test["questions"]):
            q_html += f"<p>{i+1}. {q['text']}</p>"
            for key, val in q["options"].items():
                q_html += f"<label><input type='radio' name='q{i}' value='{key}'> {val}</label><br>"
        html = html.replace("{{title}}", test["title"])
        html = html.replace("{{form}}", q_html)
        html = html.replace("{{test_id}}", test_id)
        return html

    def respond(self, content):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(content.encode('utf-8'))

    def serve_static(self):
        path = self.path.lstrip('/')
        if os.path.exists(path):
            self.send_response(200)
            if path.endswith(".css"):
                self.send_header("Content-type", "text/css")
            elif path.endswith(".js"):
                self.send_header("Content-type", "application/javascript")
            self.end_headers()
            with open(path, 'rb') as f:
                self.wfile.write(f.read())
        else:
            self.send_error(404)

if __name__ == '__main__':
    print("Сервер запущен на http://0.0.0.0:8000")
    HTTPServer(("0.0.0.0", 8000), SimpleHandler).serve_forever()
