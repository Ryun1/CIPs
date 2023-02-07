# Test Vector for CIP-0072

Schema version `0.0.1`

## Keys



## Certificate Registration Example

### Human Readable Format

```javascript
{
	"subject": "d684512ccb313191dd08563fd8d737312f7f104a70d9c72018f6b0621ea738c5b8213c8365b980f2d8c48d5fbb2ec3ce642725a20351dbff9861ce9695ac5db8",
	"rootHash": "8c4e9eec512f5f277ab811ba75c991d51600c80003e892e601c6b6c19aaf8a33",
  "schema_version": "0.0.1",
  "type": { 
    "action": "REGISTER",
    "releaseNumber": "1.0.0",
    "releaseName": "My First Release",
  }
}
```

### Blake2b-256 Hash



### Full Cert

```javascript
"1667":{
	"subject": "d684512ccb313191dd08563fd8d737312f7f104a70d9c72018f6b0621ea738c5b8213c8365b980f2d8c48d5fbb2ec3ce642725a20351dbff9861ce9695ac5db8",
	"rootHash": "8c4e9eec512f5f277ab811ba75c991d51600c80003e892e601c6b6c19aaf8a33",
  "schema_version": "0.0.1",
  "type": { 
    "action": "REGISTER",
    "releaseNumber": "1.0.0",
    "releaseName": "My First Release",
  },
	"signature": {
		"r": "5114674f1ce8a2615f2b15138944e5c58511804d72a96260ce8c587e7220daa90b9e65b450ff49563744d7633b43a78b8dc6ec3e3397b50080",
		"s": "a15f06ce8005ad817a1681a4e96ee6b4831679ef448d7c283b188ed64d399d6bac420fadf33964b2f2e0f2d1abd401e8eb09ab29e3ff280600",
		"algo": "Ed25519−EdDSA",
		"pub": "b7a3c12dc0c8c748ab07525b701122b88bd78f600c76342d27f25e5f92444cde"
	}
}
```