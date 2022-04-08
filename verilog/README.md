# Verilog hardware model

The hardware description is in [src/](src/)


The documentation for each module is in [doc/README.md](doc/README.md)


The verification for each module is in [verif/](verif/)

## How to contribute/what to learn
Install (see [contributor_dependencies.sh](contributor_dependencies.sh) for debian/ubuntu systems):
 - Dependency: python3 and python-dev-tools <https://www.python.org/downloads/>
 - Simulation: iverilog and/or verilator <http://iverilog.icarus.com>
 - Simulation: cocotb <https://github.com/cocotb/cocotb>
 - Synthesis: yosys <https://github.com/YosysHQ/yosys>
 - Static Timing analysis: opensta <http://opensta.org>
 - SystemVerilog to Verilog: sv2v <https://github.com/zachjs/sv2v.git>
 - Linter and formatter: verible <https://github.com/chipsalliance/verible>
 - Optional: Check [verif/README.md](verif/README.md) for a docker alternative.

You need basic knowledge in:
 - Writing python scripts
 - Computer architecture (Computer Architecture: A Quantitative Approach by John L. Hennessy, David A. Patterson, Krste Asanovi)
 - Basic SystemVerilog/Verilog RTL design <http://www.asic-world.com/verilog/veritut.html>
 - Logical effort <http://bwrcs.eecs.berkeley.edu/Classes/icdesign/ee141_f05/Lectures/Notes/ComputingLogicalEffort.pdf>
 - General VLSI design (CMOS VLSI Design: A Circuits and Systems Perspective by Neil Weste, David Harris)
 - Understand how synthesis works and be aware of it when writing RTL
 - Basic understanding of Static Timing Analysis
 - Read open source code to get familiar with it (example: <https://github.com/lowRISC/ibex>)
 - What subset of SystemVerilog is **synthesizable**.
 - How do we initialize registers and bringup a chip in a known state
 - Clock Gating / Data Gating

How to contribute:
 - Write testbench in [verif/](verif/) (create a unique directory for every verilog file)
 - Write your design in [src/](src/)
 - Optional: You can use formal verification (using yosys)
 - Optional: You can also use simple SystemVerilog testbenches (cf [tools/simu](tools/simu) )
 - Optional: You can synthetize your design in And Inverter Graph (cf [tools/synth_aig](tools/synth_aig) )
 - Optional: You can synthetize your design for 130/45/15/7nm and run Static Timing Analysis on it (cf [tools/synth_sky130](tools/synth_sky130) [tools/synth_ng45](tools/synth_ng45) )
 - Optional: You can synthetize your design for FPGA (cf [tools/synth_xil](tools/synth_xil) )
 - Optional: You can try your design on an actual FPGA
 - Optional: You can use OpenLane to check how it would perform on 130nm <https://github.com/The-OpenROAD-Project/OpenLane>
 - Use Linter to check your code: 
```
verible-verilog-lint <path to .sv file> --autofix inplace-interactive
# More information about the warnings here: https://chipsalliance.github.io/verible/lint.html
```
 - Format your code (even if your code is already well formated, it helps if everyone is using the same formatter):
```
verible-verilog-format <path to .sv file>
```
 - Write documentation in [doc/](doc/)

## Interactive block diagram

```
TODO using mermaid
```

## Verilog coding guideline

In order to be compatible with opensource EDA tools (yosys, iverilog, verilator...)
We program using SystemVerilog and convert it to Verilog using `sv2v`.
```
// Only use comments with "//" do not use "/* ... */"
    // Only indent with spaces, no tabulation because of some weird
    // with propriatory tools

module <MODULE'S NAME> #(
    parameter integer <PARAMETER'S NAME> = ... // only use [A-Z_0-9] for constant's names
) (
    input logic <INPUT'S NAME>,
    output logic <INPUT'S NAME>
);

logic [<SIZE>-1:0] <WIRE'S NAME>; // use little endian for packed arrays
logic <WIRE'S NAME> [<SIZE>-1]; // use big endian for unpacked arrays

// use "assign" statements (with blocking '=') for combinational logic
assign <SOME WIRE> = <...>;

// if using assign is unpractical use combinational blocks
always_comb
begin
    // Only use blocking statements
    a = b; // Such a simple assigment should use "assign"
end

always_ff
begin
    // do not use casex and prefer case inside over casez
    unique case inside (select)
        2b'00: e = 1'b0;
        2b'01: e = ...;
        default: e = ...; // set defaults even if not required
    endcase
end

// always name your "generate" (if / for...) statements

assign big_bit_vector[7:0] = {4'b0000, smaller_vector[3:0]}; // be explicit

assign counter[3:0] = 4'(counter_q + 4'b1); // explicitely discard the carry

// Write a testcase using cocotb in verification/<MODULE'S NAME> for every module
// At least check you can synthetise using yosys (default "synth" or AIG)
```
