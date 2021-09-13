loop:	0x30 dei 0x21 deo			; red
        0x30 dei 0x22 deo			; green
        0x30 dei 0x23 deo			; blue
	x ldw 0x24 deo				; write x
	y ldw 0x25 deo				; write y
	0x00 0x20 deo				; draw
	0x00 0x26 deo				; commit
	x ldw 0x30 dei add 0x24 dei mod x stw	; change x
	y ldw 0x30 dei add 0x25 dei mod y stw	; change y
	jmp loop

x:	db 0, 0
y:	db 0, 0
