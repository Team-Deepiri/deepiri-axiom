"""Orchestrate full ecosystem scan."""

from __future__ import annotations

from pathlib import Path

from ecosystem.apps import detect_apps, tools_for_install
from ecosystem.catalog import get_catalog
from ecosystem.devices import detect_device
from ecosystem.github_catalog import catalog_markdown, refresh_org_catalog
from ecosystem.manifest import EcosystemManifest, load_manifest, save_manifest
from ecosystem.providers import detect_providers
from ecosystem.repos import discover_local_repos, repo_links, repos_markdown


def scan_ecosystem(
    anchor: Path,
    *,
    write: bool = False,
    refresh_catalog: bool = False,
) -> EcosystemManifest:
    """Scan device, providers, apps, org catalog, and local repos."""
    anchor = anchor.resolve()
    device = detect_device()
    providers = detect_providers()
    apps = detect_apps()

    catalog_rows, catalog_source = refresh_org_catalog(anchor, force=refresh_catalog)
    entries, _ = get_catalog(anchor)
    catalog_map = {e.name: e for e in entries}
    repos = discover_local_repos(anchor, catalog=catalog_map)
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
    anchor = anchor.resolve()
    manifest = load_manifest(anchor)
    if manifest is None:
        manifest = scan_ecosystem(anchor, write=False)

    from ecosystem.manifest import manifest_markdown

    rows, source = refresh_org_catalog(anchor)
    parts = [
        manifest_markdown(manifest),
        catalog_markdown(rows, source=source),
        repos_markdown(discover_local_repos(anchor)),
    ]
    return "\n".join(parts)
