#!/usr/bin/env python

from concurrent.futures import ThreadPoolExecutor, as_completed
from subprocess import Popen, PIPE, check_call, CalledProcessError
from os import devnull

stuff = {}

def chkconfig_list():
    global stuff
    proc = Popen(['chkconfig', '--list'], stdout=PIPE)
    out = [c.split('\t') for c in proc.communicate()[0].split('\n')]
    for s in out:
        try:
            if not s[6].strip():
                continue
        except IndexError:
            continue
        stuff[s[0].strip()] = dict([i.strip().split(':') for i in s[1:]])

def check_status(srv):
    try:
        with open(devnull, 'w') as dn:
            proc = check_call(['/sbin/service', srv, 'status'], stdout=dn, stderr=dn)
            return proc, srv
    except CalledProcessError, e:
        return e.returncode, srv

if __name__ == "__main__":
    chkconfig_list()
    srvs = [srv for srv in stuff.keys() if stuff[srv]['5'] == 'on']
    print("Services on in runlevel 5:\n%s" % ', '.join(sorted(srvs)))
    with ThreadPoolExecutor(max_workers=5) as executor:
        fl = dict((executor.submit(check_status, srv), srv) for srv in srvs)
        for future in as_completed(fl):
            if future.result()[0] != 0:
                print("service %s status: reports unusual returncode of %s" %
                      (future.result()[1], future.result()[0]))
