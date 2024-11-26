import threading
import random
import time


class Bank():

    def __init__(self):
        self.balance = 0
        self.lock = threading.Lock()


    def deposit(self):
        self.lock.acquire()
        for i in range(100):
            replenishment = random.randint(50, 500)
            self.balance += replenishment
            if self.balance >= 500 and self.lock.locked():
                self.lock.release()
                print(f"Пополнение: {replenishment}. Баланс: {self.balance}")
            time.sleep(0.001)

    def take(self):
        self.lock.acquire()
        for i in range(100):
            replenishment = random.randint(50, 500)
            print(f"Запрос на {replenishment}")
            if replenishment <= self.balance:
                self.balance -= replenishment
                print(f"Снятие: {replenishment}. Баланс: {self.balance}")

            else:
                print("Запрос отклонён, недостаточно средств")
                self.lock.acquire()


bk = Bank()

# Т.к. методы принимают self, в потоки нужно передать сам объект класса Bank
th1 = threading.Thread(target=Bank.deposit, args=(bk,))
th2 = threading.Thread(target=Bank.take, args=(bk,))

th1.start()
th2.start()
th1.join()
th2.join()

print(f'Итоговый баланс: {bk.balance}')