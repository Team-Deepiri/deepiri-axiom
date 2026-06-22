"""Deepiri ecosystem auto-detection and linking."""

from ecosystem.manifest import EcosystemManifest, load_manifest, save_manifest
from ecosystem.scanner import scan_ecosystem

__all__ = [
    "EcosystemManifest",
    "load_manifest",
    "save_manifest",
    "scan_ecosystem",
]
