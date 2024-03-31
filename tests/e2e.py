from selenium import webdriver
from selenium.webdriver.common.by import By
import sys


def test_scores_service(url):

    driver = webdriver.Chrome()

    try:
        driver.get(url)
        score_element = driver.find_element(By.ID, 'current_score')
        print(score_element.text)
        return 1 <= int(score_element.text) <= 1000

    except Exception as e:
        print(f"An error occurred: {e}")
        return False
    finally:
        driver.quit()


def main_function(url):

    if test_scores_service(url):
        print('Test passed!')
        return 0
    else:
        print('Test failed!')
        return -1


if __name__ == "__main__":
    test_url = 'http://localhost:8777/score'
    exit_code = main_function(test_url)
    sys.exit(exit_code)
