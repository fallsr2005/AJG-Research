# Lab 08 - AJG - Nasdaq Historical-Price Evidence

## Purpose

This is the saved historical-price source record for the September 3, 2026 Lab 08 comparison. It preserves the exact Nasdaq API rows used for the AJG, AON, and MRSH price inputs after the provider returned HTTP 200.

## Retrieval method

Nasdaq's historical endpoint returned data when queried with a browser-style `User-Agent` header and a multi-day ISO date range. Direct one-day or headerless links can return a 400 response, so this saved record is the cited price evidence in the Lab 08 report.

Retrieved September 17, 2026 with these read-only commands:

```text
curl.exe -sS -A "Mozilla/5.0" "https://api.nasdaq.com/api/quote/ajg/historical?assetclass=stocks&fromdate=2026-08-01&todate=2026-09-10&limit=100"
curl.exe -sS -A "Mozilla/5.0" "https://api.nasdaq.com/api/quote/aon/historical?assetclass=stocks&fromdate=2026-08-01&todate=2026-09-10&limit=100"
curl.exe -sS -A "Mozilla/5.0" "https://api.nasdaq.com/api/quote/mrsh/historical?assetclass=stocks&fromdate=2026-08-01&todate=2026-09-10&limit=100"
```

Each response reported `status.rCode: 200` and the fields `Date`, `Close/Last`, `Volume`, `Open`, `High`, and `Low`.

## Saved Nasdaq rows for September 3, 2026

| Symbol | Date | Close/Last | Open | High | Low | Volume |
|---|---|---:|---:|---:|---:|---:|
| AJG | 09/03/2026 | $266.66 | $265.81 | $271.27 | $264.69 | 1,499,432 |
| AON | 09/03/2026 | $327.00 | $332.00 | $336.45 | $325.6775 | 1,465,067 |
| MRSH | 09/03/2026 | $188.46 | $188.75 | $191.22 | $187.585 | 1,981,343 |

## Relevant response records

```json
{"symbol":"AJG","date":"09/03/2026","close":"$266.66","volume":"1,499,432","open":"$265.81","high":"$271.27","low":"$264.69"}
{"symbol":"AON","date":"09/03/2026","close":"$327.00","volume":"1,465,067","open":"$332.00","high":"$336.45","low":"$325.6775"}
{"symbol":"MRSH","date":"09/03/2026","close":"$188.46","volume":"1,981,343","open":"$188.75","high":"$191.22","low":"$187.585"}
```

MRSH is the correct price symbol for Marsh on this date. The company changed its NYSE symbol from `MMC` to `MRSH` effective January 14, 2026. [Company symbol-change notice](https://www.marsh.com/en/corp/about/news/marsh-mclennan-to-change-nyse-symbol-to-mrsh.html)
