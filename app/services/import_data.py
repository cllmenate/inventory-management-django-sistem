from typing import Any

import pandas as pd
from django.core.exceptions import ValidationError
from django.db import transaction


class DataImportService:
    def __init__(self, file_obj: Any, file_type: str) -> None:
        self.file = file_obj
        self.file_type = file_type

    def extract(self) -> Any:
        """Extrai os dados do arquivo para um DataFrame do Pandas."""
        try:
            if self.file_type == "csv":
                return pd.read_csv(self.file)
            elif self.file_type == "json":
                return pd.read_json(self.file)
            elif self.file_type == "xlsx" or self.file_type == "xls":
                return pd.read_excel(self.file)
            elif self.file_type == "xml":
                try:
                    return pd.read_xml(self.file, parser="lxml")
                except Exception:
                    return pd.read_xml(self.file)
            else:
                raise ValueError(
                    f"Formato de arquivo '{self.file_type}' não suportado."
                )
        except Exception as e:
            raise ValidationError(  # noqa: B904
                f"Erro ao ler arquivo: {str(e)}"
            )

    def _resolve_foreign_key(
        self, model_class: Any, field_name: str, value: Any
    ) -> Any:
        if value is None or value == "":
            return value

        field = model_class._meta.get_field(field_name)
        if not (field.is_relation and field.many_to_one):
            return value

        if str(value).isdigit():
            return value

        related_model = field.related_model
        search_fields = ["name", "title", "nome", "titulo"]
        for s_field in search_fields:
            try:
                related_model._meta.get_field(s_field)
                related_obj = related_model.objects.filter(**{
                    f"{s_field}__iexact": str(value).strip()
                }).first()
                if related_obj:
                    return related_obj
            except Exception:
                continue

        raise ValidationError(
            f"Relacionamento '{value}' não encontrado "
            f"no modelo {related_model.__name__}."
        )

    def _prepare_row_data(
        self,
        model_class: Any,
        row_dict: dict[str, Any],
        mapping_dict: dict[str, str] | None,
    ) -> dict[str, Any]:
        data = row_dict
        if mapping_dict:
            data = {
                model_field: data.get(csv_col)
                for csv_col, model_field in mapping_dict.items()
            }

        for field_name, value in data.items():
            data[field_name] = self._resolve_foreign_key(
                model_class, field_name, value
            )

        return data

    def transform_and_load(
        self, model_class: Any, mapping_dict: dict[str, str] | None = None
    ) -> int:
        """
        Transforma e carrega os dados no modelo especificado.
        :param model_class: A classe do modelo Django (ex: Product).
        :param mapping_dict: Dicionário opcional mapeando colunas do arquivo
        para campos do modelo.
        """
        df = self.extract()

        # Otimização: Normalização de nomes de colunas
        df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

        objects_to_create = []
        errors = []

        # Itera sobre as linhas do DataFrame
        for index, row in df.iterrows():
            try:
                data = self._prepare_row_data(
                    model_class, row.to_dict(), mapping_dict
                )

                # Instancia o modelo (sem salvar ainda) para validar
                obj = model_class(**data)
                obj.full_clean()
                objects_to_create.append(obj)
            except Exception as e:
                errors.append(f"Linha {index + 1}: {str(e)}")

        if errors:
            raise ValidationError(errors)

        # Usar save() em vez de bulk_create para garantir que Signals
        # (estoque) sejam disparados
        created_count = 0
        if objects_to_create:
            with transaction.atomic():
                for obj in objects_to_create:
                    obj.save()
                    created_count += 1

            # Limpa o cache para garantir que
            # a UI mostre os novos dados imediatamente
            from django.core.cache import cache

            cache.clear()

        return created_count
