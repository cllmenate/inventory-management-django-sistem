import pandas as pd
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML


class DataExportService:
    @staticmethod
    def _prepare_data(queryset):
        """Prepara os dados do queryset, convertendo relações para strings."""
        data = []
        for obj in queryset:
            item = {}
            for field in obj._meta.fields:
                value = getattr(obj, field.name)
                # Se for uma relação (ForeignKey),
                # usa a representação em string (__str__)
                if field.is_relation and value:
                    item[field.name] = str(value)
                else:
                    item[field.name] = value
            data.append(item)
        return pd.DataFrame(data)

    @staticmethod
    def export_to_csv(queryset, filename):
        df = DataExportService._prepare_data(queryset)
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = f'attachment; filename="{filename}.csv"'  # noqa: E501
        df.to_csv(path_or_buf=response, index=False)
        return response

    @staticmethod
    def export_to_json(queryset, filename):
        df = DataExportService._prepare_data(queryset)
        response = HttpResponse(content_type="application/json")
        response["Content-Disposition"] = f'attachment; filename="{filename}.json"'  # noqa: E501
        df.to_json(path_or_buf=response, orient="records", indent=4)
        return response

    @staticmethod
    def export_to_xml(queryset, filename):
        df = DataExportService._prepare_data(queryset)
        response = HttpResponse(content_type="application/xml")
        response["Content-Disposition"] = f'attachment; filename="{filename}.xml"'  # noqa: E501
        # XML needs a root element, pandas .to_xml makes it easy
        try:
            df.to_xml(
                path_or_buffer=response,
                index=False,
                root_name="data",
                row_name="item",
                parser="lxml",
            )
        except Exception:
            # Fallback if lxml is not behaving or not found
            # (though we added it)
            df.to_xml(
                path_or_buffer=response,
                index=False,
                root_name="data",
                row_name="item",
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
                "Erro ao gerar PDF. Verifique as dependências do sistema.",
                status=500,
            )

        response = HttpResponse(pdf, content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="{filename}.pdf"'  # noqa: E501
        return response
