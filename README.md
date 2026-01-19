# File Structure

```
rtl2aig/
├─ testcases/                 
│   └─ simple_fsm.v
├─ openroad/                
│   └─ dff2ff.v
├─ wrappers/                  
├─ aags/                      
├─ cpp/                       # Final generated C++ file output directory
├─ wrapper.py                 
├─ rtl_to_aag.py              
├─ aag_to_cpp.py              
├─ rtl2cpp_1bitsel.py         # Automation script that calls wrapper + rtl_to_aag + aag_to_cpp
└─ README.md                  
```

# Run

command:

```
python3 rtl2cpp_1bitsel.py <verilog_file> --clk_name <clk> --rst_name <rst> [--wrapper_prefix <prefix>] [--output_dir <dir>] [--aag_dir <dir>] [--cpp_dir <dir>] [--clean]
```

| Parameter          | Description                                                  |
| ------------------ | ------------------------------------------------------------ |
| `<verilog_file>`   | Path to the original Verilog module, e.g., `testcases/simple_fsm.v`     |
| `--clk_name`       | Name of the clock signal, e.g., `clk`                             |
| `--rst_name`       | Name of the reset signal, e.g., `rst`                             |
| `--wrapper_prefix` | Prefix for the generated wrapper modules, default is `top`                           |
| `--output_dir`     | Directory to store generated wrapper files, default is `./wrappers`                 |
| `--aag_dir`        | Directory for intermediate AAG files, default is `./aags`                         |
| `--cpp_dir`        | Directory for final C++ output files, default is `./cpp`                                                                |
| `--clean`          | If specified, intermediate files (wrapper and AAG) will be deleted after generating C++ files       |



# Test

```
python3 rtl2cpp_1bitsel.py testcases/simple_fsm.v --clk_name clk --rst_name rst --clean
```