#include <stdint.h>

#include "vm.h"
#include "glue.h"

uint16_t devices_read(cpu_t *cpu, uint16_t addr) {
	uint16_t res = 0;

	switch (addr) {
        case 0x0000:
            res = glue_read_char();
			break;
    }

	return res;
}

void devices_write(cpu_t *cpu, uint16_t addr, uint16_t val) {
	switch (addr) {
		case 0x0000:
			glue_print_char((uint8_t) val);
			break;
	}
	return;
}
