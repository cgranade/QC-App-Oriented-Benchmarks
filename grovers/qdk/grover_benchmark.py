"""
Grover's Algorithm Benchmark Program - QDK
"""

import sys
from pathlib import Path
benchmark_root = Path(__file__).parent

sys.path.insert(0, str(benchmark_root / ".." / ".." / "_common"))
import metrics
sys.path.insert(0, str(benchmark_root / ".." / ".." / "_common" / "qdk"))
import execute as ex

import numpy as np
import qutip as qt
import qsharp.experimental
noise_model = qsharp.experimental.get_noise_model_by_name('ideal')
noise_model['x'] = ex.relaxation_noise(1, qt.sigmax() * np.pi / 2, 1.0, 100.0, 100.0)
noise_model['y'] = ex.relaxation_noise(1, qt.sigmay() * np.pi / 2, 1.5, 100.0, 100.0)
noise_model['z'] = ex.relaxation_noise(1, qt.sigmaz() * np.pi / 2, 1.5, 100.0, 100.0)
noise_model['h'] = ex.relaxation_noise(1, qt.qip.operations.hadamard_transform() * np.pi / 2, 2.5, 100.0, 100.0)
noise_model['cnot'] = ex.relaxation_noise(2, qt.cnot() * np.pi / 2, 3.0, 100.0, 100.0)
ex.set_noise_model(noise_model)

import numpy as np

# Since this module is intended to be run from the repo root, we need to tell
# the qsharp package where to find our benchmark.
import qsharp
project = str((benchmark_root / "GroverBenchmark.csproj").absolute())
if project not in qsharp.projects:
    qsharp.projects.add(project)

# We can now import the callable from the new project.
from SriInternational.QcAppBenchmarks.BersteinVazirani import (
    RunGroverBenchmark, RunGrover
)

def run(min_qubits: int = 2,
        max_qubits: int = 3,
        max_n_circuits: int = 100,
        n_shots: int = 100,
        verbose: bool = False):

    metrics.init_metrics()

    for n_qubits in range(max(2, min_qubits), max_qubits + 1):
        n_circuits = min(2 ** n_qubits, max_n_circuits)
        # We need enough qubits to decompose Controlled Z into hardware-level
        # intrinsics.
        qsharp.config['experimental.simulators.nQubits'] = n_qubits + int(np.ceil(np.log2(n_qubits + 1)))

        if 2 ** n_qubits <= max_n_circuits:
            s_range = list(range(n_circuits))
        else:
            s_range = np.random.choice(2 ** n_qubits, n_circuits, False)

        for secret_number in s_range:
            histogram = ex.execute(
                RunGroverBenchmark,
                nQubits=n_qubits, secretNumber=secret_number,
                nShots=n_shots
            )
            resources = RunGrover.estimate_resources(
                nQubits=n_qubits, secretNumber=secret_number
            )
            print(f"n_qubits = {n_qubits}, secret_number = {secret_number}, depth = {resources['Depth']}, results = {histogram}")


if __name__ == '__main__':
    run()
