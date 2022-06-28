`timescale 100ps/100ps

module dummy_icache #(
    parameter ADDRESS_LENGTH = 30,
    parameter INSTR_LENGTH = 32, // Length of a sinrle instruction

    // How many bits of data can this module can get from the MEM interface at
    // once. It should we a multiple of INSTR_LENGTH
    parameter WRITE_LANE = 32
) (
    input logic i_clk,
    input logic i_rst,

    input logic i_if_brch,
    input logic [ADDRESS_LENGTH-1:0] i_if_brch_addr,
    input logic i_if_ready,
    output logic o_if_instr_valid,
    output logic [INSTR_LENGTH-1:0] o_if_instr0,
    output logic [INSTR_LENGTH-1:0] o_if_instr1,

    output logic [ADDRESS_LENGTH-1:0] o_mem_req_addr,
    output logic o_mem_req_ready, // This module is requesting a line to the main memory
    input logic i_mem_data_valid, // must stay valid for 1 cycle
    input logic i_mem_addr_valid, // unsupported [1]
    input logic [WRITE_LANE-1:0] i_mem_bus
);
typedef enum logic[1:0] {ST_IDLE, ST_INSTR0, ST_INSTR1} state_t;
logic is_idle;
logic pairing_bit_set; // Pairing bit is set
logic err_refill_unsupported; // This cache does not support refill
// at random addresses by the main memory controller [1]
logic error_pairing_bit_on_second_instr; // If the pairing bit was set a first
// instruction it should not be set on the second instruction too, this cache
// only supports dual issue [2]

state_t state_d, state_q;

logic [ADDRESS_LENGTH-1:0] int_addr_q;
logic [ADDRESS_LENGTH-1:0] int_addr_d;
logic int_addr_en;
always_ff @ (posedge i_clk or posedge i_rst) begin
    if (i_rst == 1'b1) int_addr_q <= {ADDRESS_LENGTH{1'b0}};
    else if (int_addr_en) int_addr_q <= int_addr_d;
end

logic mem_data_valid_q;
always_ff @ (posedge i_clk or posedge i_rst) begin
    if (i_rst == 1'b1) mem_data_valid_q <= 1'b0;
    else mem_data_valid_q <= i_mem_data_valid;
end

// We update the requested address (o_mem_req_addr) when we get the response
// from the last request
assign int_addr_en = is_idle | i_mem_data_valid;
assign is_idle = (state_q == ST_IDLE)? 1'b1: 1'b0;

always_comb begin
    if (i_if_brch == 1'b1 && pairing_bit_set == 1'b0 /* [3] */) int_addr_d = i_if_brch_addr;
    // [3] Special case exercised by seed 1656440283: It this module returns
    // an instruction instr_A from address A which contains a branch (jump)
    // to address B. The next fetch will be address A+1 and only the after
    // the instruction at address B will be fetched.
    // If the instruction at address A+1 has its pairing bit set this module
    // is expected to return 2 instructions (from address A+1 and A+2) before
    // jumping to address B.

    // Auto-increment the next address to request
    else if (~is_idle) int_addr_d = int_addr_q + 1;
    else int_addr_d = int_addr_q;
end

logic state_d_idle;
assign state_d_idle = (state_d == ST_IDLE)? 1: 0;
assign o_mem_req_ready = ~state_d_idle & ~i_mem_data_valid;

// Requesting address to MEM as soon as the last request returns
assign o_mem_req_addr = (i_mem_data_valid == 1 && mem_data_valid_q == 0)? int_addr_d : int_addr_q;

assign err_refill_unsupported = i_mem_addr_valid; // [1]

logic state_instr1_d;
logic state_instr1_q;
assign state_instr1_d = (state_q == ST_INSTR1)? 1'b1: 1'b0;
always_ff @ (posedge i_clk) begin
    if (i_rst == 1'b1) state_instr1_q <= 1'b0;
    else state_instr1_q <= state_instr1_d;
end

// TODO o_if_instr_valid should not be set if i_if_ready == 0
always_comb begin
    unique case (state_q)
        // Data returned from main memory and no pairing bit -> we can
        // return a single instruction
        ST_INSTR0 : o_if_instr_valid = i_mem_data_valid
                                                & ~i_mem_bus[INSTR_LENGTH-1];
        // Data returned from main memory, we have been in ST_INSTR1 for more
        // than 1 cycle -> This has to be the second instruction
        // we can return both instruction to the CPU IF
        ST_INSTR1 : o_if_instr_valid = i_mem_data_valid & state_instr1_q;
        default : o_if_instr_valid = 0;
    endcase
end
assign error_pairing_bit_on_second_instr = state_q == ST_INSTR1 // [2]
                                       && i_mem_data_valid == 1'b1
                                       && i_mem_bus[INSTR_LENGTH-1] == 1;


logic [INSTR_LENGTH-1:0] int_instr; // Internal cached instruction

// No reset required, won't be used before initilization
always_ff @ (posedge i_clk) begin
    if (state_d == ST_INSTR1 && state_q == ST_INSTR0) int_instr <= i_mem_bus;
end
assign o_if_instr0 = (state_q == ST_INSTR1)? int_instr : i_mem_bus;
assign o_if_instr1 = (state_q == ST_INSTR1)? i_mem_bus : {INSTR_LENGTH{1'b0}};

always_ff @ (posedge i_clk or posedge i_rst) begin
    if (i_rst == 1'b1) state_q <= ST_IDLE; // Initial state
    else               state_q <= state_d;
end
// State transistion: Next state
always_comb begin
    unique case (state_q)
        ST_INSTR0 : begin
                if (i_mem_data_valid == 1'b1 && i_if_ready == 1'b1
                                       && pairing_bit_set == 1'b1) begin
                    // Received instruction from main memory, cpu is ready
                    // and pairing bit is set
                    state_d = ST_INSTR1;
                end else begin
                    // Stay in ST_INSTR0
                    // if we are still waiting for an instruction from main
                    // memory. Or if we got the last instruction's pairing bit
                    // was not set. Or if the cpu's instruction fetch stage
                    // is not ready to consume the instruction
                    state_d = ST_INSTR0;
                end
            end
        ST_INSTR1 : begin
                if (i_mem_data_valid == 1'b1 && i_if_ready == 1'b1) state_d = ST_INSTR0;
                // If cpu's instruction fetch stage is not ready or if we
                // are still waiting for the main memory to return an
                // instruction we stay in ST_INSTR1
                else state_d = ST_INSTR1;
            end
        default : begin
                if (i_if_ready ==  1'b1) state_d = ST_INSTR0;
                else state_d = ST_IDLE;
            end
    endcase
end
assign pairing_bit_set = i_mem_bus[INSTR_LENGTH-1];

initial begin
  $dumpfile ("trace.vcd");
  $dumpvars;
  #1;
end

endmodule

// TODO: Formal
// TODO: Coverage / verilator: https://docs.cocotb.org/en/stable/simulator_support.html
