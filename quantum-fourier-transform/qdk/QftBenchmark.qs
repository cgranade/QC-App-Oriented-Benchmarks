namespace SriInternational.QcAppBenchmarks.Qft {
    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Canon;
    open Microsoft.Quantum.Convert;
    open Microsoft.Quantum.Arithmetic;
    open Microsoft.Quantum.Arrays;
    open Microsoft.Quantum.Diagnostics;
    open Microsoft.Quantum.Math;

    // TODO: Move this operation to a common.qs.
    operation EstimateBenchmarkHistogram(op : Unit => Int, nShots : Int, maxOutput : Int) : Double[] {
        mutable results = [0, size=maxOutput + 1];
        for _ in 1..nShots {
            let result = op();
            set results w/= result <- results[result] + 1;
        }
        return Mapped(DividedByD(_, IntAsDouble(nShots)), Mapped(IntAsDouble, results));
    }

    @EntryPoint() // Allow running from the command line as well.
    operation RunQft(nQubits : Int, secretNumber : Int, verbose : Bool) : Int {
        use register = Qubit[nQubits];
        ApplyPauliFromBitString(
            PauliX, true,
            IntAsBoolArray(secretNumber, nQubits),
            register
        );
        within {
            QFT(BigEndian(Reversed(register)));
        } apply {
            if verbose {
                DumpMachine();
            }
        }
        return MeasureInteger(LittleEndian(register));
    }

    @EntryPoint()
    operation RunQftBenchmark(nQubits : Int, secretNumber : Int, verbose : Bool, nShots : Int) : Double[] {
        return EstimateBenchmarkHistogram(
            Delayed(RunQft, (nQubits, secretNumber, verbose)),
            nShots, 2^nQubits - 1
        );
    }

}
