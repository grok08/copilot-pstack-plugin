### Worktree and simulator cleanup

**You own the disk and the safety gate.** Prune merged or abandoned git worktrees and stale iOS simulators to reclaim space. Deletion is irreversible, so every step guards against deleting something in use or holding uncommitted work.

1. Snapshot and audit. Record available disk usage, then run `scripts/worktree-audit.sh` (principle-build-the-lever). It reads paths from `git worktree list`, never hand-typed, because worktrees can be nested or stored outside the repository. It classifies each worktree by size, age, merge state, uncommitted work, and PR state, then suggests a bucket. It cannot determine whether a Copilot session is still using a worktree.
2. The bucket is advice, not permission. Check each candidate against the active client's session list or ask the user which sessions they are keeping. Do not treat `safe` as evidence that no session is using a worktree.
3. Verify usage before deleting. For every candidate, check accessible session status and ask the user when the active client does not expose enough information. Do not infer session activity from a guessed transcript path. An agent may have spawned work in a sibling worktree that is not obvious from its name.
4. Pause on irreversible loss. `wip:N` is N tracked uncommitted edits. Show the diff and get a decision first, since removing a clean worktree is recoverable from its branch but uncommitted work is gone. `scratch:N` is untracked content; identify the files before removal. Per Autonomy, clean and merged and not in use may proceed. `wip` and in-use worktrees require a pause.
5. Prune the confirmed set. Per path, `git worktree remove --force <path>`. If the directory survives on ignored build artifacts, remove only that confirmed path, then run `git worktree prune`. Branch refs survive, so no commits are lost. Confirm disk usage and re-list the worktrees.
6. Simulators and other reclaimers. On macOS, stale iOS simulators can be listed and removed with `xcrun simctl`; inspect targets before deleting. More when needed: Xcode `DerivedData` and `iOS DeviceSupport`, package caches, and other named build caches. Clear only caches the user has not said to keep. Use OS-specific disk and cache tools rather than assuming macOS paths on other platforms.

This is the one playbook that deletes user state with no code review to catch a slip, so the gates above are the review.

**Reply:** report disk usage before and after when available, worktrees pruned, and a one-line reason for each held back (in-use, uncommitted work, or missing session status).
