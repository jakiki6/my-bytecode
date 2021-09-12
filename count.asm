_start:	0x0000
loop:	1 add
	dup 0xffff neq jmpc loop
	drop
stop:	brk
