"""OIDC token verification and RBAC helpers.

In production, JWKS should be fetched from `{settings.oidc_issuer}/.well-known/jwks.json`
and cached. This module stubs the verification call site so the auth
integration point is explicit and swappable (Auth0 / Keycloak / Cognito).
"""
from jose import jwt


def decode_and_verify_token(token: str, settings) -> dict:
    """Decode and verify a bearer JWT against the configured OIDC issuer.

    Raises ValueError on any validation failure.
    """
    if not settings.oidc_issuer:
        raise ValueError("OIDC is not configured on this deployment")

    try:
        # NOTE: replace `key=` with the fetched JWKS in production; this is a
        # structural placeholder so downstream code has a single call site.
        claims = jwt.decode(
            token,
            key="",
            options={"verify_signature": False, "verify_aud": False},
        )
    except Exception as exc:
        raise ValueError(f"Invalid token: {exc}") from exc

    return claims
