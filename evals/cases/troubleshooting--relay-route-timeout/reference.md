# Troubleshoot routes in Northwind Relay

Fix a route that the **Routes** page and the command line report as timed out.

## Error: `route billing: timed out`

### Symptom

The **Routes** page shows the route's **State** as **Timed out**. At the command line, `relay route status billing` prints `route billing: timed out`.

### Cause

The route's consumer group acknowledged no message within the route timeout, so Relay stopped delivering to it. [UNVERIFIED: the route timeout's value and where it is set]

### Resolution

To restore delivery, restart the route:

1. Restart the route:

   ```bash
   relay route restart billing
   ```

   The command prints `route billing: Active`.

2. Confirm the state:

   ```bash
   relay route status billing
   ```

   The output reads `route billing: Active`, and the **Routes** page shows **Active**.

## Related

- [Routing model in Northwind Relay](routing-model.md) explains how a route delivers to its consumer group.
- [Route settings in Northwind Relay](route-settings.md) lists every setting a route accepts.
