import logging

class HTTPHandler(logging.Handler):
    """
    A class which sends records to a Web server, using either GET or
    POST semantics.
    """
    def __init__(self, host, url, method="GET", secure=False, credentials=None):
        """
        Initialize the instance with the host, the request URL, and the method
        ("GET" or "POST")
        """
        logging.Handler.__init__(self)
        method = method.upper()
        if method not in ["GET", "POST"]:
            raise ValueError("method must be GET or POST")
        self.host = host
        self.url = url
        self.method = method
        self.secure = secure
        self.credentials = credentials

    def mapLogRecord(self, record):
        """
        Default implementation of mapping the log record into a dict
        that is sent as the CGI data. Overwrite in your class.
        Contributed by Franz Glasner.
        """
        return record.__dict__

    def emit(self, record):
        """
        Emit a record.

        Send the record to the Web server as a percent-encoded dictionary
        """
        try:
            import http.client, urllib.parse
            host = self.host
            if self.secure:
                h = http.client.HTTPSConnection(host)
            else:
                h = http.client.HTTPConnection(host)
            url = self.url
            data = urllib.parse.urlencode(self.mapLogRecord(record))
            if self.method == "GET":
                if (url.find('?') >= 0):
                    sep = '&'
                else:
                    sep = '?'
                url = url + "%c%s" % (sep, data)
            h.putrequest(self.method, url)
            # support multiple hosts on one IP address...
            # need to strip optional :port from host, if present
            i = host.find(":")
            if i >= 0:
                host = host[:i]
            h.putheader("Host", host)
            if self.method == "POST":
                h.putheader("Content-type",
                            "application/x-www-form-urlencoded")
                h.putheader("Content-length", str(len(data)))
            if self.credentials:
                import base64
                s = ('u%s:%s' % self.credentials).encode('utf-8')
                s = 'Basic ' + base64.b64encode(s).strip()
                h.putheader('Authorization', s)
            h.endheaders(data if self.method == "POST" else None)
            h.getresponse()    #can't do anything with the result
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)

