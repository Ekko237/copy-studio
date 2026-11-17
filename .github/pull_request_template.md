## Change

Describe the problem, what changed, and any related issue.

## Checklist

- [ ] This PR targets `main` and stays focused on one change.
- [ ] Documentation matches the behavior; shared README instructions agree in both languages.
- [ ] No secrets, private brand facts, personal information, or generated artifacts are included.
- [ ] For behavior changes, I described a sanitized manual run and checked the approval gates (or explained why this does not apply).
- [ ] I followed [CONTRIBUTING.md](https://github.com/Ekko237/copy-studio/blob/main/CONTRIBUTING.md) and the [Code of Conduct](https://github.com/Ekko237/copy-studio/blob/main/CODE_OF_CONDUCT.md).
- [ ] I ran all six CI check commands below successfully.

```bash
python3 scripts/check_frontmatter.py
python3 scripts/check_skill.py
bash -n install.sh
bash -n scripts/install-deps.sh
python3 -m py_compile scripts/check_skill.py scripts/check_frontmatter.py
python3 -c "import json, pathlib; files=['.claude-plugin/plugin.json', '.claude-plugin/marketplace.json', '.codex-plugin/plugin.json', '.agents/plugins/marketplace.json']; [json.loads(pathlib.Path(p).read_text(encoding='utf-8')) for p in files]; print('manifests ok')"
```

Check results or limitations:
