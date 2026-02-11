import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
from calculator_page import CalculatorPage


class TestCalculatorPOM:
    """Tests utilisant le Page Object Pattern"""
    
    @pytest.fixture(scope="class")
    def driver(self):
        """Configuration du driver Chrome pour les tests"""
        chrome_options = Options()
        
        # Configuration pour environnement CI/CD
        if os.getenv('CI'):
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            driver = webdriver.Chrome(options=chrome_options)
        else:
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
        
        driver.implicitly_wait(10)
        
        yield driver
        driver.quit()
    
    @pytest.fixture(scope="function")
    def calculator_page(self, driver):
        """Fixture qui retourne une instance de CalculatorPage"""
        page = CalculatorPage(driver)
        page.load_page()
        return page
    
    def test_page_loads_pom(self, calculator_page):
        """Test 1: Vérifier que la page se charge avec POM"""
        assert calculator_page.is_page_loaded()
        assert calculator_page.get_title() == "Calculatrice Simple"
    
    def test_addition_pom(self, calculator_page):
        """Test 2: Test de l'addition avec POM"""
        result = calculator_page.calculate(15, "add", 10)
        assert "Résultat: 25" in result
    
    def test_subtraction_pom(self, calculator_page):
        """Test 3: Test de la soustraction avec POM"""
        result = calculator_page.calculate(20, "subtract", 8)
        assert "Résultat: 12" in result
    
    def test_multiplication_pom(self, calculator_page):
        """Test 4: Test de la multiplication avec POM"""
        result = calculator_page.calculate(6, "multiply", 7)
        assert "Résultat: 42" in result
    
    def test_division_pom(self, calculator_page):
        """Test 5: Test de la division avec POM"""
        result = calculator_page.calculate(100, "divide", 4)
        assert "Résultat: 25" in result
    
    def test_division_by_zero_pom(self, calculator_page):
        """Test 6: Test de la division par zéro avec POM"""
        result = calculator_page.calculate(10, "divide", 0)
        assert "Erreur: Division par zéro" in result
    
    def test_decimals_pom(self, calculator_page):
        """Test 7: Test avec décimaux avec POM"""
        result = calculator_page.calculate(7.5, "add", 2.5)
        assert "Résultat: 10" in result
    
    def test_negatives_pom(self, calculator_page):
        """Test 8: Test avec négatifs avec POM"""
        result = calculator_page.calculate(-5, "multiply", 3)
        assert "Résultat: -15" in result


if __name__ == "__main__":
    pytest.main(["-v", "--html=report-pom.html", "--self-contained-html"])