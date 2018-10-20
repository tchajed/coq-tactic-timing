#!/usr/bin/env python3

import re
import pandas as pd
import numpy as np

class TimeReport:
    def __init__(self, tactic, time, success, backtracks):
        self.tactic = tactic
        self.time = time
        self.success = success
        self.backtracks = backtracks

    @classmethod
    def parse(cls, line):
        m = re.match("Tactic call ((?P<tactic>.+) )?" +
                "ran for (?P<time>[0-9.]+) secs.*\\(" +
                ("(?P<result>(success)" + "|"
                    "(failure( after (?P<backtracks>[0-9]+) backtracking)?))") +
                "\\)(\\n)?", line)
        if m is None:
            return None
        tactic = m.group("tactic")
        time = float(m.group("time"))
        result = m.group("result")
        if result == "success":
            success = True
            backtracks = 0
        else:
            success = False
            backtracks = int(m.group("backtracks") or 0)
        return cls(tactic, time, success, backtracks)

    def df_row(self):
        return [self.tactic, self.time, self.success]

    df_header = ["tactic", "time", "success"]

if __name__ == "__main__":
    import argparse
    import sys

    parser = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-t", "--threshold",
            type=float,
            default=0.1,
            help="threshold to print time")
    parser.add_argument("--slow-log",
            dest="slow_log",
            type=bool,
            help="print the slow log")
    parser.add_argument("coq_output",
            type=argparse.FileType(),
            help="file with Coq's output")

    args = parser.parse_args()
    thresh = args.threshold

    reports = []
    for line in args.coq_output:
        rep = TimeReport.parse(line)
        if rep is not None:
            reports.append(rep)
    if not reports:
        sys.exit(0)
    df = pd.DataFrame([rep.df_row() for rep in reports], columns=TimeReport.df_header)
    if args.slow_log:
        slowlog = df[df["time"] > thresh]
        if slowlog.empty:
            print("(no queries slower than {}s)".format(thresh))
        else:
            print(slowlog)
        print()

    tactics = df.groupby(['tactic', 'success'], sort=False)
    print("Stats")
    pd.set_option('display.width', 150)
    aggregated = tactics['time'].agg(['sum', 'count', 'mean', 'std'])
    print(aggregated.sort_values(by='sum', ascending=False))
