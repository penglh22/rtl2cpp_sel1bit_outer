import os
import argparse


def rtl_to_aag(
    rtl_path: str,
    clock_name: str,
    rst_name: str,
    rstn_name: str,
    top_name: str,
    aag_path: str,
):
    if rst_name and rstn_name:
        raise ValueError("rst and rstn cannot be used together")

    yosys_command = f"read_verilog -sv {rtl_path}; setattr -unset always_comb p:*; prep {f'-top {top_name}' if top_name else '-auto-top'} -flatten; proc; zinit -all; async2sync; dffunmap; techmap -map openroad/dff2ff.v; delete */{clock_name}; opt_clean; {f'delete */{rst_name}; setundef -zero -undriven; ' if rst_name else f'delete */{rstn_name}; setundef -one -undriven; ' if rstn_name else ''}synth; aigmap; write_aiger -ascii {aag_path};"
    print(yosys_command)
    os.system('yosys -q -p "' + yosys_command + '"')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--rtl_path", required=True, help="path to rtl")
    parser.add_argument("--clk_name", required=True, help="name of clock")
    parser.add_argument("--rst_name", help="name of reset")
    parser.add_argument("--rstn_name", help="name of resetn")
    parser.add_argument(
        "--top_name", help="name of top module, if not specified, use yosys auto-top"
    )
    parser.add_argument("--aag_path", required=True, help="path to generated aag")
    args = parser.parse_args()
    if args.rst_name and args.rstn_name:
        raise ValueError("--rst_name and --rstn_name cannot be used together")

    rtl_to_aag(
        rtl_path=args.rtl_path,
        clock_name=args.clk_name,
        rst_name=args.rst_name,
        rstn_name=args.rstn_name,
        top_name=args.top_name,
        aag_path=args.aag_path,
    )


if __name__ == "__main__":
    main()
