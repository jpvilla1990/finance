from fastapi import FastAPI
import uvicorn
from modules.backEnd.backEnd import BackEnd

app = FastAPI()
backEnd = BackEnd(
    dataFolder="data"
)

@app.get("/finance/stock_data/downloadAllStocks")
async def downloadAllStocks():
    return backEnd.downloadAllStocks()

@app.get("/finance/stock_data/downloadStocksCountry")
async def downloadStocksCountry():
    return backEnd.downloadStocksCountry("ARG")

@app.get("/finance/stock_data/getAllStocksInfo")
async def getAllStocksInfo():
    return backEnd.getAllStocksInfo()

if __name__ == "__main__":
    uvicorn.run(app=app, host="127.0.0.1", port=9100)