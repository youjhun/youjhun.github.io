// The models accept SI units. Display conversions belong to the lab controls.
export function onePole(gm: number, resistance: number, capacitance: number, beta = 0) {
  const openGain = gm * resistance
  const loopFactor = 1 + beta * openGain
  const dcGain = openGain / loopFactor
  const tau = (resistance * capacitance) / loopFactor

  return { dcGain, tau, poleHz: 1 / (2 * Math.PI * tau) }
}

export function bode(model: ReturnType<typeof onePole>, frequencyHz: number) {
  const ratio = frequencyHz / model.poleHz
  return {
    gainDb: 20 * Math.log10(model.dcGain / Math.hypot(1, ratio)),
    phaseDeg: (-180 / Math.PI) * Math.atan(ratio),
  }
}

export function outputRecovery(
  gm: number,
  resistance: number,
  capacitance: number,
  beta: number,
  input: number,
  disturbance: number,
) {
  const { dcGain, tau } = onePole(gm, resistance, capacitance, beta)
  const equilibrium = dcGain * input
  return {
    equilibrium,
    tau,
    equilibriumDifferential: input - beta * equilibrium,
    currentChange: -gm * beta * disturbance,
    error: (time: number) => disturbance * Math.exp(-time / tau),
  }
}

export function parallelRC(current: number, resistance: number, capacitance: number) {
  const open = resistance === Infinity
  const tau = resistance * capacitance
  const finalVoltage = current * resistance
  const initialSlope = current / capacitance

  // The capacitor starts discharged. expm1 preserves accuracy when t ≪ RC.
  function at(time: number) {
    const resistorCurrent = open ? 0 : -current * Math.expm1(-time / tau)
    return {
      voltage: open ? initialSlope * time : resistance * resistorCurrent,
      resistorCurrent,
      capacitorCurrent: current * Math.exp(-time / tau),
    }
  }

  function timeToVoltage(voltage: number) {
    if (voltage >= finalVoltage) return Infinity
    return open ? voltage / initialSlope : -tau * Math.log1p(-voltage / finalVoltage)
  }

  return { tau, finalVoltage, initialSlope, at, timeToVoltage }
}
