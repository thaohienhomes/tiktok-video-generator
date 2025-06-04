#!/usr/bin/env python3
"""
Simple HTTP Server để test cơ bản
Không dùng FastAPI hay bất kỳ framework nào
"""

import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        logger.info(f"GET request for {self.path}")
        
        try:
            if self.path == "/":
                response_data = {
                    "message": "Simple HTTP Server works!",
                    "status": "success",
                    "server": "http.server"
                }
                self.send_json_response(response_data)
                
            elif self.path == "/health":
                response_data = {
                    "health": "OK",
                    "server": "simple_http"
                }
                self.send_json_response(response_data)
                
            else:
                self.send_error(404, "Not Found")
                
        except Exception as e:
            logger.error(f"Error handling request: {e}")
            self.send_error(500, f"Internal Server Error: {str(e)}")
    
    def send_json_response(self, data):
        """Send JSON response"""
        try:
            json_data = json.dumps(data)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(json_data)))
            self.end_headers()
            self.wfile.write(json_data.encode('utf-8'))
            logger.info(f"Sent response: {json_data}")
        except Exception as e:
            logger.error(f"Error sending JSON response: {e}")
            self.send_error(500, f"Error creating response: {str(e)}")
    
    def log_message(self, format, *args):
        """Override to use logger"""
        logger.info(format % args)

def run_server(host='127.0.0.1', port=8003):
    """Start the HTTP server"""
    try:
        server_address = (host, port)
        httpd = HTTPServer(server_address, SimpleHandler)
        logger.info(f"🚀 Simple HTTP Server starting on http://{host}:{port}")
        httpd.serve_forever()
    except Exception as e:
        logger.error(f"❌ Server failed to start: {e}")
        raise

if __name__ == "__main__":
    print("Starting Simple HTTP Server...")
    run_server() 