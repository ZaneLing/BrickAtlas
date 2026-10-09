# BrickPlan 1.1 validation

- Semantic: 17 tests passed, including all goal tables and exact mandatory order.
- HTTP: 12 episodes and 39 responses passed; 12 sessions recovered after restart.
- Browser: 6 full/repair sessions passed through actual buttons; replay, exports, probe identity, desktop/mobile layout, and no page exceptions checked.
- Browser runtime: Playwright, headless firefox 141.0. Local Chrome launch timed out before navigation; the installed Firefox completed the suite.
- Geometry/graph: 342,704 states, 2,843,080 directed transitions; no UNKNOWN geometry.
- Versioned CLI: oracle evaluation covers all 12 episodes; release and transition certificates are bound to the report and checked during freezing.
- Base preservation: every original 1.0 artifact hash checked.

These are software validation controls. No paid model evaluation or human study was run.

| Control | Complete success | Repair completion |
| --- | ---: | ---: |
| attach-only | 3/12 | 0/3 |
| fault-and-recover | 12/12 | 3/3 |
| oracle | 12/12 | 3/3 |

Reports and screenshots: `tem/brickplan-v1.1/validation/`. The acceptance snapshot is packaged in `release-check.json`. See the protocol and appendix for physical and statistical limits.
