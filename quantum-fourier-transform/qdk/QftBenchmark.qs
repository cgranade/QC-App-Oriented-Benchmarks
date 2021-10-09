namespace SriInternational.QcAppBenchmarks.Qft {
    open SriInternational.QcAppBenchmarks;
    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Canon;
    open Microsoft.Quantum.Convert;
    open Microsoft.Quantum.Arithmetic;
    open Microsoft.Quantum.Arrays;
    open Microsoft.Quantum.Diagnostics;
    open Microsoft.Quantum.Math;


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
