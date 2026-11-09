# Benchmarks

Per call overhead and data transfer speed of the remotebmi client and server implementations:

- **current**: `RemoteBmiClient` (httpx) with `binary_values=True` and keep-alive enabled,
  against `run-bmi-server` (connexion).
- **lean Python**: `LeanBmiClient` (http.client) against `run-lean-bmi-server` (plain ASGI app on uvicorn).
- **Rust**: `LeanBmiClient(transport="rust")` against the Rust server, both from the [remotebmi_rs](../../rust) package.
- **grpc4bmi**: [grpc4bmi](https://github.com/eWaterCycle/grpc4bmi) 0.5 as baseline.

The model does no work, so all measured time is overhead.
Each server runs in its own process on localhost, the client in the benchmark process.

```shell
pip install -e .[dev] uvloop httptools grpc4bmi
pip install ../rust  # optional, needs Rust toolchain
python benchmarks/benchmark.py --json results.json --markdown results.md
python benchmarks/benchmark.py --report results.json  # report from earlier results
```

grpc4bmi does not work on Python 3.14, so these results are from Python 3.12.

## Results

On an AMD Ryzen 7 7700 (8 cores, 16 threads) with Linux, uvicorn using uvloop and httptools.

### Per call overhead (get_var_grid)

| Stack | Time per call | Speedup vs current |
|---|---:|---:|
| direct model call (no remotebmi) | 0.03 µs |  |
| Dispatcher only (Python part of lean and Rust servers) | 1.1 µs |  |
| LeanBmiClient without network (Python part of lean client) | 1.1 µs |  |
| current: RemoteBmiClient (httpx) -> connexion | 392 µs | 1.0x |
| lean Python: LeanBmiClient (http.client) -> lean ASGI | 62 µs | 6.3x |
| LeanBmiClient (http.client) -> Rust server | 43 µs | 9.2x |
| LeanBmiClient (Rust transport) -> lean ASGI | 36 µs | 10.9x |
| Rust: LeanBmiClient (Rust transport) -> Rust server | 16 µs | 24.1x |
| grpc4bmi (baseline) | 143 µs | 2.7x |

### get_value of smooth float32 values, zstd level 1 compresses 1.32x

| Stack | 4 kB | 400 kB | 4 MB | 40 MB |
|---|---:|---:|---:|---:|
| current (httpx -> connexion) | 789 µs (0.0051 GB/s) | 1.01 ms (0.4 GB/s) | 4.64 ms (0.86 GB/s) | 72.65 ms (0.55 GB/s) |
| lean Python | 69 µs (0.058 GB/s) | 118 µs (3.4 GB/s) | 869 µs (4.6 GB/s) | 58.23 ms (0.69 GB/s) |
| lean Python + zstd | 90 µs (0.044 GB/s) | 581 µs (0.69 GB/s) | 6.38 ms (0.63 GB/s) | 124.77 ms (0.32 GB/s) |
| Rust | 19 µs (0.21 GB/s) | 72 µs (5.6 GB/s) | 593 µs (6.7 GB/s) | 12.05 ms (3.3 GB/s) |
| Rust + zstd | 33 µs (0.12 GB/s) | 487 µs (0.82 GB/s) | 5.78 ms (0.69 GB/s) | 87.49 ms (0.46 GB/s) |
| grpc4bmi | 341 µs (0.012 GB/s) | 14.66 ms (0.027 GB/s) | 154.51 ms (0.026 GB/s) |  |

### set_value of smooth float32 values, zstd level 1 compresses 1.32x

| Stack | 4 kB | 400 kB | 4 MB | 40 MB |
|---|---:|---:|---:|---:|
| current (httpx -> connexion) | 876 µs (0.0046 GB/s) | 1.03 ms (0.39 GB/s) | 4.04 ms (0.99 GB/s) | 62.47 ms (0.64 GB/s) |
| lean Python | 66 µs (0.06 GB/s) | 152 µs (2.6 GB/s) | 780 µs (5.1 GB/s) | 47.33 ms (0.85 GB/s) |
| lean Python + zstd | 88 µs (0.046 GB/s) | 611 µs (0.65 GB/s) | 6.63 ms (0.6 GB/s) | 126.81 ms (0.32 GB/s) |
| Rust | 17 µs (0.23 GB/s) | 67 µs (6 GB/s) | 569 µs (7 GB/s) | 21.86 ms (1.8 GB/s) |
| Rust + zstd | 29 µs (0.14 GB/s) | 526 µs (0.76 GB/s) | 5.84 ms (0.69 GB/s) | 81.26 ms (0.49 GB/s) |
| grpc4bmi | 339 µs (0.012 GB/s) | 14.93 ms (0.027 GB/s) | 153.42 ms (0.026 GB/s) |  |

### get_value of sparse float32 values, zstd level 1 compresses 2.75x

| Stack | 4 kB | 400 kB | 4 MB | 40 MB |
|---|---:|---:|---:|---:|
| current (httpx -> connexion) | 815 µs (0.0049 GB/s) | 1.00 ms (0.4 GB/s) | 3.03 ms (1.3 GB/s) | 68.28 ms (0.59 GB/s) |
| lean Python | 68 µs (0.059 GB/s) | 117 µs (3.4 GB/s) | 741 µs (5.4 GB/s) | 59.47 ms (0.67 GB/s) |
| lean Python + zstd | 94 µs (0.043 GB/s) | 1.13 ms (0.35 GB/s) | 10.93 ms (0.37 GB/s) | 133.53 ms (0.3 GB/s) |
| Rust | 18 µs (0.23 GB/s) | 71 µs (5.6 GB/s) | 571 µs (7 GB/s) | 10.96 ms (3.7 GB/s) |
| Rust + zstd | 30 µs (0.13 GB/s) | 1.04 ms (0.38 GB/s) | 10.43 ms (0.38 GB/s) | 126.28 ms (0.32 GB/s) |
| grpc4bmi | 338 µs (0.012 GB/s) | 14.37 ms (0.028 GB/s) | 150.41 ms (0.027 GB/s) |  |

### set_value of sparse float32 values, zstd level 1 compresses 2.75x

| Stack | 4 kB | 400 kB | 4 MB | 40 MB |
|---|---:|---:|---:|---:|
| current (httpx -> connexion) | 895 µs (0.0045 GB/s) | 1.02 ms (0.39 GB/s) | 2.04 ms (2 GB/s) | 70.89 ms (0.56 GB/s) |
| lean Python | 65 µs (0.061 GB/s) | 155 µs (2.6 GB/s) | 779 µs (5.1 GB/s) | 47.53 ms (0.84 GB/s) |
| lean Python + zstd | 91 µs (0.044 GB/s) | 1.58 ms (0.25 GB/s) | 11.11 ms (0.36 GB/s) | 146.18 ms (0.27 GB/s) |
| Rust | 18 µs (0.23 GB/s) | 67 µs (6 GB/s) | 613 µs (6.5 GB/s) | 20.87 ms (1.9 GB/s) |
| Rust + zstd | 33 µs (0.12 GB/s) | 1.06 ms (0.38 GB/s) | 10.88 ms (0.37 GB/s) | 128.63 ms (0.31 GB/s) |
| grpc4bmi | 339 µs (0.012 GB/s) | 14.55 ms (0.027 GB/s) | 152.61 ms (0.026 GB/s) |  |

- smooth: zstd costs 75.44 ms for 40 MB and saves 9 MB, so pays off on links slower than about 1022 Mbit/s.
- sparse: zstd costs 115.33 ms for 40 MB and saves 25 MB, so pays off on links slower than about 1765 Mbit/s.

## Observations

- Most overhead of the current stack is in connexion (request validation, routing) and httpx,
  not in Python itself: the Python parts of the lean client and the dispatcher in
  the lean and Rust servers take about 1 µs each.
- The Rust stack is about 2 µs slower than a bare TCP ping-pong between two Python processes
  on the same machine (about 12 µs).
- grpc4bmi sends values as a list of numbers in protobuf which is slow for large arrays,
  and its `set_value` fails above the 4 MiB gRPC message limit, hence the missing 40 MB column.
- zstd level 1 compresses float32 model output 1.3x (smooth fields) to 2.8x (70% zeros),
  but compressing and decompressing takes longer than transferring the raw bytes on localhost.
  Only enable `LeanBmiClient(compress=True)` for slow networks.
