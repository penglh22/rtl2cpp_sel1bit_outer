module top2(
    input wire clk,
    input wire rst,
    input wire in,
    output wire outn_0
);

simple_fsm leaftest (
    .clk(clk),
    .rst(rst),
    .in(in),
    .out(),
    .outn(outn),
);

    assign outn_0 = outn;

endmodule
