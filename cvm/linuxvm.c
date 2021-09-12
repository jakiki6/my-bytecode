#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <unistd.h>

#include "vm.h"

int main(int argc, char *argv[]) {
	if (argc != 2) {
		printf("%s <rom>\n", argv[0]);
		return 1;
	}

	cpu_t *cpu = malloc(sizeof(cpu_t *));
	vm_init_cpu(cpu, malloc(65536));

	FILE *file = fopen(argv[1], "r");
	fread(cpu->mem, 1, 65536, file);
	fclose(file);

	while (vm_cycle_cpu(cpu));

	free(cpu->mem);
	free(cpu);
}

void glue_print_char(uint8_t val) {
	printf("%c", val);
}

uint8_t glue_read_char() {
	uint8_t c;
	read(STDIN_FILENO, &c, 1);
	return c;
}
