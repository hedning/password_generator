#!/usr/bin/env python

# site:salt:length

from argparse import ArgumentParser
import bcrypt
import os
import getpass

home = os.getenv('HOME')
saltfile = home + '/.saltinfo'
log_rounds = 25

def get_salt(site):
	salts = [x for x in open(saltfile) if x[0] != '#']
	for i, v in enumerate(salts):
		v = v.split(':')
		if v[0] == site:
			return salts, i, v
	return salts, 0, []
	
def write_salts(salts):
	fi = open(saltfile, 'w')
	fi.write('\n'.join(salts))
	fi.close()

def generate_salt(length):
	return ':'.join([site, bcrypt.gensalt(), str(length)])

def generate(site):
	salts, index, info = get_salt(site)
	if info != []:
		length = options.length if options.length > 0 else int(info[2])
		salt = generate_salt(length)
		print 'Already exists a salt for this site. Generating new one, backing up the old'
		salts[index] = salt
		salts.insert(0, '#' + ':'.join(info))
	else:
		length = options.length
		salt = generate_salt(length)
		salts.append(salt)
	info = salt.split(':')
	write_salts(salts)
	return salts, index, info

parser = ArgumentParser(description='Generates new passwords using a master password and an url.')

parser.add_argument('site', type=str, nargs=1,
		help='The site you want to the password for')
parser.add_argument('--generate', '-g', dest='generate', action='store_const',
		default=get_salt, const=generate,
		help='will generate a new password, ie. a new salt')
parser.add_argument('--length', '-l', dest='length', type=int, nargs=1, default=-1,
		help='the length of the hash')
parser.add_argument('--store', '-s', dest='store', action='store_true',
		help='will store the hash, so next time you call prog with site it will not prompt for the master password NYI')
parser.add_argument('--clean', dest='clean', action='store_true',
		help='Cleans out hashes not in use')
parser.add_argument('--undo', '-u', dest='undo', action='store_true',
		help='Restores the recently used hash for the site NYI.')

options = parser.parse_args()
site = options.site[0]

salts, index, info = options.generate(site)

password = getpass.getpass()

print bcrypt.hashpw(password+site, info[1]).replace(info[1], '')[:int(info[2])]
