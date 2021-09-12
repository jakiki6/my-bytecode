_start:	msg
loop:	dup ldb
	dup 0 eq jmpc stop
	0x00 deo
	1 add
	jmp loop
stop:	brk

msg:	db "Hello world!\n", 0
