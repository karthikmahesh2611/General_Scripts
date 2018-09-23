import requests
import argparse
import shelve
import sys
import os

#Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("--create", help="Create robot.txt",action="store_true")
parser.add_argument("--update", help="replace all Allow  rules with Disallow",action="store_true")
parser.add_argument("--status", help="output the count of changed lines",action="store_true")



args = parser.parse_args()

#Check if any optional argument is selected
if len(sys.argv) == 1:
	print("No option selected. Nothing to do.")
	print("Use --help to view the options")
	sys.exit(0)

#Open a shelve file to retain changed lines value after script exits
try:
	values = shelve.open('changed_lines.dat')
	changed_lines = values.setdefault('changed_lines', 0)
except:
	print("Error in opening file 'changed_lines.dat'")
	sys.exit(1)

#Create the new robots file and reset the changed_line counter
if (args.create):
	with open("robots.txt","w") as f:
		response = requests.get("https://google.com/robots.txt")
		data = response.text
		f.write(data)
		changed_lines = 0
	values['changed_lines'] = changed_lines
	values.close()
	sys.exit(0)


if (args.update):
	with open("robots.txt","r") as f:
		with open("robots.txt_new","a") as f_new:
			for line in f.readlines():
				if("Disallow" in line):
					new_value = line.replace("Disallow", "Allow")
					f_new.write(new_value)
					changed_lines = changed_lines + 1
				elif("Allow" in line):
					new_value = line.replace("Allow", "Disallow")
					f_new.write(new_value)
					changed_lines = changed_lines + 1
				else:
					f_new.write(line)
	os.remove("robots.txt")
	os.rename("robots.txt_new", "robots.txt")
	values['changed_lines'] = changed_lines
	values.close()
	sys.exit(0)



if (args.status):
	print("Number of changed lines: {}".format(changed_lines))
	values.close()
	sys.exit(0)
