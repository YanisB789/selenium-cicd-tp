import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import os

class TestCalculator:
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
            # En CI, on utilise le chromedriver du système
            driver = webdriver.Chrome(options=chrome_options)
        else:
            # En local, on utilise webdriver-manager
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
        
        driver.implicitly_wait(10)
        
        yield driver
        driver.quit()
    
    def test_page_loads(self, driver):
        """Test 1: Vérifier que la page se charge correctement"""
        file_path = os.path.abspath("../src/index.html")
        driver.get(f"file://{file_path}")
        
        # Vérifier le titre
        assert "Calculatrice Simple" in driver.title
        
        # Vérifier la présence des éléments principaux
        assert driver.find_element(By.ID, "num1").is_displayed()
        assert driver.find_element(By.ID, "num2").is_displayed()
        assert driver.find_element(By.ID, "operation").is_displayed()
        assert driver.find_element(By.ID, "calculate").is_displayed()
    
    def test_addition(self, driver):
        """Test 2: Tester l'addition"""
        file_path = os.path.abspath("../src/index.html")
        driver.get(f"file://{file_path}")
        
        # Saisir les valeurs
        driver.find_element(By.ID, "num1").send_keys("10")
        driver.find_element(By.ID, "num2").send_keys("5")
        
        # Sélectionner l'addition
        select = Select(driver.find_element(By.ID, "operation"))
        select.select_by_value("add")
        
        # Cliquer sur calculer
        driver.find_element(By.ID, "calculate").click()
        
        # Vérifier le résultat
        result = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "result"))
        )
        assert "Résultat: 15" in result.text
    
    def test_division_by_zero(self, driver):
        """Test 3: Tester la division par zéro"""
        file_path = os.path.abspath("../src/index.html")
        driver.get(f"file://{file_path}")
        
        # Saisir les valeurs
        driver.find_element(By.ID, "num1").clear()
        driver.find_element(By.ID, "num1").send_keys("10")
        driver.find_element(By.ID, "num2").clear()
        driver.find_element(By.ID, "num2").send_keys("0")
        
        # Sélectionner la division
        select = Select(driver.find_element(By.ID, "operation"))
        select.select_by_value("divide")
        
        driver.find_element(By.ID, "calculate").click()
        
        # Vérifier le message d'erreur
        result = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "result"))
        )
        assert "Erreur: Division par zéro" in result.text
    
    def test_all_operations(self, driver):
        """Test 4: Tester toutes les opérations"""
        file_path = os.path.abspath("../src/index.html")
        driver.get(f"file://{file_path}")
        
        operations = [
            ("add", "8", "2", "10"),
            ("subtract", "8", "2", "6"),
            ("multiply", "8", "2", "16"),
            ("divide", "8", "2", "4")
        ]
        
        for op, num1, num2, expected in operations:
            # Nettoyer les champs
            driver.find_element(By.ID, "num1").clear()
            driver.find_element(By.ID, "num2").clear()
            
            # Saisir les valeurs
            driver.find_element(By.ID, "num1").send_keys(num1)
            driver.find_element(By.ID, "num2").send_keys(num2)
            
            # Sélectionner l'opération
            select = Select(driver.find_element(By.ID, "operation"))
            select.select_by_value(op)
            
            # Calculer
            driver.find_element(By.ID, "calculate").click()
            
            # Vérifier le résultat
            result = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "result"))
            )
            assert f"Résultat: {expected}" in result.text
            time.sleep(1)
    
    def test_page_load_time(self, driver):
        """Test 5: Mesurer le temps de chargement de la page"""
        start_time = time.time()
        
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../src/index.html"))
        driver.get(f"file://{file_path}")
        
        # Attendre que la page soit complètement chargée
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "calculator"))
        )
        
        load_time = time.time() - start_time
        print(f"\nTemps de chargement: {load_time:.2f} secondes")
        
        # Vérifier que le chargement prend moins de 3 secondes
        assert load_time < 3.0, f"Page trop lente à charger: {load_time:.2f}s"

    def test_decimal_numbers(self, driver):
        """Test 6: Tester avec des nombres décimaux"""
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../src/index.html"))
        driver.get(f"file://{file_path}")
        
        # Test avec des décimaux
        driver.find_element(By.ID, "num1").clear()
        driver.find_element(By.ID, "num1").send_keys("10.5")
        driver.find_element(By.ID, "num2").clear()
        driver.find_element(By.ID, "num2").send_keys("2.5")
        
        # Tester l'addition
        select = Select(driver.find_element(By.ID, "operation"))
        select.select_by_value("add")
        
        driver.find_element(By.ID, "calculate").click()
        
        # Attendre que le résultat contienne du texte (pas vide)
        result = WebDriverWait(driver, 10).until(
            lambda d: d.find_element(By.ID, "result").text != ""
        )
        
        result_element = driver.find_element(By.ID, "result")
        assert "Résultat: 13" in result_element.text
        
        # Tester la multiplication avec décimaux
        driver.find_element(By.ID, "num1").clear()
        driver.find_element(By.ID, "num1").send_keys("5.5")
        driver.find_element(By.ID, "num2").clear()
        driver.find_element(By.ID, "num2").send_keys("2")
        
        select.select_by_value("multiply")
        driver.find_element(By.ID, "calculate").click()
        
        # Attendre que le résultat soit mis à jour
        WebDriverWait(driver, 10).until(
            lambda d: "11" in d.find_element(By.ID, "result").text
        )
        
        result_element = driver.find_element(By.ID, "result")
        assert "Résultat: 11" in result_element.text

    def test_negative_numbers(self, driver):
        """Test 7: Tester avec des nombres négatifs"""
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../src/index.html"))
        driver.get(f"file://{file_path}")
        
        # Test avec des nombres négatifs
        driver.find_element(By.ID, "num1").clear()
        driver.find_element(By.ID, "num1").send_keys("-10")
        driver.find_element(By.ID, "num2").clear()
        driver.find_element(By.ID, "num2").send_keys("5")
        
        # Addition avec négatif
        select = Select(driver.find_element(By.ID, "operation"))
        select.select_by_value("add")
        
        driver.find_element(By.ID, "calculate").click()
        
        result = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "result"))
        )
        assert "Résultat: -5" in result.text
        
        # Soustraction avec deux négatifs
        driver.find_element(By.ID, "num1").clear()
        driver.find_element(By.ID, "num1").send_keys("-8")
        driver.find_element(By.ID, "num2").clear()
        driver.find_element(By.ID, "num2").send_keys("-3")
        
        select.select_by_value("subtract")
        driver.find_element(By.ID, "calculate").click()
        
        result = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "result"))
        )
        assert "Résultat: -5" in result.text

if __name__ == "__main__":
    pytest.main(["-v", "--html=report.html", "--self-contained-html"])