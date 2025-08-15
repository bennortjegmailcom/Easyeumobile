from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # iPhone 11 viewport
        context = browser.new_context(
            viewport={'width': 414, 'height': 896},
            is_mobile=True,
            user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 13_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Mobile/15E148 Safari/604.1'
        )
        page = context.new_page()
        try:
            page.goto("http://localhost:5173")
            page.wait_for_load_state('networkidle')
            page.screenshot(path="jules-scratch/verification/verification.png")
        except Exception as e:
            print(f"An error occurred: {e}")
            # Try a different port if 5173 fails
            try:
                page.goto("http://localhost:3000")
                page.wait_for_load_state('networkidle')
                page.screenshot(path="jules-scratch/verification/verification.png")
            except Exception as e2:
                print(f"An error occurred on port 3000 as well: {e2}")
        finally:
            browser.close()

if __name__ == "__main__":
    run()
