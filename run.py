import multiprocessing
from bot import run_bot
from server import run_server

if __name__ == "__main__":
    bot_process = multiprocessing.Process(target=run_bot)
    fastapi_process = multiprocessing.Process(target=run_server)

    bot_process.start()
    fastapi_process.start()

    bot_process.join()
    fastapi_process.join()
