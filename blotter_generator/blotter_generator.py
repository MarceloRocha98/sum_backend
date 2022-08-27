from random import randrange, choices
import os
import time


def gen_blotter(ticker):
    volume = randrange(1000, 10000)
    price = randrange(1, 100)
    return f"{ticker},{volume},{price}"


tickers_path = "ibov_tickers.txt"
blotters_path = "blotters.txt"

with open(tickers_path) as f:
    ticker_list = f.read().splitlines()

file_exists = os.path.exists(blotters_path)
if not file_exists:
    print("File not found! Running for first time...")
    open(blotters_path, "a").write("ticker,volume,price\n")


while True:
    start = time.time()
    interval_seconds = randrange(3, 5)
    new_blotters_count = randrange(1000, 10000)

    blotters = [
        gen_blotter(ticker) for ticker in choices(ticker_list, k=new_blotters_count)
    ]

    open(blotters_path, "a").write("\n".join(blotters))
    time_elapsed = time.time() - start
    sleep_for = interval_seconds - time_elapsed
    print(f"{new_blotters_count} generated in {time_elapsed}s")
    print(f"Sleeping for {sleep_for}s\n")
    time.sleep(sleep_for)
