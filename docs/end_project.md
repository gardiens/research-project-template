<div align="center">

# 🏁 Ending a project
### What I expect when you hand in

</div>

## 📌 What this is

Two things: a repo I can run, and a report I can read in one sitting. This page is the checklist for both. Its twin, `start_project.md`, covers the beginning.

---

## 📦 Delivering the code

### The README

A concise README following the template at the bottom of this repo's README is enough. In three lines (clone, install, run) I should be able to get your code running (the CUDA step excepted).

### One entry point

Everything except visualisation goes through `python train.py args=...`. No `train_v2_final.py`, no `old/` folder, no commented-out blocks. If it is not used, delete it; git remembers.

### The results table

Each line states the config and the checkpoint used to reproduce it, plus roughly how long it takes and on what GPU.

### Before pushing the final version
Run the linter once on the whole repo before pushing the final version:
`pre-commit run --all-files`. If you want type hints without writing them by hand, [RightTyper](https://github.com/RightTyper/RightTyper) infers them from a run, including tensor shapes:

```bash
python3 -m pip install righttyper
python3 -m righttyper --infer-shapes --python-version 3.10 your_script.py [args...]
```

It needs Python 3.12+ to run (a separate env is fine), and `--no-output-files` lets you preview before it edits your files in place. Read the diff: it sometimes types things you did not want typed.

---

## 📝 Writing the report

### What I actually read

Your report should explain what you did, what you found, what did not work, and why you think it did not work. Clearly state your hypotheses and the conclusions you draw from your experiments.

Please do not fill sections with generic ChatGPT-generated text. I would much rather read two honest, precise pages than ten pages of vague or meaningless content.

You are responsible for everything you submit. In particular, be very careful with highly technical claims or details that you do not fully understand yourself. If something is included in the report, you should be able to explain and defend it.

I will pay particular attention to this point, and unsupported or fabricated technical details will be taken very seriously.
### Results section

A structure a colleague gave me, which I now use for most results sections:

> We have CAUSE, which causes PROBLEMS, therefore we (or they) do CONTRIBUTION, and here is
> WHY it solves it.

It looks trivial and it fixes most unclear paragraphs.

Negative results are results. "It didn't work, here is my hypothesis, here is the experiment that would test it" is more useful to me than a good-looking table with no analysis.

### Numbers

One seed is fine for a student project, but say it. If you have several, report mean and std. Don't claim state of the art; compare to the literature and say where you stand.

Put the experimental setup (dataset, splits, model, hyperparameters, compute) in one place so I can find it.

### Figures

All subfigures the same size and aligned, font size at least the text's, axis labels with units, the same color for the same method across figures, with a colorbar. It doesn't change the content, it changes a lot how the report is perceived.

### Last pass

Reread it once as the reader: can someone who did not follow the project understand the first page alone? That page is what most people will read.

---

## 📬 What to hand in

The repo link with the tag, and the report as PDF. If something is unfinished, say it in the
README in a TODO or roadmap section rather than hoping I won't notice. I will. A clear "not done" reads much better than a
silent gap.
