# Create an alert rule for a stalled stream

An alert rule in Northwind Relay checks a stream on a schedule and fires when the stream stops delivering messages.

## Before you begin

- You run Northwind Relay 2.4.0 or later, because alert rules are available from 2.4.0.
- You have the permission to create alert rules. [UNVERIFIED: the permission or role that grants it]
- You know which stream to watch.
- You know how long a gap without messages counts as a stall. [UNVERIFIED: whether the rule takes a gap length, and its unit]

## Steps

The **Evaluation interval** sets how often the rule checks the stream, in seconds. The default is 60.

To create an alert rule that fires when a stream stops delivering messages:

1. Open **Alert rules**. [UNVERIFIED: how to reach the Alert rules screen]
2. Select **New alert rule**.
3. In **Stream**, choose the stream to watch. [UNVERIFIED: the control type and whether the field accepts one stream or several]
4. In **Condition**, choose **Delivery gap**. [UNVERIFIED: that Delivery gap is a Condition option, and how it detects a stream that stopped delivering]
5. In **Evaluation interval**, enter the number of seconds between checks, or keep the default of 60.
6. Select **Save rule**. [UNVERIFIED: what the screen shows after saving, and whether the rule appears with the state **Normal**]
