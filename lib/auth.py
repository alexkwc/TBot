import asyncio


class Auth:
    def __init__(self, driver, username, password, baseUrl):
        self.driver = driver
        self.username = username
        self.password = password
        self.baseUrl = baseUrl

    async def login(self):
        self.driver.find_element_by_xpath(
            f'//input[@type="text"]'
        ).send_keys(self.username)
        self.driver.find_element_by_xpath(
            f'//input[@type="password"]'
        ).send_keys(self.password)
        self.driver.find_element_by_xpath(
            f'//input[@type="password"]'
        ).submit()
        return True

    async def logout(self):
        return self.driver.execute_script("window.location.href='logout.php'")

    async def tmpLogout(self, waitTime):
        await self.logout()
        await asyncio.sleep(waitTime)
        self.driver.get(self.baseUrl)
        await self.login()
