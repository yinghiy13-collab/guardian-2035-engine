import os
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from cryptographic_core import GuardianCrypto
from merkle_ledger import MerkleLedger

app = FastAPI(title="Guardian 2035 API v1.0")

# ✅ ใช้ตัวแปรสภาพแวดล้อม — ไม่ใส่คีย์จริงลงโค้ด
SECRET_KEY = os.getenv(
    "GUARDIAN_SECRET",
    "PLEASE_REPLACE_WITH_REAL_FERNET_KEY_32BYTES_="  # ค่าตัวอย่าง — ไม่ใช่จริง
)
crypto = GuardianCrypto(SECRET_KEY)
ledger = MerkleLedger()

class AuditPayload(BaseModel):
    data: str
    metadata: dict

@app.get("/health")
async def health():
    return {"status": "active", "version": "1.0.0-sandbox"}

@app.post("/auditlog")
async def log_entry(payload: AuditPayload, x_api_key: str = Header(None)):
    # ✅ ตรวจสอบผ่านตัวแปร — ไม่เขียนรหัสจริง
    VALID_KEY = os.getenv("YINGYAI_API_KEY", "audit-verification-sandbox-only")
    if x_api_key != VALID_KEY:
        raise HTTPException(403, "Unauthorized")
    
    encrypted = crypto.encrypt(payload.data)
    entry_hash = ledger.add_entry(encrypted)
    return {
        "merkle_root": ledger.get_root(),
        "entry_hash": entry_hash,
        "status": "recorded"
   }
