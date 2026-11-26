import { strict as assert } from "node:assert"
import { test } from "node:test"
import { bode, onePole, outputRecovery, parallelRC } from "./circuit-response"

function near(actual: number, expected: number, tolerance = 1e-10) {
  assert.ok(Math.abs(actual - expected) <= tolerance, `expected ${actual} ≈ ${expected}`)
}

test("DC gain, Bode corner and gain–bandwidth product match the single-pole model", () => {
  const gm = 1e-3
  const capacitance = gm / (2 * Math.PI * 1e6)
  const small = onePole(gm, 100e6, capacitance)
  const large = onePole(gm, 1000e6, capacitance)
  const closed = onePole(gm, 100e6, capacitance, 0.01)

  near(small.dcGain, 1e5)
  near(small.poleHz, 10)
  near(large.dcGain, 1e6)
  near(large.poleHz, 1)
  near(bode(small, 0).gainDb, 100)
  near(bode(small, small.poleHz).gainDb, 100 - 10 * Math.log10(2))
  near(bode(small, small.poleHz).phaseDeg, -45)
  near(bode(small, 1e6).gainDb, bode(large, 1e6).gainDb, 1e-8)
  near(closed.dcGain, 1e5 / 1001)
  near(closed.poleHz, 10010)
  near(closed.dcGain * closed.poleHz, 1e6, 1e-8)
})

test("negative feedback opposes both signs of output disturbance within the declared rails", () => {
  for (const kick of [-0.5, 0.5]) {
    const open = outputRecovery(1e-3, 10e3, 100e-9, 0, 0.1, kick)
    const closed = outputRecovery(1e-3, 10e3, 100e-9, 0.2, 0.1, kick)
    near(closed.error(0), kick)
    near(closed.currentChange, -0.2e-3 * kick)
    near(closed.tau, open.tau / 3)
    near(closed.error(closed.tau), kick / Math.E)
    near(closed.equilibrium, 1 / 3)
    near(closed.equilibriumDifferential, 0.1 / 3)
  }
  for (const beta of [0, 1]) {
    for (const kick of [-0.5, 0.5]) {
      const response = outputRecovery(1e-3, 10e3, 100e-9, beta, 0.1, kick)
      assert.ok(Math.abs(response.equilibrium + response.error(0)) < 4)
    }
  }
})

test("finite RC current splits obey KCL and the 63.2% point", () => {
  const model = parallelRC(1e-3, 1e3, 1e-6)
  const initial = model.at(0)
  near(initial.voltage, 0)
  near(initial.resistorCurrent, 0)
  near(initial.capacitorCurrent, 1e-3)
  for (const time of [0, 1e-3, 8e-3]) {
    const state = model.at(time)
    near(state.resistorCurrent + state.capacitorCurrent, 1e-3)
    near(state.resistorCurrent * 1e3, state.voltage)
  }
  near(model.tau, 1e-3)
  near(model.at(model.tau).voltage, 1 - 1 / Math.E)
  near(model.timeToVoltage(0.5), 1e-3 * Math.log(2))
  assert.equal(model.timeToVoltage(1), Infinity)
  assert.equal(model.timeToVoltage(5), Infinity)
})

test("the R → ∞ limit keeps the shared initial slope and reaches compliance linearly", () => {
  const open = parallelRC(1e-3, Infinity, 1e-6)
  assert.equal(open.tau, Infinity)
  near(open.at(0).voltage, 0)
  near(open.at(5e-3).voltage, 5)
  near(open.at(5e-3).capacitorCurrent, 1e-3)
  near(open.at(5e-3).resistorCurrent, 0)
  near(open.timeToVoltage(5), 5e-3)
  for (const resistance of [1e3, 10e3, 1e15, Infinity]) {
    const model = parallelRC(1e-3, resistance, 1e-6)
    near(model.initialSlope, 1000)
    near(model.at(1e-9).voltage / 1e-9, 1000, 1e-3)
  }
  near(parallelRC(1e-3, 1e15, 1e-6).at(5e-3).voltage, 5)
})
