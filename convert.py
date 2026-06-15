import pandas as pd

df = pd.read_excel(
    "DOT 대시보드.xlsb",
    sheet_name="ASP",
    engine="pyxlsb"
)

day_df = pd.read_excel(
    "DOT 대시보드.xlsb",
    sheet_name="재원일수",
    engine="pyxlsb"
)

master_df = pd.read_excel(
    "DOT 대시보드.xlsb",
    sheet_name="마스터",
    engine="pyxlsb"
)

df.to_parquet("ASP.parquet", index=False)
day_df.to_parquet("재원일수.parquet", index=False)
master_df.to_parquet("마스터.parquet", index=False)

print("변환 완료")