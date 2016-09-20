from app import app
import subprocess

def nsupdate(ip, hostname):
    command = 'server %s.\n' % app.config['NSUPDATE_SERVER'] 
    command += 'zone %s.\n' % app.config['NSUPDATE_DOMAIN'] 
    command += 'update delete %s.%s\n' % (hostname, app.config['NSUPDATE_DOMAIN'])
    command += 'update add %s.%s. %s A %s\n' % (hostname, app.config['NSUPDATE_DOMAIN'], app.config['NSUPDATE_TTL'], ip)
    command += 'send\n'
    command = 'nsupdate -k {0} << EOF\n{1}\nEOF\n'.format(app.config['NSUPDATE_KEY'], command)
    return subprocess.call(command, shell=True)

