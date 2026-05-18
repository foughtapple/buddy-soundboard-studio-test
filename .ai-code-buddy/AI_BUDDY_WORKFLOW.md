# AI Buddy Workflow

Active repo: `foughtapple/buddy-soundboard-studio-test`
Branch: `main`
Project type: `python_windows`
Allowed modification scope: only this repository unless the user explicitly changes the active project in AI Code Buddy.

Required ChatGPT process:

1. Read and update `.ai-code-buddy/project-requirements.txt` if the request changes persistent requirements.
2. Newer user requirements override older contradictory requirements.
3. Make a short plan.
4. Apply changes only in this repo.
5. Treat console/build/test output from AI Buddy as debugging input.
6. Use the project type in `.ai-code-buddy/project.json` to choose build/test/run/package conventions.
7. For large work, end intermediate batches with `AI_BUDDY_CONTINUE_EDITING`.
8. Finish completed repo changes with `AI_BUDDY_READY_TO_PULL`.

