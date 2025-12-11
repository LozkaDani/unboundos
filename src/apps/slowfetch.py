import os
class slowfetch_class():
    def __init__(self):
        self.OS_NAME=""
        self.WM=""
        self.VERSION=""
        self.config = {}
        self.config = self.parse_simple_config('root/system/cfg/slowfetch.cfg')
        self.slowfetch_out()


    def parse_simple_config(self, file_path):
        """Парсит простой конфиг в формате ключ=значение"""
        self.config = {}
        current_dir = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(current_dir, file_path)

        with open(full_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # Пропускаем пустые строки и комментарии
                if not line or line.startswith('#'):
                    continue

                # Разделяем по первому знаку '='
                if '=' in line:
                    key, value = line.split('=', 1)
                    self.config[key.strip()] = value.strip()

        return self.config


    def slowfetch_out(self):
        global config
        self.OS_NAME = self.config.get('OS_NAME')
        self.WM = self.config.get('WM')
        self.VERSION = self.config.get('VERSION')
        #print(self.OS_NAME, self.WM, self.VERSION)
        print(f" ___        	    ___          ")
        print(f"/   \       	   /   \         OS: {self.OS_NAME}")
        print(f"|   |              |   |         WM: {self.WM}")
        print(f"| @ |   UnboundOS  | @ |         VERSION: {self.VERSION}")
        print(f"|   |              |   |         ")
        print(f"\___/     \___/    \___/         ")
        print("")
        print("")
        print("")
