from fastapi import APIRouter, HTTPException
from typing import List, Dict
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/admin/stats")
async def get_admin_stats():
    try:
        return {
            "network_health": await get_network_health(),
            "system_metrics": await get_system_metrics(),
            "validator_stats": await get_validator_stats(),
            "defi_metrics": await get_defi_metrics()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/admin/validator/{address}/slash")
async def slash_validator(address: str, reason: str):
    try:
        return await perform_validator_slash(address, reason)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/admin/emergency/pause")
async def pause_network():
    try:
        return await perform_emergency_pause()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))