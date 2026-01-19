import os
import re
import argparse

def parse_port(port_str):
    port_str = port_str.strip()
    vec_match = re.match(r"\[(\d+)\s*:\s*(\d+)\]\s*(\w+)", port_str)
    if vec_match:
        msb = int(vec_match.group(1))
        lsb = int(vec_match.group(2))
        name = vec_match.group(3)
        width = abs(msb - lsb) + 1
        return name, width
    else:
        return port_str, 1

def generate_bit_wrappers(verilog_path, output_dir, top_prefix="top"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(verilog_path, "r") as f:
        code = f.read()

    module_match = re.search(r"module\s+(\w+)\s*\((.*?)\)\s*;", code, re.S)
    if not module_match:
        raise Exception("Cannot find module definition in the file.")
    module_name = module_match.group(1)
    port_list_str = module_match.group(2)

    ports = [p.strip() for p in port_list_str.split(",")]
    inputs = []
    outputs = []

    for p in ports:
        if p.startswith("input"):
            name, width = parse_port(p.replace("input", "").replace("wire","").strip())
            inputs.append((name, width))
        elif p.startswith("output"):
            name, width = parse_port(p.replace("output", "").replace("wire","").replace("reg","").strip())
            outputs.append((name, width))

    if not outputs:
        raise Exception("No output ports found.")

    wrapper_idx = 0
    for out_name, out_width in outputs:
        for bit_idx in range(out_width):
            top_name = f"{top_prefix}{wrapper_idx}"
            wrapper_file = os.path.join(output_dir, f"{top_name}.v")
            with open(wrapper_file, "w") as wf:
                # 写模块头
                wf.write(f"module {top_name}(\n")
                for i, (inp_name, inp_width) in enumerate(inputs):
                    comma = "," if i < len(inputs) - 1 or out_width > 0 else ""
                    if inp_width == 1:
                        wf.write(f"    input wire {inp_name}{comma}\n")
                    else:
                        wf.write(f"    input wire [{inp_width-1}:0] {inp_name}{comma}\n")
                # 输出单 bit
                wf.write(f"    output wire {out_name}_{bit_idx}\n")
                wf.write(");\n\n")

                # 对多bit输出定义中间信号
                if out_width > 1:
                    wf.write(f"    wire [{out_width-1}:0] tmp_{out_name};\n\n")
                    wrapper_output = f"tmp_{out_name}[{bit_idx}]"
                else:
                    wrapper_output = out_name

                # 实例化原模块
                wf.write(f"{module_name} leaftest (\n")
                for inp_name, _ in inputs:
                    wf.write(f"    .{inp_name}({inp_name}),\n")
                for o_idx, (o_name, o_width) in enumerate(outputs):
                    if o_name == out_name:
                        if o_width > 1:
                            wf.write(f"    .{o_name}(tmp_{o_name}),\n")
                        else:
                            wf.write(f"    .{o_name}({o_name}),\n")
                    else:
                        if o_width > 1:
                            wf.write(f"    .{o_name}(),\n")
                        else:
                            wf.write(f"    .{o_name}(),\n")
                wf.write(");\n\n")

                # 中间信号对应 bit 赋值给输出
                wf.write(f"    assign {out_name}_{bit_idx} = {wrapper_output};\n\n")
                wf.write("endmodule\n")

            print(f"Generated wrapper: {wrapper_file}")
            wrapper_idx += 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Verilog wrappers for each output bit.")
    parser.add_argument("verilog_file", type=str, help="Path to original Verilog file")
    parser.add_argument("output_dir", type=str, help="Directory to store generated wrapper files")
    parser.add_argument("--prefix", type=str, default="top", help="Prefix for wrapper module names")
    args = parser.parse_args()

    generate_bit_wrappers(args.verilog_file, args.output_dir, top_prefix=args.prefix)
