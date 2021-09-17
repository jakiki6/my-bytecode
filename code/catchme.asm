_start:	0x30 dei x stw		; init x
	0x30 dei y stw		; init y
	1 fc stw
main:	; limit x and y
	x ldw 0x24 dei mod x stw
	y ldw 0x25 dei mod y stw

	0x30 dei 0x21 deo	; red
	0x30 dei 0x22 deo	; green
	0x30 dei 0x23 deo	; blue

	x ldw 0x24 deo		; write x
	y ldw 0x25 deo		; write y

	0x00 0x20 deo		; draw

	fc ldw 1 sub fc stw	; decrement frame counter
	fc ldw 0 neq jmpc .nc	; check if we hit 0
	0x00 0x26 deo		; commit
	30 fc stw		; reset frame counter
.nc:


.x:     x ldw			; read x
        0x30 dei 1 and		; value
        0x30 dei 1 and		; negative?
        jmpc .nx
        add			; add to x
        jmp .dx
.nx:    sub			; sub from x
.dx:    x stw
.y:	y ldw			; read y
	0x30 dei 1 and		; value
	0x30 dei 1 and 		; negative?
	jmpc .ny
	add			; add to y
	jmp .dy
.ny:	sub			; sub from y
.dy:	y stw

	jmp main

x: word
y: word
fc: word
