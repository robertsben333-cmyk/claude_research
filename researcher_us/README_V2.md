# Stage E V2 — The Shadow News Grounding Engine

## 1. Overview & Problem Definition

In **Stage E V1** (`researcher_us/`), Claude unpriced hunters generated signed impact scores (`expected_impact_pct`) for unpriced earnings clues. However, V1 suffered from fundamental structural issues:
1. **Unanchored Impact Scores:** The raw scores were subjective heuristics lacking a formal quantitative mapping to market discounting.
2. **Symptom-Chasing in `LESSONS.md`:** Post-mortem heuristic lists acted as Ptolemaic epicycles—logging past failure modes without providing a functional mapping:
   $$\Delta \text{Price} = f(\text{Unpriced Shock}, \text{Current Market State}, \text{Positioning})$$
3. **The Discarded Baseline Paradox:** V1 assumed wire news copy was 100% priced in and discarded it. Yet wire copy is the **only news with real, observable ground-truth price discovery**.

**Stage E V2** solves this by establishing a **Shadow Grounding Layer**. We shadow observable wire news, score it under Claude's evaluation framework, observe the real market response across liquid timeframes, and use that empirical calibration surface to ground runtime unpriced findings.

---

## 2. Core Architecture: The Symmetric Calibration Mechanism

To avoid volatility double-counting and beta contamination, Stage E V2 enforces **strict calibration symmetry** between the shadow ledger and runtime unscaling.

```
[Observable Wire News Event i]
                │
                ▼
[Shadow Profiler: Claude Score S_i] ────► [Market Returns ΔP_{i, τ} & SPY Returns]
                │                                    │
                │                                    ▼
                │                  [Beta-Stripped Excess Return: α_{i, τ} = ΔP_{i, τ} - β_i · ΔP_{SPY, τ}]
                │                                    │
                │                                    ▼
                │                  [Unit-Volatility Normalization: α̃_{i, τ} = α_{i, τ} / IV_i]
                │                                    │
                └─────────────────┬──────────────────┘
                                  ▼
                 [Fitted Response Factor κ_{τ, L}]
             κ_{τ, L} = Σ (α̃_{i, τ} · S_i) / Σ (S_i^2)
                                  │
 ┌────────────────────────────────┴────────────────────────────────┐
 │ Calibration Matrix: Dimensionless response elasticity           │
 │ (Standardized alpha per unit of volatility per Claude point)    │
 └────────────────────────────────┬────────────────────────────────┘
                                  │
                                  ▼
                 [Runtime Unpriced Finding j (Score S_j)]
                                  │
                                  ▼
                 [Target Stock Live Event IV (IV_{live})]
                                  │
                                  ▼
                 [Symmetric Unscaling to Absolute Return]
            Grounded_Impact_τ(j) = S_j · κ_{τ, L_j} · IV_{live}
                                  │
                                  ▼
         [Multi-Horizon Grounded Ranking Key: impact_sum_τ]
```

### The Calibration Steps:
1. **Beta-Stripped Alpha:**
   $$\alpha_{i, \tau} = \Delta P_{i, \tau} - \beta_i \cdot \Delta P_{\text{SPY}, \tau}$$
2. **Unit-Volatility Normalization (Shadow):**
   $$\widetilde{\alpha}_{i, \tau} = \frac{\alpha_{i, \tau}}{IV_i}$$
3. **Empirical Horizon Response Factor ($\kappa_{\tau, L}$):**
   $$\kappa_{\tau, L} = \frac{\sum_{i \in \text{Shadow}_L} \widetilde{\alpha}_{i, \tau} \cdot S_i}{\sum_{i \in \text{Shadow}_L} S_i^2}$$
4. **Symmetric Unscaling (Runtime):**
   $$\text{Grounded\_Impact}_{\tau}(j) = S_j \cdot \kappa_{\tau, L_j} \cdot IV_{\text{live}}$$
   - **Zero Beta Leakage:** Market beta is strictly confined to benchmark subtraction in Step 1.
   - **No Volatility Double-Counting:** Historical volatility is normalized out in Step 2 and symmetrically re-applied at runtime in Step 4.

---

## 3. The 9 Tracked Liquid Timeframes

To allow empirical analysis of noise decay versus structural repricing, V2 tracks 9 liquid horizons:

| Horizon ($\tau$) | Description | Dynamics Captured |
| :--- | :--- | :--- |
| **`5m`** | $t_0 \to +5\text{ min}$ | High-frequency algorithmic headline digestion |
| **`15m`** | $t_0 \to +15\text{ min}$ | Initial intraday liquidity cross |
| **`60m`** | $t_0 \to +60\text{ min}$ | First full hour / initial sell-side take |
| **`session_close`** | $t_0 \to$ Day Closing Auction | End-of-day market-on-close auction |
| **`next_open`** | $t_0 \to$ Next Opening Auction | Overnight shock absorption (AMC prints) |
| **`next_close`** | $t_0 \to$ Next Session Close | 24-hour baseline benchmark |
| **`1d`** | $t_0 \to +24\text{ hours}$ | Rolling 24-hour price discovery |
| **`5d`** | $t_0 \to +5\text{ trading days}$ | Institutional rebalancing & conference call digestion |
| **`1m`** | $t_0 \to +21\text{ trading days}$ | Full monthly fundamental re-rating |

---

## 4. Components & File Manifest

- **`researcher_us/scripts/edge_shadow_engine.py`**:
  - Ingests wire news and regulatory releases with timestamps $t_0$.
  - Ingests high-frequency 5m/15m bars and daily bars for stocks and SPY.
  - Computes 60-day rolling beta ($\beta$) against SPY.
  - Generates excess alpha ($\alpha$) and unit-volatility normalized alpha ($\widetilde{\alpha}$).
  - Maintains `researcher_us/analysis/shadow-ledger.json`.
- **`researcher_us/scripts/edge_grounded_score.py`**:
  - Connects runtime unpriced hunter findings (`hunts/*.json`) to the calibration matrix.
  - Applies symmetric unscaling: $S_j \cdot \kappa_{\tau, L_j} \cdot IV_{\text{live}}$.
  - Emits `edge-scores-grounded.json` with multi-horizon grounded keys (`impact_sum_5m`, ..., `impact_sum_1m`).
- **`researcher_us/analysis/shadow-ledger.json`**:
  - The shared calibration database storing historical wire observations and the empirical response matrix $\kappa_{\tau, L}$.

---

## 5. Usage & Pipeline Commands

### A. Run Shadow Ingestion & Update Calibration Matrix:
```bash
python researcher_us/scripts/edge_shadow_engine.py
```

### B. Score an Edge Run with Symmetric Grounding:
```bash
python researcher_us/scripts/edge_grounded_score.py --run research/2026/09/2026-09-09/edge
```
This generates `edge-scores-grounded.json` containing calibrated impact sums across all 9 liquid horizons alongside raw baseline diagnostics.
