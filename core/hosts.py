from django_hosts import patterns, host


host_patterns = patterns(
    '',
    host(r'api', 'core.apps.api.url_router', name='api'),
    host(r'dashboard', 'core.apps.oauth.urls', name='dashboard'),
    host(r'staff', 'core.urls', name='staff'),
)
