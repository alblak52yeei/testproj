from Src.Logics.reporting import reporting

class csv_reporting(reporting):
    def create(self, key: str) -> str:
        data = self.data
        keys = []

        # Получаем список всех атрибутов и проходим по ним
        attrs = dir(data[key][0]) 

        for attr in attrs:
            if not attr.startswith("_") or attr.startswith("create_"):
                keys.append(attr)

        self.fields = keys

        data = self.data[key]
        headers = "; ".join(self.fields)
        result = headers + '\n'
        
        for element in data:
            row = ""

            for field in self.fields:
                val = getattr(element, field)
                row += f"{val}; "

            result += row[:-1] + '\n'
        
        return result