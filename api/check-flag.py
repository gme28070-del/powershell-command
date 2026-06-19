from http.server import BaseHTTPRequestHandler
import json

# A flag correta que o aluno deve encontrar
CORRECT_FLAG = "CTF{p0w3rsh3ll_m4st3r_2026}"

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        
        user_flag = data.get("flag", "")
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        if user_flag == CORRECT_FLAG:
            response = {"success": True, "message": "Parabéns! Você encontrou a flag correta!"}
        else:
            response = {"success": False, "message": "Flag incorreta. Continue tentando!"}
            
        self.wfile.write(json.dumps(response).encode('utf-8'))
        return