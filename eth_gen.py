import threading

from eth_account import Account
from bip_utils import Bip39MnemonicGenerator, Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes

lock = threading.Lock()
found_prefixes_count = 0
found_all_prefixes = False
found_addresses = {}
count = 0


def get_data():
    global found_addresses
    print(f"Выберите режим работы программы:\n"
          f"1. Поиск по префиксу (сразу после 0x)\n"
          f"2. Поиск по вхождению (неважно, в каком месте)\n"
          f"3. Поиск по суффиксу (в конце)")

    mode = input("Введите номер выбранного режима: ")
    if mode not in '123':
        print('Выбран неверный режим работы!')
        return False
    mode = int(mode)

    print("Длина фразы:\n1. 12 слов\n2. 24 слова")

    length = input("Введите номер выбранной длины фразы: ")
    if length not in '12':
        print('Выбрана неверная длина фразы!')
        return False
    length = int(length)

    num_addresses = input("Сколько адресов вы хотите найти?: ")
    if not num_addresses.isdigit() or int(num_addresses) <= 0:
        print('Введите целое положительное число!')
        return False
    num_addresses = int(num_addresses)

    desired_prefixes = []
    for i in range(num_addresses):
        prefix = input(f"Введите желаемый {'' if mode == 1 or mode == 2 else 'вхождение '}адреса {i + 1} (без 0x): ")
        desired_prefixes.append(prefix)
        if not is_valid_prefix(prefix):
            print("Префикс содержит недопустимые символы. Пожалуйста, используйте только символы от 0 до F.")
            return False
    found_addresses = {prefix: None for prefix in desired_prefixes}
    return desired_prefixes, mode, length


def is_valid_prefix(prefix):
    valid_chars = set("0123456789abcdefABCDEF")
    return all(char in valid_chars for char in prefix)


def generate_address(desired_prefixes, mode, length):
    global found_prefixes_count, found_all_prefixes, found_addresses, count
    try:
        while not all(found_addresses.values()):
            count += 1
            if count % 1000 == 0:
                print(f"Проверено {count} адресов, продолжаем поиск...")
            mnemonic = Bip39MnemonicGenerator().FromWordsNumber(12 if length == 1 else 24)
            seed_bytes = Bip39SeedGenerator(mnemonic).Generate()

            bip44_ctx = Bip44.FromSeed(seed_bytes, Bip44Coins.ETHEREUM)
            bip44_acc_ctx = bip44_ctx.Purpose().Coin().Account(0)
            bip44_chg_ctx = bip44_acc_ctx.Change(Bip44Changes.CHAIN_EXT)
            address_key = bip44_chg_ctx.AddressIndex(0).PrivateKey().Raw().ToBytes()

            account = Account.from_key(address_key)
            address = account.address

            for prefix in desired_prefixes:
                if mode == 1:
                    remake = "0x" + prefix
                    if address.lower().startswith(remake.lower()) and found_addresses.get(prefix) is None:
                        found_addresses[prefix] = (address, mnemonic, prefix)
                        print(f"Найден адрес с префиксом {remake}: {address}")
                        with open('wallets.txt', 'a') as f:
                            f.write(f"Префикс: {remake}, Адрес: {address}, Мнемоническая фраза: {mnemonic}\n")
                            print("Префикс и мнемоническая фраза успешно записаны в файл wallets.txt")
                        with lock:
                            found_prefixes_count += 1
                            if found_prefixes_count == len(desired_prefixes):
                                found_all_prefixes = True
                        break
                elif mode == 2:
                    if prefix.lower() in address.lower() and found_addresses.get(prefix) is None:
                        found_addresses[prefix] = (address, mnemonic, prefix)
                        print(f"Найден адрес с вхождением {prefix}: {address}")
                        with open('wallets.txt', 'a') as f:
                            f.write(f"Вхождение: {prefix}, Адрес: {address}, Мнемоническая фраза: {mnemonic}\n")
                            print("Вхождение и мнемоническая фраза успешно записаны в файл wallets.txt")
                        with lock:
                            found_prefixes_count += 1
                            if found_prefixes_count == len(desired_prefixes):
                                found_all_prefixes = True
                        break
                elif mode == 3:
                    if address.lower().endswith(prefix.lower()) and found_addresses.get(prefix) is None:
                        found_addresses[prefix] = (address, mnemonic, prefix)
                        print(f"Найден адрес с суффиксом {prefix}: {address}")
                        with open('wallets.txt', 'a') as f:
                            f.write(f"Суффикс: {prefix}, Адрес: {address}, Мнемоническая фраза: {mnemonic}\n")
                            print("Суффикс и мнемоническая фраза успешно записаны в файл wallets.txt")
                        with lock:
                            found_prefixes_count += 1
                            if found_prefixes_count == len(desired_prefixes):
                                found_all_prefixes = True
                        break

    except KeyboardInterrupt:
        print("\nПоиск остановлен пользователем.")
    finally:
        return [(address, mnemonic.ToStr(), prefix) for prefix, (address, mnemonic, prefix) in found_addresses.items()]


def worker(desired_prefixes, mode, length):
    global lock
    while not found_all_prefixes:
        try:
            address, mnemonic, prefix = generate_address(desired_prefixes, mode, length)
        except Exception as e:
            print(f"Ошибка выполнения потока: {e}")


if __name__ == '__main__':
    data = get_data()
    if data:
        desired_prefixes, mode, length = data
        num_threads = 15
        threads = []

        for _ in range(num_threads):
            thread = threading.Thread(target=worker, args=(desired_prefixes, mode, length))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()
        print(f'Успешно найдено {len(desired_prefixes)} желаемых адресов.')
