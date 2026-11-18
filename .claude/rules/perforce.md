# Perforce checkout before edit

Applies when a file edit fails because it is not checked out, is read-only, or is outside the writable workspace.
Background: [`Feature_PerforceIntegration.md`](../../Features/Feature_PerforceIntegration.md).

1. **Stop.** Don't try to work around the block.
2. **Tell the user** which file(s) need checkout (full path) and what you intended to change.
3. **Wait** for confirmation that checkout is done, then edit with normal tools (`Edit`, `Write`).

## No workarounds

- Shell one-liners, Node/Python patch scripts, or other indirect writes that bypass the write denial
- Repeated retries hoping permissions changed
- Editing a copy elsewhere and asking the user to merge (unless they explicitly want that)

Example, if `d:\p4\...\sparrowTools.py` returns "Write permission denied":

> `sparrowTools.py` needs to be checked out in Perforce before I can apply the resolution fix. Check it out and let me know when ready.

Then apply the planned edit after the user confirms.
