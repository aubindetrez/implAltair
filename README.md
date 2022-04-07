# implAltair
GNU Implementation of the Altair ISA

AltairX ISA, emulator and overview: https://github.com/Kannagi/AltairX

## Status
This is a work in progress, no working prototype available yet.
Contributions are welcome.

## TODOs
 - Create a release/tag for the ISA
 - Instruction cache ('dummy' version)
 - Instruction cache 4-way set-associative 64KB
 - Floating point division - Shift-and-subtract division algorithm
 - Floating point division - Sweeney, Robertson and Tocher algorithm
 - Multicore cache coherence modeling (High-level)
Write-through VS write back cache. Directory protocol?
 - Multicore cache coherence implementation - coherence controller (1 per core)
 - Multicore cache coherence testing
 - IO bus
 - GPU/accelerator bus
 - Benchmark: <https://github.com/embench/embench-iot>
 - Add compression in cache
 - Profile Guided Optimization (PGO) embedded in the compiler (using the hardware simulation)
 - (smart) Scan chain support
