#include <stdint.h>

typedef struct {
	uint16_t pc;
	uint16_t ps;
	uint16_t rs;

	uint8_t *mem;
} cpu_t;

cpu_t *create_cpu();
void free_cpu(cpu_t *cpu);
