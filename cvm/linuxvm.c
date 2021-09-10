#include "vm.h"

int main() {
	cpu_t *cpu = create_cpu();

	while (cycle_cpu(cpu));

	free_cpu(cpu);
}
