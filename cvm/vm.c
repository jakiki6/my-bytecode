#include <stdint.h>
#include <stdlib.h>

#include "vm.h"

static uint8_t fetch_byte(cpu_t *cpu) {
	uint8_t res = cpu->mem[cpu->pc];
	cpu->pc++;
}

static uint16_t fetch_word(cpu_t *cpu) {
	return fetch_byte(cpu) | (fetch_byte(cpu) << 8);
}

static void push_ps(cpu_t *cpu, uint16_t word) {
	cpu->ps = cpu->ps - 2;
	cpu->mem[cpu->ps] = word & 0xff;
	cpu->mem[cpu->ps+1] = word >> 8;
}

static uint16_t pop_ps(cpu_t *cpu) {
	uint16_t res = cpu->mem[cpu->ps] | (cpu->mem[cpu->ps+1] << 8);
	cpu->ps = cpu->ps + 2;
	return res;
}

static void push_rs(cpu_t *cpu, uint16_t word) {
    cpu->mem[cpu->ps] = word & 0xff;
    cpu->mem[cpu->ps+1] = word >> 8;
    cpu->rs = cpu->rs + 2;
}

static uint16_t pop_rs(cpu_t *cpu) {               
    cpu->rs = cpu->rs - 2;
    uint16_t res = cpu->mem[cpu->rs] | (cpu->mem[cpu->rs+1] << 8);
    return res;
}

static void push_stack(cpu_t *cpu, uint16_t word, uint8_t is_rs) {
	if (is_rs) {
		push_rs(cpu, word);
	} else {
		push_ps(cpu, word);
	}
}

static uint16_t pop_stack(cpu_t *cpu, uint8_t is_rs) {
	if (is_rs) {
        return pop_rs(cpu);
    } else {
        return pop_ps(cpu);
    }
}

cpu_t *create_cpu() {
	cpu_t *cpu = malloc(sizeof(cpu_t *));

	cpu->pc = 0;
	cpu->ps = 0xff00;
	cpu->rs = 0xffff;

	cpu->mem = malloc(65536);

	return cpu;
}

void free_cpu(cpu_t *cpu) {
	free(cpu->mem);
	free(cpu);
}

void cycle_cpu(cpu_t *cpu) {
	uint8_t opcode = fetch_byte(cpu);
	uint8_t is_rs = (opcode & 0b10000000) >> 7;
}
