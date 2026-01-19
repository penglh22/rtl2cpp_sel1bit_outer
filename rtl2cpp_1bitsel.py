import os
import glob
import argparse
import subprocess
import shutil

def run_pipeline(
    verilog_file,
    output_dir,
    wrapper_prefix,
    clk_name,
    rst_name,
    aag_dir,
    cpp_dir,
    clean_intermediate=False
):
    # 调用 wrapper 脚本
    wrapper_cmd = [
        "python3",
        "wrapper.py",
        verilog_file,
        output_dir,
        "--prefix",
        wrapper_prefix
    ]
    print("Running wrapper script...")
    subprocess.run(wrapper_cmd, check=True)

    # 遍历
    wrapper_files = sorted(glob.glob(os.path.join(output_dir, f"{wrapper_prefix}*.v")))

    if not os.path.exists(aag_dir):
        os.makedirs(aag_dir)
    if not os.path.exists(cpp_dir):
        os.makedirs(cpp_dir)

    for idx, wfile in enumerate(wrapper_files):
        aag_file = os.path.join(aag_dir, f"{wrapper_prefix}_{idx}.aag")
        cpp_file = os.path.join(cpp_dir, f"io_generater_outer_{idx}.h")

        # 运行 rtl_to_aag.py
        rtl_to_aag_cmd = [
            "python3",
            "rtl_to_aag.py",
            "--rtl_path",
            f"{wfile} {verilog_file}",
            "--clk_name",
            clk_name,
            "--rst_name",
            rst_name,
            "--top_name",
            os.path.splitext(os.path.basename(wfile))[0],
            "--aag_path",
            aag_file
        ]

        print(f"Running rtl_to_aag for {wfile}...")
        subprocess.run(rtl_to_aag_cmd, check=True)

        # 运行 aag_to_cpp.py
        aag_to_cpp_cmd = [
            "python3",
            "aag_to_cpp.py",
            "--aag_path",
            aag_file,
            "--cpp_path",
            cpp_file,
            "--ignore"
        ]
        print(f"Running aag_to_cpp for {aag_file}...")
        subprocess.run(aag_to_cpp_cmd, check=True)

    # 删除中间文件（可选）
    if clean_intermediate:
        print("Cleaning intermediate files...")
        shutil.rmtree(output_dir)
        shutil.rmtree(aag_dir)

    print("All finished. CPP files are in:", cpp_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run full RTL->AAG->CPP pipeline for each output bit.")
    parser.add_argument("verilog_file", type=str, help="Path to original Verilog file")
    parser.add_argument("--wrapper_prefix", type=str, default="top", help="Prefix for wrapper modules")
    parser.add_argument("--clk_name", type=str, required=True, help="Clock signal name")
    parser.add_argument("--rst_name", type=str, required=True, help="Reset signal name")
    parser.add_argument("--output_dir", type=str, default="./wrappers", help="Directory for intermediate wrapper Verilog files")
    parser.add_argument("--aag_dir", type=str, default="./aags", help="Directory for intermediate AAG files")
    parser.add_argument("--cpp_dir", type=str, default="./cpp", help="Directory for final CPP files")
    parser.add_argument("--clean", action="store_true", help="Delete intermediate files, keep only final CPP files")
    args = parser.parse_args()

    run_pipeline(
        args.verilog_file,
        args.output_dir,
        args.wrapper_prefix,
        args.clk_name,
        args.rst_name,
        args.aag_dir,
        args.cpp_dir,
        clean_intermediate=args.clean
    )
