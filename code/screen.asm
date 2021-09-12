_start:	0			; y
yl:	dup 0x25 deo		; write to y register
	0			; x
xl:	dup 0x24 deo		; write to x register
	0x30 dei 0x21 deo	; red
        0x30 dei 0x22 deo	; green
        0x30 dei 0x23 deo	; blue
	0x00 0x20 deo		; write
	1 add			; increment x
	dup 0x24 dei eq		; reached end?
	not jmpc xl		; if not, jump
	drop			; drop x
	1 add			; increment y
	dup 0x25 dei eq		; reached end?
	not jmpc yl		; if not, jump
stop:	0x00 0x26 deo		; commit
	jmp $			; hang
