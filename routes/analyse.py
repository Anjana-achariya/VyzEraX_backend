from fastapi import APIRouter, UploadFile, File, HTTPException
import tempfile
import os

from services.data_loader import load_dataset
from services.profiler import profile_dataframe
from services.chart_engine import generate_charts

router = APIRouter()

@router.post("/analyse")
def analyze_file(file: UploadFile = File(...)):
    suffix = os.path.splitext(file.filename)[-1]

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(file.file.read())
        tmp_path = tmp.name

    try:
        df = load_dataset(tmp_path)

        profile = profile_dataframe(df)
        charts = generate_charts(df, profile["column_summary"])

        return {
            "profile": profile,
            "charts": charts
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    finally:
        os.remove(tmp_path)
