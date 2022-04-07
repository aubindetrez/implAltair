export COCOTB_REDUCED_LOG_FMT=1
SIM = icarus
TOPLEVEL_LANG = verilog
VERILOG_SOURCES = $(shell pwd)/../../src/alu.v
TOPLEVEL = ALU 
MODULE = test_alu

include $(shell cocotb-config --makefiles)/Makefile.sim

clean_all: clean
	rm -rf __pycache__ results.xml
