module top0(
    input wire clk,
    input wire rst,
    input wire in,
    output wire out_0
);

    wire [1:0] tmp_out;

simple_fsm leaftest (
    .clk(clk),
    .rst(rst),
    .in(in),
    .out(tmp_out),
    .outn(),
);

    assign out_0 = tmp_out[0];

endmodule
