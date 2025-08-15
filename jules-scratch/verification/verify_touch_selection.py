import asyncio
from playwright.async_api import async_playwright, expect
import os

async def main():
    async with async_playwright() as p:
        # Use a device that supports touch
        iphone = p.devices['iPhone 11']
        browser = await p.webkit.launch()
        context = await browser.new_context(**iphone)
        page = await context.new_page()

        # Get the absolute path to the index.html file
        file_path = os.path.abspath('index.html')
        await page.goto(f'file://{file_path}')

        # Wait for the timeline to be rendered
        await expect(page.locator('.equipment-row')).to_have_count(7)

        # Define the blocks for the touch gesture within the day shift
        start_block_selector = '.equipment-row:first-child .shift-section[data-shift="day"] .time-block[data-index="10"]'
        end_block_selector = '.equipment-row:first-child .shift-section[data-shift="day"] .time-block[data-index="15"]'

        start_block = page.locator(start_block_selector)
        end_block = page.locator(end_block_selector)

        # Get bounding boxes for the elements
        start_box = await start_block.bounding_box()
        end_box = await end_block.bounding_box()

        # Simulate touch drag using touchscreen API
        await page.touchscreen.tap(start_box['x'] + start_box['width'] / 2, start_box['y'] + start_box['height'] / 2)

        # Start the swipe from the start block
        await page.mouse.move(start_box['x'] + start_box['width'] / 2, start_box['y'] + start_box['height'] / 2)
        await page.mouse.down()

        # Move to the end block to simulate the drag
        await page.mouse.move(end_box['x'] + end_box['width'] / 2, end_box['y'] + end_box['height'] / 2)
        await page.mouse.up()

        # Check if the booking modal is visible
        booking_modal = page.locator('#booking-modal')
        await expect(booking_modal).to_be_visible()

        # Check if the selection info is visible
        selection_info = page.locator('#selection-info')
        await expect(selection_info).to_be_visible()

        # Take a screenshot
        await page.screenshot(path="jules-scratch/verification/verification.png")

        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
