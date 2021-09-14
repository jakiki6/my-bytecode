_start:	0x100
loop:	dup 0x30 dei swap stb
	1 add
	dup 0x200 neq jmpc loop
	0x100 sjmp
