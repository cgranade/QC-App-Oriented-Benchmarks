namespace SriInternational.QcAppBenchmarks {
    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Canon;
    open Microsoft.Quantum.Arrays;
    open Microsoft.Quantum.Math;
    open Microsoft.Quantum.Convert;

    operation EstimateBenchmarkHistogram(op : Unit => Int, nShots : Int, maxOutput : Int) : Double[] {
        mutable results = [0, size=maxOutput + 1];
        for _ in 1..nShots {
            let result = op();
            set results w/= result <- results[result] + 1;
        }
        return Mapped(DividedByD(_, IntAsDouble(nShots)), Mapped(IntAsDouble, results));
    }

}
