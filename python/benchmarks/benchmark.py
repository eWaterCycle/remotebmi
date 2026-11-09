"""Benchmark per-call overhead and data transfer of remotebmi implementations.

Runs each server in a subprocess on localhost and calls it from this process.

Usage:

    python benchmarks/benchmark.py [--quick] [--json results.json] [--markdown results.md]

Optional implementations are skipped when not installed:
remotebmi_rs (Rust server and transport) and grpc4bmi (baseline).
"""

import argparse
import importlib.util
import json
import platform
import socket
import subprocess
import sys
import time
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from functools import partial
from pathlib import Path
from typing import Any

import numpy as np
from bmipy import Bmi

HERE = Path(__file__).parent
HAS_RUST = importlib.util.find_spec("remotebmi_rs") is not None


def _grpc4bmi_works() -> bool:
    # grpc4bmi pins an old protobuf which can not be imported on Python 3.14
    try:
        import grpc4bmi.bmi_grpc_client  # noqa: F401
    except Exception:  # noqa: BLE001
        return False
    return True


HAS_GRPC4BMI = _grpc4bmi_works()


def make_field(size: int, kind: str) -> np.ndarray:
    """Float32 test data.

    smooth: like temperature, smooth in space with small noise.
    sparse: like precipitation, 70% zeros.
    """
    rng = np.random.default_rng(42)
    if kind == "sparse":
        values = rng.gamma(2.0, 3.0, size)
        values[rng.random(size) < 0.7] = 0
        return values.astype(np.float32)
    side = int(np.ceil(np.sqrt(size)))
    y, x = np.mgrid[0:side, 0:side] / side
    field = 280 + 10 * np.sin(6 * x) * np.cos(4 * y) + rng.normal(0, 0.01, (side, side))
    result: np.ndarray = field.ravel()[:size].astype(np.float32)
    return result


class BenchModel(Bmi):
    """Model that does no work, so all measured time is overhead."""

    def __init__(self, size: int = 1000, kind: str = "smooth"):
        self.value = make_field(size, kind)

    def initialize(self, config_file: str) -> None:
        pass

    def update(self) -> None:
        pass

    def update_until(self, time: float) -> None:
        pass

    def finalize(self) -> None:
        pass

    def get_component_name(self) -> str:
        return "bench"

    def get_input_item_count(self) -> int:
        return 1

    def get_output_item_count(self) -> int:
        return 1

    def get_input_var_names(self) -> tuple[str]:
        return ("field",)

    def get_output_var_names(self) -> tuple[str]:
        return ("field",)

    def get_var_grid(self, name: str) -> int:
        return 0

    def get_var_type(self, name: str) -> str:
        return "float32"

    def get_var_units(self, name: str) -> str:
        return "K"

    def get_var_itemsize(self, name: str) -> int:
        return 4

    def get_var_nbytes(self, name: str) -> int:
        return int(self.value.nbytes)

    def get_var_location(self, name: str) -> str:
        return "node"

    def get_current_time(self) -> float:
        return 0.0

    def get_start_time(self) -> float:
        return 0.0

    def get_end_time(self) -> float:
        return 1.0

    def get_time_units(self) -> str:
        return "s"

    def get_time_step(self) -> float:
        return 1.0

    def get_value(self, name: str, dest: np.ndarray) -> np.ndarray:
        dest[:] = self.value
        return dest

    def get_value_ptr(self, name: str) -> np.ndarray:
        return self.value

    def get_value_at_indices(
        self, name: str, dest: np.ndarray, inds: np.ndarray
    ) -> np.ndarray:
        dest[:] = self.value[inds]
        return dest

    def set_value(self, name: str, src: np.ndarray) -> None:
        self.value[:] = src

    def set_value_at_indices(
        self, name: str, inds: np.ndarray, src: np.ndarray
    ) -> None:
        self.value[inds] = src

    def get_grid_rank(self, grid: int) -> int:
        return 1

    def get_grid_size(self, grid: int) -> int:
        return int(self.value.size)

    def get_grid_type(self, grid: int) -> str:
        return "unstructured"

    def get_grid_shape(self, grid: int, shape: np.ndarray) -> np.ndarray:
        return shape

    def get_grid_spacing(self, grid: int, spacing: np.ndarray) -> np.ndarray:
        return spacing

    def get_grid_origin(self, grid: int, origin: np.ndarray) -> np.ndarray:
        return origin

    def get_grid_x(self, grid: int, x: np.ndarray) -> np.ndarray:
        return x

    def get_grid_y(self, grid: int, y: np.ndarray) -> np.ndarray:
        return y

    def get_grid_z(self, grid: int, z: np.ndarray) -> np.ndarray:
        return z

    def get_grid_node_count(self, grid: int) -> int:
        return int(self.value.size)

    def get_grid_edge_count(self, grid: int) -> int:
        return 0

    def get_grid_face_count(self, grid: int) -> int:
        return 0

    def get_grid_edge_nodes(self, grid: int, edge_nodes: np.ndarray) -> np.ndarray:
        return edge_nodes

    def get_grid_face_edges(self, grid: int, face_edges: np.ndarray) -> np.ndarray:
        return face_edges

    def get_grid_face_nodes(self, grid: int, face_nodes: np.ndarray) -> np.ndarray:
        return face_nodes

    def get_grid_nodes_per_face(
        self, grid: int, nodes_per_face: np.ndarray
    ) -> np.ndarray:
        return nodes_per_face


def serve(implementation: str, port: int, size: int, kind: str) -> None:
    """Run in subprocess: serve BenchModel until killed."""
    model = BenchModel(size, kind)
    if implementation == "rust":
        from remotebmi.server.rust import serve_rust

        serve_rust(model, port=port)
    elif implementation == "grpc4bmi":
        from concurrent import futures

        import grpc
        from grpc4bmi import bmi_pb2_grpc
        from grpc4bmi.bmi_grpc_server import BmiServer

        # Same as grpc4bmi.run_server.serve
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        bmi_pb2_grpc.add_BmiServiceServicer_to_server(BmiServer(model), server)
        server.add_insecure_port(f"127.0.0.1:{port}")
        server.start()
        server.wait_for_termination()
    else:
        import uvicorn

        from remotebmi.server import make_app
        from remotebmi.server.lean import make_lean_app

        app = make_app(model) if implementation == "connexion" else make_lean_app(model)
        uvicorn.run(app, host="127.0.0.1", port=port, log_level="warning")


def free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return int(s.getsockname()[1])


@contextmanager
def server_process(implementation: str, size: int, kind: str) -> Iterator[int]:
    port = free_port()
    cmd = [
        sys.executable,
        __file__,
        "serve",
        implementation,
        str(port),
        str(size),
        kind,
    ]
    process = subprocess.Popen(cmd)
    try:
        for _ in range(600):
            try:
                socket.create_connection(("127.0.0.1", port), timeout=0.1).close()
                break
            except OSError:
                if process.poll() is not None:
                    msg = f"{implementation} server exited"
                    raise RuntimeError(msg) from None
                time.sleep(0.05)
        yield port
    finally:
        process.terminate()
        process.wait()


def make_client(name: str, port: int) -> Bmi:
    url = f"http://127.0.0.1:{port}"
    if name == "httpx":
        from remotebmi import RemoteBmiClient

        # Best case for current client, default has keep-alive and binary_values off
        return RemoteBmiClient(url, max_keepalive_connections=10, binary_values=True)
    if name == "grpc4bmi":
        import grpc
        from grpc4bmi.bmi_grpc_client import BmiClient

        return BmiClient(grpc.insecure_channel(f"127.0.0.1:{port}"))
    from remotebmi.client.lean import LeanBmiClient

    transport, _, compress = name.partition("+")
    return LeanBmiClient(url, transport=transport, compress=compress == "zstd")


# Client, server, label
STACKS = [
    ("httpx", "connexion", "current: RemoteBmiClient (httpx) -> connexion"),
    ("python", "lean", "lean Python: LeanBmiClient (http.client) -> lean ASGI"),
    ("python", "rust", "LeanBmiClient (http.client) -> Rust server"),
    ("rust", "lean", "LeanBmiClient (Rust transport) -> lean ASGI"),
    ("rust", "rust", "Rust: LeanBmiClient (Rust transport) -> Rust server"),
    ("grpc4bmi", "grpc4bmi", "grpc4bmi (baseline)"),
]


def available(client: str, server: str) -> bool:
    if "rust" in (client.partition("+")[0], server):
        return HAS_RUST
    if "grpc4bmi" in (client, server):
        return HAS_GRPC4BMI
    return True


def time_per_call(fn: Callable[[], Any], min_time: float, repeat: int = 5) -> float:
    """Best mean time per call in seconds over repeated batches."""
    fn()
    n = 1
    while True:
        start = time.perf_counter()
        for _ in range(n):
            fn()
        elapsed = time.perf_counter() - start
        if elapsed >= min_time / repeat:
            break
        n *= 2
    best = elapsed / n
    for _ in range(repeat - 1):
        start = time.perf_counter()
        for _ in range(n):
            fn()
        best = min(best, (time.perf_counter() - start) / n)
    return best


def bench_overhead(min_time: float) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    model = BenchModel()
    results.append(
        {
            "stack": "direct model call (no remotebmi)",
            "seconds": time_per_call(lambda: model.get_var_grid("field"), min_time),
        }
    )
    from remotebmi.server.lean import Dispatcher

    dispatch = Dispatcher(model)
    results.append(
        {
            "stack": "Dispatcher only (Python part of lean and Rust servers)",
            "seconds": time_per_call(
                lambda: dispatch("GET", "/get_var_grid/field", "", "", b""), min_time
            ),
        }
    )
    from remotebmi.client.lean import LeanBmiClient

    class CannedTransport:
        """Responds without network, to measure Python part of LeanBmiClient."""

        def request(self, *_: Any) -> tuple[int, str, str, str, bytes]:
            return 200, "application/json", "", "", b"0"

        def close(self) -> None:
            pass

    lean_client = LeanBmiClient("http://localhost", transport=CannedTransport())
    results.append(
        {
            "stack": "LeanBmiClient without network (Python part of lean client)",
            "seconds": time_per_call(
                lambda: lean_client.get_var_grid("field"), min_time
            ),
        }
    )
    for row in results:
        print(f"  {row['stack']:<60} {row['seconds'] * 1e6:8.1f} µs", flush=True)
    for client_name, server, label in STACKS:
        if not available(client_name, server):
            continue
        with server_process(server, 1000, "smooth") as port:
            client = make_client(client_name, port)
            seconds = time_per_call(partial(client.get_var_grid, "field"), min_time)
        results.append({"stack": label, "seconds": seconds})
        print(f"  {label:<60} {seconds * 1e6:8.1f} µs", flush=True)
    return results


def bench_transfer(
    sizes: list[int], kinds: list[str], min_time: float
) -> list[dict[str, Any]]:
    results = []
    transfer_stacks = [
        ("httpx", "connexion", "current (httpx -> connexion)"),
        ("python", "lean", "lean Python"),
        ("python+zstd", "lean", "lean Python + zstd"),
        ("rust", "rust", "Rust"),
        ("rust+zstd", "rust", "Rust + zstd"),
        ("grpc4bmi", "grpc4bmi", "grpc4bmi"),
    ]
    for kind in kinds:
        for size in sizes:
            for client_name, server, label in transfer_stacks:
                if not available(client_name, server):
                    continue
                if client_name == "grpc4bmi" and size * 4 > 4 * 1024 * 1024:
                    # set_value fails with RESOURCE_EXHAUSTED above 4 MiB message limit
                    continue
                with server_process(server, size, kind) as port:
                    client = make_client(client_name, port)
                    dest = np.empty(size, np.float32)
                    src = make_field(size, kind)
                    get = time_per_call(
                        partial(client.get_value, "field", dest), min_time
                    )
                    set_ = time_per_call(
                        partial(client.set_value, "field", src), min_time
                    )
                    np.testing.assert_array_equal(dest, src)
                row = {
                    "stack": label,
                    "kind": kind,
                    "size": size,
                    "bytes": size * 4,
                    "get_value_seconds": get,
                    "set_value_seconds": set_,
                }
                results.append(row)
                print(
                    f"  {kind:<6} {size:>9} {label:<30} get {get * 1e3:8.3f} ms"
                    f"  set {set_ * 1e3:8.3f} ms",
                    flush=True,
                )
    return results


def compression_ratios(sizes: list[int], kinds: list[str]) -> dict[str, float]:
    from remotebmi._http import zstd

    if zstd is None:
        return {}
    size = max(sizes)
    return {
        kind: len(make_field(size, kind).tobytes())
        / len(zstd.compress(make_field(size, kind).tobytes(), 1))
        for kind in kinds
    }


def environment() -> dict[str, Any]:
    from remotebmi._http import zstd

    def has(module: str) -> bool:
        return importlib.util.find_spec(module) is not None

    return {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "processor": platform.processor() or platform.machine(),
        "uvloop": has("uvloop"),
        "httptools": has("httptools"),
        "zstd": zstd is not None,
        "remotebmi_rs": HAS_RUST,
        "grpc4bmi": HAS_GRPC4BMI,
    }


def _size(nbytes: int) -> str:
    for unit in ("B", "kB", "MB", "GB"):
        if nbytes < 1000:
            return f"{nbytes:g} {unit}"
        nbytes //= 1000
    return f"{nbytes} TB"


def _duration(seconds: float) -> str:
    if seconds < 1e-6:
        return f"{seconds * 1e6:.2f} µs"
    if seconds < 1e-5:
        return f"{seconds * 1e6:.1f} µs"
    if seconds < 1e-3:
        return f"{seconds * 1e6:.0f} µs"
    return f"{seconds * 1e3:.2f} ms" if seconds < 1 else f"{seconds:.2f} s"


def markdown(results: dict[str, Any]) -> str:
    """Report results as markdown tables."""
    env = results["environment"]
    lines = [
        (
            f"Python {env['python']} on {env['platform']}, "
            f"uvloop={env['uvloop']}, httptools={env['httptools']}."
        ),
        "",
        "### Per call overhead (get_var_grid)",
        "",
        "| Stack | Time per call | Speedup vs current |",
        "|---|---:|---:|",
    ]
    overhead = results["overhead"]
    current = next(r["seconds"] for r in overhead if r["stack"].startswith("current"))
    for row in overhead:
        speedup = current / row["seconds"] if row["seconds"] > 1e-7 else float("inf")
        floor = row["stack"].startswith(
            ("direct", "Dispatcher", "LeanBmiClient without")
        )
        lines.append(
            f"| {row['stack']} | {_duration(row['seconds'])} "
            f"| {'' if floor else f'{speedup:.1f}x'} |"
        )
    transfer = results["transfer"]
    stacks = list(dict.fromkeys(r["stack"] for r in transfer))
    for kind in dict.fromkeys(r["kind"] for r in transfer):
        rows = [r for r in transfer if r["kind"] == kind]
        sizes = sorted({r["bytes"] for r in rows})
        ratio = results["zstd_ratio"].get(kind)
        ratio_text = f", zstd level 1 compresses {ratio:.2f}x" if ratio else ""
        for op in ("get_value", "set_value"):
            lines += [
                "",
                f"### {op} of {kind} float32 values{ratio_text}",
                "",
                "| Stack | " + " | ".join(_size(b) for b in sizes) + " |",
                "|---|" + "---:|" * len(sizes),
            ]
            for stack in stacks:
                cells = []
                for nbytes in sizes:
                    row = next(
                        (
                            r
                            for r in rows
                            if r["stack"] == stack and r["bytes"] == nbytes
                        ),
                        None,
                    )
                    if row is None:
                        cells.append("")
                        continue
                    seconds = row[f"{op}_seconds"]
                    rate = nbytes / seconds / 1e9
                    cells.append(f"{_duration(seconds)} ({rate:.2g} GB/s)")
                lines.append(f"| {stack} | " + " | ".join(cells) + " |")
    lines += ["", _break_even(results)]
    return "\n".join(lines) + "\n"


def _break_even(results: dict[str, Any]) -> str:
    """Network bandwidth below which zstd makes Rust get_value of largest array faster."""
    text = []
    for kind, ratio in results["zstd_ratio"].items():
        rows = [r for r in results["transfer"] if r["kind"] == kind]
        if not rows:
            continue
        nbytes = max(r["bytes"] for r in rows)
        times = {
            r["stack"]: r["get_value_seconds"] for r in rows if r["bytes"] == nbytes
        }
        if "Rust" not in times or "Rust + zstd" not in times:
            continue
        extra = times["Rust + zstd"] - times["Rust"]
        saved = nbytes * (1 - 1 / ratio)
        if extra <= 0:
            text.append(f"{kind}: zstd is faster even on localhost.")
        elif saved <= 0:
            text.append(f"{kind}: zstd does not reduce the size.")
        else:
            mbit = saved / extra * 8 / 1e6
            text.append(
                f"{kind}: zstd costs {_duration(extra)} for {_size(nbytes)} "
                f"and saves {_size(int(saved))}, "
                f"so pays off on links slower than about {mbit:.0f} Mbit/s."
            )
    return "\n".join(f"- {t}" for t in text)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--quick", action="store_true", help="Fewer sizes, shorter runs"
    )
    parser.add_argument("--json", type=Path, help="Write results to this JSON file")
    parser.add_argument("--markdown", type=Path, help="Write report to this file")
    parser.add_argument(
        "--report", type=Path, help="Only make report from earlier JSON results"
    )
    args = parser.parse_args()
    if args.report:
        print(markdown(json.loads(args.report.read_text())))
        return
    min_time = 0.3 if args.quick else 1.0
    sizes = (
        [1_000, 1_000_000] if args.quick else [1_000, 100_000, 1_000_000, 10_000_000]
    )
    kinds = ["smooth"] if args.quick else ["smooth", "sparse"]

    env = environment()
    print("Environment:", env)
    print("Per call overhead of get_var_grid:")
    overhead = bench_overhead(min_time)
    print("Transfer of float32 values with get_value and set_value:")
    transfer = bench_transfer(sizes, kinds, min_time)
    results = {
        "environment": env,
        "overhead": overhead,
        "transfer": transfer,
        "zstd_ratio": compression_ratios(sizes, kinds),
    }
    if args.json:
        args.json.write_text(json.dumps(results, indent=2))
    report = markdown(results)
    if args.markdown:
        args.markdown.write_text(report)
    print(report)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "serve":
        serve(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5])
    else:
        main()
