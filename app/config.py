import json
import os
from typing import Any

DEFAULT_SETTINGS_PATH = "app/settings.json"

class Config:
    def __init__(self, config_path: str = DEFAULT_SETTINGS_PATH):
        self.config_path = config_path
        self.settings = self.load_settings()

    def load_settings(self) -> dict[str, Any]:
        if os.path.exists(self.config_path):
            with open(self.config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        # 默认结构，避免 KeyError
        return {
            "whisper_path": "",
            "model_path": "",
            "openvino_script_path": "",
            "openvino_enabled": False,
            "openvino_shell": "auto",
        }

    def get(self, key: str, default=None):
        return self.settings.get(key, default)

    def set(self, key: str, value):
        self.settings[key] = value
        self.save()

    def save(self):
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(self.settings, f, indent=4, ensure_ascii=False)

config = Config()
