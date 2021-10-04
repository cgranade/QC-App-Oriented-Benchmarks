"""
Quantum Fourier Transform Benchmark Program - QDK
"""

import sys
from pathlib import Path
benchmark_root = Path(__file__).parent

sys.path.insert(0, str(benchmark_root / ".." / ".." / "_common" / "qdk"))
import execute as ex

# Since this module is intended to be run from the repo root, we need to tell
# the qsharp package where to find our benchmark.
import qsharp
qsharp.projects.add(str(benchmark_root / "QftBenchmark.csproj"))

# We can now import the callable from the new project.
from SriInternational.QcAppBenchmarks.Qft import RunQftBenchmark

def run(min_qubits: int, max_qubits: int, secret_number: int, verbose: bool = False):
    results = []
    for n_qubits in range(min_qubits, max_qubits):
        results.append(ex.execute(RunQftBenchmark, nQubits=n_qubits, secretNumber=secret_number, verbose=verbose))
    return results

if __name__ == '__main__':
    run()
