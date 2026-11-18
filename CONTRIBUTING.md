# Contributing

Thanks for helping improve Copy Studio. Follow the [Code of Conduct](CODE_OF_CONDUCT.md), and use [issues](https://github.com/Ekko237/copy-studio/issues) for bugs and feature requests.

## Set up and run locally

Copy Studio is a Claude Code and Codex skill. You need git, bash, tar, a network connection, and one of those agents; the checks also need Python 3.

From the checkout root, install the skill, its five dependencies, and the slash command using the command in [README.md](README.md#from-a-checkout):

```bash
bash install.sh
```

This writes to both `~/.claude` and `~/.codex`. Set `COPY_STUDIO_CLAUDE_HOME` and `COPY_STUDIO_CODEX_HOME` for custom destinations. If you only need the five dependencies:

```bash
bash scripts/install-deps.sh
```

Open a new Claude Code or Codex session and run the README's verification prompt:

```text
/copy-studio an Instagram post for the new template library
```

Expect Stage 0, a strategy with no candidate copy, and an approval gate. For real jobs, prepare your own fact base and channel calibration file as described in the README; keep private material out of contributions.

## Checks

Run every command below from the checkout root. These are the exact commands in [.github/workflows/check.yml](.github/workflows/check.yml).

```bash
python3 scripts/check_frontmatter.py
python3 -m unittest scripts.test_check_frontmatter
python3 scripts/check_skill.py
bash -n install.sh
bash -n scripts/install-deps.sh
python3 -m py_compile scripts/check_skill.py scripts/check_frontmatter.py
python3 -c "import json, pathlib; files=['.claude-plugin/plugin.json', '.claude-plugin/marketplace.json', '.codex-plugin/plugin.json', '.agents/plugins/marketplace.json']; [json.loads(pathlib.Path(p).read_text(encoding='utf-8')) for p in files]; print('manifests ok')"
```

Python compilation creates `scripts/__pycache__/`; remove generated files before submitting.

## Branches and pull requests

- Work on a focused topic branch and target `main` with your pull request.
- Explain the problem, the change, and which checks you ran. For behavior changes, describe a manual run and its approval gates using sanitized material.
- Keep English and Chinese README instructions consistent when changing shared behavior. Do not include secrets, private brand facts, or personal information.
- If you change folder structure, update the README tree in the same PR.
- Follow the existing release format in `CHANGELOG.md`: dated version headings and `v<version>` release links. For release changes, keep `metadata.version` in `skills/copy-studio/SKILL.md`, both plugin manifest versions, and the entry in `.claude-plugin/marketplace.json` aligned. Avoid unrelated version changes.
