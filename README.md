# P-Stack for GitHub Copilot Chat and CLI

I maintain this Agent Plugins 1.0 package in [`grok08/copilot-pstack-plugin`](https://github.com/grok08/copilot-pstack-plugin). It adapts the upstream P-Stack workflow for GitHub Copilot Chat in VS Code and VS Code Insiders, and for GitHub Copilot CLI. It includes 47 skills, the `poteto-agent` and `comment-sicko` agent profiles, and the `/poteto-mode` command. This is an independent port, not the official Cursor plugin. See [ADAPTATION.md](ADAPTATION.md) for host details and upstream attribution.

## Install in VS Code

In VS Code or VS Code Insiders, run **Chat: Install Plugin From Source** from the Command Palette and enter `https://github.com/grok08/copilot-pstack-plugin`. You can also install it from the Plugins section of the Agent Customizations editor. Plugin support must be enabled with `chat.plugins.enabled`.

In Copilot Chat, use `/poteto-mode` to start the P-Stack workflow. Plugin skills appear with the plugin prefix, such as `/pstack:how` or `/pstack:swarm`.

JetBrains IDEs use GitHub Copilot Chat too, but their customization support differs by client. GitHub lists Agent Skills as a preview feature for JetBrains. This repository has not verified installation of the Agent Plugins package or its Copilot-specific agents and commands in JetBrains, so it does not claim full JetBrains plugin support.

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

## Update an installation

For a marketplace installation, refresh the catalog and update P-Stack:

```sh
copilot plugin marketplace update pstack
copilot plugin update pstack@pstack
```

Restart Copilot CLI after the update. For each release, keep the versions in `plugin.json` and `.github/plugin/marketplace.json` in sync with the release tag (for example, tag `v1.0.3` uses manifest version `1.0.3`). A Git tag alone does not update the marketplace catalog.

## Try a local checkout in Copilot CLI

From a local checkout, run `copilot --plugin-dir .` in the repository directory.

This loads the plugin from that checkout, not from the marketplace. To run a tagged release, fetch the tags, check out the desired tag, and start Copilot CLI again:

```sh
git fetch origin --tags
git switch --detach vX.Y.Z
copilot --plugin-dir .
```

Use `/poteto-mode` to start the P-Stack workflow. You can also ask Copilot to apply a skill such as `how`, `swarm`, or `principle-prove-it-works`.

## Validate

With Python 3.10 or later, run:

```sh
python scripts/port_upstream.py --validate
python -m unittest discover -s scripts -p "test_*.py"
```

Run the bundled workflow script checks with Bun:

```sh
cd skills/poteto-mode/scripts
bun run typecheck
bun run test
```

## Source and license

The source is the P-Stack plugin from [`cursor/plugins`](https://github.com/cursor/plugins/tree/main/pstack), snapshot `adf3218ca2f5b9971eedc07a76bef22df7701539`. The upstream MIT license is preserved in [LICENSE](LICENSE). Copilot host adaptations are documented in [ADAPTATION.md](ADAPTATION.md).
