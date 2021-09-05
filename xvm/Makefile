all: run

run: os.img
	qemu-system-i386 -enable-kvm -hda $<

os.img:
	nasm -f bin -o $@ vm.asm

clean:
	rm os.img 2> /dev/null || true

.PHONY: all run clean
