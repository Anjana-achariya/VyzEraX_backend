# from fastapi import FastAPI, UploadFile, File, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# import pandas as pd
# import tempfile
# import os

# from services.data_loader import load_dataset
# from services.profiler import profile_dataframe, get_column_summary
# from services.chart_engine import generate_charts

# from routes.analyse import router as analyse_router
# from routes.insights import router as insights_router

# app = FastAPI(title="AI analytics backend")


# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],

#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
# app.include_router(analyse_router, prefix="/api")
# app.include_router(insights_router, prefix="/api")

# @app.post("/analyse")
# def analyze_file(file: UploadFile = File(...)):
#     suffix = os.path.splitext(file.filename)[-1]

#     with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
#         tmp.write(file.file.read())
#         tmp_path = tmp.name

#     try:
#         df = load_dataset(tmp_path)

#         profile = profile_dataframe(df)

        
#         print("PROFILE KEYS:", profile.keys())

#         charts = generate_charts(df, profile["column_summary"])

#         return {
#             "profile": profile,
#             "charts": charts
#         }

#     except Exception as e:
#         print("ANALYSE ERROR:", repr(e))
#         raise HTTPException(status_code=400, detail=str(e))

#     finally:
#         os.remove(tmp_path)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.analyse import router as analyse_router
from routes.insights import router as insights_router

app = FastAPI(title="AI analytics backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analyse_router, prefix="/api")
app.include_router(insights_router, prefix="/api")
