# SUN Failure Modes

Scope: v2 diagnostics aggregate the existing SUN v1 seen-test rule predictions by SUN class label. They are a portability stress test, not a competitive zero-shot learning benchmark.

Classes summarized: 645. Mean class coverage: 0.0760. Mean class conflict rate: 0.9236.

## Lowest Coverage Classes

- abbey (n=4): coverage=0.0000, conflict=1.0000
- access road (n=4): coverage=0.0000, conflict=1.0000
- airfield (n=4): coverage=0.0000, conflict=1.0000
- airplane cabin (n=4): coverage=0.0000, conflict=1.0000
- airport airport (n=4): coverage=0.0000, conflict=1.0000
- airport entrance (n=4): coverage=0.0000, conflict=1.0000
- airport terminal (n=4): coverage=0.0000, conflict=1.0000
- alcove (n=4): coverage=0.0000, conflict=1.0000
- amusement arcade (n=4): coverage=0.0000, conflict=1.0000
- amusement park (n=4): coverage=0.0000, conflict=1.0000

## Highest Conflict Classes

- abbey (n=4): conflict=1.0000, coverage=0.0000
- access road (n=4): conflict=1.0000, coverage=0.0000
- airfield (n=4): conflict=1.0000, coverage=0.0000
- airplane cabin (n=4): conflict=1.0000, coverage=0.0000
- airport airport (n=4): conflict=1.0000, coverage=0.0000
- airport entrance (n=4): conflict=1.0000, coverage=0.0000
- airport terminal (n=4): conflict=1.0000, coverage=0.0000
- alcove (n=4): conflict=1.0000, coverage=0.0000
- amusement arcade (n=4): conflict=1.0000, coverage=0.0000
- amusement park (n=4): conflict=1.0000, coverage=0.0000

## Interpretation

SUN remains reported as a stress-test/portability result. The diagnostics show that low coverage and high conflict are class-dependent, so v2 does not strengthen the manuscript into a competitive SUN claim.
