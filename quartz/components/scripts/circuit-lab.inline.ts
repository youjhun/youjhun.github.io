import { bode, onePole, outputRecovery, parallelRC } from "./circuit-response"

type Point = [number, number]
type Axis = {
  label: string
  ticks: number[]
  domain: [number, number]
  format?: (value: number) => string
}
type Series = { points: Point[]; style?: string }

const svgNamespace = "http://www.w3.org/2000/svg"
const milli = 1e-3
const micro = 1e-6

function svgElement(tag: string, attributes: Record<string, number | string>, content = "") {
  const element = document.createElementNS(svgNamespace, tag)
  for (const [key, value] of Object.entries(attributes)) element.setAttribute(key, String(value))
  element.textContent = content
  return element
}

function timeAxis(end: number, ticks: number[]): Axis {
  return { label: "시간 (ms)", domain: [0, end], ticks }
}

function chart(
  panel: HTMLElement,
  name: string,
  x: Axis,
  y: Axis,
  series: Series[],
  cursor?: number,
  dots: Point[] = [],
) {
  const svg = panel.querySelector<SVGSVGElement>(`[data-chart="${name}"]`)!
  const left = 66
  const right = 572
  const top = 29
  const bottom = 174
  const scale = (value: number, [low, high]: Axis["domain"]) => (value - low) / (high - low)
  const px = (value: number) => left + scale(value, x.domain) * (right - left)
  const py = (value: number) => bottom - scale(value, y.domain) * (bottom - top)
  const elements: SVGElement[] = []
  const line = (x1: number, y1: number, x2: number, y2: number, style: string) => {
    elements.push(svgElement("line", { x1, y1, x2, y2, class: style }))
  }
  const label = (x: number, y: number, text: string, anchor = "middle") => {
    elements.push(svgElement("text", { x, y, "text-anchor": anchor }, text))
  }

  label(left, 20, y.label, "start")
  label((left + right) / 2, 224, x.label)
  for (const tick of y.ticks) {
    line(left, py(tick), right, py(tick), "grid")
    label(left - 8, py(tick) + 5, (y.format ?? String)(tick), "end")
  }
  for (const tick of x.ticks) {
    line(px(tick), top, px(tick), bottom, "grid")
    label(px(tick), bottom + 22, (x.format ?? String)(tick))
  }
  line(left, top, left, bottom, "axis")
  line(left, bottom, right, bottom, "axis")

  if (cursor !== undefined) line(px(cursor), top, px(cursor), bottom, "cursor")
  series.forEach(({ points, style }, index) => {
    if (points.length === 0) return
    elements.push(
      svgElement("polyline", {
        points: points.map(([x, y]) => `${px(x).toFixed(2)},${py(y).toFixed(2)}`).join(" "),
        class: style ?? `series-${index}`,
      }),
    )
  })
  dots.forEach(([x, y], index) => {
    elements.push(svgElement("circle", { cx: px(x), cy: py(y), r: 5, class: `series-${index}` }))
  })
  svg.replaceChildren(...elements)
}

function sample(from: number, to: number, evaluate: (x: number) => number): Point[] {
  return Array.from({ length: 161 }, (_, index) => {
    const x = from + ((to - from) * index) / 160
    return [x, evaluate(x)]
  })
}

function reading(panel: HTMLElement, message: string) {
  panel.querySelector("output")!.textContent = message
}

function value(panel: HTMLElement, id: string) {
  return Number(panel.querySelector<HTMLInputElement | HTMLSelectElement>(`#${id}`)!.value)
}

function feedback(panel: HTMLElement) {
  const beta = value(panel, "lab-beta")
  const kickMv = value(panel, "lab-kick")
  const response = outputRecovery(1e-3, 10e3, 100e-9, beta, 0.1, kickMv * milli)
  const reference = outputRecovery(1e-3, 10e3, 100e-9, 0, 0.1, kickMv * milli)
  chart(
    panel,
    "error",
    timeAxis(4, [0, 1, 2, 3, 4]),
    { label: "출력 오차 e (mV)", domain: [-500, 500], ticks: [-500, -250, 0, 250, 500] },
    [response, reference].map((model) => ({
      points: sample(0, 4, (t) => model.error(t * milli) / milli),
    })),
  )
  reading(
    panel,
    `β ${beta.toFixed(2)} · ΔV ${kickMv} mV · τ ${(response.tau / milli).toFixed(3)} ms (β = 0: 1.000 ms)
평형 Vout ${response.equilibrium.toFixed(3)} V · 평형 V+ − V− ${(response.equilibriumDifferential / milli).toFixed(2)} mV · Δi ${(response.currentChange / micro).toFixed(1)} µA`,
  )
}

function frequencyLabel(frequency: number) {
  if (frequency >= 1e6) return `${+(frequency / 1e6).toPrecision(4)} MHz`
  if (frequency >= 1e3) return `${+(frequency / 1e3).toPrecision(4)} kHz`
  return `${+frequency.toPrecision(4)} Hz`
}

function frequencyResponse(panel: HTMLElement) {
  const gm = 1e-3
  const capacitance = gm / (2 * Math.PI * 1e6)
  const megaOhms = value(panel, "lab-bode-r")
  const resistance = megaOhms * 1e6
  const beta = 1 / value(panel, "lab-target")
  const logF = value(panel, "lab-log-f")
  const baseline = onePole(gm, 100e6, capacitance)
  const open = onePole(gm, resistance, capacitance)
  const closed = onePole(gm, resistance, capacitance, beta)
  const models = [baseline, open, closed]
  const x: Axis = {
    label: "주파수 f (Hz, 로그 축)",
    domain: [-1, 7],
    ticks: [-1, 1, 3, 5, 7],
    format: (log) => ({ "-1": "0.1", 1: "10", 3: "1k", 5: "100k", 7: "10M" })[String(log)]!,
  }
  chart(
    panel,
    "gain",
    x,
    { label: "전압 이득 (dB)", domain: [-25, 125], ticks: [-20, 0, 40, 80, 120] },
    models.map((model) => ({ points: sample(-1, 7, (log) => bode(model, 10 ** log).gainDb) })),
    logF,
  )
  chart(
    panel,
    "phase",
    x,
    { label: "위상 (°)", domain: [-95, 5], ticks: [-90, -60, -45, -30, 0] },
    models.map((model) => ({ points: sample(-1, 7, (log) => bode(model, 10 ** log).phaseDeg) })),
    logF,
  )
  const frequency = 10 ** logF
  const measured = bode(closed, frequency)
  reading(
    panel,
    `개방루프 R ${megaOhms} MΩ · DC ${open.dcGain.toLocaleString("ko-KR")} V/V · 극점 ${frequencyLabel(open.poleHz)}
폐루프 DC ${closed.dcGain.toFixed(2)} V/V · 극점 ${frequencyLabel(closed.poleHz)}
관측 ${frequencyLabel(frequency)} · 폐루프 ${measured.gainDb.toFixed(2)} dB · 위상 ${measured.phaseDeg.toFixed(1)}°`,
  )
}

function charging(panel: HTMLElement) {
  const resistance = value(panel, "lab-rc-r")
  const compliance = value(panel, "lab-compliance")
  const time = value(panel, "lab-time")
  const model = parallelRC(milli, resistance, micro)
  const boundary = model.timeToVoltage(compliance) / milli
  const end = 8
  const validEnd = Math.min(end, boundary)
  const x = timeAxis(end, [0, 2, 4, 6, 8])
  const voltage = (ms: number) => model.at(ms * milli).voltage
  // A slider value exactly at the boundary can differ by a few floating-point ulps.
  const withinCompliance = (volts: number) => volts <= compliance * (1 + 4 * Number.EPSILON)
  chart(
    panel,
    "voltage",
    x,
    { label: "전압 V (V)", domain: [0, 8.5], ticks: [0, 2, 4, 6, 8] },
    [
      { points: sample(0, validEnd, voltage) },
      {
        points: [
          [0, compliance],
          [end, compliance],
        ],
      },
      { points: withinCompliance(voltage(end)) ? [] : sample(boundary, end, voltage) },
    ],
    time,
  )
  chart(
    panel,
    "currents",
    x,
    { label: "전류 (mA)", domain: [0, 1.05], ticks: [0, 0.25, 0.5, 0.75, 1] },
    [
      { points: sample(0, validEnd, (ms) => model.at(ms * milli).capacitorCurrent / milli) },
      { points: sample(0, validEnd, (ms) => model.at(ms * milli).resistorCurrent / milli) },
    ],
    time,
  )
  const state = model.at(time * milli)
  const limit = Number.isFinite(boundary)
    ? `${boundary.toFixed(2)} ms에 도달`
    : "유한 시간에 도달하지 않음"
  const measured = withinCompliance(state.voltage)
    ? `V ${state.voltage.toFixed(3)} V · iC ${(state.capacitorCurrent / milli).toFixed(3)} mA · iR ${(state.resistorCurrent / milli).toFixed(3)} mA`
    : `이상 V ${state.voltage.toFixed(3)} V · 정전류 동작 범위 초과`
  reading(panel, `컴플라이언스 ${compliance} V · ${limit}\nt ${time.toFixed(1)} ms · ${measured}`)
}

function slope(panel: HTMLElement) {
  const kiloOhms = value(panel, "lab-compare-r")
  const capacitance = value(panel, "lab-cap") * micro
  const base = parallelRC(milli, 1e3, capacitance)
  const chosen = parallelRC(milli, kiloOhms * 1e3, capacitance)
  const open = parallelRC(milli, Infinity, capacitance)
  const end = Math.ceil((1.25 * chosen.tau) / milli)
  const top = Math.ceil(open.at(end * milli).voltage / 2) * 2
  const x = timeAxis(end, [0, end / 4, end / 2, (3 * end) / 4, end])
  chart(
    panel,
    "comparison",
    x,
    { label: "전압 V (V)", domain: [0, top], ticks: [0, top / 4, top / 2, (3 * top) / 4, top] },
    [base, chosen, open].map((model) => ({
      points: sample(0, end, (ms) => model.at(ms * milli).voltage),
    })),
    undefined,
    [base, chosen].map((model) => [model.tau / milli, model.at(model.tau).voltage]),
  )
  reading(
    panel,
    `C ${(capacitance / micro).toFixed(1)} µF · 공통 초기 상승률 ${(base.initialSlope * milli).toFixed(3)} V/ms
1 kΩ에서 τ ${(base.tau / milli).toFixed(2)} ms · ${kiloOhms} kΩ에서 τ ${(chosen.tau / milli).toFixed(2)} ms`,
  )
}

const renderers = { feedback, bode: frequencyResponse, charging, slope }

function renderPanel(panel: HTMLElement) {
  const name = panel.dataset.circuitPanel as keyof typeof renderers
  renderers[name](panel)
}

document.addEventListener("nav", () => {
  document.querySelectorAll<HTMLElement>(".circuit-lab [data-circuit-panel]").forEach(renderPanel)
})

document.addEventListener("input", (event) => {
  const panel = (event.target as Element).closest<HTMLElement>(".circuit-lab [data-circuit-panel]")
  if (panel) renderPanel(panel)
})
