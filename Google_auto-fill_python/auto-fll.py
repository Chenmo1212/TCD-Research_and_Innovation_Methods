import random
from time import sleep

import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains


def get_values(need_len):
    res = []

    for i in range(need_len):
        need_data = {
            'row': np.array([]),
            'col': np.array([])
        }

        for part in new_row_data:
            temp = [0] * len(part)
            index = random.choices(list(range(len(part))), weights=part)[0]
            temp[index] = 1

            need_data['row'] = np.hstack((need_data['row'], np.array(temp)))

        for index, part in enumerate(new_col_data):
            temp = [0] * len(part)
            idx = random.choices(list(range(len(part))), weights=part)[0]
            temp[idx] = 1

            if index == 4:
                new_index = random.choices(list(range(len(part))), weights=part)[0]
                temp[new_index] = 1

            # need_data['col'].append(temp)
            need_data['col'] = np.hstack((need_data['col'], np.array(temp)))

        need_data['row'] = list(np.rint(need_data['row']))
        need_data['col'] = list(np.rint(need_data['col']))
        res.append(need_data)

    return res


def fill_form(row_data, col_data):
    option = webdriver.ChromeOptions()
    option.add_experimental_option("detach", True)

    option.add_argument("-incognito")
    option.add_experimental_option("excludeSwitches", ['enable-automation'])
    # option.add_argument("--headless")  # Use this and the following option to run Headless
    # option.add_argument("disable-gpu")

    s = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=s, options=option)
    driver.maximize_window()
    driver.get('https://forms.gle/b9SvcgtfmzMwA4o76')
    # driver.get('https://forms.gle/XhBb4rCRJsQn235i6')

    # Use the following snippets to get elements by their class names
    radio_buttons = driver.find_elements(By.CLASS_NAME, "docssharedWizToggleLabeledContainer")
    row_radio_buttons = driver.find_elements(By.CLASS_NAME, "T5pZmf")

    for index, item in enumerate(row_data):
        if item == 1.0:
            row_radio_buttons[index].click()

    for index, item in enumerate(col_data):
        if item == 1.0:
            radio_buttons[index].click()

    submit = driver.find_element(By.CLASS_NAME, "uArJ5e.UQuaGc.Y5sE8d.VkkpIf.QvWxOd")
    print(submit)
    actions = ActionChains(driver)
    actions.move_to_element(submit).click().perform()

    sleep(1)
    driver.close()


def get_new_data(origin):
    new_data = []
    for i in origin:
        values = list(i.values())
        values = np.array(values)
        values = np.rint(values * need)
        new_data.append(list(values))
    return new_data


if __name__ == '__main__':
    curr_total = 34

    row_radio_data = [
        {"a": 1 / curr_total, "b": 2 / curr_total, "c": 19 / curr_total, "d": 9 / curr_total, "e": 0 / curr_total, },
        {"a": 1 / curr_total, "b": 4 / curr_total, "c": 9 / curr_total, "d": 11 / curr_total, "e": 8 / curr_total, },
        {"a": 0 / curr_total, "b": 3 / curr_total, "c": 3 / curr_total, "d": 6 / curr_total, "e": 22 / curr_total, },
        {"a": 7 / curr_total, "b": 12 / curr_total, "c": 4 / curr_total, "d": 7 / curr_total, "e": 4 / curr_total, },
        {"a": 5 / curr_total, "b": 4 / curr_total, "c": 9 / curr_total, "d": 12 / curr_total, "e": 4 / curr_total, }]

    col_radio_data = [
        {"a": 8.8 / 100, "b": 52.9 / 100, "c": 23.5 / 100, "d": 14.7 / 100},
        {"a": 20.6 / 100, "b": 79.4 / 100},
        {"a": 15.2 / 100, "b": 24.2 / 100, "c": 30.3 / 100, "d": 27.3 / 100, "e": 2.99 / 100, },
        {"a": 70.6 / 100, "b": 79.4 / 100, "c": 5.9 / 100},
        {"a": 17.6 / 100, "b": 29.4 / 100, "c": 64.7 / 100, "d": 17.6 / 100, "e": 29.4 / 100},
        {"a": 67.6 / 100, "b": 23.5 / 100, "c": 8.8 / 100}]

    total = 50
    need = total - curr_total

    new_row_data = get_new_data(row_radio_data)
    new_col_data = get_new_data(col_radio_data)

    need_data = get_values(need)

    for i in need_data[:5]:
        fill_form(row_data=i['row'], col_data=i['col'])
        sleep(1)
