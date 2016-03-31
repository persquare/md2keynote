# -*- coding: utf-8 -*-
#
# Copyright 2013 Evan Jones
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
#
"""
A little script to bridge Python to AppleScript (formally known as OSA), on
OS X obviously. The `OSAScript` class wraps any string of AppleScript code and
exposes any subroutines/events in the code (``on funcName(args,...) ... end
funcName`` blocks) as attributes. Usage examples can be found at the bottom
under the ``if __name__ == '__main__':``
"""

from   functools import partial
import Cocoa, struct
from   Cocoa import NSAppleEventDescriptor as NSAED

# int literal/constant, like in C
INT = lambda s: struct.unpack('>i', s)[0]
intchrs = partial (struct.pack, '>i')

# based on, basically, reverse engineering the headers. Can't find them linked
# anywhere :S
kCurrentProcess            = 2
kAutoGenerateReturnID      = -1
kAnyTransactionID          = 0
kASSubroutineEvent         = INT ('psbr')
typeProcessSerialNumber    = INT ('psn ')
keyASSubroutineName        = INT ('snam')
typeAppleScript            = INT ('ascr')
keyDirectObject            = INT ('----')
typeIEEE64BitFloatingPoint = INT ('doub')

# Cocoa/Carbon ProcessSerialNumber struct - { UInt32, UInt32 }
struct_ProcessSerialNumber = 'II'

class OSAScript(object):
    def __init__(self, source):
        self.script = Cocoa.NSAppleScript.alloc().initWithSource_ (source)

    def __getattr__(self, evtname):
        return partial (self.execute_event, evtname)

    def execute_event(self, evtname, *args):
        procdes = NSAED.descriptorWithDescriptorType_bytes_length_ (
                        typeProcessSerialNumber,
                        struct.pack (struct_ProcessSerialNumber, 0, kCurrentProcess),
                        struct.calcsize (struct_ProcessSerialNumber))

        evt = NSAED.appleEventWithEventClass_eventID_targetDescriptor_returnID_transactionID_ (
                    typeAppleScript, kASSubroutineEvent, procdes,
                    kAutoGenerateReturnID, kAnyTransactionID)

        updateDescriptorKeywords (evt,
            [(keyASSubroutineName, evtname),
             (keyDirectObject,     args)])

        out, err = self.script.executeAppleEvent_error_ (evt, None)
        
        if err is not None:
            raise OSAError (err)

        return convertDescriptor (out)

class OSAError(Exception):
    """ Raised when there's an error returned by an OSA script """

# map NSA.E.D. descriptor types for value descriptors to the corresponding
# value accessors, or conversion functions where appropriate
descTypeToConverter = {
    INT ('bool'): NSAED.booleanValue,
    INT ('enum'): NSAED.enumCodeValue,
    INT ('long'): NSAED.int32Value,
    INT ('utxt'): NSAED.stringValue,
    INT ('doub'): lambda d: struct.unpack('d', d.data())[0],

    # NSA.E.D. listDescriptors are 1-based
    INT ('list'): lambda d: [ convertDescriptor (d.descriptorAtIndex_ (i))
                              for i in xrange (1, d.numberOfItems() + 1) ],

    INT ('reco'): lambda d: { kwd: d.descriptorForKeyword_ (kwd)
                              for i in xrange (1, d.numberOfItems() + 1)
                              for kwd in [d.keywordForDescriptorAtIndex_ (i)] }
}

typeToDescConstructor = [
    (bool,          NSAED.descriptorWithBoolean_),
    (int,           NSAED.descriptorWithInt32_),
    (basestring,    NSAED.descriptorWithString_),

    (float,         lambda v:
        NSAED.descriptorWithDescriptorType_bytes_length_ (
            typeIEEE64BitFloatingPoint, struct.pack ('d', v), struct.calcsize ('d'))),

    ((tuple, list), lambda v: seqToListDescriptor (v)),
    (dict,          lambda v: dictToRecordDescriptor (v))
]

def convertDescriptor (d):
    conv = descTypeToConverter.get (d.descriptorType())
    return conv and conv (d)

def toDescriptor (v):
    for typ, construct in typeToDescConstructor:
        if isinstance (v, typ):
            return construct (v)
    return NSAED.nullDescriptor()

def seqToListDescriptor (v):
    ld = NSAED.listDescriptor()
    for i, val in enumerate (v):
        # NSA.E.D. listDescriptors are 1-based
        ld.insertDescriptor_atIndex_ (toDescriptor (val), i + 1)
    return ld

def updateDescriptorKeywords (rd, items):
    for prop, val in items:
        rd.setDescriptor_forKeyword_ (toDescriptor (val), prop)

def dictToRecordDescriptor (v):
    rd = NSAED.recordDescriptor()
    updateDescriptorKeywords (rd, v.iteritems())
    return rd


if __name__ == '__main__':
            
    mail_script = OSAScript (u'''\

on sendmail(recipient, subject, content)
    set x to subject
    set y to content
    set z to recipient
    tell application "Mail"
        set newMsg to make new outgoing message with properties { ¬
            subject: x, content: y, visible: true ¬
        }
        tell newMsg
            make new to recipient at end of to recipients ¬
                with properties { address: z }
            send
        end tell
    end tell
end sendmail

on getaddr()
    tell application "Mail"
        if (count of accounts) < 1 then return ""
        set acct to last item of accounts
        set addrs to email addresses of acct
        if (count of addrs) < 1 then return ""
        set addr to last item of addrs
        return addr
    end tell
end getaddr

on echo(args)
    repeat with arg in args
        say arg
    end repeat
end echo

    ''')

    mail_script.echo (['Here are some numbers:', 4.5, 3])
    
    myaddr = mail_script.getaddr()

    if not myaddr:
        print 'Couldn\'t find primary email account'

    else:
        print 'My address:', myaddr

        conf = raw_input ('Send test email to self? (y/n) ')
        
        if conf.strip().lower() in ('y', 'yes'):
            mail_script.sendmail (myaddr, 'Test Email',
                'This is a test, autogenerated in Python, sent through Mail.app')
