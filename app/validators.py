import re

def validate_domain(domain):
    domval = re.compile('^([a-zA-Z0-9\-]){1,64}$')
    if domval.match(domain) == None:
        return False
    return True

def validate_ip(ip):
    ipval = re.compile('^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)')
    if ipval.match(ip) == None:
        return False
    return True

