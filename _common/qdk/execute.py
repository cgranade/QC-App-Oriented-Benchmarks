## IMPORTS ##

from typing import TYPE_CHECKING

import numpy as np
import qutip as qt
from qutip.qip.gates import expand_operator

from qsharp.loader import QSharpCallable
from typing import Callable, Optional, Any

# Enable interoperability with Q#.
# NB: This will by default search the folder containing the ipynb file for Q#
#     programs. Since this repo is designed for use with notebooks at the
#     repo root, we will use project references to include each benchmark.
import qsharp

# Enable submitting Q# programs to Azure Quantum providers.
import qsharp.azure

# Enable noisy simulation.
import qsharp.experimental
qsharp.experimental
qsharp.experimental.enable_noisy_simulation()

## GLOBAL STATE ##

noise_model: Optional[Any] = None
use_hardware: bool = False

## INITIAL CONFIGURATION ##

noise_model = qsharp.experimental.get_noise_model_by_name('ideal')
def relaxation_noise(n_qubits: int, adj_U: qt.Qobj, gate_time: float, t1: float, t2: float) -> qt.Qobj:
    t2_eff = 1 / (1 / t2 - 0.5 * 1 / t1)
    
    # Add noise on each qubit independently.
    D = sum(
        dissipator(expand_operator(qt.destroy(2), n_qubits, [idx_qubit]), 1 / t1) +
        dissipator(expand_operator(qt.sigmaz(), n_qubits, [idx_qubit]), 1 / (2 * t2_eff))
        for idx_qubit in range(n_qubits)
    )
    angle = np.pi / 2
    H = adj_U / gate_time
    I = qt.qeye([2] * n_qubits)
    L = qt.tensor(I, H) - qt.tensor(H.trans(), I)
    L.dims = D.dims
    return (gate_time * (-1j * L + D)).expm()
# TODO: set properties of default noise model here

## NOISE MODELLING ##

def dissipator(lindblad_op, coeff=1.0):
    A = lindblad_op
    AdA = A.dag() * A
    d_out, d_in = A.dims
    I = qt.qeye(d_in)
    D = coeff * (qt.tensor(A.conj(), A) - (0.5) * (qt.tensor(AdA.trans(), I) + qt.tensor(I, AdA)))
    # set dims to super
    D.dims = [[d_in, d_out], [d_in, d_out]]
    return D

## EXECUTE INTERFACE ##

def connect(resource_id: str, location: str) -> None:
    qsharp.azure.connect(resourceId=resource_id, location=location)

def set_noise_model(model: Optional[Any]) -> None:
    global noise_model
    noise_model = model

def set_execution_target(target: str):
    qsharp.azure.target(target)

def execute(callable: QSharpCallable, **kwargs):
    if use_hardware:
        return qsharp.azure.execute(callable, **kwargs)
    else:
        if noise_model is None:
            return callable.simulate(**kwargs)
        else:
            qsharp.experimental.set_noise_model(noise_model)
            return callable.simulate_noise(**kwargs)
