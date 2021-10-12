namespace SriInternational.QcAppBenchmarks.BersteinVazirani {
    open SriInternational.QcAppBenchmarks;
    open Microsoft.Quantum.Canon;
    open Microsoft.Quantum.Arithmetic;
    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Arrays;
    open Microsoft.Quantum.Convert;
    open Microsoft.Quantum.Math;

    function NIterations(nQubits : Int) : Int {
        let nItems = 1 <<< nQubits; // 2^numQubits
        // compute number of iterations:
        let angle = ArcSin(1. / Sqrt(IntAsDouble(nItems)));
        let nIterations = Round(0.25 * PI() / angle - 0.5);
        return nIterations;
    }

    operation ReflectAboutMarkedItem(secretNumber : Int, register : Qubit[]) : Unit {
        use target = Qubit();
        within {
            X(target);
            H(target);
        } apply {
            (ControlledOnInt(secretNumber, X))(register, target);
        }
        // Not needed on ideal hardware, but useful in the presence of noise.
        // Note that we cannot use `is Adj + Ctl` in an operation containing
        // irreversible operations such as Reset.
        Reset(target);
    }

    operation ReflectAboutInitialState(register : Qubit[]) : Unit is Adj + Ctl {
        within {
            ApplyToEachCA(H, register);
            ApplyToEachCA(X, register);
        } apply {
            Controlled Z(Most(register), Tail(register));
        }
    }

    operation RunGrover(nQubits : Int, secretNumber : Int) : Int {
        use register = Qubit[nQubits];

        // Prepare the state |++…+⟩.
        ApplyToEachCA(H, register);

        for _ in 1..NIterations(nQubits) {
            ReflectAboutMarkedItem(secretNumber, register);
            ReflectAboutInitialState(register);
        }

        return MeasureInteger(LittleEndian(register));
    }

    @EntryPoint()
    operation RunGroverBenchmark(nQubits : Int, secretNumber : Int, nShots : Int) : Double[] {
        return EstimateBenchmarkHistogram(
            Delayed(RunGrover, (nQubits, secretNumber)),
            nShots, 2^nQubits - 1
        );
    }
}
