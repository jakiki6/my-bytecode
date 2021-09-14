#include <stdint.h>

#include "vm.h"
#include "devices.h"

static uint8_t fetch_byte(cpu_t *cpu) {
	uint8_t res = cpu->mem[cpu->pc];
	cpu->pc++;
	return res;
}

static uint16_t fetch_word(cpu_t *cpu) {
	return fetch_byte(cpu) | (fetch_byte(cpu) << 8);
}

static void write_byte(cpu_t *cpu, uint16_t addr, uint8_t val) {
	cpu->mem[addr] = val;
}

static void write_word(cpu_t *cpu, uint16_t addr, uint16_t val) { 
    write_byte(cpu, addr, val & 0xff);
	write_byte(cpu, addr + 1, val >> 8);
}

static uint8_t read_byte(cpu_t *cpu, uint16_t addr) {
	return cpu->mem[addr];
}

static uint16_t read_word(cpu_t *cpu, uint16_t addr) {
	return read_byte(cpu, addr) | (read_byte(cpu, addr + 1) << 8);
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

void vm_init_cpu(cpu_t *cpu, uint8_t *mem) {
	cpu->pc = 0;
	cpu->ps = 0xff00;
	cpu->rs = 0xffff;

	cpu->mem = mem;
}

uint8_t vm_cycle_cpu(cpu_t *cpu) {
	uint8_t opcode = fetch_byte(cpu);
	uint8_t is_rs = (opcode & 0b10000000) >> 7;
	opcode = opcode & 0b11111;

	uint16_t a, b, c;

	switch (opcode) {
		case 0b00000:	// break
			return 0;
			break;
		case 0b00001:	// literal
			push_stack(cpu, fetch_word(cpu), is_rs);
			break;
		case 0b00010:	// set stack, pushes old one
			if (is_rs) {
				uint16_t oldval = cpu->rs;
				cpu->rs = fetch_word(cpu);
				push_rs(cpu, oldval);
			} else {
				uint16_t oldval = cpu->ps;
                cpu->ps = fetch_word(cpu);
                push_ps(cpu, oldval);
			}
			break;
		case 0b00011:	// drop
			pop_stack(cpu, is_rs);
			break;
		case 0b00100:	// dup
			a = pop_stack(cpu, is_rs);
			push_stack(cpu, a, is_rs);
			push_stack(cpu, a, is_rs);
			break;
		case 0b00101:   // swap
			b = pop_stack(cpu, is_rs);
            a = pop_stack(cpu, is_rs);
            push_stack(cpu, a, is_rs); 
            push_stack(cpu, b, is_rs);
            break;
		case 0b00110:	// over
			b = pop_stack(cpu, is_rs);
			a = pop_stack(cpu, is_rs);
			push_stack(cpu, a, is_rs);
			push_stack(cpu, b, is_rs);
			push_stack(cpu, a, is_rs);
			break;
		case 0b00111:	// rotate
			c = pop_stack(cpu, is_rs);
			b = pop_stack(cpu, is_rs);
            a = pop_stack(cpu, is_rs);
            push_stack(cpu, b, is_rs);
            push_stack(cpu, c, is_rs);
            push_stack(cpu, a, is_rs);
			break;
		case 0b01000:	// equal
			b = pop_stack(cpu, is_rs);
            a = pop_stack(cpu, is_rs);
			push_stack(cpu, (int16_t) a == b, is_rs);
			break;
		case 0b01001:	// not
			a = pop_stack(cpu, is_rs);
			push_stack(cpu, a ^ 1, is_rs);
			break;
		case 0b01010:	// greater than
			b = pop_stack(cpu, is_rs);
            a = pop_stack(cpu, is_rs);
            push_stack(cpu, (int16_t) a > b, is_rs);
			break;
		case 0b01011:   // less than
            b = pop_stack(cpu, is_rs);
            a = pop_stack(cpu, is_rs);
            push_stack(cpu, (int16_t) a < b, is_rs);
			break;
		case 0b01100:	// jump
			cpu->pc = pop_stack(cpu, is_rs);
			break;
		case 0b01101:;	// jump conditionally
			uint16_t tpc = pop_stack(cpu, is_rs);
			a = pop_stack(cpu, is_rs);
			if (a) {
				cpu->pc = tpc;
			}
			break;
		case 0b01110:	// jump stash
			push_stack(cpu, cpu->pc, !is_rs);
			cpu->pc = pop_stack(cpu, is_rs);
			break;
		case 0b01111:	// stash
			a = pop_stack(cpu, is_rs);
			a = pop_stack(cpu, !is_rs);
			break;
		case 0b10000:	// add
			b = pop_stack(cpu, is_rs);
            a = pop_stack(cpu, is_rs);
            push_stack(cpu, a + b, is_rs);
			break;
		case 0b10001:   // subtract
            b = pop_stack(cpu, is_rs);
            a = pop_stack(cpu, is_rs);
            push_stack(cpu, a - b, is_rs);
			break;
		case 0b10010:   // multiply
            b = pop_stack(cpu, is_rs);
            a = pop_stack(cpu, is_rs);
            push_stack(cpu, a * b, is_rs);
			break;
		case 0b10011:   // divide
            b = pop_stack(cpu, is_rs);
            a = pop_stack(cpu, is_rs);
            push_stack(cpu, a / b, is_rs);
			break;
		case 0b10100:   // modulo
            b = pop_stack(cpu, is_rs);
            a = pop_stack(cpu, is_rs);
            push_stack(cpu, a % b, is_rs);
			break;
		case 0b10101:   // and
            b = pop_stack(cpu, is_rs);
            a = pop_stack(cpu, is_rs);
            push_stack(cpu, a & b, is_rs);
			break;
		case 0b10110:   // or
            b = pop_stack(cpu, is_rs);
            a = pop_stack(cpu, is_rs);
            push_stack(cpu, a | b, is_rs);
			break;
		case 0b10111:   // xor
            b = pop_stack(cpu, is_rs);
            a = pop_stack(cpu, is_rs);
            push_stack(cpu, a ^ b, is_rs);
			break;
		case 0b11000:   // shift
            b = pop_stack(cpu, is_rs);
            a = pop_stack(cpu, is_rs);
            uint8_t is_right = b & 0b1000000000000000 >> 15;
			b = b & 0b0111111111111111;

			if (is_right) {
				a = a << b;
			} else {
				a = a >> b;
			}

			push_stack(cpu, a, is_rs);
			break;
		case 0b11001:	// load byte
			a = pop_stack(cpu, is_rs);
			push_stack(cpu, read_byte(cpu, a), is_rs);
			break;
		case 0b11010:   // load word
            a = pop_stack(cpu, is_rs);
            push_stack(cpu, read_word(cpu, a), is_rs);
            break;
		case 0b11011:	// store byte
			a = pop_stack(cpu, is_rs);
			b = pop_stack(cpu, is_rs);
			write_byte(cpu, a, (uint8_t) b);
			break;
		case 0b11100:   // store word 
            a = pop_stack(cpu, is_rs);
            b = pop_stack(cpu, is_rs);
            write_word(cpu, a, b);
			break;
		case 0b11101:	// device in
			a = pop_stack(cpu, is_rs);
			push_stack(cpu, devices_read(cpu, a), is_rs);
			break;
		case 0b11110:	// device out
			a = pop_stack(cpu, is_rs);
			b = pop_stack(cpu, is_rs);

			devices_write(cpu, a, b);
			break;
		case 0b11111:;	// call native blob
			uintptr_t addr = pop_stack(cpu, is_rs) + (uintptr_t) (&cpu->mem[0]);
			((void (*)()) addr)();
		default:
			break;
	}

	return 1;
}
