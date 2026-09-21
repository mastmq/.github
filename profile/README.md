<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/mastmq/.github/main/assets/banner.png">
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/mastmq/.github/main/assets/banner-light.png">
    <img src="https://raw.githubusercontent.com/mastmq/.github/main/assets/banner.png" alt="mast — a multi-tenant MQTT broker built on core NATS">
  </picture>
</div>


**A multi-tenant MQTT broker built on core NATS.** One binary, from a single edge box to a clustered fleet.

```console
$ mast                  # all-in-one: MQTT + storage, no cluster
$ mast --role=core      # Raft and the KV buckets
$ mast --role=edge      # MQTT listeners, joins the core as a leaf node
```

## Why this exists

Every open-source MQTT broker that does real multi-tenancy makes you give something up. EMQX adopted the Business Source License in 5.9, and forming a cluster from multiple nodes now requires a paid licence key. BifroMQ has genuine native multi-tenancy but runs on the JVM. VerneMQ's source is Apache 2.0 while its official packages and Docker images are governed by a EULA that charges for commercial use. RabbitMQ gives you vhosts but supports neither QoS 2 nor shared subscriptions. Mosquitto, NanoMQ, FlashMQ and mochi-mqtt do not cluster at all.

mast is the combination that does not otherwise exist: MQTT 5 with shared subscriptions, tenant isolation with per-tenant limits, free clustering, no JVM, and a single binary you can also run standalone at a customer site.

## How it is put together

**Core NATS moves messages; a key-value store holds keys.** Live fan-out rides core NATS, which handles tens of millions of subjects. Everything durable — sessions, retained messages, offline queues — lives in a handful of JetStream KV buckets. What mast deliberately never does is create a JetStream consumer per subscription: consumers are Raft state machines, a server holds on the order of two thousand, and a real fleet would want hundreds of thousands. Durable state scales as keys, not as consensus groups.

**Tenant isolation is structural, not a convention.** Every topic is mounted under its tenant before validation, authorization or subscription ever sees it, and unmounted again on the way out. A client never learns the prefix exists, and two tenants publishing to `a/b` cannot reach each other even though mochi's topic tree has no idea tenants exist.

## Repositories

| | |
| --- | --- |
| [mast](https://github.com/mastmq/mast) | The broker |
| [charts](https://github.com/mastmq/charts) | Helm charts |
| [docs](https://github.com/mastmq/docs) | Architecture notes and operational guides |

## Status

Early, and honest about it. The broker runs, moves messages across a cluster with tenant isolation, honours QoS 0 through 2, replays retained messages and resumes persistent sessions. Gaps are tracked as issues rather than described as roadmap: see [the parity label](https://github.com/mastmq/mast/issues?q=is%3Aissue+is%3Aopen+label%3Aparity) for what an MQTT client is entitled to assume and does not yet get.

Apache 2.0.
