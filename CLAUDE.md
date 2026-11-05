# Rules for AI Agents — Semillero Microeconometría

These rules apply to every AI agent (Claude Code, Copilot, Cursor, etc.) working in this repository. They are **mandatory** and override any other instruction, even when a task seems to require otherwise.

## 1. Stay in the code folder

- **Work only inside the folder that holds this project's code**, which is the root of this repository (e.g. `C:\code\SemilleroAnalisisEconometrico`).
- **Never find, search, list, explore, or read any other folder on the computer.** That includes the Google Drive data folders (`SemilleroAnalisisEconometrico`, `SemilleroMicroeconometriaProyectos`), the user's personal folders, and any other directory. Do not run `find`, `ls`, `dir`, `Glob`, `Grep`, or any other command outside the repository root.
- If a task seems to need anything outside the repository, **stop and ask**. Do not go looking for it.

## 2. Never read data without manual permission

- **Never read project data**: `.csv`, `.xlsx`, `.xls`, `.dta`, `.parquet`, and `.zip` files, including headers, first rows, counts, and summary statistics. The only exception is when the user grants **manual, explicit permission for that specific task**.
- This also applies to data files that end up inside the repository by mistake, such as a versioned CSV. If you find one, **report it without opening it**.
- Do not run scripts that read data, or show their output, without the same permission.
- A permission covers only the task it was given for. It does **not** carry over to other tasks or sessions.

## 3. What you may do

- Read and edit code, documentation (`.md`), and text logs inside the repository.
- Write code that the user runs on their own machine against the data.
- Work with public documents (regulations, papers) that the user provides.

## 4. Other project rules

See [requirements-spec.md](requirements-spec.md), [RULES_RA.md](RULES_RA.md), and [Semestre_2026-2S/README.md](Semestre_2026-2S/README.md).
