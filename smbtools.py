#!/usr/bin/env python

import re
import sys
import subprocess32
import os
import shutil


def create_basic_share():
	try:
		with open('/etc/samba/smb.conf', 'a') as f:
			share_name = raw_input('What would you like to name this share? ')
			share_path = raw_input('What is the path of the directory that you want to share? ')
			share_users = raw_input('Who are the valid users (separate them with a space)? ')

			if os.path.exists(share_path):
				f.write('\n')
				f.write('[%s]' % share_name)
				f.write('\n')
				f.write('path = %s' % share_path)
				f.write('\n')
				f.write('available = yes')
				f.write('\n')
				f.write('read only = no')
				f.write('\n')
				f.write('browsable = yes')
				f.write('\n')
				f.write('public = yes')
				f.write('\n')

				print('\nShare created...\n')
				print('Trying to restart Samba service...')
				subprocess32.Popen(['sudo', '/etc/init.d/samba', 'restart'], shell=False)
			else:
				print('\nThis path doesn\'t exist. Run it again, and make sure you add a path that exists.\n')


	except Exception, e:
		raise e


def delete_share():
	try:
		print('These are your current shares:')
		list_shares()
		share_to_delete = '[%s]\n' % raw_input('Which share would you like to delete? ')

		yn = ['y','n']
		confirm = raw_input('Are you sure you want to delete this share [y,n]? ')
		while confirm not in yn:
			confirm = raw_input('Please select y or n. Are you sure you want to delete this share [y,n]? ')
					
		line_list = []

		if confirm == 'y':
			with open('/etc/samba/smb.conf', 'r') as f:
				for line in f.readlines():
					line_list.append(line)

			if share_to_delete in line_list:
				start_pos = line_list.index(share_to_delete)
				end_pos = start_pos + 7
				del line_list[start_pos:end_pos]


				with open('/etc/samba/smb.conf', 'w') as fi:
					fi.truncate()
					fi.seek(0)
					for i in line_list:
						fi.write(i)
				print('Share deleted...')
				print('Trying to restart Samba service...')
				subprocess32.Popen(['sudo', '/etc/init.d/samba', 'restart'], shell=False)
			else:
				print('%s doesn\'t exist. Run again and select a share that exists...' % share_to_delete[1:len(share_to_delete) - 2])

		elif confirm == 'n':
			print('Ok, closing SMBTools...')


	except Exception, e:
		raise e


def list_shares():
	print('\n')
	try:
		with open('/etc/samba/smb.conf', 'r') as f:
			for line in f.readlines():
				if re.match(r'\[.*\]', line):
					end_pos = len(line) - 2
					print(line[1:end_pos])
				else:
					pass
	except Exception, e:
		raise e
	print('\n')


def backup_smbconf():
	if os.path.exists('/etc/samba/smb.conf'):
		print('Backing up smb.conf...')
		shutil.copyfile('/etc/samba/smb.conf', '/usr/share/smbtools/smb_backup.conf')
		print('Successfully backed up /etc/samba/smb.conf to /usr/share/smbtools/smb_backup.conf...')
	else:
		print('Can\'t find /etc/samba/smb.conf. Make sure Samba is installed...')


def restore_smbconf():
	if os.path.exists('smbtoolstest_backup.txt'):
		print('Restoring backup smb.conf...')
		shutil.copyfile('/usr/share/smbtools/smb_backup.conf', '/etc/samba/smb.conf')
	else:
		yn = ['y','n']
		confirm_backup = raw_input('Can\'t find your smb.conf backup. Create a backup now [y,n]? ')
		while confirm_backup not in yn:
			confirm_backup = raw_input('Please select y or n. Create a backup now [y,n]? ')
		if confirm_backup == 'y':
			backup_smbconf()
			print('Successfully restored smb.conf...')
			print('Trying to restart Samba service...')
			subprocess32.Popen(['sudo', '/etc/init.d/samba', 'restart'], shell=False)
		elif confirm_backup == 'n':
			print('Ok, closing SMBTools...')


def main():
	if '-ls' in sys.argv:
		list_shares()
	elif '-n' in sys.argv:
		create_basic_share()
	elif '-d' in sys.argv:
		delete_share()
	elif '--help' in sys.argv or '-h' in sys.argv:
		print("""
You must have root privileges.

You can pass the following flags:

-ls to show your current shares.
-n to create a new basic share.
-d to delete an existing share.

example: sudo smbtools -ls to list all the current shares.
""")

	else:
		print('You need to pass a flag to do something. Use the -h or --help flag to see what flags you can use (ex: smbtools --help)...')


if __name__ == '__main__':
	main()