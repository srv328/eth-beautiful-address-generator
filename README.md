# eth-beautiful-address-generator
this python script allows you to generate eth addresses with your prefixies

**Requirements:**

* Python 3.6 or later
* `eth_account` library (`pip install eth_account`)
* `bip_utils` library (`pip install bip_utils`)

**How to Use:**

1. **Run the script:** Open a terminal or command prompt, navigate to the directory where you saved the script, and run it using the command `python eth_gen.py`.
2. **Specify the number of addresses:** The script will first ask you how many vanity addresses you want to generate. Enter the desired number.
3. **Enter prefixes:** For each address, you will be prompted to enter the desired prefix (including the leading "0x"). 
4. **Wait for results:** The script will start generating random Ethereum addresses and checking if they match any of the specified prefixes. This process can take some time depending on the complexity of the prefixes.
5. **Stop the search (optional):** If you want to stop the search before all addresses are found, press **Ctrl+C**. The script will print the addresses that have been found so far.
6. **View results:** The script will print a list of all the generated addresses and their corresponding mnemonic phrases.
