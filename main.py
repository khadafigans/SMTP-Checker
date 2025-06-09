import os
import smtplib
import ssl
from email.message import EmailMessage
from concurrent.futures import ThreadPoolExecutor, as_completed
from pystyle import Write, Colors, Colorate, Center
from colorama import Fore, Style, init
from datetime import datetime

init(autoreset=True)

# === EDIT THIS VARIABLE TO SET YOUR TEST RECIPIENTS ===
TEST_RECIPIENTS = ["youremail@example.com" ,"youranothermail@secondmail.com"]

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_ascii():
    smtp_checker = r"""

███████╗███╗   ███╗████████╗██████╗      ██████╗██╗  ██╗███████╗ ██████╗██╗  ██╗███████╗██████╗ 
██╔════╝████╗ ████║╚══██╔══╝██╔══██╗    ██╔════╝██║  ██║██╔════╝██╔════╝██║ ██╔╝██╔════╝██╔══██╗
███████╗██╔████╔██║   ██║   ██████╔╝    ██║     ███████║█████╗  ██║     █████╔╝ █████╗  ██████╔╝
╚════██║██║╚██╔╝██║   ██║   ██╔═══╝     ██║     ██╔══██║██╔══╝  ██║     ██╔═██╗ ██╔══╝  ██╔══██╗
███████║██║ ╚═╝ ██║   ██║   ██║         ╚██████╗██║  ██║███████╗╚██████╗██║  ██╗███████╗██║  ██║
╚══════╝╚═╝     ╚═╝   ╚═╝   ╚═╝          ╚═════╝╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
                                                                                                
   """
    by = r"""
                                 
                        ██████╗ ██╗   ██╗
                        ██╔══██╗╚██╗ ██╔╝
                        ██████╔╝ ╚████╔╝ 
                        ██╔══██╗  ╚██╔╝  
                        ██████╔╝   ██║   
                        ╚═════╝    ╚═╝   
                 
    """
    bob_marley = r"""

██████╗  ██████╗ ██████╗     ███╗   ███╗ █████╗ ██████╗ ██╗     ███████╗██╗   ██╗
██╔══██╗██╔═══██╗██╔══██╗    ████╗ ████║██╔══██╗██╔══██╗██║     ██╔════╝╚██╗ ██╔╝
██████╔╝██║   ██║██████╔╝    ██╔████╔██║███████║██████╔╝██║     █████╗   ╚████╔╝ 
██╔══██╗██║   ██║██╔══██╗    ██║╚██╔╝██║██╔══██║██╔══██╗██║     ██╔══╝    ╚██╔╝  
██████╔╝╚██████╔╝██████╔╝    ██║ ╚═╝ ██║██║  ██║██║  ██║███████╗███████╗   ██║   
╚═════╝  ╚═════╝ ╚═════╝     ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝   ╚═╝   
                                                                                 
   """
    print()
    print(Center.XCenter(Colorate.Horizontal(Colors.red_to_green, smtp_checker, 1)))
    print(Center.XCenter(Colorate.Horizontal(Colors.yellow_to_green, by, 1)))
    print(Center.XCenter(Colorate.Horizontal(Colors.red_to_green, bob_marley, 1)))
    print()

def parse_smtp_line(line):
    parts = line.strip().split('|')
    if len(parts) < 3:
        return None
    host = parts[0].strip()
    username = parts[1].strip()
    password = parts[2].strip()
    from_addr = parts[3].strip() if len(parts) > 3 and parts[3].strip() else username
    return host, username, password, from_addr

def check_smtp(host, username, password, from_addr, test_recipients):
    port = 587  # Default to STARTTLS
    try:
        server = smtplib.SMTP(host, port, timeout=10)
        server.ehlo()
        server.starttls(context=ssl.create_default_context())
        server.ehlo()
        server.login(username, password)
        msg = EmailMessage()
        msg['Subject'] = 'SMTP Test by Bob Marley'
        msg['From'] = from_addr
        msg['To'] = ", ".join(test_recipients)
        msg.set_content(
            f'This is a test email sent by SMTP checker.\n\n'
            f'SMTP: {host}\nFrom: {from_addr}\nTo: {", ".join(test_recipients)}'
        )
        server.send_message(msg)
        server.quit()
        return True
    except Exception:
        return False

def main():
    clear()
    print_ascii()
    smtp_file = Write.Input("Give me your SMTP List:", Colors.green_to_yellow, interval=0.005)
    thread_count = int(Write.Input("Thread ? ", Colors.green_to_yellow, interval=0.005))
    try:
        with open(smtp_file, "r") as f:
            lines = [line.strip() for line in f if line.strip()]
    except Exception as e:
        Write.Print(f"\nError reading file: {e}\n", Colors.red_to_yellow, interval=0.002)
        return

    combos = []
    for line in lines:
        parsed = parse_smtp_line(line)
        if parsed:
            combos.append(parsed)
        else:
            Write.Print(f"[SKIP] Invalid line format: {line}\n", Colors.red_to_yellow, interval=0.001)

    live_count = 0
    die_count = 0
    valid_lines = []

    def worker(combo):
        host, username, password, from_addr = combo
        Write.Print(f"\n[>] Checking {host} .....\n", Colors.yellow_to_green, interval=0.001)
        result = check_smtp(host, username, password, from_addr, TEST_RECIPIENTS)
        if result:
            Write.Print(f"[>] {host} is VALID sent test email successfully!\n", Colors.green_to_yellow, interval=0.001)
            return (True, combo)
        else:
            Write.Print(f"[>] {host} is DIE sent test email failed!\n", Colors.red_to_yellow, interval=0.001)
            return (False, combo)

    with ThreadPoolExecutor(max_workers=thread_count) as executor:
        futures = [executor.submit(worker, combo) for combo in combos]
        for future in as_completed(futures):
            res, combo = future.result()
            if res:
                live_count += 1
                valid_lines.append('|'.join(combo))
            else:
                die_count += 1

    Write.Print("\nCurrent total :\n", Colors.green_to_yellow, interval=0.005)
    Write.Print(f"[LIVE] {live_count}\n", Colors.green_to_yellow, interval=0.005)
    Write.Print(f"[DIE] {die_count}\n", Colors.red_to_yellow, interval=0.005)

    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    if valid_lines:
        result_file = f"valid_smtp_{now}.txt"
        with open(result_file, "w") as f:
            for vline in valid_lines:
                f.write(vline + "\n")
        Write.Print(f"\n[+] Valid SMTP combos saved to {result_file}\n", Colors.green_to_yellow, interval=0.005)
    else:
        Write.Print("\n[-] No valid SMTP combos found.\n", Colors.red_to_yellow, interval=0.005)

if __name__ == "__main__":
    main()
