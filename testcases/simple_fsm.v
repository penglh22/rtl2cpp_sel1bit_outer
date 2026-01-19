module simple_fsm (
    input  wire clk,
    input  wire rst,
    input  wire in,
    output reg  [1:0] out,
    output reg  outn
);

    always @(posedge clk) begin
        if (rst) begin
            out[0] <= 1'b0;
            out[1] <= 1'b0;
            outn <= 1'b0;
        end else begin
            out[0] <= in ^ out[0];
            out[1] <= ~in ^ out[1];
            outn <= ~(in ^ out[0]);
        end
    end
endmodule
