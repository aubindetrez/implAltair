import random
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge
from cocotb.triggers import FallingEdge
from cocotb.triggers import Timer
import cocotb.simulator as simulator

DEBUG = False # Main switch to turn on/off debugging prints
SIM_DURATION = 100
CLOCK_PERIOD_NS = 1 # ns
MAX_LOOKUP_LATENCY_PS = 13*CLOCK_PERIOD_NS*1000

mem_with_pairing = [
      0b01000000000000000011000100000101 # no pairing r3 = r4 + r5
    , 0b11000000000000000011000100000111 # pairing r3 = r4 + r7
    , 0b01000000000000000011000100000110 # r3 = r4 + r6
    , 0b01000000000000000011000100001000 # no pairing r3 = r4 + r8
    , 0b01000000000000000100000100001010 # no pairing r4 = r4 + r10
    , 0b01000000000000000100000100001011 # no pairing r4 = r4 + r11
    , 0b01000000000000000100000100001100 # no pairing r4 = r4 + r12
    , 0b01000000000000000110000100001001 # no pairing r4 = r6 + r9
    , 0b01000000000000000111000100001001 # no pairing r4 = r7 + r9
    , 0b01000000000000000101000100001010 # no pairing r4 = r5 + r10
    , 0b01000000000000000101000100001011 # no pairing r4 = r5 + r11
    , 0b01000000000000000101000100001100 # no pairing r4 = r5 + r12
    , 0b01000000000000000111000100001001 # no pairing r4 = r7 + r9
    , 0b01000000000000001000000100001001 # no pairing r4 = r8 + r9
        ]

def mem_read(memory, address):
    if int(address) >= len(memory):
        return 0x00000000
    else:
        return memory[int(address)]

def random_address(memory):
    if random.randint(0, 100) > 20: # 20% chance
        return random.randint(0, 2**30-1)
    else: # 80% of the fetches are within the hardcoded cache lines range
        return random.randint(0, len(memory))

async def reset_sequence(dut):
    clock = Clock(dut.i_clk, CLOCK_PERIOD_NS, units="ns") # 1ns clock period
    cocotb.fork(clock.start())
    if DEBUG:
        print("[v] Clock initialized")
    dut.i_rst.value = 0b1
    dut.i_if_brch.value = 0b0
    dut.i_if_brch_addr.value = 0b0
    dut.i_if_ready.value = 0b0
    dut.i_mem_data_valid.value = 0b0
    dut.i_mem_addr_valid.value = 0b0
    dut.i_mem_bus.value = 0x00000000
    await Timer(200, units="ps") # reset counters
    dut.i_rst.value = 0b0
    await Timer(200, units="ps") # reset counters
    dut.i_if_ready.value = 0b1
    if DEBUG:
        print("[v] Reset sequence done")
    await Timer(200, units="ps") # reset counters
    # TODO test reset sequence

async def cpu_if_interface(dut, memory):
    """
    Emulates a Central Processing Unit (CPU) Instruction Fetch (IF)
    connected to the device 'dut'.
    Inputs:
        dut.i_if_brch.value
        dut.i_if_brch_addr.value
        dut.i_if_ready.value
    Outputs:
        dut.o_if_instr_valid.value
        dut.o_if_instr0.value
        dut.o_if_instr1.value
    """
    program_counter = 0 # CPU's program counter
    will_jump = False
    future_jump_address = 0

    # TODO measure the latency of one memory access
    _, last_req_time = simulator.get_sim_time() # How low it takes for cache to return a line
    # only counts cycles when i_if_ready is set
    while True:
        # Set the CPU as busy at random interval
        #if random.randint(0, 100) > 5: # stall 5% of the time
        #    dut.i_if_ready.value = 0b1
        #else:
        #    dut.i_if_ready.value = 0b0
        # FIXME Use the random approach
        # FIXME substract cycles when i_if_ready is not set from the waiting
        # time (do not trigger timeout if i_if_ready not set)
        dut.i_if_ready.value = 0b1

        if dut.i_if_ready.value == 0b1:
            if dut.o_if_instr_valid.value == 0b1:
                # The cache gave us new instructions to execute

                _, current_time = simulator.get_sim_time()
                if DEBUG:
                    print("IF> Last instruction took {}ps = {} clock cycle"
                            .format(
                                current_time-last_req_time
                                ,(current_time-last_req_time)/(CLOCK_PERIOD_NS*1000)
                                ))
                last_req_time = current_time
                if DEBUG:
                    print("IF> Current timestamp: {}ps".format(last_req_time))
                    print(("IF> Receive instruction 0: {} (expected to match"
                        " address 0x{:x})").format(dut.o_if_instr0.value,
                                program_counter))
                # Check if returned instruction 0 matches the fetched address:
                assert int(dut.o_if_instr0.value) == mem_read(memory, program_counter), "Instruction should match the one at address 0x{:x}".format(program_counter)
                pairing = is_pairing_set(dut.o_if_instr0.value)
                # Check if pairing bit is set and check instruction 1
                if pairing:
                    if DEBUG:
                        print("IF> Pairing bit set")
                        print(("IF> Receive instruction 1: {} (expected to match"
                            " address 0x{:x})").format(dut.o_if_instr1.value,
                                program_counter+1))
                    assert is_pairing_set(dut.o_if_instr1.value) == False, "Pairing should not be set on INSTR1"
                    assert dut.o_if_instr1.value == mem_read(memory,
                        program_counter+1), """ Instruction should match the
                        one at address 0x{:x}""".format(program_counter+1)
                else:
                    if DEBUG:
                        print("IF> Pairing bit not set")
                    assert dut.o_if_instr1.value == 0x00000000, """Instruction 1
                        should be NOP because pairing is not set"""


                # Here the CPU decodes and executes instructions...
                await Timer(100, units="ps")

                # Jump (branch) if a branch was taken 2 cycles ago
                if will_jump:
                    if DEBUG:
                        print("IF> A jump was sent 1 fetch ago, next instruction should be the branch target")
                    program_counter = future_jump_address
                else:
                    if pairing:
                        program_counter += 2
                        if DEBUG:
                            print(("IF> Instruction's pairing bit set: incrementing program_counter"
                                " by 2 -> new program_counter=0x{:x}")
                                .format(program_counter))
                    else:
                        program_counter += 1
                        if DEBUG:
                            print(("if> instruction's pairing bit not set: incrementing program_counter"
                                " by 1 -> new program_counter=0x{:x}")
                                .format(program_counter))

                # 20% of the fetches results in a branch
                if random.randint(0, 100) > 20:
                    # No branch
                    will_jump = False
                    dut.i_if_brch.value = 0b0
                else:
                    # Branching
                    # Next instruction will fetched from 'program_counter'
                    # The instruction after will be fetched from the branch target
                    will_jump = True
                    future_jump_address = random_address(memory) # Random branch target
                    dut.i_if_brch.value = 0b1
                    if DEBUG:
                        print(("IF> Sending branch to address:"
                            " 0x{:x}").format(future_jump_address))

                # Will be ignored if i_if_brch is not set
                dut.i_if_brch_addr.value = future_jump_address
        else:
            # CPU's IF stage is not ready
            assert dut.o_if_instr_valid.value == 0, """i_if_ready is not set, cpu
                not ready to receive instructions"""
            if DEBUG:
                print("IF> Not ready")

        # Wait one cycle
        await RisingEdge(dut.i_clk)

        if DEBUG:
            print("IF> +1 Clock Cycle")

def is_pairing_set(instruction):
    return (instruction&0x80000000) == 0x80000000

async def mem_interface(dut, memory):
    """
    Emulates a Memory Interface connected to the device 'dut'
    The memory interface has a random access latency.
    Inputs:
        dut.i_mem_data_valid
        dut.i_mem_addr_valid
        dut.i_mem_bus
    Outputs:
        dut.o_mem_req_addr.value
        dut.o_mem_req_ready.value.binstr
    """
    while True:
        access_latencies = [0, 1, 2, 5] # array of possible access latency (cyc)
        mem_interface_reset = 0b0 # TODO use a realistic reset
        if mem_interface_reset == 0b1:
            if DEBUG:
                print("MEM> Reset")
            dut.i_mem_data_valid.value = 0b0
            dut.i_mem_addr_valid.value = 0b0
        else:
            if dut.o_mem_req_ready == 0b1:
                # cache is issuing a request to main memory
                requested_address = dut.o_mem_req_addr.value

                if DEBUG:
                    print("MEM> **Request received for address 0x{:x}**".format(int(requested_address)))

                # Random access latency for this access
                assert len(access_latencies)>0 # Access_latencies should be initialized
                latency = access_latencies[random.randint(0, len(access_latencies)-1)]

                if DEBUG:
                    print("MEM> Latency for this request: {}".format(latency))

                for cyc in range(latency):
                    if DEBUG:
                        print("MEM> +1 Clock Cycle")
                    await RisingEdge(dut.i_clk)
                    # while the cache is requesting a line the address should not
                    # change
                    assert dut.o_mem_req_ready.value.binstr == "1", """The cache is
                        should keep mem_ready to until the memory returns the
                        requested data"""
                    assert dut.o_mem_req_addr.value == requested_address, """The
                        cache should keep mem_req_addr constant until the memory
                        responds"""

                # Main memory returns the cache line
                await Timer(200, units="ps")
                assert dut.o_mem_req_ready.value.binstr == "1", """The cache is
                    should keep mem_ready to until the memory returns the
                    requested data"""
                assert dut.o_mem_req_addr.value == requested_address, """The
                    cache should keep mem_req_addr constant until the memory
                    responds"""
                dut.i_mem_data_valid.value = 0b1
                dut.i_mem_addr_valid.value = 0b0 # Note: Not supported by the dummy cache
                tmp_val = mem_read(memory, dut.o_mem_req_addr.value)
                dut.i_mem_bus.value = tmp_val

                if DEBUG:
                    print("MEM> Returning data: {:032b} (memory address 0x{:x})"
                            .format(tmp_val, int(dut.o_mem_req_addr.value)))

                await Timer(CLOCK_PERIOD_NS*1000-300, units="ps") # i_mem_data_valid should last at least 1 cycle

                assert dut.o_mem_req_ready.value == 0, """
                    The cache should stop requesting a line when it is returned:
                    o_mem_req_ready should be 0 when i_mem_data_valid==1'b1"""
            else: # dut.o_mem_req_ready == 0b0
                if DEBUG:
                    print("MEM> No request received")
                # No request to main memory, we do not return anything
                dut.i_mem_data_valid.value = 0b0
                dut.i_mem_addr_valid.value = 0b0
        await Timer(100, units="ps") # Give some time for the combinational logic

        if DEBUG:
            print("MEM> +1 Clock Cycle")
        await RisingEdge(dut.i_clk)

@cocotb.test()
async def test_interfaces(dut):
    """
    Tests interfaces with the CPU Instruction Fetch stage
    and with the main memory controller
    """
    await reset_sequence(dut)

    # Check interface with the CPU Instruction Fetch stage
    cocotb.fork(cpu_if_interface(dut, mem_with_pairing))

    # Check interface with main memory
    cocotb.fork(mem_interface(dut, mem_with_pairing))

    for i in range(SIM_DURATION): # TODO add a parameter
        await RisingEdge(dut.i_clk)
