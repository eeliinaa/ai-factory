from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Font

from ..domain import SpreadsheetArtifactSpec
from .pathing import artifact_output_path


def render_spreadsheet_artifact(output_dir: Path, file_name: str, spec: SpreadsheetArtifactSpec) -> tuple[Path, str]:
    file_path, rendered_format = artifact_output_path(output_dir, file_name, "xlsx")
    file_path.parent.mkdir(parents=True, exist_ok=True)

    workbook = Workbook()
    default_sheet = workbook.active
    workbook.remove(default_sheet)

    for index, sheet_spec in enumerate(spec.sheets):
        worksheet = workbook.create_sheet(title=sheet_spec.name[:31] or f"Sheet{index + 1}")
        for column_index, column_spec in enumerate(sheet_spec.columns, start=1):
            cell = worksheet.cell(row=1, column=column_index, value=column_spec.header)
            cell.font = Font(bold=True)
            if column_spec.width:
                worksheet.column_dimensions[cell.column_letter].width = column_spec.width
        for row_index, row_values in enumerate(sheet_spec.rows, start=2):
            for column_index, value in enumerate(row_values, start=1):
                worksheet.cell(row=row_index, column=column_index, value=value)
        worksheet.freeze_panes = "A2"

    if not spec.sheets:
        worksheet = workbook.create_sheet(title="Sheet1")
        worksheet["A1"] = spec.workbook_title
        worksheet.freeze_panes = "A2"

    workbook.save(file_path)
    return file_path, rendered_format