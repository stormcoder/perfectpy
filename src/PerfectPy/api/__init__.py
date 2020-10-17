#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, generators, division, absolute_import, with_statement, print_function
import logging
import sys
import os
import urllib2
from urllib import urlencode
#import urllib
import json
#import base64
import time

TRACE = 5


class CustomLogging(logging.Logger):
    """A custom logger that incorporates trace


    Extends:
        log.Logger

    Variables:
        TRACE {number} -- [description]

    """
    def trace(self, msg, *args, **kwargs):
        fn, lno, func = self.__findCaller()
        exc_info = sys.exc_info()
        record = self.makeRecord(self.name, TRACE, fn, lno, msg, args, exc_info, func)
        self.handle(record)
        return

    def __findCaller(self):
        """
        Find the stack frame of the caller so that we can note the source
        file name, line number and function name.
        """
        _srcfile = __file__
        if hasattr(sys, 'frozen'):
            _srcfile = "logging%s__init__%s" % (os.sep, __file__[-4:])
        elif __file__[-4:].lower() in ['.pyc', '.pyo']:
            _srcfile = __file__[:-4] + '.py'
        else:
            _srcfile = __file__
        _srcfile = os.path.normcase(_srcfile)

        def currentframe():
            """Return the frame object for the caller's stack frame."""
            try:
                raise Exception
            except:
                return sys.exc_info()[2].tb_frame.f_back.f_back
        f = currentframe()
        if f is not None:
            f = f.f_back
        rv = "(unknown file)", 0, "(unknown function)"
        while hasattr(f, "f_code"):
            co = f.f_code
            filename = os.path.normcase(co.co_filename)
            if filename == _srcfile:
                f = f.f_back
                continue
            rv = (co.co_filename, f.f_lineno, co.co_name)
            break
        return rv


def loggingSetup(logfilepath, loglevel=TRACE):
    from logging.handlers import RotatingFileHandler
    logformat = "%(asctime)-15s %(levelname)-8s: %(threadName)-8s: %(module)-12s: %(funcName)-15s: %(lineno)-4s %(message)s"
    logging._handlers.clear()
    handler = RotatingFileHandler(logfilepath, 'a', 1000000, 10)
    formatter = logging.Formatter(logformat)
    handler.setFormatter(formatter)
    logging.setLoggerClass(CustomLogging)
    logging.addLevelName(TRACE, "TRACE")
    logging.captureWarnings(True)
    lg = logging.getLogger("Perfecto")
    lg.addHandler(handler)
    lg.setLevel(loglevel)

    return lg


log = loggingSetup("PerfectoAPI.log")


class APIClient:
    """
    REST API binding for Python 2.x

    Variables:

    """
    def __init__(self, securityToken, baseURL):
        """
        Initialize the APUClient Instance

        Arguments:
            securityKey {string} -- security token for authentication.
        """
        log.trace("APIClient.__init__   '%s'" % (baseURL))
        self.__url = baseURL
        self.__securityToken = securityToken
        self.__securityKeyStr = "securityToken"

    def send_get(self, uri):
        """
        Issues a GET request (read) against the API and returns the result
        (as Python dict).

        Arguments:
            uri {string} -- The API method to call including parameters
                             (e.g. handsets?operation=list)

        Returns:
            dict -- Server response data
        """
        log.trace("send_get  '%s'" % uri)
        return self.__send_request('GET', uri, None, None)

    def send_post(self, uri, data):
        """
         Send POST

        Issues a POST request (write) against the API and returns the result
        (as Python dict).

        Arguments:
            uri {string} -- The API method to call including parameters
                            (e.g. add_case/1)
            data {dict} --  The data to submit as part of the request (as
                            Python dict, strings must be UTF-8 encoded)

        Returns:
            dict -- response data
        """
        log.trace("send_post '%s', data length = '%s'" % (uri, len(data)))
        return self.__send_request('POST', uri, data)


    def __send_request(self, method, uri, data):
        """
        Do the heavy lifting for requests

        Arguments:
            method {String} -- HTTP method name
            uri {string} -- full URL
            data {dict} -- Any request data

        Returns:
            dict -- The response data

        Raises:
            APIError -- Any error responses get raised as exceptions
        """
        log.trace("__send_request  '%s', '%s', data length is '%s'" % (method, uri, len(data) if data else 0))
        url = (self.__url + uri + "&" + urlencode({self.__securityKeyStr: self.__securityToken})).encode('ascii', "ignore")
        log.debug("Request URL is '%s'" % url)
        request = urllib2.Request(url, data if data else None)
        #TODO: Fix post handling
        if (method == 'POST'):
            #auth = self.__securityToken
            #log.debug("auth = '%s'" % auth)
            #request.add_header('Authorization', 'Basic %s' % auth)
            request.add_header("Content-Type", "application/octet-stream")
            request.add_header("Content-Length", str(len(data)))
            #request.add_header("Content-Encoding", "base64")


        e = None
        try:
            response = urllib2.urlopen(request).read()
            log.debug(response)
        except urllib2.HTTPError as e:
            response = e.read()
            log.error("Error sending request because '%s'\n%s" % (e.message, response))
            log.error(e)


        if response:
            try:
                result = json.loads(response)
            except:
                log.warn("Failed to parse reponse as json. Trying XML.")
                try:
                    from .xmltodict import parse
                    result = parse(response)
                except:
                    log.error("Failed to parse response as either json or xml and giving up.")
                    result = response
                    raise Exception("Unable to parse response as either json or xml.")
        else:
            log.warn("No reponse received.")
            result = {}

        if e is not None:
            if result and 'error' in result:
                error = '"' + result['error'] + '"'
            else:
                error = 'No additional error message received' if not result else '"%s"' % result
            raise APIError('REST API returned HTTP %s (%s)' % (e.code, error))
        return result


class APIError(Exception):
    pass


class APIBase:
    """
    Base class for classes accessing the REST API
    """

    def initClient(self, securityToken, baseURL='https://mobilecloud.perfectomobile.com/services/'):
        self.client = APIClient(securityToken, baseURL)
        return


def properParams(base, params):
    log.debug(params)
    return "%s&%s" % (base, params)


def timeMilis(plusSecs=0, plusMins=0, plusHours=0):
    """
    Return current time in milis if no arguments.
    If arguments are present it will be current time plus argument time.

    Arguments:
        plusSecs {int}: Add this amount of seconds to current time
        plusMins {int}: Add this amount of minutes to current time
        plusHours {int}: Add this amount of hours to current time

    Return:
        time in milis
    """
    return int(round(time.time() * 1000)) + int(round(plusSecs * 1000)) + int(round(plusMins * 60 * 1000)) + int(round(plusHours * 60 * 60 * 1000))
