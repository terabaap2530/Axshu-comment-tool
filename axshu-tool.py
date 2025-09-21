#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import requests
import threading
import http.server
import socketserver
from platform import system

# Password
PASSWORD = "AXSHU786"

def cls():
    os.system('clear' if system() == 'Linux' else 'cls')

def banner():
    print("\033[1;36m")
    print("===========================================")
    print("          AXSHU SERVER TERMUX TOOL         ")
    print("===========================================")
    print("\033[0m")

def check_config_files():
    """Check if config directory and files exist"""
    if not os.path.exists('config'):
        os.makedirs('config')
        return False
    
    required_files = ['tokennum.txt', 'post_url.txt', 'comments.txt', 'hatersname.txt', 'time.txt']
    for file in required_files:
        if not os.path.exists(f'config/{file}'):
            return False
    return True

def setup_wizard():
    """Interactive setup wizard for all configurations"""
    cls()
    banner()
    print("\n\033[1;33m[SETUP WIZARD]\033[0m")
    print("We need to configure some settings before starting...\n")
    
    # Ensure config directory exists
    if not os.path.exists('config'):
        os.makedirs('config')
    
    # 1. Facebook Tokens
    print("\n\033[1;34m[1/5] FACEBOOK ACCESS TOKENS\033[0m")
    print("Enter your Facebook access tokens (one per line)")
    print("Type 'done' when finished")
    
    tokens = []
    token_count = 1
    while True:
        token = input(f"Token {token_count}: ").strip()
        if token.lower() == 'done':
            if len(tokens) == 0:
                print("Please enter at least one token!")
                continue
            break
        if token:
            tokens.append(token)
            token_count += 1
    
    with open('config/tokennum.txt', 'w') as f:
        for token in tokens:
            f.write(token + '\n')
    print(f"[+] {len(tokens)} tokens saved")
    
    # 2. Post URL/ID
    print("\n\033[1;34m[2/5] FACEBOOK POST ID\033[0m")
    print("Enter the Facebook Post ID you want to comment on")
    print("Example: 123456789012345 or username_123456789012345")
    
    post_id = ""
    while not post_id:
        post_id = input("Post ID: ").strip()
        if not post_id:
            print("Please enter a valid Post ID!")
    
    with open('config/post_url.txt', 'w') as f:
        f.write(post_id)
    print("[+] Post ID saved")
    
    # 3. Comments
    print("\n\033[1;34m[3/5] COMMENTS\033[0m")
    print("Enter comments to post (one per line)")
    print("Type 'done' when finished")
    
    comments = []
    comment_count = 1
    while True:
        comment = input(f"Comment {comment_count}: ").strip()
        if comment.lower() == 'done':
            if len(comments) == 0:
                print("Please enter at least one comment!")
                continue
            break
        if comment:
            comments.append(comment)
            comment_count += 1
    
    with open('config/comments.txt', 'w') as f:
        for comment in comments:
            f.write(comment + '\n')
    print(f"[+] {len(comments)} comments saved")
    
    # 4. Name Prefix
    print("\n\033[1;34m[4/5] NAME PREFIX\033[0m")
    print("Enter the name prefix for comments")
    print("Example: 'John Doe' will make comments like 'John Doe Amazing post!'")
    
    name = ""
    while not name:
        name = input("Name Prefix: ").strip()
        if not name:
            print("Please enter a name prefix!")
    
    with open('config/hatersname.txt', 'w') as f:
        f.write(name)
    print("[+] Name prefix saved")
    
    # 5. Time Delay
    print("\n\033[1;34m[5/5] TIME DELAY\033[0m")
    print("Enter delay between comments (in seconds)")
    print("Recommended: 5-10 seconds to avoid detection")
    
    delay = ""
    while not delay:
        delay = input("Delay (seconds): ").strip()
        if not delay.isdigit() or int(delay) <= 0:
            print("Please enter a valid positive number!")
            delay = ""
    
    with open('config/time.txt', 'w') as f:
        f.write(delay)
    print("[+] Time delay saved")
    
    print("\n\033[1;32m[+] Setup completed successfully!\033[0m")
    print("You can now run the tool without setup next time.")
    time.sleep(2)
    return True

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"S3RV3R 0FF AXSHU")

def execute_server():
    """Start HTTP server"""
    PORT = 4000
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print(f"[+] Server running at http://localhost:{PORT}")
        httpd.serve_forever()

def read_config_file(filename):
    """Read configuration file"""
    try:
        with open(f'config/{filename}', 'r') as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"[-] Config file {filename} not found!")
        return []

def post_comments():
    """Main function to post comments"""
    # Read all configuration
    tokens = read_config_file('tokennum.txt')
    post_id = read_config_file('post_url.txt')
    comments = read_config_file('comments.txt')
    haters_name = read_config_file('hatersname.txt')
    delay_config = read_config_file('time.txt')
    
    # Validate configuration
    if not tokens or not post_id or not comments or not haters_name or not delay_config:
        print("[-] Invalid configuration! Please run setup again.")
        return
    
    post_id = post_id[0]
    haters_name = haters_name[0]
    delay = int(delay_config[0])
    
    print(f"\n[+] Starting comment posting with:")
    print(f"   - Tokens: {len(tokens)}")
    print(f"   - Post ID: {post_id}")
    print(f"   - Comments: {len(comments)}")
    print(f"   - Name Prefix: {haters_name}")
    print(f"   - Delay: {delay} seconds\n")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0.0; Samsung Galaxy S9 Build/OPR6.170623.017; wv) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.125 Mobile Safari/537.36',
    }
    
    # Start posting comments
    comment_count = 0
    token_index = 0
    
    try:
        while True:
            for comment in comments:
                token = tokens[token_index % len(tokens)]
                full_comment = f"{haters_name} {comment}"
                
                # Prepare API request
                url = f"https://graph.facebook.com/{post_id}/comments"
                parameters = {'access_token': token, 'message': full_comment}
                
                # Send comment (simulated for now)
                print(f"[+] Comment {comment_count + 1}: {full_comment}")
                print(f"   - Using Token {token_index + 1}/{len(tokens)}")
                
                # Uncomment below to actually send comments
                """
                response = requests.post(url, json=parameters, headers=headers)
                if response.ok:
                    print(f"[✓] Successfully posted")
                else:
                    print(f"[✗] Failed to post: {response.text}")
                """
                
                comment_count += 1
                token_index += 1
                time.sleep(delay)
            
            print(f"\n[+] Completed {len(comments)} comments. Restarting...\n")
            
    except KeyboardInterrupt:
        print(f"\n[!] Process interrupted. Total comments: {comment_count}")
    except Exception as e:
        print(f"[!] Error: {e}")

def main():
    cls()
    banner()
    
    # Check password
    entered_password = input("Enter Password: ").strip()
    if entered_password != PASSWORD:
        print('[-] Incorrect Password!')
        sys.exit(1)
    
    # Check if configuration exists
    if not check_config_files():
        print("\n[!] First time setup required...")
        if not setup_wizard():
            print("[-] Setup failed. Exiting.")
            sys.exit(1)
    
    # Start HTTP server in background
    server_thread = threading.Thread(target=execute_server)
    server_thread.daemon = True
    server_thread.start()
    
    # Start posting comments
    try:
        post_comments()
    except Exception as e:
        print(f"[!] Error in main: {e}")
    
    print("\n[+] Thank you for using AXSHU Server Tool!")

if __name__ == '__main__':
    main()
