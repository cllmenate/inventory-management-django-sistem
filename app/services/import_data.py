import pandas as pd
from django.core.exceptions import ValidationError
from django.db import transaction


class DataImportService:
    def __init__(self, file_obj, file_type):
        self.file = file_obj
        self.file_type = file_type

    def extract(self):
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

    def transform_and_load(self, model_class, mapping_dict=None):
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
                data = row.to_dict()

                # Se houver mapeamento personalizado, aplica aqui
                if mapping_dict:
                    data = {
                        model_field: data.get(csv_col)
                        for csv_col, model_field in mapping_dict.items()
                    }

                # Resolução automática de ForeignKeys por Nome/Título
                for field_name, value in data.items():
                    if value is None or value == "":
                        continue

                    field = model_class._meta.get_field(field_name)
                    if field.is_relation and field.many_to_one:
                        related_model = field.related_model
                        # Tenta encontrar o objeto pelo Nome ou Título
                        # se o valor não for um ID numérico
                        if not str(value).isdigit():
                            related_obj = None
                            # Campos comuns para busca por nome
                            search_fields = ["name", "title", "nome", "titulo"]
                            for s_field in search_fields:
                                try:
                                    related_model._meta.get_field(s_field)
                                    related_obj = related_model.objects.filter(
                                        **{f"{s_field}__iexact": str(value).strip()}  # noqa: E501
                                    ).first()
                                    if related_obj:
                                        break
                                except Exception:
                                    continue

                            if related_obj:
                                data[field_name] = related_obj
                            else:
                                raise ValidationError(
                                    f"Relacionamento '{value}' não encontrado no modelo {related_model.__name__}."  # noqa: E501
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
