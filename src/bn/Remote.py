"""
This module provides the logic to make the remote request to the provider and
returns a dictionary {Name: (rank, total births)} such as:
{Justin: (74, 24567), Emma: (43, 2321)}

It also provides the caching functionality since the two are simple and linked
heavily by the data format.

TODO: more dynamic, i.e. more providers of information
      more error handling
      introduce TDD
      use a more friendly serialization versus pickle for integration
"""

import urllib, urllib2, re, os, time, pickle

__version__ = "$Id"

class Request(object):
    """This class performs an HTTP request for data based on a specific year
       when passed to the send command.
    """
    def __init__(self):
        self.url = 'http://www.socialsecurity.gov/cgi-bin/popularnames.cgi'
        sstr = r"<td>([0-9]+)</td>\s*<td>([A-Za-z]+)</td>\s*<td>([0-9,]+)</td>"
        self.srf = re.compile(sstr)
 
    def send(self, year):
        """Perform a remote request and return the data as a dictionary
           {Justin: (24, 23222), Emma: (22, 23423)}
        """
        values = {'year': str(year),'top': '1000', 'number': 'n'}
        data = urllib.urlencode(values)
        req = urllib2.Request(self.url, data)
        tries = 1
        while True:
            try:
                rec = urllib2.urlopen(req).read()
                break
            except:
                pass
            time.sleep(2+tries)
            tries += 1
            if tries > 3:
                return None
        rval = {}
        # This is very fragile, but anything in html will be.
        wwa = 1
        stf2, ostf = None, None
        for ln in rec.splitlines():
            stf = self.srf.search(ln)
            if stf:
                rval[stf.group(2)] = (stf.group(1), 
                                      stf.group(3).replace(',', ''))
                ostf = stf
                wwa = 2
                continue
            if wwa == 2:
                stf2 = re.search(r'<td>([A-Za-z]+)</td>', ln)
                wwa = 3
                continue
            if wwa == 3:
                stf3 = re.search(r'<td>([0-9,]+)</td>', ln)        
                rval[stf2.group(1)] = (ostf.group(1), 
                                       stf3.group(1).replace(',', ''))
                wwa = 1
                stf2, ostf = None, None
        return rval

class Cache(object):
    """Cache the information passed to ~/.bn/cache if the information is more
       than three hours old. Otherwise, pass back the cached information.
    """
    def __init__(self):
        """Check to see if the cache path exists, do nothing. Else, attempt to
           create the directory path.
        """
        self.wrkdir = os.path.join(os.path.expanduser('~'), '.bn')
        if not os.path.isdir(self.wrkdir):
            try:
                os.makedirs(self.wrkdir)
            except OSError:
                raise 

    def read(self, year):
        """Attempt to retrieve cached data based on the year given. If the 
           cache is greater than three hours old, return no data.
        """
        try:
            if time.time() - os.path.getmtime(os.path.join(self.wrkdir, 
                                              'cache'+str(year))) < 60*60*3:
                with open(os.path.join(self.wrkdir, 'cache'+str(year))) as f:
                    return pickle.load(f)
        except OSError:
            return None
   
    def write(self, inform, year):
        """Attempt to write the data 'inform' to the cache of 'year'. Since
           this is a Python application with no need for integration, use 
           pickle.
        """
        try:
            with open(os.path.join(self.wrkdir, 'cache'+str(year)), 'w') as f:
                pickle.dump(inform, f)
        except OSError:
            raise
    
if __name__ == '__main__':
    import doctest
    doctest.testmod()
