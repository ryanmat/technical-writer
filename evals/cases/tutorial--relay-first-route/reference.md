# Route your first stream in Northwind Relay

Create a stream and a route, send one message, and watch it arrive at a consumer group.

By the end you have a stream named `orders`, a route that sends the messages tagged `region`
`east` to the `billing` consumer group, and one message that made the trip. The exercise uses
the sample values from the quickstart notes.

## Before you begin

- You have Northwind Relay. [UNVERIFIED: the version this tutorial was written against]
- You have the permission to create streams and routes. [UNVERIFIED: the permission or role that grants it]
- You have the `relay` command on your path.

## Create a stream

To create the `orders` stream:

1. Click **Streams**. The **Streams** page opens.
2. Click **New stream**.
3. In **Stream name**, enter `orders`.
4. Click **Save stream**. The stream appears on the **Streams** page.

## Create a route

To route the `east` orders to the `billing` group:

1. Click **Routes**. The **Routes** page opens.
2. Click **New route**.
3. In **Stream**, select `orders`.
4. In **Filter key**, enter `region`, and in **Filter value**, enter `east`.
5. In **Consumer group**, enter `billing`.
6. Click **Save route**. The route appears on the **Routes** page as **Active**.

## Send a message and watch it arrive

To send one message through the route:

1. Send a message tagged for the east region:

   ```bash
   relay send orders --key region --value east "order 1001"
   ```

   The command prints `sent to orders (1 route matched)`.

2. Read the consumer group:

   ```bash
   relay tail billing
   ```

   The output shows `order 1001`.

## Summary

To summarize:

- You created the `orders` stream.
- You created a route from `orders` to `billing` with the filter `region` `east`.
- You sent one message and read it from the consumer group.

Now a producer can write to `orders` and the `billing` group receives only the east orders.

## Next steps

- [Routing model in Northwind Relay](routing-model.md) explains why a message can reach more than one group.
- [Create a route](create-a-route.md) covers the route settings the tutorial left at their defaults.
- [Route settings in Northwind Relay](route-settings.md) lists every setting a route accepts.
