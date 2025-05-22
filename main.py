import asyncio
from playwright.async_api import async_playwright


async def check_all_arco_checkboxes(page):
    # Tìm tất cả các label chứa checkbox
    labels = await page.query_selector_all('label.arco-checkbox')

    for label in labels:
        # Kiểm tra nếu nó chưa checked (dựa vào class chứa "arco-checkbox-checked")
        label_class = await label.get_attribute("class")
        if label_class and "arco-checkbox-checked" not in label_class:
            # continue arco-checkbox checkbox-YKibDc
            if any(cls.startswith("checkbox-") for cls in label_class.split()):
                continue
            print("label_class: ", label_class)
            await label.click()

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # Để quan sát trình duyệt
        context = await browser.new_context()

        # Tab 1: Lấy email tạm thời
        temp_mail_page = await context.new_page()
        await temp_mail_page.goto("https://temp-mail.org/vi/", timeout=40000)  # 60 giây
        await temp_mail_page.wait_for_selector('input#mail')
        await asyncio.sleep(2)  # Đợi email hiển thị

        # Lấy email từ input field
        email_input = await temp_mail_page.query_selector('input#mail')
        email = await email_input.input_value()
        print("Email tạm thời:", email)

        # Tab 2: Mở trang đăng ký BytePlus
        byteplus_page = await context.new_page()
        await byteplus_page.goto("https://console.byteplus.com/auth/signup")
        await byteplus_page.wait_for_selector('input#Email_input')
        await asyncio.sleep(1)

        # Điền email vào ô đăng ký
        await byteplus_page.fill('input#Email_input', email)

        username = email.split('@')[0]
        await byteplus_page.wait_for_selector('input#Identity_input')

        # Điền username vào ô đăng ký
        await byteplus_page.fill('input#Identity_input', username)

        await byteplus_page.wait_for_selector('input#Password_input')

        # Điền password vào ô đăng ký
        password = 'Abcd123@123'
        await byteplus_page.fill('input#Password_input', password)

        await  check_all_arco_checkboxes(byteplus_page)
        # Chờ nút xuất hiện
        await byteplus_page.wait_for_selector('button[type="submit"]:has-text("Verify email address")')

        # Click vào nút
        await byteplus_page.click('button[type="submit"]:has-text("Verify email address")')
        # Đợi để bạn xem hoặc tiếp tục điền các trường khác nếu cần
        await asyncio.sleep(40000)

        # await browser.close()

asyncio.run(main())
