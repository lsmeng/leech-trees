"""Summarize a run_*.out file from forced_family: totals, capped inventory,
witness check.  Usage: analyze.py RUN.out [SHAPES.txt]"""
import sys
import re


def main():
    path = sys.argv[1]
    shapes = None
    if len(sys.argv) > 2:
        shapes = [l.strip() for l in open(sys.argv[2])]
    done = capped = found = 0
    tot_nodes = 0
    max_nodes = 0
    capped_ids = []
    wit = []
    for line in open(path):
        if line.startswith("RES"):
            m = dict(p.split("=") for p in line.split()[1:])
            done += 1
            tot_nodes += int(m["nodes"])
            max_nodes = max(max_nodes, int(m["nodes"]))
            if m["capped"] == "1":
                capped += 1
                capped_ids.append(int(m["id"]))
            found += int(m["found"])
        elif line.startswith("WITNESS"):
            wit.append(line.strip())
    print(f"{path}: shapes done {done}, capped {capped}, labelings found {found}, "
          f"total nodes {tot_nodes:,}, max nodes/shape {max_nodes:,}")
    if wit:
        print("!!!!!!!! WITNESSES FOUND !!!!!!!!")
        for w in wit:
            print(w)
    if capped_ids and shapes:
        out = path.replace(".out", ".capped_shapes.txt")
        with open(out, "w") as fh:
            for i in capped_ids:
                fh.write(shapes[i] + "\n")
        print(f"  capped shapes -> {out}")
    return capped_ids


if __name__ == "__main__":
    main()
