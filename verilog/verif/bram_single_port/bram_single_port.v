module bram_single_port (
	clk,
	wr,
	addr,
	din,
	dout
);
	parameter integer DATASIZE = 32;
	parameter integer ADDRSIZE = 10;
	input wire clk;
	input wire wr;
	input wire [ADDRSIZE - 1:0] addr;
	input wire [DATASIZE - 1:0] din;
	output reg [DATASIZE - 1:0] dout;
	reg [DATASIZE - 1:0] mem [0:(2 ** ADDRSIZE) - 2];
	always @(posedge clk)
		if (wr) begin
			dout <= din;
			mem[addr] <= din;
		end
		else
			dout <= mem[addr];
endmodule
