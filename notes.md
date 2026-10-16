# My Notes: Telecom Self-Healing Test Pipeline

## Day 0: Understanding the problem

### 1. What is a button's hidden id?
- A button on a web page has a name users see, like "Recharge Now".
- It also has a hidden name tag in the code, called an id, like "btn1".
- Users never see the id, but the computer uses it.

### 2. What is a locator?
- A locator is the hidden id (or address) my test uses to find a button.
- Example: "Click the button with id btn1."

### 3. What is a test file?
- A test file is my test steps written in Python so the computer can run them.
- A manual test case is followed by a person.
- A test file is followed by the computer, without anyone watching.

### 4. Why does a test fail when the app works fine?
- A developer renames the hidden id (btn1 becomes recharge-button).
- The developer updates the app everywhere, so the app still works.
- My test file is separate, and nobody updated it.
- The test still looks for btn1, can't find it, and fails.
- Nobody told the tester, and the button looks the same on screen.

### 5. Key words
- False failure: the test fails but the app is fine.
- Test maintenance: fixing broken tests by hand.
- Self-healing: AI finds the new id and fixes the test.

### 6. My project in one line
- I am building a system that tests a telecom app automatically,
  and uses AI to fix tests that break because of renamed ids.


### Day 1: installing Python in Vscode 
- Installed Git in pc
- Installed Python in Vs code
- in VS code singed in using Git
- Cloned GitHub repo in to my VS code
- Im using Git tool to save my work im using GitHub website
-git status: shows what changed.
git add: chooses which changed files go into the next snapshot.
git commit: saves the snapshot on my laptop, with a message.
git push: uploads the snapshots to GitHub

## Day 2
- Built a small telecom app with 3 pages: login -> plans -> recharge
- Every box and button has a hidden id, like login-btn and recharge-btn
- Tests find elements using these ids (locators)
- I found ids with right-click -> Inspect
- The app only works while my server is running: python -m http.server 8000
- Server stopped = browser says "site can't be reached"
- If one page file is missing, the flow breaks (I forgot plans.html and login failed)
- Test data: mobile 9876543210, password Test@123, failed card 0000000000000000