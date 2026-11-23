"""
Build the Appendix A graphs with pandas, seaborn and matplotlib.

Put this file in the same folder as:
    correctness_tables.md   (test case, category, and the type of error of each program; "None" = passed)
    failure_report.md       (result of each program on each test case: Pass / Wrong output / Timeout,
                             plus a "Passed" row with the number of test cases each program passed)
    case_tables.md          (runtime in ms of the baseline and each program on each test case)

The correctness graphs take the category of each test case from correctness_tables.md and the
results from failure_report.md. Before drawing, the script checks that the two files agree on every
result and that the "Passed" row matches the count; if anything disagrees, it stops and says where.

Run:
    pip install pandas seaborn matplotlib
    python seaborn_figures.py

It writes 16 PNG files (600 dpi, 6.5 in wide) into a folder called "figures":
    fig_A1_task1_correctness.png ... fig_A8_task8_correctness.png
    fig_A9_task1_runtime.png     ... fig_A16_task8_runtime.png
"""
import os
import re

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.patches import Patch

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "figures")
os.makedirs(OUT, exist_ok=True)

PROGRAMS = ["gpt-oss zero-shot", "gpt-oss multi-shot",
            "Qwen2.5-Coder zero-shot", "Qwen2.5-Coder multi-shot"]

# Colours: light = zero-shot, dark = multi-shot; blue = gpt-oss, orange = Qwen2.5-Coder
PROGRAM_COLORS = {"gpt-oss zero-shot": "#a4c2ec", "gpt-oss multi-shot": "#3f78d1",
                  "Qwen2.5-Coder zero-shot": "#eebb9e", "Qwen2.5-Coder multi-shot": "#df7145"}
RESULT_COLORS = {"Pass": "#1f8a4c", "Wrong output": "#c8352e", "Timeout": "#d08a00"}
HATCH = {"Wrong output": "xxxx", "Timeout": "////"}
MODEL_COLORS = {"gpt-oss": "#2a78d6", "Qwen2.5-Coder": "#eb6834"}

# One theme for every figure: white background, light horizontal grid lines
sns.set_theme(style="whitegrid", font="DejaVu Sans", font_scale=0.7,
              rc={"grid.color": "#e6e5e1", "axes.edgecolor": "#8a8984"})


# ---------------------------------------------------------------- 1. Read the .md files
def read_md_tables(filename):
    """Turn every markdown table in the file into a pandas DataFrame.
    Returns {task number: DataFrame}. The task number comes from the heading above each table."""
    tables, task, rows = {}, None, []
    for line in open(os.path.join(HERE, filename), encoding="utf-8"):
        heading = re.search(r"Task (\d+)", line)
        if heading and not line.startswith("|"):
            task, rows = int(heading.group(1)), []
        elif line.startswith("|") and not line.startswith("|---"):
            rows.append([cell.strip() for cell in line.strip().strip("|").split("|")])
            tables[task] = pd.DataFrame(rows[1:], columns=rows[0])   # first row = column names
    return tables


CORRECTNESS = read_md_tables("correctness_tables.md")
FAILURES = read_md_tables("failure_report.md")
RUNTIME = read_md_tables("case_tables.md")


def results_table(task):
    """One row per test case: Test case, Type (category), and the four programs' results.
    Categories come from correctness_tables.md, results from failure_report.md."""
    categories = CORRECTNESS[task]
    report = FAILURES[task]
    passed_row = report[report["Test case"] == "Passed"].iloc[0]
    report = report[report["Test case"] != "Passed"]

    table = categories[["Test case", "Type"]].merge(report[["Test case"] + PROGRAMS], on="Test case")
    if len(table) != len(categories) or len(table) != len(report):
        raise ValueError(f"Task {task}: the two files do not list the same test cases")

    for program in PROGRAMS:
        # correctness_tables.md says "None" where failure_report.md says "Pass"
        expected = categories[program].replace("None", "Pass").tolist()
        for case, mine, theirs in zip(table["Test case"], table[program], expected):
            if mine != theirs:
                raise ValueError(f"Task {task}, test case {case}, {program}: "
                                 f"failure_report.md says {mine!r}, correctness_tables.md says {theirs!r}")
        count = (table[program] == "Pass").sum()
        if str(count) != passed_row[program].split("/")[0]:
            raise ValueError(f"Task {task}, {program}: 'Passed' row says {passed_row[program]}, "
                             f"but {count} test cases are marked Pass")
    return table


# ---------------------------------------------------------------- 2. Correctness figure
def correctness_figure(task, fig_number):
    table = results_table(task)
    table["label"] = table["Test case"] + "  " + table["Type"]       # e.g. "02  Sample"

    # Seaborn wants "long" data: one row per (test case, program) instead of one column per program
    long = table.melt(id_vars=["label"], value_vars=PROGRAMS, var_name="program", value_name="result")
    long["height"] = long["result"].map(lambda r: 1 if r == "Pass" else -1)   # up = passed, down = failed

    fig, (ax_a, ax_b) = plt.subplots(2, 1, figsize=(6.5, 7.0),
                                     gridspec_kw={"hspace": 0.75})

    # (a) One group of four bars per test case
    sns.barplot(data=long, x="label", y="height", hue="program", hue_order=PROGRAMS,
                palette=PROGRAM_COLORS, order=table["label"], width=0.8, saturation=1, ax=ax_a, legend=False)

    # Seaborn draws one "container" of bars per program, in hue_order.
    # Turn each failed bar into a white bar with a hatch in the program's colour.
    for program, bars in zip(PROGRAMS, ax_a.containers):
        results = long[long["program"] == program].set_index("label").loc[table["label"], "result"]
        for bar, result in zip(bars, results):
            if result != "Pass":
                bar.set_facecolor("white")
                bar.set_edgecolor(PROGRAM_COLORS[program])
                bar.set_hatch(HATCH[result])

    ax_a.axhline(0, color="black", linewidth=0.8)
    ax_a.set_ylim(-1.35, 1.35)
    ax_a.set_yticks([1, -1], ["Passed", "Failed"])
    ax_a.tick_params(axis="x", rotation=90, labelsize=6)
    ax_a.set_xlabel("Test case number and category")
    ax_a.set_ylabel("")
    ax_a.grid(axis="x", visible=False)
    ax_a.legend(handles=[Patch(color=PROGRAM_COLORS[p], label=p) for p in PROGRAMS] + [
                    Patch(facecolor="#bdbdbd", label="Plain = passed"),
                    Patch(facecolor="white", edgecolor="#9e9e9e", hatch="xxxx", label="Cross-hatched = wrong output"),
                    Patch(facecolor="white", edgecolor="#9e9e9e", hatch="////", label="Diagonal hatch = timeout")],
                loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=4, frameon=False, fontsize=6.2)

    # (b) How many test cases each program passed, got wrong, or timed out on.
    # countplot counts the rows for us; order/hue_order keep zero counts as empty slots.
    sns.countplot(data=long, x="program", hue="result", order=PROGRAMS,
                  hue_order=["Pass", "Wrong output", "Timeout"], palette=RESULT_COLORS,
                  width=0.8, saturation=1, ax=ax_b, legend=False)
    for bars in ax_b.containers:                       # write the count on top of each bar
        ax_b.bar_label(bars, fontsize=6.5, fontweight="bold", padding=1)
    ax_b.set_xticks(range(4), [p.replace(" ", "\n", 1) for p in PROGRAMS])
    ax_b.set_ylim(0, len(table) + 2.5)
    ax_b.yaxis.get_major_locator().set_params(integer=True)    # whole numbers only on the y-axis
    ax_b.set_xlabel("")
    ax_b.set_ylabel(f"Number of test cases (out of {len(table)})")
    ax_b.grid(axis="x", visible=False)

    fig.legend(handles=[Patch(color=RESULT_COLORS["Pass"], label="Passed"),
                        Patch(color=RESULT_COLORS["Wrong output"], label="Wrong output"),
                        Patch(color=RESULT_COLORS["Timeout"], label="Timeout (over 10 s)")],
               loc="lower center", ncol=3, frameon=False)
    sns.despine(fig)                                     # remove the top and right borders
    fig.subplots_adjust(left=0.10, right=0.98, top=0.91, bottom=0.10)
    fig.savefig(os.path.join(OUT, f"fig_A{fig_number}_task{task}_correctness.png"), dpi=600)
    plt.close(fig)


# ---------------------------------------------------------------- 3. Runtime figure
def runtime_figure(task, fig_number):
    table = RUNTIME[task]
    average = table[table["Test case"] == "Average"].iloc[0]    # the "Average" row of the table
    cases = table[table["Test case"] != "Average"]

    fig, axes = plt.subplots(2, 1, figsize=(6.5, 4.3), sharex=True)
    for ax, model in zip(axes, ["gpt-oss", "Qwen2.5-Coder"]):
        # Only the baseline and this model's correct programs ("-" = program failed, so not timed)
        columns = ["Baseline"] + [f"{model} {s}" for s in ["zero-shot", "multi-shot"]
                                  if cases[f"{model} {s}"].iloc[0] != "-"]
        long = cases.melt(id_vars=["Test case"], value_vars=columns,
                          var_name="program", value_name="runtime")
        long["runtime"] = long["runtime"].astype(float)

        # Legend names include each program's average runtime
        def name(col):
            setting = "Baseline" if col == "Baseline" else col.split(" ")[-1].capitalize()
            return f"{setting} (average {float(average[col]):.2f} ms)"
        long["program"] = long["program"].map(name)
        names = [name(c) for c in columns]

        # hue = colour, style = line and marker: baseline black dashed with dots,
        # zero-shot solid with circles, multi-shot dotted with squares
        colors = {n: ("black" if c == "Baseline" else MODEL_COLORS[model]) for n, c in zip(names, columns)}
        dashes = {n: ((4, 2.5) if c == "Baseline" else "" if "zero" in c else (1.5, 1.2))
                  for n, c in zip(names, columns)}
        markers = {n: ("o" if c == "Baseline" or "zero" in c else "s") for n, c in zip(names, columns)}
        sns.lineplot(data=long, x="Test case", y="runtime", hue="program", style="program",
                     hue_order=names, style_order=names, palette=colors, dashes=dashes,
                     markers=markers, markersize=4, linewidth=1.1, ax=ax)

        ax.set_title(model, loc="left")
        ax.set_ylabel("Runtime (ms)")
        ax.grid(axis="x", visible=False)
        ax.legend(title=None, loc="upper right", ncol=3, frameon=False, fontsize=6.5)
        low, high = ax.get_ylim()
        ax.set_ylim(low, high + (high - low) * 0.22)       # room for the legend above the lines

    axes[1].set_xlabel("Test case")
    sns.despine(fig)
    fig.tight_layout(h_pad=1.2)
    fig.savefig(os.path.join(OUT, f"fig_A{fig_number}_task{task}_runtime.png"), dpi=600)
    plt.close(fig)


# ---------------------------------------------------------------- 4. Make all 16 figures
if __name__ == "__main__":
    for task in range(1, 9):
        correctness_figure(task, task)          # Figures A1-A8
        runtime_figure(task, task + 8)          # Figures A9-A16
        print(f"Task {task} done")
    print("Figures saved in", OUT)
