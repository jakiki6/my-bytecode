	bits 16
	org 0x7c00
start:	cli
	jmp 0x0000:.fix_cs

.fix_cs:
	xor ax, ax
	mov ds, ax
	mov es, ax

	mov ax, 0x1000
	mov ss, ax
	mov sp, 0xffff
	sti
	cld

	; registers:
	; sp=ps bp=rs si=pc ax=accumulator dx=rs?
init:	mov si, dap
	mov ah, 0x42
	int 0x13

	mov ax, 0x1000
	mov ds, ax
	mov es, ax

	mov bp, 0xff00
	xor si, si

main:	lodsb

	; is rs?
	xor dx, dx
	test al, 0b10000000
	jne .not_rs
	inc dx			; set flag
.not_rs:
	cmp al, 0		; is brk?
	je halt

	cmp al, 0x02
	ja .one_byte

	mov bl, al		; fetch word
	lodsw

	cmp bl, 0x01
	jne .setstack
	call push_stack
	jmp main

.setstack:
	cmp dl, 0x00
	jne .setrs
	mov sp, ax
	jmp main
.setrs:	mov bp, ax
	jmp main

.one_byte:
	mov bx, table
	and al, 0b11111
	sub al, 3
	shl al, 2
	add bx, ax
	call word [bx]
	jmp main

halt:	jmp 0xffff:0x0000

push_stack:
	cmp dl, 0x00
	jne .rs
	push ax
	ret
.rs:	mov word [bp], ax
	inc bp
	inc bp
	ret

not_implemented:
	ret
func_drop:
	pop ax
	ret
func_dup:
	pop ax
	push ax
	push ax
	ret
func_over:
	pop bx
	pop ax
	push ax
	push bx
	push ax
	ret
func_rotate:
	pop cx
	pop bx
	pop ax
	push bx
	push cx
	push ax
	ret

dap:
dap.header:
	db dap.end - dap        ; header
dap.unused:
	db 0x00         ; unused
dap.count:
	dw 0x0080       ; number of sectors
dap.offset_offset:
	dw 0            ; offset
dap.offset_segment:
	dw 0x1000       ; segment
dap.lba_lower:   
	dd 1            ; lba
dap.lba_upper:
	dd 0            ; lba
dap.end:

table:	dw func_drop				; 0b00011
	dw func_dup				; 0b00100
	dw func_over				; 0b00101
	dw func_rotate				; 0b00110
	dw not_implemented			; 0b00111
	dw not_implemented			; 0b01000
	dw not_implemented			; 0b01001
	dw not_implemented			; 0b01010
	dw not_implemented			; 0b01011
	dw not_implemented			; 0b01100
	dw not_implemented			; 0b01101
	dw not_implemented			; 0b01110
	dw not_implemented			; 0b01111
	dw not_implemented			; 0b10000
	dw not_implemented			; 0b10001
	dw not_implemented			; 0b10010
	dw not_implemented			; 0b10011
	dw not_implemented			; 0b10100
	dw not_implemented			; 0b10101
	dw not_implemented			; 0b10110
	dw not_implemented			; 0b10111
	dw not_implemented			; 0b11000
	dw not_implemented			; 0b11001
	dw not_implemented			; 0b11010
	dw not_implemented			; 0b11011
	dw not_implemented			; 0b11100
	dw not_implemented			; 0b11101
	dw not_implemented			; 0b11110
	dw not_implemented			; 0b11111

%assign space_left 510-($-$$)
%warning space_left bytes left

times space_left nop
db 0x55, 0xaa
