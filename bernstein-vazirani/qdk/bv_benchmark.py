"""
Bernstein–Vazirani Benchmark Program - QDK
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
noise_model['x'] = ex.relaxation_noise(1, qt.sigmax() * np.pi / 2, 2.0, 100.0, 100.0)
noise_model['y'] = ex.relaxation_noise(1, qt.sigmay() * np.pi / 2, 2.5, 100.0, 100.0)
noise_model['z'] = ex.relaxation_noise(1, qt.sigmaz() * np.pi / 2, 2.5, 100.0, 100.0)
noise_model['h'] = ex.relaxation_noise(1, qt.qip.operations.hadamard_transform() * np.pi / 2, 2.5, 100.0, 100.0)
noise_model['cnot'] = ex.relaxation_noise(2, qt.cnot() * np.pi / 2, 10.0, 100.0, 100.0)
ex.set_noise_model(noise_model)

import numpy as np

# Since this module is intended to be run from the repo root, we need to tell
# the qsharp package where to find our benchmark.
import qsharp
qsharp.projects.add(str(benchmark_root / "BvBenchmark.csproj"))

# We can now import the callable from the new project.
from SriInternational.QcAppBenchmarks.BersteinVazirani import (
    RunBvBenchmark, RunBv
)

def run(min_qubits: int, max_qubits: int, max_n_circuits: int, n_shots: int, verbose: bool = False):

    metrics.init_metrics()

    for n_qubits in range(min_qubits, max_qubits + 1):
        n_circuits = min(2 ** (n_qubits - 1), max_n_circuits)
        qsharp.config['experimental.simulators.nQubits'] = n_qubits

        if 2 ** n_qubits <= max_n_circuits:
            s_range = list(range(n_circuits))
        else:
            s_range = np.random.choice(2 ** (n_qubits - 1), n_circuits, False)

        for secret_number in s_range:
            histogram = ex.execute(
                RunBvBenchmark,
                nQubits=n_qubits, secretNumber=secret_number,
                nShots=n_shots
            )
            resources = RunBv.estimate_resources(
                nQubits=n_qubits, secretNumber=secret_number
            )
            print(f"n_qubits = {n_qubits}, secret_number = {secret_number}, depth = {resources['Depth']}, results = {histogram}")


if __name__ == '__main__':
    run()
