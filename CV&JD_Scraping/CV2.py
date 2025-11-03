import os
from playwright.sync_api import sync_playwright

authFile = "./CV&JD_Scraping/linkedinAuth.json"
url = input("enter the profile URL : ")
# url = "https://www.linkedin.com/in/baraasallout/"

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

    page.wait_for_selector("section.pv-profile-card:has(#experience)")

    #get the name
    name = page.locator("h1").first.inner_text()
    # with open("./final project/cvv.txt", "a") as f:
    #     f.write("Name: "+ name+ "\n")

    #get the "about text"
    about = page.locator("div.display-flex.ph5.pv3").first.inner_text()

    #press show all experiences button if found
    expSeeAllButton = page.locator("#navigation-index-see-all-experiences")
    allExp = []
    if expSeeAllButton.count() > 0:
        expSeeAllButton.first.click()
        # wait for the detailed layout
        page.wait_for_selector("li.pvs-list__paged-list-item", timeout=20000)
        expBlocks = page.locator("li.pvs-list__paged-list-item span[aria-hidden='true']")
        for i in range(expBlocks.count()):
            allExp.append(expBlocks.nth(i).inner_text())
        #go back from the exp page
        page.go_back()
    else:
        expBlocks = page.locator("#experience ~ div ul > li.artdeco-list__item span[aria-hidden='true']")
        for i in range(expBlocks.count()):
            allExp.append(expBlocks.nth(i).inner_text())


    #press the show all button in the skills section
    #^= : starts with,   *= contains
    skillsSeeAllButton = page.locator("a[id^='navigation-index-Show-all-'][id*='skills']")
    if skillsSeeAllButton:
        skillsSeeAllButton.click()
        # wait for the detailed layout
        page.wait_for_selector("a[data-field='skill_page_skill_topic']", timeout=20000)
        #scroll down to load more skills
        previousCount = 0
        while True:
            # page.mouse.wheel(0, 1000)
            # page.wait_for_timeout(1000)
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(1000)
            currentcount = page.locator("a[data-field='skill_page_skill_topic']").count()
            if currentcount == previousCount:
                print(currentcount)
                break
            previousCount = currentcount
        skillBlocks = page.locator("a[data-field='skill_page_skill_topic'] span[aria-hidden='true']")
    
    allSkills = []
    for j in range(skillBlocks.count()):
        allSkills.append(skillBlocks.nth(j).inner_text().strip())

    #clear duplicate skills
    skillsClean = []
    for skill in allSkills:
        if skill not in skillsClean:
            skillsClean.append(skill)


    with open("./final/cv.txt", "w", encoding="utf-8") as f:
        f.write("Name: "+ name+ "\n"+ 
                "About: \n"+ about+ "\n"+
                "Experience: \n"+ "\n".join(allExp)+ "\n"
                "Skills: \n"+ "\n".join(skillsClean))
