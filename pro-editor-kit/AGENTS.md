# AGENTS.md — pro-editor-kit

You are inside `pro-editor-kit/`. Follow [START-HERE-FOR-AGENTS.md](START-HERE-FOR-AGENTS.md).
Your model playbook is in [models/](models/). Run `python3 tools/kit.py doctor` first and `python3 -m unittest discover -s tests` after changing any tool.
Tools are Python 3.9+ standard library only, so keep them dependency-free. Every tool change needs a test in `tests/test_tools.py`.
