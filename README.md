# telecom-ai-test-pipeline
Project created using devops technology and AI testing on telecom domain

![Tests](https://github.com/SWAPNA121198/telecom-ai-test-pipeline/actions/workflows/tests.yml/badge.svg)

# Telecom AI Test Pipeline

A test automation project for a small telecom web app (login, prepaid plans, recharge). It combines **Playwright UI tests**, a **GitHub Actions CI pipeline**, and **AI** that drafts test cases and repairs broken locators, with a human approving every fix.

Built by a manual tester (5 years, telecom domain) moving into automation, DevOps and AI-assisted testing.

## The problem

Automated UI tests find elements using locators such as `#login-btn`. When a developer renames an id, the app still works but the tests fail. These are **false failures**, and fixing them by hand (test maintenance) takes a lot of testers' time.

## What this project does

1. **Tests a telecom app automatically.** 14 Playwright tests cover login, plan selection and recharge: positive, negative, boundary and failed-payment cases.
2. **Runs in CI.** A GitHub Actions pipeline starts the app and runs the suite on every push.
3. **Generates test cases with AI.** An LLM reads written requirements (`specs/`) and drafts test cases. I review them against my own.
4. **Heals broken locators with AI.** When a locator is not found, the AI reads the page HTML and suggests a new selector. The suggestion is saved as *pending*, and the test files only change after a human approves it.

## How it fits together

## How it fits together

Developer pushes code
        |
        v
GitHub Actions starts
        |
        v
Start the telecom app
        |
        v
Run the Playwright tests
        |
        v
Is a locator broken?
        |
        +-- No  --> Green tick
        |
        +-- Yes --> AI suggests a new locator
                            |
                            v
                    Saved as "pending"
                            |
                            v
                    Human approves or rejects
                            |
                            v
                    Tests updated + healing report


                    A developer pushes code to GitHub.
Explanation:                     
GitHub Actions starts the pipeline.
The telecom app is started.
The Playwright tests run.
If no locator is broken, you get a green tick.
If a locator is broken, the AI suggests a new one.
The suggestion is saved as pending.
A human approves or rejects it.
If approved, the tests are updated, and either way the decision goes into the healing report.


The AI steps run locally with an API key. The CI pipeline runs the 14 standard tests, and skips the two AI demo tests because it has no key.

## Results

| Measure | Result |
|---|---|
| Automated UI tests | 14, all passing locally and in CI |
| Manual test cases traced to automation | 10 (Excel) plus 4 boundary cases from AI review |
| AI-generated test cases | 12: 8 duplicates, 4 new and valid, 0 invented |
| Broken locators healed correctly | 9 of 9 (see `ai/healing_accuracy.md`) |

### Honest limits

- The app is small, so finding the right element is easier than on a large production page.
- The AI was given a clear description of each element.
- The accuracy figure comes from a single run, and AI output can vary.
- "Correct" means the suggested selector matches exactly one element and it is the intended one.

This is why healed locators go through human approval and are recorded in `ai/healing_report.md`.

## Project structure

```
app/                       Telecom demo app (login, plans, recharge)
tests/                     Playwright tests (pytest)
specs/                     Written requirements used as AI input
ai/generate_tests.py       Requirements -> draft test cases
ai/healing.py              Locator healing helper (saves pending suggestions)
ai/review_healing.py       Human approval of healed locators
ai/measure_healing.py      Breaks 9 locators on purpose and measures accuracy
.github/workflows/         CI pipeline
```

## How to run it

```bash
pip install -r requirements.txt
python -m playwright install chromium

# Terminal 1: start the app
python -m http.server 8000

# Terminal 2: run the tests
python -m pytest tests --headed --slowmo=300
```

### AI features (optional)

Create a Gemini API key, store it as an environment variable (never commit it), then:

```bash
# Windows
setx GEMINI_API_KEY "your-key"

python ai/generate_tests.py        # draft test cases from specs/
python -m ai.measure_healing       # measure healing accuracy
python -m ai.review_healing        # approve or reject healed locators
```

## Tools

Python, Playwright, pytest, GitHub Actions (YAML), Git and GitHub, Google Gemini API, HTML and JavaScript (demo app).

## What I learned

- Turning manual test cases into automated tests, with reusable helpers and assertions
- Building a CI pipeline and managing dependencies and ignored files
- Prompting an LLM with a role, rules and an output format, then reviewing its output critically
- Why AI-suggested fixes need human approval and an audit trail

## Next steps

- Package the app and tests with Docker
- Test a GenAI telecom support chatbot for wrong or made-up answers

<!-- Demo GIF: add it here once recorded
![Self-healing demo](docs/self-healing-demo.gif)
-->