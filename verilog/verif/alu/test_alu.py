import random
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge
from cocotb.triggers import FallingEdge

@cocotb.test()
async def test_slts(dut):
    clock = Clock(dut.i_clk, 10, units="us") # 10us period clock
    cocotb.fork(clock.start())
    dut.i_clk.value = 0b0
    dut.i_rst.value = 0b0
    dut.i_en.value = 0b1

    for i in range(100):
        dut.i_function.value = 0b0010 # SLTS
        dut.i_inv_c.value = 0b1
        neg_b = int(random.random()*100) % 2
        i_b = neg_b*2**31 + int(random.random()*2**31)
        dut.i_b.value = i_b
        neg_c = int(random.random()*100) % 2
        i_c = neg_c*2**31 + int(random.random()*2**31)
        dut.i_c.value = i_c
        i_rd = int(random.random()*2**6)
        dut.i_rd.value = i_rd

        #print("i_b = " + '{:032b}'.format(i_b))
        #print("i_c = " + '{:032b}'.format(i_c))
        if neg_b:
            i_b = -i_b
        if neg_c:
            i_c = -i_c
        await RisingEdge(dut.i_clk)
        #print("output = " + dut.o_val.value.binstr)
        #print("expect = " + '{:032b}'.format(i_b<i_c))
        assert dut.o_val.value.binstr == '{:032b}'.format(i_b<i_c), "Wrong SLTS result"
        assert dut.o_rd.value.binstr == '{:06b}'.format(i_rd), "Wrong register being written"
        assert dut.o_wr.value.binstr == "1", "SLTS is supported to write register"
        await RisingEdge(dut.i_clk)

@cocotb.test()
async def test_sltu(dut):
    clock = Clock(dut.i_clk, 10, units="us") # 10us period clock
    cocotb.fork(clock.start())
    dut.i_clk.value = 0b0
    dut.i_rst.value = 0b0
    dut.i_en.value = 0b1

    for i in range(100):
        dut.i_function.value = 0b1010 # SLTU
        dut.i_inv_c.value = 0b1
        i_b = int(random.random()*2**32)
        dut.i_b.value = i_b
        i_c = int(random.random()*2**32)
        dut.i_c.value = i_c
        i_rd = int(random.random()*2**6)
        dut.i_rd.value = i_rd
        await RisingEdge(dut.i_clk)
        assert dut.o_val.value.binstr == '{:032b}'.format(i_b<i_c), "Wrong SLTU result"
        assert dut.o_rd.value.binstr == '{:06b}'.format(i_rd), "Wrong register being written"
        assert dut.o_wr.value.binstr == "1", "SLTU is supported to write register"
        await RisingEdge(dut.i_clk)

@cocotb.test()
async def test_sub(dut):
    clock = Clock(dut.i_clk, 10, units="us") # 10us period clock
    cocotb.fork(clock.start())
    dut.i_clk.value = 0b0
    dut.i_rst.value = 0b0
    dut.i_en.value = 0b1

    # SUB
    for i in range(100):
        dut.i_function.value = 0b0000 # ADD
        dut.i_inv_c.value = 0b1 # invert c (makes it -c)
        i_b = int(random.random()*2**32)
        dut.i_b.value = i_b
        i_c = int(random.random()*2**32)
        dut.i_c.value = i_c
        i_rd = int(random.random()*2**6)
        dut.i_rd.value = i_rd
        await RisingEdge(dut.i_clk)

        assert dut.o_val.value.binstr == '{:032b}'.format((i_b-i_c)%2**32), "Wrong SUB (unsigned) result"
        assert dut.o_rd.value.binstr == '{:06b}'.format(i_rd), "Wrong register being written"
        assert dut.o_wr.value.binstr == "1", "SUB is supported to write register"
        await RisingEdge(dut.i_clk)


@cocotb.test()
async def test_add(dut):
    clock = Clock(dut.i_clk, 10, units="us") # 10us period clock
    cocotb.fork(clock.start())
    dut.i_clk.value = 0b0
    dut.i_rst.value = 0b0
    dut.i_en.value = 0b1

    # ADD
    for i in range(100):
        dut.i_function.value = 0b0000 # ADD
        dut.i_inv_c.value = 0b0
        i_b = int(random.random()*2**32)
        dut.i_b.value = i_b
        i_c = int(random.random()*2**32)
        dut.i_c.value = i_c
        i_rd = int(random.random()*2**6)
        dut.i_rd.value = i_rd
        await RisingEdge(dut.i_clk)

        assert dut.o_val.value.binstr == '{:032b}'.format((i_b+i_c)%2**32), "Wrong ADD (unsigned) result"
        assert dut.o_rd.value.binstr == '{:06b}'.format(i_rd), "Wrong register being written"
        assert dut.o_wr.value.binstr == "1", "ADD is supported to write register"
        await RisingEdge(dut.i_clk)


