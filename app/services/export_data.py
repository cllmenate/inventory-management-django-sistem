import pandas as pd
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML


class DataExportService:
    @staticmethod
    def export_to_csv(queryset, filename):
        df = pd.DataFrame(list(queryset.values()))
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = f'attachment; filename="{filename}.csv"'
        df.to_csv(path_or_buf=response, index=False)
        return response

    @staticmethod
    def export_to_json(queryset, filename):
        df = pd.DataFrame(list(queryset.values()))
        response = HttpResponse(content_type="application/json")
        response["Content-Disposition"] = f'attachment; filename="{filename}.json"'
        df.to_json(path_or_buf=response, orient="records", indent=4)
        return response

    @staticmethod
    def export_to_xml(queryset, filename):
        df = pd.DataFrame(list(queryset.values()))
        response = HttpResponse(content_type="application/xml")
        response["Content-Disposition"] = f'attachment; filename="{filename}.xml"'
        # XML needs a root element, pandas .to_xml makes it easy
        df.to_xml(
            path_or_buffer=response, index=False, root_name="data", row_name="item"
        )
        return response

    @staticmethod
    def export_to_pdf(queryset, template_name, context, filename):
        html_string = render_to_string(template_name, context)
        try:
            html = HTML(string=html_string)
            pdf = html.write_pdf()
        except Exception:
            # Fallback or simple error message if weasyprint fails
            return HttpResponse(
                "Erro ao gerar PDF. Verifique as dependências do sistema.", status=500
            )

        response = HttpResponse(pdf, content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="{filename}.pdf"'
        return response
