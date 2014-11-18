#!/usr/bin/env python

from email.Message import Message
import email
import errno
import json
import smtplib
import sys
import threading
import time

import gevent
from gevent.wsgi import WSGIServer, WSGIHandler
from gevent.queue import Queue

from flask import Flask, Response
from flask import render_template

PORT = 5000
DEFAULT_THRESHOLD = 2000

#SMTP INFORMATION
SMTP_SERVER = 'smtp.gmail.com'
SMTP_USER = 'example@gmail.com'
SMTP_PWD = '******'
SMTP_PORT = 587
TARGET_EMAIL = 'example@gmail.com'

stat_data = {}

class ServerSentEvent( object ):

    def __init__( self, data ):
        self.data = data
        self.event = None
        self.id = None
        self.desc_map = {
            self.data : "data",
            self.event : "event",
            self.id : "id"
        }

    def encode( self ):
        if not self.data:
            return ""
        lines = ["%s: %s" % (v, k) 
                 for k, v in self.desc_map.iteritems() if k]

        return "%s\n\n" % "\n".join(lines)

app = Flask( __name__ )

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/data_streaming")
def data_streaming():
    '''
    SSE API
    '''

    global stat_data
    def gen():
        while True:
            gevent.sleep( 1 )
            data = stat_data
            if data == {}:
                continue
            ev = ServerSentEvent( json.dumps( { 'stat_data': data,
                                                'threshold': threshold } ) )
            yield ev.encode()

    return Response( gen(), mimetype="text/event-stream")


def connect_smtp( smtp_addr, smtp_port, uname, pwd ):
    '''
    connect to smtp server and return a smtplib.SMTP object
    '''

    server=smtplib.SMTP( smtp_addr, smtp_port)

    server.ehlo()
    server.starttls()
    server.login( uname, pwd )
    return server

def send_email( server, to, subj, content ):

    msg = Message()
    msg['Mime-Version']='1.0'
    msg['From']    = SMTP_USER
    msg['To']      = to
    msg['Subject'] = subj
    msg['Date']    = email.Utils.formatdate()
    msg.set_payload( content )

    failed = server.sendmail( SMTP_USER, to, str(msg) )

def check_threshold( stat_data ):

    for s, data in stat_data.items():
        if int(data) > threshold.get( s, DEFAULT_THRESHOLD  ):
            print "\n** Traffic spike! Sending alert to", TARGET_EMAIL, "**"
            alert_msg = time.ctime() + "\nServer:" + s + " Traffic: "+data
            print alert_msg
            #try:
                #Set SMTP information before use these codes.
            #    smtp = connect_smtp( SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PWD )
            #    send_email( smtp, TARGET_EMAIL, 'Traffic Spike!', alert_msg )
            #except Exception,e:
            #    print "Fail to send alert Email"
            #    print e

def stream_data( file_path ):

    global stat_data
    while True:
        print "Streaming data..."
        try:
            with open( file_path ) as fd:
                sv = fd.readline().rstrip("\n")
                servers = sv.split("\t")

                while True:
                    stat = fd.readline().rstrip("\n")
                    if stat == "":
                        # Read the end of file, wait 10 seconds
                        # and reopen the log file.
                        gevent.sleep( 10 )
                        break
                    stat = stat.split("\t")
                    stat = zip( servers, stat )
                    stat_data = dict( stat )
                    check_threshold( stat_data )
                    gevent.sleep( 1 )
        except IOError, e:
            if e.errno == 2:
                print "Log file", file_path, "not found"
            return

class ErrorHandler(WSGIHandler):
    def process_result(self):
        try:
            WSGIHandler.process_result(self)
        except IOError, e:
            # Broken pipe error happen when client disconnect, just ignore it
            if e.errno == errno.EPIPE:
                pass
            else:
                raise


if __name__ == '__main__':

    current_stat = {}
    threshold = { 'stat01': 2000, 'stat02':2200, 'stat03':2300, 'stat04':2500 }

    if len( sys.argv ) < 2 :
        print "Wrong command, expect: python traffic.py datafile.txt"
        exit(1)

    file_path = sys.argv[1]

    def start_server():
        WSGIServer.handler_class = ErrorHandler
        server = WSGIServer(("", PORT), app)
        print "Please open a web browser to http://127.0.0.1:", PORT
        ferr = open('out.log', 'w')
        server.log = ferr  #redirect the server log
        server.serve_forever()

    # use a independent thread to run the server
    t = threading.Thread( target = start_server )
    t.daemon = True
    t.start()

    gevent.sleep(0.5)
    raw_input( "Press Enter to start streaming data." )

    stream_data( file_path )
