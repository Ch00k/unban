import re
import subprocess

JAILS = ('dovecot-iptables', 'dovecot-iptables-rc')
IP_LIST_RE = re.compile(r'^\s+.*Banned\s+IP\s+list:\s+(.*)$')


def get_banned_ips(jail):
    out = run_f2b_client(['fail2ban-client', 'status', jail])

    for line in out.decode().split('\n'):
        if 'Banned IP list' in line:
            match = IP_LIST_RE.match(line)
            if not match:
                raise RuntimeError("Could not find banned IP list")

            ip_list = match.group(1)
            return ip_list.split()
    else:
        raise RuntimeError("Could not find banned IP list")


def unban_ip(jails, ip):
    for jail in jails:
        run_f2b_client(['fail2ban-client', 'set', jail, 'unbanip', ip])


def find_banned_ip(ip):
    banning_jails = []

    for jail in JAILS:
        if ip in get_banned_ips(jail):
            banning_jails.append(jail)
    return banning_jails


def run_f2b_client(command):
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()

    if proc.returncode != 0:
        raise RuntimeError(err)

    return out
