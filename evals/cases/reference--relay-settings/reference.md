# Alert rule settings in Northwind Relay

Every setting an alert rule accepts, with its default and what it does.

The values below hold for Northwind Relay 2.4.0, the release the rule editor's help text describes. Alert rules are available from 2.4.0. Use this page beside the task that creates a rule.

## Settings

One row per setting, in the order the rule editor shows them. A default the help text does not show carries the marker.

| Setting | Default | Description |
|---|---|---|
| **Stream** | none; required | The stream the rule watches. |
| **Evaluation interval** | 60 | How often the rule checks the stream, in seconds. |
| **Delivery gap** | [UNVERIFIED: the default delivery gap, which the help text does not show] | The gap, in seconds, at which the rule fires. |
| **Severity** | warning | The label the alert carries when the rule fires: one of info, warning, or critical. |
| **Notification channel** | the workspace channel | Where the alert is sent. |
