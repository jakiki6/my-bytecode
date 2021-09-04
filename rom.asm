_start:	msg
loop:	dup msg_end eq jmpc stop
	dup ldb 0x0000 deo
	1 add
	jmp loop
stop:	brk

msg:	db "Hello world!\n"
msg_end:
