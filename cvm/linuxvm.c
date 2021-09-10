#include <stdio.h>

#include "vm.h"

int main(int argc, char *argv[]) {
	if (argc != 2) {
		printf("%s <rom>\n", argv[0]);
		return 1;
	}

	cpu_t *cpu = create_cpu();

	FILE *file = fopen(argv[1], "r");
	fread(cpu->mem, 1, 65536, file);
	fclose(file);

	while (cycle_cpu(cpu));

	free_cpu(cpu);
}
