"""Cloud integration module for scanmenow.

This module provides Firestore-backed storage.  The ``google-cloud-firestore``
package is a soft/optional dependency; it is only imported when
``SCANMENOW_BACKEND=firestore`` is active.  SQLite-only deployments never
need to install the ``[cloud]`` extra.
"""
