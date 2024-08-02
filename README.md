# Coq tactic timing summary

Script that takes the output of Coq with some Ltac `time` commands and
summarizes by labels and succeed/fail status.

## Demo

```txt
Stats
                        sum  count      mean    max
tactic     success                                 
tc_solve   True     142.033  29517  0.004812  0.908
wp_pures   True     123.621   1688  0.073235  1.028
tc_solve   False     25.462  37264  0.000683  0.199
iFrameHyp  True      24.534   1744  0.014068  0.884
           False     20.885   2235  0.009345  0.199
iFrame any True      16.433    268  0.061317  1.044
```

Notice that "iFrameHyp" has two consecutive lines, one for cases where it
succeeded and the other for failures.

The label "iFrame any" has a space, which is handled correctly.

To get the above log, I wrapped the implementations of three tactics,
`tc_solve`, `iFrameHyp`, and `iFrame` with calls to `time`, then re-compiled.
This produces output with thousands of lines like:

```txt
Tactic call tc_solve ran for 0.017 secs (0.017u,0.s) (success)
Tactic call iFrameHyp ran for 0.018 secs (0.018u,0.s) (success)
Tactic call tc_solve ran for 0.01 secs (0.01u,0.s) (success)
Tactic call iFrameHyp ran for 0.01 secs (0.01u,0.s) (success)
Tactic call tc_solve ran for 0.005 secs (0.005u,0.s) (success)
Tactic call iFrameHyp ran for 0.005 secs (0.005u,0.s) (success)
```
