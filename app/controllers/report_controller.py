import pandas as pd
from fastapi import APIRouter
from starlette.responses import FileResponse

from app.services.driver.news_crud import get_news_sheets
from app.services.driver.prompts_crud import get_prompts

router = APIRouter()


@router.get("/report/")
def generate_report() -> FileResponse:
    """
    Generate an Excel report based on prompt entries and sheet entries.

    Returns:
        FileResponse: The generated Excel report as a file response.
    """
    prompt_entry = get_prompts()
    sheet_entries = get_news_sheets()

    df_indicators = pd.DataFrame([i for i in prompt_entry])

    df_report = pd.DataFrame(columns=['id'] + df_indicators['indicator_name'].tolist())

    report_rows = []
    for entry in sheet_entries:
        row = {'id': entry["url"],
               'fecha': entry["date"],
               'texto': entry["text"],
               'etiqueta': entry["tag"]}

        if entry["sheet"] is not None:
            for indicator in entry["sheet"]["indicators"]:
                if indicator["indicator_name"] in [i["indicator_name"] for i in prompt_entry]:
                    row[indicator["indicator_name"]] = indicator["response"]

            missing_indicators = set(df_report.columns) - set(row.keys())
            for ind in missing_indicators:
                row[ind] = "Dato no extraído"

            report_rows.append(row)

    df_report = pd.concat([df_report, pd.DataFrame(report_rows)], ignore_index=True)

    df_report.set_index('id', inplace=True)

    df_report.replace([float('inf'), float('-inf')], "Infinito", inplace=True)
    df_report.fillna("Dato no extraído", inplace=True)
    file_path = "reporte.xlsx"
    df_report.to_excel(file_path)

    return FileResponse(path=file_path, filename="reporte.xlsx",
                        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
