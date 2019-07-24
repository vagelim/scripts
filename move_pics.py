#!/usr/bin/env python

import sys
import shutil
import os
import glob

def main():
	dir = os.getcwd()
	dir = dir + '/'
	for file in glob.glob(dir + "*01*"):
		print file
		shutil.move(file, "Jan")
		
	for file in glob.glob(dir + "*02*"):
		print file
		shutil.move(file, "Feb")
		
	for file in glob.glob(dir + "*03*"):
		print file
		shutil.move(file, "Mar")
		
		
	for file in glob.glob(dir + "*04*"):
		print file
		shutil.move(file, "Apr")
	
	
	for file in glob.glob(dir + "*05*"):
		print file
		shutil.move(file, "May")
	
	
	for file in glob.glob(dir + "*06*"):
		print file
		shutil.move(file, "June")
	
	
	for file in glob.glob(dir + "*07*"):
		print file
		shutil.move(file, "July")
	
	
	for file in glob.glob(dir + "*08*"):
		print file
		shutil.move(file, "Aug")
	
	
	for file in glob.glob(dir + "*09*"):
		print file
		shutil.move(file, "Sept")
	
	
	for file in glob.glob(dir + "*10*"):
		print file
		shutil.move(file, "Oct")
	
	
	for file in glob.glob(dir + "*11*"):
		print file
		shutil.move(file, "Nov")
	
	
	for file in glob.glob(dir + "*12*"):
		print file
		shutil.move(file, "Dec")
	
if __name__ == "__main__":
	main()
