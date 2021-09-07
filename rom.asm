_start:	msg
loop:	dup ldb
	dup 0 eq jmpc stop
	0x0000 deo
	1 add
	jmp loop
stop:	code native

msg:	db "Hello world!\n", 0
code:	db "print('Hi')", 0
