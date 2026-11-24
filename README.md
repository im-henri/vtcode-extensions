# VTCode Extensions

The official VTCode extension marketplace. VTCode always includes this
marketplace in the **Extensions** sidebar; nothing needs to be configured.

The marketplace is only an index: [`marketplace.json`](marketplace.json) lists
the GitHub repositories that hold each extension. Extension code, versions and
packages live in those repositories, and VTCode installs from their GitHub
releases exactly as it does for a pasted repository link.

## Format

```json
{
  "schemaVersion": 1,
  "name": "VTCode Official",
  "description": "Extensions maintained by the VTCode project.",
  "extensions": [
    {
      "id": "vtcode.hex-editor",
      "repository": "https://github.com/im-henri/vtcode-ext-hex-editor",
      "name": "Hex Editor",
      "description": "Inspect and edit binary files…"
    }
  ]
}
```

| Field | Required | Meaning |
| --- | --- | --- |
| `schemaVersion` | yes | Always `1`. VTCode ignores indexes with a version it does not know. |
| `name`, `description` | no | Shown for the marketplace as a whole. |
| `extensions[].id` | yes | The `id` from the extension's `extension.json`. VTCode uses it to tell whether the extension is already installed. |
| `extensions[].repository` | yes | `https://github.com/<owner>/<repo>`. The single source of truth: versions, packages and checksums come from its releases. |
| `extensions[].name`, `extensions[].description` | no | Display text, so the sidebar can list extensions without contacting every repository. Keep them in step with `extension.json`. |

Entries are sorted by `id`. Versions are deliberately **not** stored here:
VTCode reads them from each repository's releases, so publishing a release is
all an extension needs to do to ship an update.

## Adding an extension

The repository must publish semantic-version GitHub releases (`v1.2.3`)
containing a `vtcode-extension.zip` asset. Then add an entry to
`marketplace.json`, keep the list sorted, and check it:

```sh
python scripts/validate.py
```

## Other marketplaces

Any GitHub repository with a `marketplace.json` in this format can be added to
VTCode through the `extensions.marketplaces` setting:

```json
{ "extensions.marketplaces": ["https://github.com/someone/their-marketplace"] }
```
