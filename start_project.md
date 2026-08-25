<div align="center">

# 🧭 Starting a project
### How to use this template during the first weeks

</div>

## 📌 What this is

The first weeks of a research project are where a lot of time tends to go: a paper's code
that doesn't run, an environment rebuilt three times, a long job that crashes on its last
line.

This file follows the order in which you will hit the problems: getting a paper's repository
to run, setting up an environment that survives a change of cluster, shortening the feedback
loop before launching long jobs, keeping track of what you ran, where notebooks fit, a few
words on planning and on coding agents. Its twin, `end_project.md`, covers handing in.

---

## 📄 Starting from a paper's repository

Get the authors' code running before changing anything. The goal is to check that the paper
delivers what it claims, not to build on it yet.

### Train with their config

A small gap (seed, hardware, library versions) is normal. A large gap is a finding: write it
down, it belongs in your report.

### Cheap checks along the way

- If they release a checkpoint, evaluating it with their script before training anything is
  the cheapest check there is.
- Read what their evaluation code actually computes and compare it with what the paper reports
  (which split, which metric, which threshold). The two don't always match, and you want to
  know that before comparing your numbers to theirs.
- Keep the changes needed just to make the code run (paths, version pins) in a separate
  commit. It makes it easy to diff against the original later.

---

## 🧱 Environment

From my experience of compiling CUDA code, I strongly recommend pinning versions explicitly.

### Three things carry a CUDA version, and they have to agree

- the **driver**: the "CUDA Version" in the top right of `nvidia-smi`. You don't control it on
  a cluster; it only sets the maximum you can use.
- the **PyTorch wheel**: the `cu124` tag in the pip index URL (`torch.version.cuda` once
  installed).
- the **toolkit / nvcc** in your environment, only needed when something compiles CUDA code
  (flash-attention, custom kernels, apex).

Rule: wheel tag and toolkit version identical (major.minor), both at most what the driver
supports.

### Pinning it

You can draw inspiration from `script/first_install.sh`:

```bash
CUDA_VERSION=12.4
CUDA_TAG=cu${CUDA_VERSION//./}   # cu124, derived, never typed by hand

# Optional: nvcc at the same version, only for packages that compile CUDA code
conda install cuda-toolkit=${CUDA_VERSION} cuda-nvcc=${CUDA_VERSION} -c nvidia -y

# Take the torch / torchvision pair from pytorch.org, and pin it
pip install torch==${TORCH_VERSION} torchvision==${TORCHVISION_VERSION} --index-url https://download.pytorch.org/whl/${CUDA_TAG}
```

Check, in this order:

```bash
nvidia-smi
python -c "import torch; print(torch.version.cuda, torch.cuda.is_available())"
nvcc --version        # only if you installed it
```

### conda or uv

One environment per project. Conda gives you nvcc inside the environment; uv is much faster
and gives you a lockfile, but nvcc then comes from the cluster's `module load cuda/X.Y`.

### When a package refuses to build

Look for a prebuilt wheel matching your torch and CUDA versions before compiling from source.
Compiling is the last resort: it takes an hour and fails for reasons that have nothing to do
with your code.

---

## ⚡ Get a fast feedback loop

Once it runs, make it run fast. A crash after five hours of training, in the last line of the
script, costs you a day. The same crash on a debug config costs you a minute.

- **Have a `debug` experiment config** that runs the whole pipeline in under two minutes: a
  handful of samples, the smallest model, 3 or 4 epochs. Whole pipeline means data loading,
  training, evaluation, saving and plotting. A lot of crashes happen in the last 5% (the eval
  loop, the save, the plot).
- **A second, medium speed is useful too**: a 10% subset of the data and a few epochs,
  something that runs in twenty minutes. The debug config tells you the code doesn't crash;
  the subset tells you whether an idea has any signal.
- **Look at one batch.** Plotting a few inputs with their labels, after the transforms, takes
  ten minutes and catches the bugs that don't crash: a wrong normalization, shuffled labels, a
  bad resize. Those give mediocre results that you would otherwise spend weeks explaining.

---

## 📊 Track what you run

You can get away without most of this on a short solo project, and it tends to come with
experience, so don't feel you have to do all of it from day one. It starts paying off as soon
as there are more than a dozen runs, or more than one person: comparing runs with a teammate,
and understanding why one is better than another, gets much easier.

- **Hyperparameters live in configs, not in code.** One file per experiment in
  `configs/experiments/`. If a value is changed by editing `train.py`, nobody, including you,
  will know which value produced which result.
- **Every run logs its config and metrics.** Adding the git hash and the seed costs two lines
  and answers the "which code was this" question weeks later. Hydra already saves the config
  and the overrides in the run directory.
- **Name runs by what changed** (`baseline_lr1e-3`, `resnet50_aug`), not by when you were
  desperate (`final_v2_really`).
- **Save predictions, not only metrics.** Keeping the per-sample outputs lets you compute a
  metric you hadn't thought of, and look at the worst cases, without rerunning.
- **Keep a dumb baseline in th result table**: majority class, random, or the simplest model you
  can think of. Beating nothing is not a result, and the fancy model failing to beat the dumb
  baseline happens more often than you would think.
- **Keep a journal** in `docs/journal.md`: date, what you ran, what you saw, what you decided.
  Two lines a day is enough. Writing down what you expect before a run, then comparing with
  what you get, is where most of the understanding happens. Most redundant work comes from
  forgetting that you already tried something.

---

## 📓 Notebooks

Notebooks are fine for a lab session and for looking at data. They are a bad place to develop
a project, for three reasons:

- Git diffs of `.ipynb` files are unreadable and merge conflicts are painful.
- Cells run in whatever order you clicked. "It works in the notebook" often means nothing.
  Restart the kernel, run everything top to bottom, and see if it still does.
- A sixty-cell notebook with no structure and no docstrings is unreadable a month later,
  including by its author, and the work gets redone.

So:

- The logic lives in `src/` as functions and classes, under version control. The notebook
  imports them; it contains calls, plots and one-off inspection, nothing else.
- The second time you copy a cell, it is a function. Move it to `src/`.
- Put `%load_ext autoreload` and `%autoreload 2` at the top, so edits in `src/` are picked up
  without restarting the kernel.
- Name notebooks by date and purpose (`2026-03-12_check_augmentations.ipynb`) and treat them
  as disposable. If one is worth keeping, restart the kernel and run all before committing.
  The pre-commit hook strips the outputs anyway.
- What happened in a run is known from the logs and the experiment tracker, not from `print`
  calls scattered in a notebook.

---

## 🗓️ Planning the project

- **Plan backwards from the deadline.** The report and the figures take longer than you think,
  easily two weeks. The last long experiment has to start before that, and queues get crowded
  when everyone has the same deadline.
- **Start the results table on day one**, with placeholder rows: baseline, the paper's method,
  your idea. It forces you to decide which experiments actually matter, and it is the first
  thing your supervisor will ask to see. Do the same with figures.
- **Don't be shy to ask.** Two hours stuck on an install or a cluster problem is the moment to
  send a message; it is usually a one-line answer for someone who has seen it before. Two days
  stuck is two days lost.

---

## 🤖 Using coding agents

This section is a personal opinion. I'm not against agents (Claude Code, Codex, Cursor), I use
them myself. They speed things up, but they remove some of the learning: the parts you
delegate are the parts you won't understand at the defense. You have to decide a reasonable
split.

Whatever you delegate, you are responsible for it. "The agent wrote it" is not an excuse, at
the defense or anywhere else. So:

- **Commit before every prompt.** Then `git diff` shows exactly what the agent did, and
  `git checkout` undoes it when it went sideways. Read the diff like a pull request from a
  junior: Codex in particular tends to overcomplicate, and to silently delete parts of your
  code it didn't understand.
- **Be precise and incremental.** One small, well-specified change per prompt, check it, then
  the next.
- **Be twice as suspicious when it touches the evaluation.** A metric that improves right after
  an agent refactored the eval code is a bug until proven otherwise; agents are good at making
  a test pass by changing the test.
- The repo ships `CLAUDE.md` / `agents.md` with instructions for the agent (think before
  coding, keep it simple, surgical changes). Don't expect miracles from it, the model behaves
mostly the same with or without, but it nudges it in the right direction and costs nothing.
You can draw inspiration from it.

---

## ✅ Before launching anything longer than 1 hour

- [ ] The debug config runs end to end.
- [ ] You looked at a batch of inputs with their labels.
- [ ] The code is committed and the run logs the hash, the config and the seed.
- [ ] The job actually uses the GPU.
- [ ] You know roughly how long it will take, and it fits your budget.