import pandas as pd
from io import BytesIO
import openpyxl


def gerar_excel(dados):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        dados.to_excel(writer, index=False, sheet_name="HSE")
    return output.getvalue()


def test_excel_contains_hse_sheet():
    df = pd.DataFrame({"A": [1, 2]})
    result = gerar_excel(df)
    wb = openpyxl.load_workbook(BytesIO(result))
    assert "HSE" in wb.sheetnames
