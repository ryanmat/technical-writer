---
schema_version: "1.1"
name: multiple-task--relay-install-and-verify
description: "a multiple-task procedure for engineers from source snippets that omit the health endpoint's port, so the output carries one Before you begin section, a stem sentence in every task section, a Verify section, and an UNVERIFIED marker instead of an invented port"
tags: [user-docs, regression]
runs: 2
max_turns: 12
timeout_seconds: 600
allowed_tools: [Skill, Read]
---

Use the technical-writer skill to write a multiple-task procedure for engineers who run Northwind Relay. The goal: install the Relay agent on a host, start it, and confirm it is healthy. Return the finished Markdown document as your final message and nothing else.

Everything you may state about the product is in the three snippets below. Do not add commands, flags, defaults, ports, or versions they do not contain. The snippets never say which port the health endpoint listens on; do not invent one.

Release line, from the product's about dialog box:

```text
Northwind Relay 2.4.0
The Relay agent ships with 2.4.0 and later.
```

Commands and their output, from the agent's command reference:

```text
relay-agent install    Installs the agent as a service. Requires root. Prints: installed.
relay-agent start      Starts the service. Prints: started.
relay-agent status     Prints the service state: healthy, starting, or stopped.
```

Health endpoint, from the agent's operations note:

```text
The agent exposes GET /health on the port set in agent.yaml.
A healthy agent answers 200 with the body ok.
```
