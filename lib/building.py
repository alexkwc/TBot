from selenium.common import exceptions

BuildingIdToLocationId = {
    '10': 20,
    '11': 21
}


class Building:
    def __init__(self, driver):
        self.driver = driver

    async def build(self, buildingId):
        self.driver.execute_script("window.location.href = 'dorf2.php'")
        buildingLoc = BuildingIdToLocationId[str(buildingId)]
        self.driver.execute_script(
            f"window.location.href = 'build.php?id={buildingLoc}'"
        )
        try:
            self.driver.find_element_by_xpath(
                f'//div[@id="contract_building{buildingId}"]'
                '//button[@class="green new"]'
            ).click()
            remainingTime = self.driver.find_element_by_xpath(
                f'//div[@class="buildDuration"]//span[@class="timer"]'
            ).get_attribute('value')
            return int(remainingTime)
        except exceptions.NoSuchElementException:
            return 0

    async def upgrade(self, buildingId):
        self.driver.execute_script("window.location.href = 'dorf2.php'")
        buildingLoc = BuildingIdToLocationId[str(buildingId)]
        self.driver.execute_script(
            f"window.location.href = 'build.php?id={buildingLoc}'"
        )
        try:
            self.driver.find_element_by_xpath(
                f'//div[starts-with(@class, "upgradeButtonsContainer")]'
                '//button[@class="green build"]'
            ).click()
            remainingTime = self.driver.find_element_by_xpath(
                f'//div[@class="buildDuration"]//span[@class="timer"]'
            ).get_attribute('value')
            return int(remainingTime)
        except exceptions.NoSuchElementException:
            return 0
