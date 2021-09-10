all: linuxvm
	./$< ../rom.bin

linuxvm: linuxvm.o vm.o devices.o
	gcc -o $@ $^

%.o: %.c
	gcc -c -o $@ $<

clean:
	rm linuxvm *.o 2> /dev/null || true

.PHONY: all clean
