import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select


class CalculatorPage:
    """Page Object pour la page calculatrice"""
    
    def __init__(self, driver):
        self.driver = driver
        self.url = os.path.abspath(os.path.join(os.path.dirname(__file__), "../src/index.html"))
    
    def load_page(self):
        """Charge la page de la calculatrice"""
        self.driver.get(f"file://{self.url}")
    
    def enter_first_number(self, value):
        """Entre le premier nombre"""
        element = self.driver.find_element(By.ID, "num1")
        element.clear()
        element.send_keys(str(value))
    
    def enter_second_number(self, value):
        """Entre le deuxième nombre"""
        element = self.driver.find_element(By.ID, "num2")
        element.clear()
        element.send_keys(str(value))
    
    def select_operation(self, operation):
        """Sélectionne l'opération (add, subtract, multiply, divide)"""
        select = Select(self.driver.find_element(By.ID, "operation"))
        select.select_by_value(operation)
    
    def click_calculate(self):
        """Clique sur le bouton Calculer"""
        self.driver.find_element(By.ID, "calculate").click()
    
    def get_result(self):
        """Récupère le résultat affiché"""
        result = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "result"))
        )
        return result.text
    
    def calculate(self, num1, operation, num2):
        """Effectue un calcul complet"""
        self.enter_first_number(num1)
        self.enter_second_number(num2)
        self.select_operation(operation)
        self.click_calculate()
        return self.get_result()
    
    def is_page_loaded(self):
        """Vérifie que la page est chargée"""
        return "Calculatrice Simple" in self.driver.title
    
    def get_title(self):
        """Récupère le titre de la page"""
        return self.driver.find_element(By.TAG_NAME, "h1").text