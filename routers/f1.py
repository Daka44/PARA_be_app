from fastapi import APIRouter, HTTPException
import httpx

router = APIRouter(
    prefix="/f1",
    tags=["f1"],
)

@router.get("/latest-race-results")
async def get_latest_race_results():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://ergast.com/api/f1/current/last/results.json")
            response.raise_for_status()  # 에러 발생 시 예외 처리
            data = response.json()
            results = data["MRData"]["RaceTable"]["Races"][0]["Results"]
            return {"results": results}
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=exc.response.json())

# 다른 엔드포인트도 유사하게 구현
