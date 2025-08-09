import json
import os

class Config:
    def __init__(self, config_path="app/settings.json"):
        self.config_path = config_path
        self.settings = self.load_settings()

    def load_settings(self):
        """加载设置文件"""
        if os.path.exists(self.config_path):
            with open(self.config_path, "r") as f:
                return json.load(f)
        else:
            raise FileNotFoundError(f"Configuration file {self.config_path} not found.")

    def get(self, key, default=None):
        """获取配置项，若不存在则返回默认值"""
        return self.settings.get(key, default)
    
    def set(self, key, value):
        """设置配置项并保存到文件"""
        self.settings[key] = value
        with open(self.config_path, "w") as f:
            json.dump(self.settings, f, indent=4)
