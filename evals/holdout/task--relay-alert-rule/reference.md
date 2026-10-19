# Create an alert rule in Northwind Relay

Create an alert rule so that Northwind Relay alerts you when a stream stops delivering messages.

## Before you begin

- You have Northwind Relay version 2.4.0 or later. Alert rules are available from 2.4.0.
- You have the permission to create alert rules. [UNVERIFIED: the permission or role that grants access to Alert rules]
- You know which stream the rule watches and the delivery gap at which the rule fires.

## Steps

To create an alert rule, complete the following steps.

1. Click **Alert rules**. The **Alert rules** page opens.
2. Click **New alert rule**.
3. In **Stream**, select the stream the rule watches.
4. In **Evaluation interval**, enter how often the rule checks the stream, in seconds. The default is 60.
5. In **Delivery gap**, enter the delivery gap at which the rule fires.
6. Click **Save rule**. The rule appears on the **Alert rules** page as **Normal**.

## Next steps

- Watch the rule for one evaluation interval and confirm it stays **Normal** while the stream delivers.
