from http.server import BaseHTTPRequestHandler
import json

# ═════════════════════════════════════════════════════════════════════════════
# FLAGS NO SERVIDOR (NUNCA EXPOSTAS NO FRONTEND)
# ═════════════════════════════════════════════════════════════════════════════
FLAGS = {
    "lvl0": "CTF{p0w3rsh3ll_m4st3r_2026}",
    "lvl1": "CTF{g1t_g0t_1t_d0n3}",
    "lvl2": "CTF{s3rv1c3s_und3r_c0ntr0l}",
    "lvl3": "CTF{pr0c3ss_hunt3r}",
    "lvl4": "CTF{f1l3_p3rm1ss10ns_0k}"
}

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
            user_flag = data.get("flag", "").strip()
            level = data.get("level", "lvl0")
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            correct = FLAGS.get(level)
            
            if not correct:
                response = {"success": False, "message": "Nível inválido"}
            elif user_flag == correct:
                next_lvl = int(level.replace("lvl", "")) + 1
                response = {
                    "success": True,
                    "message": "Flag correta! Avançando...",
                    "next_level": f"/lvl{next_lvl}/"
                }
            else:
                response = {
                    "success": False,
                    "message": "Flag incorreta. Continue investigando!"
                }
                
            self.wfile.write(json.dumps(response).encode('utf-8'))
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()