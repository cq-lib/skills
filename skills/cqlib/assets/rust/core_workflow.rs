use cqlib_core::circuit::{Circuit, Instruction, Parameter, Qubit, StandardGate};
use cqlib_core::compile::resource::ResourcePolicy;
use cqlib_core::compile::{CompileConfig, CompileMode, CompileTarget, compile};
use cqlib_core::ir::qcis;
use cqlib_core::qis::Statevector;
use std::collections::HashMap;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let mut source = Circuit::new(2);
    source.rx(Qubit::new(0), Parameter::symbol("theta"))?;
    let bindings = Some(HashMap::from([("theta", std::f64::consts::PI)]));
    let bound = source.assign_parameters(&bindings)?;
    assert!(bound.used_symbols().is_empty());
    assert!(!source.used_symbols().is_empty());
    let state = Statevector::from_circuit(&bound)?;
    assert!((state.probabilities()[1] - 1.0).abs() < 1e-10);
    assert!(
        state
            .sample_shots(8)
            .iter()
            .all(|o| o.to_bitstring(2) == "01")
    );

    let mut bell = Circuit::new(2);
    bell.h(Qubit::new(0))?;
    bell.cx(Qubit::new(0), Qubit::new(1))?;
    let result = compile(
        &bell,
        CompileConfig {
            mode: CompileMode::Normal,
            target: CompileTarget::Basis(vec![
                Instruction::Standard(StandardGate::H),
                Instruction::Standard(StandardGate::CZ),
            ]),
            resource_policy: ResourcePolicy::default(),
        },
    )?;
    let text = qcis::dumps(&result.circuit)?;
    let restored = qcis::loads(&text)?;
    let probabilities = Statevector::from_circuit(&restored)?.probabilities();
    assert!((probabilities[0] - 0.5).abs() < 1e-10);
    assert!((probabilities[3] - 0.5).abs() < 1e-10);
    assert_eq!(bell.operations().len(), 2);
    println!("{text}");
    Ok(())
}
