# Security policy

## Threat model

CiteGuard is a **local command-line tool for reports you control**. It reads Markdown, performs HTTP requests to citation URLs, and parses HTML locally.

Version 0.2 rejects non-HTTP(S) URLs, embedded URL credentials, localhost, private/reserved/non-global IPs, and those addresses in redirect chains **by default**. It ignores environment proxy variables, limits redirects to five, and stops reading an HTML response after 2 MiB (configurable).

**Important:** DNS validation followed by a separate HTTP connection is subject to DNS rebinding / time-of-check vs time-of-use races. These checks are not a hardened security boundary. For a hosted service processing untrusted URLs, enforce egress firewall rules or isolate the fetcher at network level. Do **not** rely on these application checks alone.

## Opt-in private network access

`--allow-private` is intended only for known, trusted internal reports. It bypasses the address restriction and allows fetching internal services. Do not enable this for content submitted by other users.

## Other limitations

- Content from fetched pages is parsed as data, not executed. It is never sent to an external AI API.
- Maximum HTML size limits reduce memory pressure, but resource usage can still be affected by many citations and slow remote hosts.
- Citation text and source HTML can be adversarial. Results are heuristic; never interpret `clean` as factual verification.
- External requests necessarily disclose the source IP and User-Agent to target sites. No telemetry is sent by CiteGuard.
- Fixture mode performs no network requests.

## Reporting

Please report security problems privately through GitHub's vulnerability reporting feature if it is available for the repository. Avoid public exploit disclosure before maintainers have had an opportunity to review the issue.
