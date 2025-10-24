from http.server import BaseHTTPRequestHandler
import json, requests, os

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)

        user_input = data.get("prompt", "")
        if not user_input:
            self.send_response(400)
            self.send_header('Content-type','application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "prompt gerekli"}).encode())
            return

        API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-base"
        headers = {"Authorization": f"Bearer {os.environ.get('HF_API_KEY')}"}

        res = requests.post(API_URL, headers=headers, json={"inputs": user_input})
        output = res.json()

        try:
            reply = output[0]["generated_text"]
        except:
            reply = "Üzgünüm, şu anda cevap veremiyorum."

        self.send_response(200)
        self.send_header('Content-type','application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"response": reply}).encode())
