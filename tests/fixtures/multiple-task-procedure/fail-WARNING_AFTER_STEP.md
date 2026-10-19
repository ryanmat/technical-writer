# Install and verify the Northwind Relay agent

Install the Relay agent on one host and confirm it reports healthy.

## Before you begin

- You have Northwind Relay version 2.4.0 or later.
- You have root on the host.

## Install the agent

To install the agent:

1. Run `relay-agent install`. The command prints `installed` and returns.

## Start the agent

To start the agent:

1. Run `relay-agent start`. The command prints `started` and returns.

**Warning:** Starting the agent restarts the host's message buffer and drops every unsent message.

## Verify the installation

To verify the installation:

1. Run `relay-agent status`. The output reads `healthy`.
