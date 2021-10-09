namespace SriInternational.QcAppBenchmarks.BersteinVazirani {
    open SriInternational.QcAppBenchmarks;
    open Microsoft.Quantum.Canon;
    open Microsoft.Quantum.Arithmetic;
    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Arrays;
    open Microsoft.Quantum.Convert;

    operation ApplyOracle(secretNumber : Int, register : Qubit[], target : Qubit) : Unit is Adj + Ctl {
        for (patternBit, controlQubit) in Zipped(IntAsBoolArray(secretNumber, Length(register)), register) {
            if (patternBit) {
                Controlled X([controlQubit], target);
            }
        }
    }

    operation RunBv(nQubits : Int, secretNumber : Int) : Int {
        use register = Qubit[nQubits - 1];
        use aux = Qubit();

        // Prepare the state |00…01⟩.
        X(aux);

        within {
            ApplyToEachCA(H, register + [aux]);
        } apply {
            ApplyOracle(secretNumber, register, aux);
        }

        Reset(aux);
        return MeasureInteger(LittleEndian(register));
    }

    @EntryPoint()
    operation RunBvBenchmark(nQubits : Int, secretNumber : Int, nShots : Int) : Double[] {
        return EstimateBenchmarkHistogram(
            Delayed(RunBv, (nQubits, secretNumber)),
            nShots, 2^nQubits - 1
        );
    }
}
