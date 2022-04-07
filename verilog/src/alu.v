// Parametric Arithmetic Logic Unit

`define FUNC_ADD_SUB 5'b0000
`define FUNC_XOR 5'b1000
`define FUNC_OR 5'b0100
`define FUNC_AND 5'b0010
`define FUNC_LSL 5'b1010
`define FUNC_ASR 5'b0110
`define FUNC_LSR 5'b1110

`define FUNC_SLTS 5'b0010
`define FUNC_SLTU 5'b1010
`define FUNC_MOVE 5'b1101
`define FUNC_SMOVE 5'b1101

module ALU (
	input wire i_clk,
	input wire i_rst,
	input wire i_en,

	input wire [3:0] i_function,
	input wire i_inv_c, // make c = -c
	input wire i_use_imm,
	input wire [31:0] i_b,
	input wire [31:0] i_c,
	input wire [31:0] i_imm, // properly extended immediate value
	input wire [5:0] i_rd,

	output wire [5:0] o_rd, // destination register
	output wire [31:0] o_val, // value to write to the destination
	output wire o_wr // 1'b1 to write o_val to register o_rd
);

wire is_func_add;
wire [31:0] inv_c;
wire [31:0] result_sum;
wire carry_sum;
wire sum_carry_sign;

wire cmp_lts;
wire cmp_ltu;

// No need to use c_mux here because we do not have a sltsi instruction
// but it saves resources
assign cmp_lts = (i_b[31] != c_mux[31]) ? i_b[31] : (i_b[31]!=sum_carry_sign);
assign cmp_ltu = !carry_sum;

assign c_mux = i_use_imm ? i_imm : i_c;
assign inv_c = i_inv_c ? (~c_mux)+1 : c_mux;
assign {carry_sum, result_sum} = i_b + inv_c;
assign sum_carry_sign = result_sum[31];

assign o_rd = i_rd;

assign o_val = (i_function == `FUNC_ADD_SUB) ? result_sum :
	(i_function == `FUNC_SLTS) ? cmp_lts:
	(i_function == `FUNC_SLTU) ? cmp_ltu:
	(i_function == `FUNC_XOR) ? i_b ^ i_c:
	(i_function == `FUNC_OR) ? i_b | i_c:
	(i_function == `FUNC_AND) ? i_b & i_c:
	(i_function == `FUNC_MOVE) ? i_c : // Used for MOVI, i_c = imm
	(i_function == `FUNC_SMOVE) ? {i_c[15:0], i_b[15:0]}: // SMOVE: i_c = imm, i_b = rA
	32'b0;

assign o_wr = i_en;
	
endmodule

