from selenium import webdriver
from selenium.webdriver.common.by import By
import time, pdb, itertools

categories = {
    'colors': {'#008002', '#ff0101', '#800080'},
    'fills': {'url(#mask-stripe)', '', 'transparent'},
    'counts': {1,2,3},
    'shape': {'#diamond', '#oval', '#squiggle'}
}

if __name__ == '__main__':
    driver = webdriver.Firefox()
    # Open setwithfriends
    driver.get('https://setwithfriends.com/')
    time.sleep(3)
    driver.find_element(By.XPATH, '//span[text()="Enter"]').click()
    driver.find_element(By.XPATH, "//button[@title='Create a new game, which will appear in the lobby. You can also invite your friends to join by link!']").click()
    time.sleep(1)
    input("Press Enter to continue...")
    driver.find_element(By.XPATH, '//span[text()="Start game"]').click()
    # Play the set game
    time.sleep(1)
    while True:
        cards = {}
        start = time.time()
        for card in driver.find_elements(By.XPATH, "//div[contains(@style, 'visibility: visible;')]"):
            svg_uses = card.find_elements(By.CSS_SELECTOR, 'svg > use')
            shape = svg_uses[0].get_attribute('href')
            count = len(card.find_elements(By.CSS_SELECTOR, 'svg'))
            color = svg_uses[1].get_attribute('stroke')
            fill = 'transparent' if svg_uses[0].get_attribute('fill') == 'transparent' else svg_uses[0].get_attribute('mask')
            cards[(color, fill, count, shape)] = card
        start = time.time()
        for comb in itertools.combinations(cards.keys(), 2):
            missing = []
            for i, category in enumerate(categories):
                missing.append(comb[0][i] if comb[0][i] == comb[1][i] else list(categories[category] ^ {comb[0][i], comb[1][i]})[0])
            if tuple(missing) in cards:
                try:
                    start = time.time()
                    cards[tuple(missing)].click()
                    cards[comb[0]].click()
                    cards[comb[1]].click()
                finally:
                    continue

