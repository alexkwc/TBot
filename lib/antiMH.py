class AntiMH:
    def __init__(self, driver):
        self.driver = driver
        self.wakeUpTime = None

    async def getServerTime(self):
        return int(
            self.driver.find_element_by_xpath(
                '//div[@id="servertime"]'
                '//span[@class="timer" and @counting="up"]'
                ).get_attribute("value")
            )
