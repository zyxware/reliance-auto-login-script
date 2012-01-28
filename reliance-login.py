#!/usr/bin/env python
# encoding: utf-8
"""
Reliance Login Script for Python 2.x v1.0
 
Created by Kunal Dua on 2009-12-18
http://www.kunaldua.com/blog/?p=330

Updated by Anoop John - 2012-01-28
http://www.zyxware.com
 
This program is free software; you may redistribute it and/or
modify it under the same terms as Python itself.
"""
 
import urllib2, urllib, cookielib, time, re, sys

def get_url(url, data=None, timeout=60, opener=None):
  '''get_url accepts a URL string and return the server response code, response headers, and contents of the file'''
  '''ref: http://pythonfilter.com/blog/changing-or-spoofing-your-user-agent-python.html'''
  req_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; U; ru; rv:5.0.1.6) Gecko/20110501 Firefox/5.0.1 Firefox/5.0.1'
  }
  request = urllib2.Request(url, headers=req_headers)
  if not opener:
    jar = cookielib.FileCookieJar("cookies")
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(jar))
  response = opener.open(request, data)
  code = response.code
  headers = response.headers
  html = response.read()
  return code, headers, html, opener

def is_internet_on():
  '''test if the machine is connected to the internet'''
  print "Testing"
  try:
    code, headers, html, opener = get_url('http://74.125.113.99', timeout=10)
    print html
    if re.search('google.com', html):
      return True
    else:
      return False
  except: 
    print "Error"
    return False
  return False

def internet_connect():
  '''try to connect to the internet'''
  username = 'username' 
  password = 'password'
  code, headers, html, cur_opener = get_url("http://10.239.89.15/reliance/startportal_isg.do", timeout=10)
  print html
  login_data = urllib.urlencode({'userId' : username, 'password' : password, 'action' : 'doLoginSubmit'})
  code, headers, html, cur_opener = get_url('http://10.239.89.15/reliance/login.do', data=login_data, opener=cur_opener)
  print html

def internet_disconnect():
  '''try to disconnect from the internet'''
  code, headers, html, cur_opener = get_url('http://10.239.89.15/reliance/login.do', timeout=10)
  print html
  code, headers, html, cur_opener = get_url('http://10.239.89.15/reliance/logout.do', opener=cur_opener)
  print html

def internet_keep_alive():
  while True:
    if not is_internet_on():
      internet_connect()
      print "Not connected"
    else:
      print "Connected"
      pass
    time.sleep(10)

def print_usage():
  print "Reliance Netconnect AutoLogin"
  print "-----------------------------"
  print "usage:" + sys.argv[0] + " [login|logout]\n" 
  print "If there are no arguments it runs in an infinite loop and will try to remain connected to the internet."

if (len(sys.argv) > 1):
  op = sys.argv[1]
  if op == 'login':
    internet_connect()
  elif op == 'logout':
    internet_disconnect()
  else:
    print_usage()
  exit()    

''' default action - keep alive'''
internet_keep_alive();


