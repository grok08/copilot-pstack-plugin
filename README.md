# P-Stack for GitHub Copilot CLI

This repository packages a GitHub Copilot CLI port of the upstream P-Stack workflow. It includes 47 skills, the `poteto-agent` and `comment-sicko` agent profiles, and the `/poteto-mode` command. It is an independent compatibility port, not the official Cursor plugin. See [ADAPTATION.md](ADAPTATION.md) for the port details.

## Install from a GitHub repository

After publishing this repository, replace `OWNER/REPO` with its GitHub path:

```sh
copilot plugin install OWNER/REPO
```

To add this repository's marketplace instead, run:

```sh
copilot plugin marketplace add OWNER/REPO
copilot plugin marketplace browse pstack
copilot plugin install pstack@pstack
```

The marketplace is defined in `.github/plugin/marketplace.json`. The marketplace name is `pstack`.

## Try a local checkout

```sh
copilot --plugin-dir /path/to/copilot-pstack-plugin
```

Use `/poteto-mode` to start the P-Stack workflow. You can also ask Copilot to apply a skill such as `how`, `swarm`, or `principle-prove-it-works`.

## Validate

With Python 3.10 or later, run:

```sh
python scripts/port_upstream.py --validate
```

Run the bundled workflow script checks with Bun:

```sh
cd skills/poteto-mode/scripts
bun run typecheck
bun run test
```

## Source and license

The source is the P-Stack plugin from [`cursor/plugins`](https://github.com/cursor/plugins/tree/main/pstack), snapshot `adf3218ca2f5b9971eedc07a76bef22df7701539`. The upstream MIT license is preserved in [LICENSE](LICENSE). Copilot CLI changes are documented in [ADAPTATION.md](ADAPTATION.md).
