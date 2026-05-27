"""Firestore client factory with lazy import and environment-aware credentials.

The ``google-cloud-firestore`` package is an optional dependency.  It is
imported lazily inside :func:`get_firestore_client` so that the rest of the
application (SQLite mode) never fails with an ImportError on environments
where the ``[cloud]`` extra is not installed.

Environment variables
---------------------
SCANMENOW_FIRESTORE_PROJECT
    GCP project ID.  Required when running outside a GCP environment that
    provides Application Default Credentials automatically.

SCANMENOW_FIRESTORE_EMULATOR_HOST
    When set (e.g. ``localhost:8080``), the client targets the local Firestore
    emulator instead of production.  Useful for local development and CI.
"""

import os
from typing import Any


def get_firestore_client() -> Any:
    """Return an authenticated Firestore client.

    Uses Application Default Credentials (ADC) by default.  Override the
    project with ``SCANMENOW_FIRESTORE_PROJECT``.  Point to the local emulator
    with ``SCANMENOW_FIRESTORE_EMULATOR_HOST``.

    Raises:
        ImportError: If ``google-cloud-firestore`` is not installed.  Install
            the ``[cloud]`` extra: ``pip install scanmenow[cloud]``.
        google.auth.exceptions.DefaultCredentialsError: If ADC is not
            configured and no service-account key is available.
    """
    try:
        from google.cloud import firestore  # type: ignore[import]
    except ImportError as exc:
        raise ImportError(
            "google-cloud-firestore is not installed.  "
            "Install the cloud extra: pip install scanmenow[cloud]"
        ) from exc

    project = os.getenv("SCANMENOW_FIRESTORE_PROJECT")

    # When the emulator host env var is present the SDK automatically routes
    # traffic to the emulator; no credentials are required.
    kwargs: dict[str, Any] = {}
    if project:
        kwargs["project"] = project

    return firestore.Client(**kwargs)
