from fastapi import FastAPI
from pytrends.request import TrendReq

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello! FastAPI 서버 동작 중"}

@app.get("/keyword")
def keyword_info(query: str):
    pytrends = TrendReq(hl='ko', tz=540)
    pytrends.build_payload([query], cat=0, timeframe='today 12-m')
    interest_over_time_df = pytrends.interest_over_time()
    
    if interest_over_time_df.empty:
        return {"error": "데이터 없음"}
    
    avg_search_volume = int(interest_over_time_df[query].mean())
    last_value = int(interest_over_time_df[query].iloc[-1])
    
    return {
        "keyword": query,
        "평균검색량": avg_search_volume,
        "최근검색량": last_value,
        "트렌드데이터": interest_over_time_df[query].to_dict()
    }
