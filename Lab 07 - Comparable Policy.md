# Lab 07 - Comparable-Company Policy and Implied Range

## Define/Discover: what P/E means

P/E equals price per share divided by annual diluted earnings per share (EPS). Price per share is the market price of one common share at the chosen date, and diluted EPS is annual earnings allocated across diluted shares. The result is the price investors are paying for one dollar of annual earnings.

P/E makes companies of different sizes easier to compare because it puts price and earnings on a per-share basis. It complements a DCF: the DCF asks what future cash-flow assumptions imply, while P/E asks what value the target would have if investors priced its earnings like those of similar businesses.

A P/E comparison is meaningful only when the peers have comparable business economics, positive earnings, and a consistent earnings definition. It can be misleading when earnings are negative, unusually high or low, adjusted inconsistently, or affected by different growth, risk, leverage, geography, or business mix. Therefore, a lower P/E is a question to investigate, not automatic evidence of a better investment.

## Peer policy before seeing the multiples

**Policy.** For this training case, consider publicly traded franchised vehicle retailers with new and used vehicle sales, meaningful parts/service operations, positive annual earnings, and consistent total GAAP diluted EPS. Assess how each company earns money, along with scale, geography, and financing activities, before using a multiple.

| Company | Role | Decision | Rationale and qualification |
|---|---|---|---|
| Asbury Automotive (ABG) | Target | Exclude from peer set | ABG is the company being valued, so its own P/E must not enter the peer median. |
| AutoNation (AN) | Candidate peer | Use | It shares the franchised vehicle-retail and service/parts economics required by the policy. Its AutoNation Finance activity is a relevant difference to monitor. |
| Group 1 Automotive (GPI) | Candidate peer | Use with qualification | It fits the core business policy, but its U.S./U.K. footprint and 2024 acquisition of 54 Inchcape dealerships make it a qualified rather than identical peer. |

This policy is stated before the numerical comparison. The qualifications explain uncertainty; they do not justify changing the peer set merely to obtain a preferred price.

## Frozen training-case inputs

This is a retrospective training comparison: December 31, 2024 closing prices are paired with FY2024 total GAAP diluted EPS that was reported afterward. It is not a point-in-time trading claim.

| Company / role | December 31, 2024 closing price | FY2024 total GAAP diluted EPS |
|---|---:|---:|
| Asbury Automotive (ABG), target | $243.03 | $21.50 |
| AutoNation (AN), peer | $169.84 | $16.92 |
| Group 1 Automotive (GPI), qualified peer | $421.48 | $36.81 |

Formulas used:

```text
Peer P/E = peer price per share / peer annual diluted EPS
Peer-implied ABG price = peer P/E * ABG annual diluted EPS
Peer median P/E = median of valid peer P/E multiples
```

All calculations retain full precision until the displayed multiple is rounded to six decimals and the displayed price is rounded to cents.

## Implementation and validation

| Check | Calculation | Result |
|---|---|---:|
| AutoNation P/E | $169.84 / $16.92 | 10.037825x |
| Group 1 P/E | $421.48 / $36.81 | 11.450149x |
| ABG observed P/E (comparison only) | $243.03 / $21.50 | 11.303721x |
| Peer median P/E | (10.0378250591 + 11.4501494159) / 2 | 10.743987x |
| ABG price using AN | 10.0378250591 * $21.50 | $215.81 |
| ABG price using GPI | 11.4501494159 * $21.50 | $246.18 |
| ABG peer-implied range | Low to high peer-implied price | $215.81 to $246.18 |
| ABG at peer median | 10.7439872375 * $21.50 | $231.00 |

The two-peer median is the midpoint of two observations, so it is sensitive to each peer. It should not be treated as a reliable estimate merely because it is called a median.

## Evolve: remove one peer

GPI has the higher P/E, so removing it should lower the median-implied value. With GPI removed, AN is the only valid peer:

| Check | Result |
|---|---:|
| Remaining AN reference estimate | $215.81 |
| Change from the two-peer median estimate | -$15.18 |

The result falls because the remaining AN multiple is lower than the original two-peer median. One peer provides a reference estimate, not a range, because there is no longer a low-to-high set of multiple-derived prices.

## Reflection

P/E compares the market price paid for each dollar of annual earnings. AutoNation is included because it fits the core franchised vehicle-retail and service/parts policy, while Group 1 is included with an explicit geography and acquisition qualification. The ABG peer-implied range is a conditional comparison, not proof that ABG is fairly valued or an investment recommendation. It depends on the selected peers, the total GAAP diluted-EPS convention, and whether the stated business differences justify the observed multiples.

This is not financial advice

## Course sources

- [Lab 07: Comparable-Company Policy and Implied Range](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-04/lab-07-comparable-policy.md)
- [Training-case comps worked example](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-04/teach-comps-worked-example.md)
