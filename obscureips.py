#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
input: inputfile, localrange, newrange (default is 192.168.111)
change the local hostids in an output file
TODO:
- make localrange and customrange work. they don't handle unexpected constructions well yet.

    :copyright: (c) 2021 by Jeff Sutch
    :license: BSD 2.0, see LICENSE_FILE for more details.

"""
__author__ = "Jeff Sutch"
__copyright__ = "Copyright 2021, Collett Park Networks"
__credits__ = ["Jeff Sutch"]
__license__ = "GPL"
__version__ = "0.1.1"
__maintainer__ = "Jeff Sutch"
__email__ = "jeff@collettpark.com"


import sys, argparse, os, random

# manage arguments
parser = argparse.ArgumentParser(description='Convert log file ip addresses')
parser.add_argument('-f','--filename', required=True, help='input file name')
parser.add_argument('-l','--localrange',metavar='localrange',type=str,help="the range to obscure in the form of '192.168.1.'")
parser.add_argument('-n','--customrange',metavar='customrange',type=str, help="ip range to change to. default is 192.168.111.")

args = parser.parse_args()

# Read in the file

if os.path.isfile(args.filename):
    inputfileraw = open(args.filename,'r').read()

# with open(args.filename,'r') as f:
    # inputfileraw = f.read()
    # f.close()
# inputfileraw = open(args.filename,'r').read()

print(inputfileraw)

inputfile = inputfileraw.split("\n")

# set the localrange
defaultlocalrange='10.0.1.'

if args.localrange:
    inputrange=args.customrange
else:
    inputrange = defaultlocalrange

# make a list of the local ips in the file
localips = []
for line in inputfile:
    for x in line.split(','):
        if inputrange in x and x not in localips:
            localips.append(x)


# Make obscured range
defaultrange='192.168.111.'
if args.customrange:
    outputrange=args.customrange
else:
    outputrange = defaultrange


openips =  [outputrange + str(x) for x in range(10,254)]

# create the dict for replacement
ipmap = {}

def obscureip(keystore,ip):
    keystore[ip] = openips.pop(random.randrange(len(openips)))

for x in localips:
    obscureip(ipmap,x)


# replace the values in the rawfile
for k,v in ipmap.items():
    inputfileraw = inputfileraw.replace(k,v)

# write the file out
outfile = 'scrubbed_' + str(args.filename)

with open(outfile,'w') as f:
    f.write(inputfileraw)


