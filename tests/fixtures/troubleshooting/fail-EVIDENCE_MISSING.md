# Troubleshoot routes in Northwind Relay

Fix the errors a route reports on the Routes page and at the command line.

## Error: `route billing timed out`

### Symptom

The **Routes** page shows the route as **Timed out**, and `relay route status billing` prints `timed out`.

### Cause

The consumer group acknowledged no message within the route timeout, so Relay stopped delivering to it.

### Resolution

To restore delivery, restart the route:

```bash
relay route restart billing
```
