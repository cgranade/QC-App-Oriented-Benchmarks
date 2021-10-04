## IMPORTS ##

from typing import TYPE_CHECKING

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
# TODO: set properties of default noise model here

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
