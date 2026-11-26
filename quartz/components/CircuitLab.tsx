// @ts-ignore: Quartz bundles inline scripts as strings.
import script from "./scripts/circuit-lab.inline"
import styles from "./styles/circuit-lab.scss"
import { QuartzComponent, QuartzComponentConstructor } from "./types"

function Slider({
  id,
  label,
  min,
  max,
  step,
  value,
}: {
  id: string
  label: string
  min: number
  max: number
  step: number
  value: number
}) {
  return (
    <label class="circuit-lab-control" for={id}>
      {label}
      <input id={id} type="range" min={min} max={max} step={step} value={value} />
    </label>
  )
}

function Chart({ name, label }: { name: string; label: string }) {
  return (
    <svg
      class="circuit-lab-chart"
      data-chart={name}
      viewBox="0 0 600 230"
      role="img"
      aria-label={label}
    />
  )
}

function Legend({ labels }: { labels: string[] }) {
  return (
    <ul class="circuit-lab-legend" aria-label="범례">
      {labels.map((label, index) => (
        <li class={`series-${index}`} key={label}>
          {label}
        </li>
      ))}
    </ul>
  )
}

function Feedback() {
  return (
    <section id="feedback" data-circuit-panel="feedback">
      <h2>비반전 OP-AMP와 출력 교란</h2>
      <p>
        분압기는 β = R<sub>g</sub>/(R<sub>f</sub> + R<sub>g</sub>)만큼을 반전 입력으로 되돌린다.
        출력이 순간적으로 ΔV만큼 움직이면, 차동 입력은 −βΔV만큼 변하고 전압 제어 전류원은 Δi = −g
        <sub>m</sub>βΔV만큼 반응한다.
      </p>
      <p>
        두 곡선은 각각의 DC 평형점으로부터의 오차다. β를 높이면 τ<sub>cl</sub> = RC/(1 + βg
        <sub>m</sub>R)이 짧아진다. 이 예에서는 g<sub>m</sub> = 1 mS, R = 10 kΩ, C = 100 nF, 입력은
        100 mV다. ±5 V 전원에서 선형 출력 범위를 ±4 V로 가정한다. 모든 설정의 평형점과 교란 직후
        출력이 그 범위 안에 있다.
      </p>
      <div class="circuit-lab-controls">
        <Slider id="lab-beta" label="피드백 비율 β (0–1)" min={0} max={1} step={0.01} value={0.2} />
        <Slider
          id="lab-kick"
          label="초기 출력 교란 ΔV (mV)"
          min={-500}
          max={500}
          step={25}
          value={200}
        />
      </div>
      <Legend labels={["피드백 적용", "β = 0"]} />
      <Chart name="error" label="시간에 따른 평형점 기준 출력 오차" />
      <output data-reading="" for="lab-beta lab-kick" />
    </section>
  )
}

function Bode() {
  return (
    <section id="bode" data-circuit-panel="bode">
      <h2>이득과 대역폭</h2>
      <p>
        A(s) = g<sub>m</sub>R/(1 + sRC). DC에서는 s = 0이므로 A<sub>0</sub> = g<sub>m</sub>R이고,
        사인파에서는 s = j2πf를 대입한다. 이득이 A<sub>0</sub>의 1/√2로 떨어지는 주파수가 f
        <sub>p</sub> = 1/(2πRC)다. R만 키우면 DC 이득은 오르고 극점은 낮아진다. 충분히 높은
        주파수에서는 A(j2πf) ≈ g<sub>m</sub>/(j2πfC)다. 예를 들어 저항을 10R로 바꾸면 A(s) = 10g
        <sub>m</sub>R/(1 + 10sRC)이고, 이 회로의 DC 이득은 10g<sub>m</sub>R이다.
      </p>
      <p>
        g<sub>m</sub> = 1 mS, C ≈ 159.15 pF, 기준 R = 100 MΩ인 단일 극점 소신호 모델이다. 피드백을
        걸면 T(s) = A(s)/(1 + βA(s))가 된다. 이 모델에서 T(0)·f<sub>cl</sub> = g<sub>m</sub>/(2πC) =
        1 MHz다. 출력과 입력이 선형 범위 안에 있다고 가정하며 포화, 추가 극점, 슬루율은 생략한다.
      </p>
      <div class="circuit-lab-controls">
        <label class="circuit-lab-control" for="lab-bode-r">
          비교할 R (MΩ)
          <select id="lab-bode-r">
            <option value="10">10</option>
            <option value="100">100</option>
            <option value="1000" selected>
              1,000
            </option>
          </select>
        </label>
        <label class="circuit-lab-control" for="lab-target">
          저항비로 설정한 이득 1/β (V/V)
          <select id="lab-target">
            <option value="100" selected>
              100
            </option>
            <option value="1000">1,000</option>
            <option value="10000">10,000</option>
          </select>
        </label>
        <Slider
          id="lab-log-f"
          label="관측 주파수 (log₁₀ Hz)"
          min={-1}
          max={7}
          step={0.05}
          value={3}
        />
      </div>
      <Legend labels={["기준 개방루프", "선택 R 개방루프", "선택 R 폐루프"]} />
      <Chart name="gain" label="로그 주파수에 따른 Bode 이득" />
      <Chart name="phase" label="로그 주파수에 따른 Bode 위상" />
      <output data-reading="" for="lab-bode-r lab-target lab-log-f" />
    </section>
  )
}

function Charging() {
  return (
    <section id="charging" data-circuit-panel="charging">
      <h2>정전류 병렬 RC</h2>
      <p>
        초기 전압은 0 V다. 독립 전류원 I = 1 mA가 C = 1 µF와 병렬 저항에 전류를 공급한다. I = i
        <sub>R</sub> + i<sub>C</sub>, i<sub>R</sub> = V/R, i<sub>C</sub> = C·dV/dt이므로 유한한
        R에서는 V(t) = IR(1 − e<sup>−t/RC</sup>)다.
      </p>
      <p>
        R → ∞에서 저항 경로가 끊기면 i<sub>C</sub> = I이고 V(t) = It/C다. 1 µF는 전압을 1 V 높이는
        데 1 µC가 필요하다는 뜻이다. 이상 모델에서 Q = It는 계속 늘어난다. 실제로는 전류원이
        정전류를 유지할 수 있는 최대 전압 (컴플라이언스), 커패시터의 정격과 누설을 함께 고려한다.
        그래프는 전류원 한계를 넘는 이상 전압을 점선으로 이어 그리고, 그 이후의 실제 전압과 전류는
        예측하지 않는다. 커패시터 누설과 파괴도 모델에 포함하지 않는다.
      </p>
      <div class="circuit-lab-controls">
        <label class="circuit-lab-control" for="lab-rc-r">
          병렬 저항 R
          <select id="lab-rc-r">
            <option value="1000" selected>
              1 kΩ
            </option>
            <option value="10000">10 kΩ</option>
            <option value="Infinity">∞ (저항 제거)</option>
          </select>
        </label>
        <Slider
          id="lab-compliance"
          label="전류원 컴플라이언스 (V)"
          min={0.5}
          max={8}
          step={0.5}
          value={5}
        />
        <Slider id="lab-time" label="관측 시간 (ms)" min={0} max={8} step={0.1} value={1} />
      </div>
      <Legend labels={["정전류 구간 V", "컴플라이언스 전압", "한계 이후의 이상 V"]} />
      <Chart name="voltage" label="병렬 RC 전압과 전류원 컴플라이언스" />
      <Legend labels={["커패시터 전류 iC", "저항 전류 iR"]} />
      <Chart name="currents" label="정전류 구간의 커패시터 전류와 저항 전류" />
      <output data-reading="" for="lab-rc-r lab-compliance lab-time" />
    </section>
  )
}

function Slope() {
  return (
    <section id="slope" data-circuit-panel="slope">
      <h2>시정수와 초기 상승률</h2>
      <p>
        C와 I를 고정하면 t = 0⁺에서 V = 0이므로 i<sub>R</sub> = 0이고, 세 곡선 모두 dV/dt = I/C로
        시작한다. R이 클수록 기울기가 천천히 줄어들며 더 높은 최종 전압 IR의 약 63.2%에 도달하는 데
        더 오래 걸린다. 점은 각 유한 저항의 t = RC를 표시한다. 이 비교에서는 I = 1 mA이고 이상적인
        전류원이 전압 제한 없이 동작한다고 가정한다.
      </p>
      <div class="circuit-lab-controls">
        <Slider id="lab-compare-r" label="비교 저항 R (kΩ)" min={2} max={6} step={1} value={4} />
        <Slider
          id="lab-cap"
          label="공통 커패시턴스 C (µF)"
          min={0.5}
          max={2}
          step={0.1}
          value={1}
        />
      </div>
      <Legend labels={["R = 1 kΩ", "선택한 R", "R → ∞ (공통 초기 접선)"]} />
      <Chart name="comparison" label="저항별 충전 곡선, 공통 초기 접선과 시정수" />
      <output data-reading="" for="lab-compare-r lab-cap" />
    </section>
  )
}

function CircuitLab() {
  return (
    <div class="circuit-lab">
      <noscript>그래프를 조작하려면 브라우저에서 JavaScript를 켜야 한다.</noscript>
      <Feedback />
      <Bode />
      <Charging />
      <Slope />
    </div>
  )
}

export default (({ slug }) => {
  const Lab: QuartzComponent = ({ fileData }) => (fileData.slug === slug ? <CircuitLab /> : null)
  Lab.css = styles
  Lab.afterDOMLoaded = script
  return Lab
}) satisfies QuartzComponentConstructor<{ slug: string }>
