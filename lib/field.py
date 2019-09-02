import asyncio
import random

from selenium.common import exceptions


FieldMap = {
    'l1': 'Woodcutter',
    'l2': 'Clay Pit',
    'l3': 'Iorn Mine',
    'l4': 'Cropland',
}


class Field:
    def __init__(self, driver):
        self.driver = driver

    async def upgrade(self, fieldType, fieldLevel):
        self.driver.execute_script("window.location.href = 'dorf1.php'")
        targetFieldType = FieldMap[fieldType]
        targetFieldName = f'{targetFieldType} Level {fieldLevel}'
        try:
            href = self.driver.find_element_by_xpath(
                f'//*[@alt="{targetFieldName}"]'
            ).get_attribute('href')
            for _ in range(0, 3):
                self.driver.get(href)
                waitTime = await self.upgradeField()
                if waitTime is not None:
                    # Either upgrade success or failed for unknown reason
                    await asyncio.sleep(waitTime)
                    return True

        except exceptions.NoSuchElementException:
            print(f"Error: {targetFieldName} does not exist.")
            return False

    async def upgradeField(self):
        try:
            upgrade = self.driver.find_element_by_xpath(
                f'//button[@class="green build"]'
            ).get_attribute('onclick')
            self.driver.execute_script(upgrade)
            return int(self.driver.find_element_by_xpath(
                f'//div[@class="buildDuration"]//span[@class="timer"]'
            ).get_attribute('value'))
        except exceptions.NoSuchElementException:
            waitTime = None
            try:
                waitTime = self.driver.find_element_by_xpath(
                    f'//span[@class="timer" and @counting="down"]'
                ).get_attribute('value')
                print(f"Unable to upgrade field. Retry in {waitTime}s")
                return waitTime + random.randint(0, 120)
            except Exception as e:
                print(f"Unknown Error: {e}")

    async def getAllFieldsInfoById(self, villageId):
        self.driver.execute_script(
            f"window.location.href = 'dorf1.php?newdid={villageId}'"
        )
        fieldInfo = {}
        for _, feildType in FieldMap.items():
            fieldInfo[feildType] = []
            fields = self.driver.find_elements_by_xpath(
                f'//area[starts-with(@alt, "{feildType}")]'
            )
            for field in fields:
                [fieldName, _, levelStr] = field.get_attribute(
                    "alt"
                ).split(" ")
                fieldInfo[fieldName].append(int(levelStr))
        return fieldInfo

    async def getBuildDuration(self):
        self.driver.execute_script("window.location.href = 'dorf1.php'")
        try:
            remainingTime = self.driver.find_element_by_xpath(
                f'//div[@class="buildDuration"]//span[@class="timer"]'
            ).get_attribute('value')
            return int(remainingTime)
        except exceptions.NoSuchElementException:
            return 0
