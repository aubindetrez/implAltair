export COCOTB_REDUCED_LOG_FMT=1
export SIM = icarus
export TOPLEVEL_LANG = verilog
export VERILOG_SOURCES = $(shell pwd)/dummy_icache.v
export SVERILOG_SOURCES = $(shell pwd)/../../src/dummy_icache.sv
export TOPLEVEL = dummy_icache
export MODULE = test_dummy_icache

include $(shell cocotb-config --makefiles)/Makefile.sim

# Convert systemVerilog to verilog
${VERILOG_SOURCES}: ${SVERILOG_SOURCES}
	$(shell pwd)/../../tools/convert_sv ${SVERILOG_SOURCES} ${VERILOG_SOURCES}

clean_all: clean
	rm -rf __pycache__ results.xml *.v # Clean generated files
