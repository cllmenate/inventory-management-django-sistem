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

                # Limpeza básica de dados
                # (remover None de campos obrigatórios se necessário)
                # ou conversão de tipos específicos

                # Instancia o modelo (sem salvar ainda) para validar
                obj = model_class(**data)
                obj.full_clean()
                objects_to_create.append(obj)
            except Exception as e:
                errors.append(f"Linha {index + 1}: {str(e)}")

        if errors:
            raise ValidationError(errors)

        # Bulk Create para performance (Best Practice em Django)
        if objects_to_create:
            with transaction.atomic():
                model_class.objects.bulk_create(objects_to_create)

        return len(objects_to_create)
