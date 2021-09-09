#include "vm.h"

int main() {
	cpu_t *cpu = create_cpu();

	free_cpu(cpu);
}
