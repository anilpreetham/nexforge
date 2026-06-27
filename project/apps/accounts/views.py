"""Account views — token login with a tight, login-specific rate limit."""

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.throttling import ScopedRateThrottle


class ThrottledObtainAuthToken(ObtainAuthToken):
    """Token login throttled by the ``auth`` scope to blunt brute-force.

    The default endpoint only inherits the broad ``anon`` rate; this scopes it
    to the tighter ``auth`` rate (see DEFAULT_THROTTLE_RATES).
    """

    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "auth"


obtain_auth_token = ThrottledObtainAuthToken.as_view()
