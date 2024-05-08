from eth_account import Account
from bip_utils import Bip39MnemonicGenerator, Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes

def generate_address(desired_prefixes):
    count = 0
    found_addresses = {prefix: None for prefix in desired_prefixes}
    try:
        while not all(found_addresses.values()):
            count += 1

            mnemonic = Bip39MnemonicGenerator().FromWordsNumber(12)
            seed_bytes = Bip39SeedGenerator(mnemonic).Generate()

            bip44_ctx = Bip44.FromSeed(seed_bytes, Bip44Coins.ETHEREUM)
            bip44_acc_ctx = bip44_ctx.Purpose().Coin().Account(0)
            bip44_chg_ctx = bip44_acc_ctx.Change(Bip44Changes.CHAIN_EXT)
            address_key = bip44_chg_ctx.AddressIndex(0).PrivateKey().Raw().ToBytes()

            account = Account.from_key(address_key)
            address = account.address

            if count % 1000 == 0:
                print(f"Проверено {count} адресов, продолжаем поиск...\nЧтобы получить найденные адреса, используйте сочетание клавиш Ctrl+C")

            for prefix in desired_prefixes:
                if address.lower().startswith(prefix.lower()) and found_addresses[prefix] is None:
                    found_addresses[prefix] = (address, mnemonic)
                    print(f"Найден адрес с префиксом {prefix}: {address}")
                    with open('wallets.txt', 'a') as f:
                        f.write(f"Адрес: {address}, Мнемоническая фраза: {mnemonic}\n")
                        print("Мнемоническая фраза успешно записана в файл wallets.txt")
                    break

    except KeyboardInterrupt:
        print("\nПоиск остановлен пользователем.")
    finally:
        return list(found_addresses.values()) 

num_addresses = int(input("Сколько адресов вы хотите найти?: "))

desired_prefixes = []
for i in range(num_addresses):
    prefix = input(f"Введите желаемый префикс адреса {i+1} (вместе с 0x): ")
    desired_prefixes.append(prefix)

found_addresses = generate_address(desired_prefixes)
print("\nВсе найденные адреса:")
for res in found_addresses:
    if res is not None:
        print(f"Адрес: {res[0]}\nМнемоническая фраза: {res[1]}")
