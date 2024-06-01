# eth-beautiful-address-generator
this python script allows you to generate eth addresses with your prefixies

**Requirements:**

* Python 3.6 or later
* `eth_account` library (`pip install eth_account`)
* `bip_utils` library (`pip install bip_utils`)

**How to Use:**

1. **Run the script:** Open a terminal or command prompt, navigate to the directory where you saved the script, and run it using the command `python eth_gen.py`.
2. **Specify the number of addresses:** The script will first ask you how many vanity addresses you want to generate. Enter the desired number.
3. **Enter prefixes:** For each address, you will be prompted to enter the desired prefix (not including the leading "0x"). 
4. **Wait for results:** The script will start generating random Ethereum addresses and checking if they match any of the specified prefixes. This process can take some time depending on the complexity of the prefixes.
5. **Stop the search (optional):** If you want to stop the search before all addresses are found, press **Ctrl+C**. The script will print the addresses that have been found so far.
6. **View results:** The script will print a list of all the generated addresses and their corresponding mnemonic phrases. Script also saves results to file `wallets.txt`

**Wallets that were found in 10 minutes of the script**
1. Префикс: d34d, Адрес: 0xd34De5c8E2cF939486152685B421336203E196d7, Мнемоническая фраза: food gap age tissue tenant sting toast august library any film margin
2. Префикс: aabbcc, Адрес: 0xaaBbCc3985A8f530DdB8e897167F5b60a036082D, Мнемоническая фраза: two lounge deliver wisdom lobster coffee stage crouch frown wood gown salmon
3. Префикс: dead, Адрес: 0xdEAD3b5dcE117b548f8A89B12Dcaf7e2dcc57e7f, Мнемоническая фраза: gun patient agree unhappy good fade ancient swap gather wheat odor pond
4. Префикс: 0x12345, Адрес: 0x123457d0A6Be3624e7b824F119027a0b12541c91, Мнемоническая фраза: blood life powder oval arctic abandon elevator yellow shoulder pet space scrap
5. Префикс: 0xabcde, Адрес: 0xabcDEB580218A5cF11132b7747422B79569DD321, Мнемоническая фраза: wide oblige cream cloud feed daring ceiling robust announce seven security blossom
6. Префикс: 0x00000, Адрес: 0x0000038c8A20621c4a4536034F9e6B7702D6bdCd, Мнемоническая фраза: peace cry pear virtual museum deputy shock inflict enlist spy razor urban
7. Префикс: 0x123456, Адрес: 0x123456DE570247652C07243Feb434Fa1dB59d0d4, Мнемоническая фраза: glow pink knee clean orbit hint dune memory south empty device unlock
