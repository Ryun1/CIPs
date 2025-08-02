
Cardano-cli:

```shell
cardano-cli conway query protocol-parameters --socket-path "$SOCKET_PATH" --mainnet > ./temp/cli-params.json
```

Cardano-db-sync:

```sql
SELECT * FROM epoch_param
ORDER BY epoch_no DESC
LIMIT 1;
```

Constitution (markdown):

https://github.com/IntersectMBO/cardano-constitution/blob/main/cardano-constitution-1/cardano-constitution-1.txt.md

Shelley Ledger Spec:

https://github.com/intersectmbo/cardano-ledger/releases/latest/download/shelley-ledger.pdf