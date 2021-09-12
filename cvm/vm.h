#include <stdint.h>

typedef struct {
	uint16_t pc;
	uint16_t ps;
	uint16_t rs;

	uint8_t *mem;
} cpu_t;

void vm_init_cpu(cpu_t *cpu, uint8_t *mem);
uint8_t vm_cycle_cpu(cpu_t *cpu);
