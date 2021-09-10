#include <stdint.h>
#include <stdio.h>

#include "vm.h"

uint16_t devices_read(cpu_t *cpu, uint16_t addr) {
	return 0;
}

void devices_write(cpu_t *cpu, uint16_t addr, uint16_t val) {
	switch (addr) {
		case 0x0000:
			printf("%c", val);
	}
	return;
}
