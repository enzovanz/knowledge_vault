---
type: concept
domain: software engineering
created: 2026-09-14
---
## Summary

PostHog is an open-source product analytics platform for understanding how people use a website or application. It combines behavioral analytics with tools such as session replay and feature flags so product teams can connect user behavior to product changes.

## Explanation

PostHog can capture custom events, group users into cohorts, visualize engagement with heatmaps, and replay sessions to reveal friction in a user journey. Its [[Feature Flags]] support controlled rollouts and experiments in client-side interfaces, backend services, or both. Organizations can self-host it for greater control over data and customization, but doing so adds infrastructure, maintenance, and learning costs.

## Example

A data pipeline can evaluate a server-side feature flag and conditionally run an optional transformation:

```python
import logging
import os

from posthog import Posthog

log = logging.getLogger(__name__)
environment = os.getenv("ENVIRONMENT", "development")

posthog = Posthog(
    os.environ["POSTHOG_PROJECT_TOKEN"],
    host="https://us.i.posthog.com",
    feature_flags_request_timeout_seconds=2,
)


def flag_enabled(flag_key: str, default: bool = False) -> bool:
    try:
        flags = posthog.evaluate_flags(
            f"orders-pipeline:{environment}",
            flag_keys=[flag_key],
            person_properties={"environment": environment},
        )
        value = flags.get_flag(flag_key)
        return default if value is None else value is True
    except Exception:
        log.exception("Could not evaluate %s; using default", flag_key)
        return default


def run_pipeline() -> None:
    orders = extract_orders()

    if flag_enabled("run-order-enrichment"):
        orders = enrich_orders(orders)
    else:
        log.info("Order enrichment disabled by feature flag")

    load_orders(orders)


try:
    run_pipeline()
finally:
    posthog.shutdown()
```

The pipeline itself still starts; the flag only controls whether the optional enrichment branch runs. A stable evaluation identity makes the result consistent, while the timeout and default behavior prevent a PostHog outage from blocking the pipeline. Feature flags should not bypass correctness-critical validation, security, or compliance steps.

Feature flags are one example of many features PostHog offers, as well as PostHog is one implementation of feature flags.

## Connections

- Category: Product Engineering → Product Analytics
- Source: [What is PostHog? and its Pros and Cons](https://medium.com/@ciente/what-is-posthog-and-its-pros-and-cons-05d8dff13194)
- Source: [PostHog Python SDK — Feature flags](https://posthog.com/docs/libraries/python#feature-flags)
