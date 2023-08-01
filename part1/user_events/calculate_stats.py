from pathlib import Path
import pandas as pd

def calculate_stats(input_path, output_path):
    """이벤트 통계 계산하기"""
    events = pd.read_json(input_path)
    stats = events.groupby(["date", "user"]).size().reset_index()
    Path(output_path).parent.mkdir(exist_ok=True)
    stats.to_csv(output_path, index=False)
