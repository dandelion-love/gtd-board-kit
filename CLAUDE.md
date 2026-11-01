@AGENTS.md

Claude Code also runs `tools/public_guard.py` as a PreToolUse hook on every Bash call
and GitHub write (`.claude/settings.json`), and wires the git hooks at session start.
