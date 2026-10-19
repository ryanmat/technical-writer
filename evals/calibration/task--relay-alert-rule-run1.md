# Create an alert rule for a stream that stops delivering messages

Create an alert rule in Northwind Relay that fires when a stream has a delivery gap.

## Before you begin

- You run Northwind Relay 2.4.0 or later. Alert rules are available from 2.4.0.
- You have the permission to create alert rules. [UNVERIFIED: the permission or role that grants it]
- You know which stream to watch.

## Steps

An alert rule checks one stream at a fixed interval. The **Evaluation interval** sets how often the rule checks the stream, in seconds. The default is 60.

To create an alert rule that fires when a stream stops delivering messages:

1. Open **Alert rules**. [UNVERIFIED: how to reach the Alert rules screen]
2. Click **New alert rule**.
3. In **Condition**, select **Delivery gap**. [UNVERIFIED: that Delivery gap is a Condition option, and any threshold or duration it needs]
4. In **Stream**, select the stream to watch. [UNVERIFIED: the control type and how streams are listed]
5. In **Evaluation interval**, enter the number of seconds between checks. Leave the default of 60 to check every 60 seconds.
6. Click **Save rule**. [UNVERIFIED: what the screen shows after the rule is saved]

## Next steps

Check the rule on the **Alert rules** screen. **Normal** is a state label in Northwind Relay. [UNVERIFIED: where Normal appears and what it tells you about the rule]
