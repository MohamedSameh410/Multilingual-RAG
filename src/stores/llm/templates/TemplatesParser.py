import os
import logging

class TemplatesParser:
    
    def __init__(self, language: str, default_language: str = "english"):
        
        self.current_path = os.path.dirname(os.path.abspath(__file__))
        self.default_language = default_language
        self.language = None

        self.logger = logging.getLogger(__name__)

        self.set_language(language= language)

    def set_language(self, language: str):
        
        if not language:
            self.logger.warning(f"Language is not set. Defaulting to default language: {self.default_language}.")
            self.language = self.default_language
        
        language_path = os.path.join(self.current_path, "locales", language.lower())
        if os.path.exists(language_path):
            self.language = language.lower()
        else:
            self.logger.warning(f"Language {language} not found. Defaulting to default language: {self.default_language}.")
            self.language = self.default_language

    def get(self, group: str, key: str, vars: dict = {}):

        if not group or not key:
            return None
        
        group_path = os.path.join(self.current_path, "locales", self.language, f"{group}.py")
        targeted_language = self.language
        
        if not os.path.exists(group_path):
            group_path = os.path.join(self.current_path, "locales", self.default_language, f"{group}.py")
            targeted_language = self.default_language

        if not os.path.exists(group_path):
            self.logger.warning(f"Group {group} not found in any language.")
            return None
        
        module = __import__(f"stores.llm.templates.locales.{targeted_language}.{group}", fromlist= [group])

        if  not module:
            self.logger.warning(f"Module {group} not found in language {targeted_language}.")
            return None
        
        key_attribute = getattr(module, key)
        return key_attribute.substitute(vars)
