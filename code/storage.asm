_start:	0x0000
loop:	dup 0x41 deo 1 add
	0x30 dei 0x40 deo
	dup 0x41 dei lth jmpc loop
	drop
stop:	brk
