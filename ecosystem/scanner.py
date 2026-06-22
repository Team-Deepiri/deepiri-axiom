"""Orchestrate full ecosystem scan."""

from __future__ import annotations

from pathlib import Path

from ecosystem.apps import detect_apps, tools_for_install
from ecosystem.devices import detect_device
from ecosystem.manifest import EcosystemManifest, load_manifest, save_manifest
from ecosystem.providers import detect_providers
from ecosystem.repos import repo_links, repos_markdown, scan_sibling_repos


def scan_ecosystem(
    anchor: Path,
    *,
    write: bool = False,
) -> EcosystemManifest:
    """Scan device, providers, apps, and sibling repos; optionally persist manifest."""
    anchor = anchor.resolve()
    device = detect_device()
    providers = detect_providers()
    apps = detect_apps()
    repos = scan_sibling_repos(anchor)
    links = repo_links(repos)
    recommended = sorted(tools_for_install(apps))

    manifest = EcosystemManifest(
        device=device.to_dict(),
        providers=[p.to_dict() for p in providers],
        apps=[a.to_dict() for a in apps],
        repos=[r.to_dict() for r in repos],
        links=links,
        recommended_tools=recommended,
    )

    if write:
        save_manifest(anchor, manifest)

    return manifest


def ecosystem_context_markdown(anchor: Path) -> str:
    """Build combined markdown block for installer prompt injection."""
    manifest = load_manifest(anchor)
    if manifest is None:
        manifest = scan_ecosystem(anchor, write=False)
    from ecosystem.manifest import manifest_markdown

    parts = [manifest_markdown(manifest)]
    repos = scan_sibling_repos(anchor)
    parts.append(repos_markdown(repos))
    return "\n".join(parts)
