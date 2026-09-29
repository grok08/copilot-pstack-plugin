# P-Stack for GitHub Copilot CLI

I maintain this GitHub Copilot CLI plugin in [`grok08/copilot-pstack-plugin`](https://github.com/grok08/copilot-pstack-plugin). It adapts the upstream P-Stack workflow and includes 47 skills, the `poteto-agent` and `comment-sicko` agent profiles, and the `/poteto-mode` command. This is an independent port, not the official Cursor plugin. See [ADAPTATION.md](ADAPTATION.md) for the adaptation details and upstream attribution.

## Install from my marketplace

Add my marketplace to GitHub Copilot CLI:

```sh
copilot plugin marketplace add grok08/copilot-pstack-plugin
```

Browse and install P-Stack:

```sh
copilot plugin marketplace browse pstack
copilot plugin install pstack@pstack
```

The marketplace name and plugin name are both `pstack`. I publish the catalog in [.github/plugin/marketplace.json](.github/plugin/marketplace.json).

To install P-Stack directly from my repository without adding the marketplace, run:

```sh
copilot plugin install grok08/copilot-pstack-plugin
```

## Try a local checkout

From a local checkout, run `copilot --plugin-dir .` in the repository directory.

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
