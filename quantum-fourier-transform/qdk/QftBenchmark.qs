namespace SriInternational.QcAppBenchmarks.Qft {
    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Canon;
    open Microsoft.Quantum.Convert;
    open Microsoft.Quantum.Arithmetic;
    open Microsoft.Quantum.Arrays;
    open Microsoft.Quantum.Diagnostics;

    @EntryPoint() // Allow running from the command line as well.
    operation RunQftBenchmark(nQubits : Int, secretNumber : Int, verbose : Bool) : Int {
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

}
