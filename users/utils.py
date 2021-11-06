from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user) -> tuple[str, str]:
    """
    Returns access and refresh token pair.
    access, refresh = get_tokens_for_user(user)
    """
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token), str(refresh)
