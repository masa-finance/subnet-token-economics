## Staking TAO to Subnet 42 and 59

To stake your TAO using `btcli`, use the following command:

```bash
btcli stake add --amount <TAO_AMOUNT> --netuid <SUBNET_ID>
```

### Example:
Stake 10 TAO to subnet 42:
```bash
btcli stake add --amount 10 --netuid 42
```

### Additional Options:
- **Stake all available TAO**:
  ```bash
  btcli stake add --all --netuid 42
  ```
- **Stake with safe staking (prevents excessive slippage)**:
  ```bash
  btcli stake add --amount 10 --netuid 42 --safe --tolerance 0.05
  ```
- **Stake to multiple subnets**:
  ```bash
  btcli stake add --amount 5 --netuid 42 --netuid 43
  ```

For an interactive guided process, simply run:
```bash
btcli stake add
```
This will prompt you for the subnet, amount, and hotkey details.

## Delegating Alpha to a validator on Subnet 42 and 59

To stake your Alpha using `btcli`, use the following command:

To delegate your **Alpha** tokens to a validator, use the following command:

```bash
btcli delegate add --amount <ALPHA_AMOUNT> --hotkey <VALIDATOR_HOTKEY> --netuid <SUBNET_ID>
```

### **Example Commands**
1. **Delegate 50 Alpha to a validator on subnet 3**:
   ```bash
   btcli delegate add --amount 50 --hotkey 5FupG3XYZ... --netuid 42
   ```

2. **Delegate all available Alpha to a validator on subnet 3**:
   ```bash
   btcli delegate add --all --hotkey 5FupG3XYZ... --netuid 42
   ```

3. **Delegate safely with slippage protection (max 5% change in delegation rate)**:
   ```bash
   btcli delegate add --amount 50 --hotkey 5FupG3XYZ... --netuid 42 --safe --tolerance 0.05
   ```

4. **Delegate interactively (guided process)**:
   ```bash
   btcli delegate add
   ```
   - This will prompt you to select the subnet, validator, and amount.

---

### **Checking Your Delegations**
To see your current delegations:
```bash
btcli delegate list
```

---

### **Removing a Delegation**
To remove your delegation:
```bash
btcli delegate remove --amount <ALPHA_AMOUNT> --hotkey <VALIDATOR_HOTKEY> --netuid <SUBNET_ID>
```

For full removal:
```bash
btcli delegate remove --all --hotkey 5FupG3XYZ... --netuid 3
```

This allows you to delegate Alpha to a validator and earn rewards passively. 🚀