export COCOTB_REDUCED_LOG_FMT=1
export SIM = icarus
export TOPLEVEL_LANG = verilog
export VERILOG_SOURCES = $(shell pwd)/bram_single_port.v
export SVERILOG_SOURCES = $(shell pwd)/../../src/bram_single_port.sv
export TOPLEVEL = bram_single_port
export MODULE = test_bram_single_port

include $(shell cocotb-config --makefiles)/Makefile.sim

# Convert systemVerilog to verilog
${VERILOG_SOURCES}: ${SVERILOG_SOURCES}
	$(shell pwd)/../../tools/convert_sv ${SVERILOG_SOURCES} ${VERILOG_SOURCES}

clean_all: clean
	rm -rf __pycache__ results.xml
