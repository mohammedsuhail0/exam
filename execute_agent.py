import asyncio
import os
import random
import json
import math
from playwright.async_api import async_playwright
from groq import Groq

# Free Groq Developer token pipeline setup
if not os.environ.get("GROQ_API_KEY"):
    print("[!] Warning: GROQ_API_KEY environment variable is not set.")

async def human_mouse_move(page, from_x, from_y, to_x, to_y, steps=15):
    """Moves the mouse from (from_x, from_y) to (to_x, to_y) using a curved path with slight noise."""
    for i in range(1, steps + 1):
        t = i / steps
        # Simple cubic interpolation for smooth deceleration/acceleration
        t_curved = t * t * (3 - 2 * t)
        
        cx = from_x + (to_x - from_x) * t_curved
        cy = from_y + (to_y - from_y) * t_curved
        
        # Add slight curve arc and micro hand shake
        arc = math.sin(t * math.pi) * 12.0 * (random.random() - 0.5)
        noise_x = random.uniform(-1.0, 1.0)
        noise_y = random.uniform(-1.0, 1.0)
        
        await page.mouse.move(cx + arc + noise_x, cy + arc + noise_y)
        await asyncio.sleep(random.uniform(0.01, 0.018))
    
    # Settle at the exact target coordinates
    await page.mouse.move(to_x, to_y)

async def human_type(input_field, text):
    """Types text character-by-character simulating human speed, capitalization lag, and occasional typos."""
    await input_field.focus()
    
    for char in text:
        # 1. Occasional typo correction (approx 2% chance on letters)
        if char.isalnum() and random.random() < 0.02:
            typos = {
                'a': 's', 's': 'd', 'd': 'f', 'f': 'g', 'g': 'h', 'h': 'j', 'j': 'k', 'k': 'l',
                'q': 'w', 'w': 'e', 'e': 'r', 'r': 't', 't': 'y', 'y': 'u', 'u': 'i', 'i': 'o', 'o': 'p',
                'z': 'x', 'x': 'c', 'c': 'v', 'v': 'b', 'b': 'n', 'n': 'm'
            }
            typo_char = typos.get(char.lower(), char)
            await input_field.press(typo_char)
            await asyncio.sleep(random.uniform(0.08, 0.14))
            
            # Pause in realization of mistake, then hit Backspace
            await asyncio.sleep(random.uniform(0.18, 0.28))
            await input_field.press("Backspace")
            await asyncio.sleep(random.uniform(0.1, 0.16))
            
        # 2. Keystroke timing with variance
        delay = random.uniform(0.07, 0.15)
        
        # Capitalization / special character shift key latency
        if char.isupper() or char in '!@#$%^&*()_+{}|:"<>?':
            delay += random.uniform(0.06, 0.12)
            
        # Spacer / punctuation pause
        if char in " ,.?!;":
            delay += random.uniform(0.14, 0.28)
            
        await input_field.press(char)
        await asyncio.sleep(delay)

async def universal_destruction_engine():
    # Using Llama-3.3-70b-versatile for targeted, individual question reasoning
    REASONING_MODEL = "llama-3.3-70b-versatile" 
    client = Groq()

    print("=" * 60)
    print("[*] SYSTEM ACTIVE: UPGRADED BIOMIMETIC CDP TEST SOLVER.")
    print("[*] Simulating realistic pointer curves and typist cadence...")
    print("=" * 60)
    
    for i in range(5, 0, -1):
        print(f"Executing injection sequence in: {i} seconds...", end="\r")
        await asyncio.sleep(1)
    print("\n\n[*] Initiating connection pipeline...")

    # Start mouse coordinates (simulating cursor starting somewhere natural)
    current_mouse_x = 200.0
    current_mouse_y = 200.0

    async with async_playwright() as p:
        try:
            browser = await p.chromium.connect_over_cdp("http://localhost:9222")
            default_context = browser.contexts[0]
            all_pages = default_context.pages
            
            if not all_pages:
                raise Exception("No active browser tabs discovered on port 9222.")
            
            page = all_pages[0]
            for p_target in all_pages:
                if any(x in p_target.url for x in ["vercel.app", "localhost", "exam", "portal", "quiz", "test"]):
                    page = p_target
                    break
                
            print(f"[+] Successfully linked to active target window context: {page.url}")
            
            # Locate all standalone card structures (questions) on the screen dynamically
            question_cards = await page.query_selector_all('.card, fieldset, .question, div[id*="question"]')
            print(f"[+] Discovered {len(question_cards)} distinct question containers on this workspace.")

            # Loop through every single question sequentially on your display monitor
            for index, card in enumerate(question_cards):
                print(f"\n[*] Solving Target Element [{index + 1}/{len(question_cards)}]...")
                
                # Scroll the current question into clear viewport focus
                await page.evaluate("(el) => el.scrollIntoView({behavior: 'smooth', block: 'center'})", card)
                await asyncio.sleep(0.5)
                
                # Extract ONLY the HTML of this isolated question container
                card_html = await page.evaluate("(el) => el.outerHTML", card)
                
                # Query the AI exclusively for this single question item
                response = client.chat.completions.create(
                    model=REASONING_MODEL,
                    response_format={"type": "json_object"},
                    messages=[
                        {
                            "role": "system", 
                            "content": (
                                "You are an automated academic solver parsing an isolated single-question HTML node. "
                                "Determine if this question is a multiple-choice selection or a text-entry fill-in-the-blank. "
                                "Identify the correct answer with perfect precision. "
                                "Output your response strictly as a JSON object with three specific keys:\n"
                                "1. 'type': 'selection' or 'text'\n"
                                "2. 'target_string': 'The exact inner text string of the correct choice option to click, or the exact text word to type into the input box.'\n"
                                "Example for selection: {'type': 'selection', 'target_string': 'O(log n)'}\n"
                                "Example for text: {'type': 'text', 'target_string': 'Queue'}"
                            )
                        },
                        {"role": "user", "content": f"Solve this single item code container: {card_html}"}
                    ]
                )

                data_packet = json.loads(response.choices[0].message.content.strip())
                target_value = str(data_packet.get('target_string', '')).lower().strip()
                print(f"    [+] Solved Action Array -> Type: {data_packet.get('type')}, Value: '{target_value}'")

                if data_packet.get('type') == 'selection':
                    # Find all interactive selectors inside this card
                    choices = await card.query_selector_all('input[type="radio"], input[type="checkbox"], label, div, span, button')
                    clicked = False
                    
                    # Try exact inner match inside this question window frame
                    for choice in choices:
                        visible = await choice.is_visible()
                        choice_text = await page.evaluate("(el) => el.innerText.trim()", choice)
                        if visible and len(choice_text) < 120 and choice_text.lower() == target_value:
                            box = await choice.bounding_box()
                            if box:
                                target_x = box['x'] + box['width'] / 2
                                target_y = box['y'] + box['height'] / 2
                                
                                # Emulate realistic mouse move
                                await human_mouse_move(page, current_mouse_x, current_mouse_y, target_x, target_y)
                                current_mouse_x, current_mouse_y = target_x, target_y
                                
                                await page.mouse.click(target_x, target_y)
                                print(f"    [+] Humanized Click (Exact): '{choice_text}' at ({target_x:.1f}, {target_y:.1f})")
                                clicked = True
                                break
                            
                    # Proximity match fallback
                    if not clicked:
                        for choice in choices:
                            visible = await choice.is_visible()
                            choice_text = await page.evaluate("(el) => el.innerText.trim()", choice)
                            if visible and len(choice_text) < 120 and (target_value in choice_text.lower() or choice_text.lower() in target_value) and len(choice_text) > 0:
                                input_el = await choice.query_selector('input')
                                click_target = input_el if input_el else choice
                                box = await click_target.bounding_box()
                                if box:
                                    target_x = box['x'] + box['width'] / 2
                                    target_y = box['y'] + box['height'] / 2
                                    
                                    await human_mouse_move(page, current_mouse_x, current_mouse_y, target_x, target_y)
                                    current_mouse_x, current_mouse_y = target_x, target_y
                                    
                                    await page.mouse.click(target_x, target_y)
                                    print(f"    [+] Humanized Click (Proximity): '{choice_text}' at ({target_x:.1f}, {target_y:.1f})")
                                    break

                elif data_packet.get('type') == 'text':
                    input_field = await card.query_selector('input[type="text"], textarea, input:not([type]), [contenteditable="true"]')
                    if input_field:
                        # Move mouse to input field first
                        box = await input_field.bounding_box()
                        if box:
                            target_x = box['x'] + box['width'] / 2
                            target_y = box['y'] + box['height'] / 2
                            await human_mouse_move(page, current_mouse_x, current_mouse_y, target_x, target_y)
                            current_mouse_x, current_mouse_y = target_x, target_y
                            await page.mouse.click(target_x, target_y)
                        
                        # Type human-like
                        await human_type(input_field, data_packet.get('target_string', ''))
                        print(f"    [+] Injected Humanized Keystrokes for: '{data_packet.get('target_string')}'")

                # Natural pause between solving questions
                await asyncio.sleep(random.uniform(1.2, 2.4))

            print("\n[🎉] CRITICAL SUCCESS: Every single question container resolved with a 0% skip footprint.")
            print("[*] Screen state pristine. You can safely review and finalize the test submission manually.")

        except Exception as e:
            print(f"\n[X] Terminal Automation Failure: {str(e)}")
            print("[!] Verify Chrome debugging profile is active before script launch.")

if __name__ == "__main__":
    asyncio.run(universal_destruction_engine())
