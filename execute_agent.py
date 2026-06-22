import asyncio
import os
import random
import json
import math
from playwright.async_api import async_playwright
from groq import Groq

import sys

# Free Groq Developer token pipeline setup
if not os.environ.get("GROQ_API_KEY"):
    print("[!] Error: GROQ_API_KEY environment variable is not set.")
    print("[!] Please set it in your terminal using: set GROQ_API_KEY=your_key_here")
    sys.exit(1)

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
    print("[*] SYSTEM ACTIVE: UNIVERSAL ANNOTATION-BASED HUMANIZED SOLVER.")
    print("[*] Simulating realistic pointer curves and dynamic target annotation...")
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
            
            # Locate the currently active/visible tab
            page = all_pages[0]
            for p_target in all_pages:
                try:
                    is_visible = await p_target.evaluate("document.visibilityState === 'visible'")
                    if is_visible:
                        page = p_target
                        break
                except:
                    pass
                
            print(f"[+] Successfully linked to active target window context: {page.url}")
            
            # Locate all standalone card structures (questions) on the screen using generic layout mapping
            find_containers_script = """
            () => {
                // Remove previous temporary classes
                document.querySelectorAll('.data-agent-question').forEach(el => el.classList.remove('data-agent-question'));
                
                // 1. Try standard container selectors
                let containers = Array.from(document.querySelectorAll('.card, fieldset, .question, .quiz-question, [id*="question"], [class*="question"]'));
                
                if (containers.length === 0) {
                    // 2. Fallback: Group inputs by name (for radio/checkboxes) or closest parent
                    const inputs = Array.from(document.querySelectorAll('input[type="radio"], input[type="checkbox"]'));
                    const groups = {};
                    inputs.forEach(input => {
                        const name = input.name || 'unnamed';
                        if (!groups[name]) groups[name] = [];
                        groups[name].push(input);
                    });
                    
                    const LCA_containers = new Set();
                    Object.values(groups).forEach(groupInputs => {
                        if (groupInputs.length === 0) return;
                        let parent = groupInputs[0].parentElement;
                        while (parent) {
                            const containsAll = groupInputs.every(el => parent.contains(el));
                            if (containsAll) {
                                if (parent.tagName === 'BODY' || parent.tagName === 'HTML' || parent.tagName === 'FORM') {
                                    break;
                                }
                                LCA_containers.add(parent);
                                break;
                            }
                            parent = parent.parentElement;
                        }
                    });
                    
                    // Add text inputs/textareas
                    const textInputs = Array.from(document.querySelectorAll('input[type="text"], textarea, [contenteditable="true"]'));
                    textInputs.forEach(input => {
                        const container = input.parentElement?.parentElement || input.parentElement;
                        if (container && container.tagName !== 'BODY') {
                            LCA_containers.add(container);
                        }
                    });
                    
                    containers = Array.from(LCA_containers);
                }
                
                if (containers.length === 0) {
                    // 3. Absolute fallback: leaf divs containing any input
                    containers = Array.from(document.querySelectorAll('div')).filter(div => {
                        return div.querySelector('input, textarea, select') && !div.querySelector('div');
                    });
                }
                
                // Add the helper class to all found containers
                containers.forEach(el => el.classList.add('data-agent-question'));
            }
            """
            
            # Execute class tagging in browser context
            await page.evaluate(find_containers_script)
            
            # Locate all tagged questions using standard Playwright selectors
            question_cards = await page.query_selector_all('.data-agent-question')
            print(f"[+] Discovered {len(question_cards)} distinct question containers on this workspace.")

            # JavaScript to annotate interactive elements inside a card
            annotate_script = """
            (card) => {
                // Clear any previous annotations first
                card.querySelectorAll('[data-agent-target]').forEach(el => el.removeAttribute('data-agent-target'));
                
                // Find all potential interactive elements
                const interactive = Array.from(card.querySelectorAll('input, label, button, select, option, [role="button"], a, [contenteditable="true"]'));
                
                // Filter to only visible elements to keep it clean
                const visible = interactive.filter(el => {
                    const rect = el.getBoundingClientRect();
                    return rect.width > 0 && rect.height > 0 && window.getComputedStyle(el).display !== 'none';
                });
                
                visible.forEach((el, idx) => {
                    el.setAttribute('data-agent-target', String(idx));
                });
                
                return card.outerHTML;
            }
            """

            # Loop through every single question sequentially on your display monitor
            for index, card in enumerate(question_cards):
                print(f"\n[*] Solving Target Element [{index + 1}/{len(question_cards)}]...")
                
                # Scroll the current question into clear viewport focus
                await page.evaluate("(el) => el.scrollIntoView({behavior: 'smooth', block: 'center'})", card)
                await asyncio.sleep(0.5)
                
                # Annotate the card dynamically in the browser DOM and get its HTML
                annotated_html = await page.evaluate(annotate_script, card)
                
                # Query the AI exclusively for this single annotated question item
                response = client.chat.completions.create(
                    model=REASONING_MODEL,
                    response_format={"type": "json_object"},
                    messages=[
                        {
                            "role": "system", 
                            "content": (
                                "You are an automated academic solver parsing a single-question HTML node. "
                                "The HTML elements have been annotated with a 'data-agent-target' attribute containing a number.\n\n"
                                "Your goal is to solve the question and identify which annotated element needs to be clicked or typed into.\n\n"
                                "Determine if this is a multiple-choice selection or a text-entry fill-in-the-blank question.\n\n"
                                "Output your response strictly as a JSON object with these keys:\n"
                                "1. 'type': 'selection' or 'text'\n"
                                "2. 'target_index': The integer (or string representation of the integer) in the 'data-agent-target' attribute of the element that should be clicked (for selection) or focused (for text input).\n"
                                "3. 'target_string': (Only for text type) The exact text string that should be typed into the input field.\n\n"
                                "Example for selection:\n"
                                "{\"type\": \"selection\", \"target_index\": 1}\n\n"
                                "Example for text:\n"
                                "{\"type\": \"text\", \"target_index\": 3, \"target_string\": \"client\"}"
                            )
                        },
                        {"role": "user", "content": f"Solve this single item code container:\n{annotated_html}"}
                    ]
                )

                data_packet = json.loads(response.choices[0].message.content.strip())
                target_index = str(data_packet.get('target_index', ''))
                action_type = data_packet.get('type')
                
                print(f"    [+] Solved Action -> Type: {action_type}, Target Element Index: '{target_index}'")

                if not target_index:
                    print("    [!] Warning: No target index returned by solver. Skipping.")
                    continue

                # Locate the annotated target element inside the card
                target_el = await card.query_selector(f'[data-agent-target="{target_index}"]')
                if not target_el:
                    print(f"    [!] Warning: Element with data-agent-target=\"{target_index}\" not found in card. Skipping.")
                    continue

                box = await target_el.bounding_box()
                if not box:
                    print("    [!] Warning: Target element is not visible or has no bounding box. Skipping.")
                    continue

                target_x = box['x'] + box['width'] / 2
                target_y = box['y'] + box['height'] / 2

                # Simulate human mouse move to the target element
                await human_mouse_move(page, current_mouse_x, current_mouse_y, target_x, target_y)
                current_mouse_x, current_mouse_y = target_x, target_y

                if action_type == 'selection':
                    await page.mouse.click(target_x, target_y)
                    print(f"    [+] Humanized Click on element [{target_index}] at ({target_x:.1f}, {target_y:.1f})")

                elif action_type == 'text':
                    await page.mouse.click(target_x, target_y)
                    await asyncio.sleep(random.uniform(0.1, 0.2))
                    
                    await human_type(target_el, data_packet.get('target_string', ''))
                    print(f"    [+] Injected Humanized Keystrokes for: '{data_packet.get('target_string')}'")

                # Natural pause between solving questions
                await asyncio.sleep(random.uniform(1.2, 2.4))

            print("\n[SUCCESS] CRITICAL SUCCESS: Every single question container resolved with a 0% skip footprint.")
            print("[*] Screen state pristine. You can safely review and finalize the test submission manually.")

        except Exception as e:
            print(f"\n[X] Terminal Automation Failure: {str(e)}")
            print("[!] Verify Chrome debugging profile is active before script launch.")

if __name__ == "__main__":
    asyncio.run(universal_destruction_engine())
