import pandas as pd

def generate_charts(df: pd.DataFrame,column_summary:dict)-> list:
    charts=[]
    for col in column_summary.get("numeric",[]):
        charts.append({
            "type":"histogram",
            "column":col
        })
        charts.append({
            "type":"box",
            "column":col
        })
        
    for col in column_summary.get("categorical",[]):
        charts.append({
            "type":"bar",
            "column":col,
            "topn":10
        })
        
    for col in column_summary.get("datetime",[]):
        charts.append({
            "type":"line",
            "x":col,
            "metric":"count"
        })
    return charts