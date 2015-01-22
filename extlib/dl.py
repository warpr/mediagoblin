#!/usr/bin/env python

#   This file is part of GNU MediaGoblin
#   Copyright (C) 2015  Kuno Woudt <kuno@frob.nl>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of copyleft-next 0.3.0.

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

# requirements:
# pip install requests
#
# and make sure the following are installed on older pythons without SNI support
# pip install pyopenssl ndg-httpsclient pyasn1

import os
import json
import pipes
import urllib
import requests

def warning (msg):
    print (msg)


def npm (name, data):
    response = requests.get('https://registry.npmjs.org/%s' % (data['package']))
    metadata = response.json()
    versioninfo = metadata['versions'][data['version']]

    link = versioninfo['dist']['tarball']

    print ("\nDownloading %s from %s" % (name, link))

    if 'source' in data:
        print ("Source: %s" % (data['source']))
    else:
        print ("Source: %s (%s)" % (metadata['repository']['url'], metadata['repository']['type']))

    if 'license' in data:
        print ("License: %s" % (data['license']))
    elif 'license' in metadata:
            print ("License: %s" % (metadata['license']))
    else:
        # FIXME: ...
        pass

    authors = [ "%s <%s>" % (m['name'], m['email']) for m in metadata['maintainers'] ]
    print ("Maintainers: ", ", ".join (authors))

    os.system ('wget %s' % (pipes.quote (link)))
    print ("FIXME: do a sha1sum comparison with", versioninfo['dist']['shasum'])

    # and here unpack the tarball in a (secure) tmp folder and then move those
    # contents to their expected place.  I think all npm distributed tar balls
    # unpack into a 'package/' folder which can be renamed to the package name.


def google_fonts (name, data):
    url_template = 'https://googlefontdirectory.googlecode.com/hg/%s/'
    os.system ('wget --no-parent --recursive --force-directories --no-host-directories --cut-dirs=2 ' + url_template % (data['package']))


drivers = {
    'npm': npm,
    'Google Fonts': google_fonts
}

if __name__ == '__main__':
    packages = json.load (open ("packages.json", "rb"))

    for lib, metadata in packages.iteritems ():
        if not 'registry' in metadata:
            warning ("Sorry, I don't know where to get " + lib)
            continue

        registry = metadata['registry']
        if not registry in drivers:
            warning ("Sorry, I don't know how to download things from " + registry)
            continue

        drivers[registry] (lib, metadata)
