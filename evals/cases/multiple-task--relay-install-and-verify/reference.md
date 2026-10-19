# Install and verify the Northwind Relay agent

Install the Relay agent on one host, start it, and confirm it reports healthy.

To put the agent into service:

1. [Install the agent](#install-the-agent)
2. [Start the agent](#start-the-agent)
3. [Verify the agent](#verify-the-agent)

## Before you begin

- You have Northwind Relay version 2.4.0 or later. The Relay agent ships with 2.4.0 and later.
- You have root on the host, which `relay-agent install` requires.
- You know the port set in `agent.yaml` for the health endpoint. [UNVERIFIED: the port the health endpoint listens on]

## Install the agent

To install the agent as a service:

1. Open a terminal on the host as root.
2. Run the installer:

   ```bash
   relay-agent install
   ```

   The command prints `installed`.

## Start the agent

To start the agent:

1. Run the start command:

   ```bash
   relay-agent start
   ```

   The command prints `started`.

## Verify the agent

To verify the agent is healthy:

1. Run the status command:

   ```bash
   relay-agent status
   ```

   The output reads `healthy`. While the service is still coming up it reads `starting`.

2. Request the health endpoint on the port set in `agent.yaml`:

   ```bash
   curl -i http://localhost:<PORT>/health
   ```

   The agent answers `200` with the body `ok`.
