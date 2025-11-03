import os
from playwright.sync_api import sync_playwright

authFile = "./CV&JD_Scraping/linkedinAuth.json"
url = input("enter the job post URL : ")
# url = "https://www.linkedin.com/jobs/collections/recommended/?currentJobId=4292766892"

with sync_playwright() as pw:
    browser = pw.chromium.launch(headless = False, slow_mo=50)

    #checks if the there's a saved session
    #if yes use it
    if os.path.exists(authFile):
        context = browser.new_context(storage_state=authFile)
        page = context.new_page()

    #if not create a new one and login then save the session
    else:
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://www.linkedin.com/login")
        emailInput = page.locator("input[type='email']")
        emailInput.fill("twodepi@gmail.com")
        passwordInput = page.locator("input[type='password']")
        passwordInput.fill("DepiDepi@1111")
        page.click("button[type='submit']")
        page.wait_for_selector("a[href*='/jobs/']", timeout=45000)
        context.storage_state(path=authFile)


    #go to the url
    page.goto(url)
    
    #get the "About the job" section
    #wait for the page to fully load
    # page.wait_for_selector("#job-details li")
    page.wait_for_selector("div.jobs-description__content")

    #get the text inside the abou this job div    
    text = page.locator("div.jobs-description--reformatted").inner_text()
    #print(text)

    with open("./final project/jobDescription.txt", "w") as f:
        f.write(text)