from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import time
import json
import openai
import os

load_dotenv()

api_key = os.getenv('OPENAI_KEY')
openai.api_key = api_key

def split_text(text):
    max_chunk_size = 2048
    chunks = []
    current_chunk = ""
    for sentence in text.split("."):
        if len(current_chunk) + len(sentence) < max_chunk_size:
            current_chunk += sentence + "."
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + "."
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

def generate_summary(text):
    input_chunks = split_text(text)
    output_chunks = []
    for chunk in input_chunks:
        response = openai.Completion.create(
            engine="davinci",
            prompt=(f"Please summarize the following text:\n{chunk}\n\nSummary:"),
            temperature=0.5,
            max_tokens=1024,
            n = 1,
            stop=None
        )
        summary = response.choices[0].text.strip()
        output_chunks.append(summary)
    return " ".join(output_chunks)

with sync_playwright() as pw:
    browser = pw.chromium.launch(headless=True)
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()

    page.goto('https://www.linkedin.com/jobs/search/?keywords=Lead%20Test%20Engineer&location=United%20States&locationId=&geoId=103644278&f_TPR=r604800&f_WT=2&position=1&pageNum=0')  # go to url
    page.wait_for_selector("#main-content")

    parsed = []
    jobItemList = page.locator('ul.jobs-search__results-list > li')
    for jobItem in jobItemList.element_handles():
        processedParsed = {}

        jobItem.click()
        page.wait_for_selector('.decorated-job-posting__details')
        description = page.locator('.show-more-less-html__markup.relative.overflow-hidden').inner_text()
        
        parsed.append({
            'title': jobItem.query_selector('div > a').inner_text(),
            'description': description
        })
        time.sleep(5)
    
    resultSummary = generate_summary(parsed[0]['description'])
    
with open('parsed.json', 'w') as file:
    json.dump(parsed, file)

with open('jobFromLinkedIn.txt', 'a') as file:  # 'a' for appending to the file
    file.write("Summary:\n")
    file.write(resultSummary)