from fastapi import APIRouter, File, UploadFile
import json

router = APIRouter()


@router.post("/temerature_analyzer/")
async def parse_uploaded_file(file: UploadFile = File(...)):
    contents = await file.read()
    file.close()
    data = json.loads(contents)
    temps = [float(values["value"]) for poits, values in data["data"].items()]
    avg_temp = sum(temps) / len(temps)
    return {"filename": file.filename, "avg_temp": avg_temp}
