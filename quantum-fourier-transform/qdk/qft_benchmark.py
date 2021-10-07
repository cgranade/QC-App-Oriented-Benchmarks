"""
Quantum Fourier Transform Benchmark Program - QDK
"""

import sys
from pathlib import Path
benchmark_root = Path(__file__).parent

sys.path.insert(0, str(benchmark_root / ".." / ".." / "_common"))
import metrics
sys.path.insert(0, str(benchmark_root / ".." / ".." / "_common" / "qdk"))
import execute as ex

# NB: We disable noise for now, as the open systems simulator does not yet support arbitrary rotations.
ex.set_noise_model(None)

import numpy as np

# Since this module is intended to be run from the repo root, we need to tell
# the qsharp package where to find our benchmark.
import qsharp
qsharp.projects.add(str(benchmark_root / "QftBenchmark.csproj"))

# We can now import the callable from the new project.
from SriInternational.QcAppBenchmarks.Qft import RunQftBenchmark, RunQft

def run(min_qubits: int, max_qubits: int, max_n_circuits: int, n_shots: int, verbose: bool = False):

    metrics.init_metrics()

    for n_qubits in range(min_qubits, max_qubits + 1):
        n_circuits = min(2 ** n_qubits, max_n_circuits)
    
        if 2 ** n_qubits <= max_n_circuits:
            s_range = list(range(n_circuits))
        else:
            s_range = np.random.choice(2 ** n_qubits, n_circuits, False)

        for secret_number in s_range:
            histogram = ex.execute(
                RunQftBenchmark,
                nQubits=n_qubits, secretNumber=secret_number, verbose=verbose,
                nShots=n_shots
            )
            resources = RunQft.estimate_resources(
                nQubits=n_qubits, secretNumber=secret_number, verbose=verbose
            )
            print(f"n_qubits = {n_qubits}, secret_number = {secret_number}, depth = {resources['Depth']}, results = {histogram}")


if __name__ == '__main__':
    run()
