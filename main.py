import websockets
import asyncio
import json
import time

import matplotlib.pyplot as plt

from memory_profiler import memory_usage


x_data = []
y_data = []

figure = plt.figure()
ax = figure.add_subplot(111)


def update_graph():
    ax.plot(x_data, y_data, color='pink')
    figure.canvas.draw()
    plt.pause(0.1)


async def main():
    url = "wss://stream.binance.com:9443/stream?streams=icpusdt@miniTicker"
    async with websockets.connect(url) as client:
        while True:
            data = json.loads(await client.recv())['data']

            event_time = time.localtime(data['E'] // 1000)
            event_time = f"{event_time.tm_hour}:{event_time.tm_min}:{event_time.tm_sec}"
            print(event_time, data['c'])
            print(memory_usage())
            x_data.append(event_time)
            y_data.append(round(float(data['c']), 2))

            update_graph()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
