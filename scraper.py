from playwright.async_api import async_playwright
import asyncio

async def extract_all_reactions(post_url, li_at_cookie, queue):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        await context.add_cookies([{
            'name': 'li_at',
            'value': li_at_cookie,
            'domain': '.www.linkedin.com',
            'path': '/'
        }])
        page = await context.new_page()
        await page.goto(post_url)
        try:
            await page.wait_for_selector('button.social-details-social-counts__count-value', timeout=10000)
            await page.click('button.social-details-social-counts__count-value')
        except Exception:
            try:
                await page.wait_for_selector('button.social-details-social-counts__reactions-count', timeout=10000)
                await page.click('button.social-details-social-counts__reactions-count')
            except Exception:
                await browser.close()
                await queue.put(None)
                return
        try:
            await page.wait_for_selector('.artdeco-modal__content', timeout=10000)
        except Exception:
            await browser.close()
            await queue.put(None)
            return
        
        await page.wait_for_timeout(2000)
        modal_content = page.locator('.artdeco-modal__content')
        previous_height = 0
        current_height = await modal_content.evaluate("el => el.scrollHeight")
        while previous_height != current_height:
            previous_height = current_height
            await modal_content.evaluate("el => el.scrollTo(0, el.scrollHeight)")
            await page.wait_for_timeout(1500)
            current_height = await modal_content.evaluate("el => el.scrollHeight")
        
        items = page.locator('li.artdeco-list__item')
        count = await items.count()
        for i in range(count):
            item = items.nth(i)
            try:
                link_loc = item.locator('a').first
                link = await link_loc.get_attribute('href')
                if link and "linkedin.com" not in link:
                    link = "https://www.linkedin.com" + link
                
                text_content = await item.inner_text()
                lines = [line.strip() for line in text_content.split('\n') if line.strip()]
                if len(lines) >= 1:
                    name = lines[0]
                    headline = lines[1] if len(lines) > 1 else "No headline"
                    profile_data = {"name": name, "headline": headline, "url": link or "N/A"}
                    await queue.put(profile_data)
            except Exception:
                pass

        await browser.close()
        await queue.put(None)
