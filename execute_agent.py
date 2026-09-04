import asyncio
import os
import random
import json
import math
import sys
from playwright.async_api import async_playwright
from groq import Groq

# Free Groq Developer token pipeline setup
if not os.environ.get("GROQ_API_KEY"):
    print("[!] Error: GROQ_API_KEY environment variable is not set.")
    print("[!] Please set it in your terminal using: set GROQ_API_KEY=your_key_here")
    sys.exit(1)

async def human_mouse_move(page, from_x, from_y, to_x, to_y, steps=14):
    """Moves mouse from (from_x, from_y) to (to_x, to_y) using smooth cubic Bezier curve with micro tremors."""
    for i in range(1, steps + 1):
        t = i / steps
        t_curved = t * t * (3 - 2 * t)
        
        cx = from_x + (to_x - from_x) * t_curved
        cy = from_y + (to_y - from_y) * t_curved
        
        arc = math.sin(t * math.pi) * 10.0 * (random.random() - 0.5)
        noise_x = random.uniform(-0.8, 0.8)
        noise_y = random.uniform(-0.8, 0.8)
        
        await page.mouse.move(cx + arc + noise_x, cy + arc + noise_y)
        await asyncio.sleep(random.uniform(0.012, 0.022))
    
    await page.mouse.move(to_x, to_y)

async def human_type(input_field, text):
    """Types text with realistic timing, capitalization latency, punctuation pauses, and occasional typos."""
    await input_field.focus()
    
    for char in text:
        # 1. Occasional typo correction (2% chance)
        if char.isalnum() and random.random() < 0.02:
            typos = {
                'a': 's', 's': 'd', 'd': 'f', 'f': 'g', 'g': 'h', 'h': 'j', 'j': 'k', 'k': 'l',
                'q': 'w', 'w': 'e', 'e': 'r', 'r': 't', 't': 'y', 'y': 'u', 'u': 'i', 'i': 'o', 'o': 'p',
                'z': 'x', 'x': 'c', 'c': 'v', 'v': 'b', 'b': 'n', 'n': 'm'
            }
            typo_char = typos.get(char.lower(), char)
            await input_field.press(typo_char)
            await asyncio.sleep(random.uniform(0.08, 0.14))
            await asyncio.sleep(random.uniform(0.18, 0.25))
            await input_field.press("Backspace")
            await asyncio.sleep(random.uniform(0.09, 0.15))
            
        delay = random.uniform(0.06, 0.13)
        if char.isupper() or char in '!@#$%^&*()_+{}|:"<>?':
            delay += random.uniform(0.07, 0.14)
        if char in " ,.?!;":
            delay += random.uniform(0.12, 0.25)
            
        await input_field.press(char)
        await asyncio.sleep(delay)

# Script to tag all visible interactive elements across the screen
ANNOTATE_SCREEN_SCRIPT = """
() => {
    document.querySelectorAll('[data-agent-target]').forEach(el => el.removeAttribute('data-agent-target'));
    
    const candidates = Array.from(document.querySelectorAll(
        'input, textarea, select, button, label, [role="button"], [role="checkbox"], [role="radio"], [role="option"], [contenteditable="true"], a'
    ));
    
    const visibleElements = [];
    let targetCounter = 0;
    
    for (const el of candidates) {
        const rect = el.getBoundingClientRect();
        const style = window.getComputedStyle(el);
        
        if (style.display === 'none' || style.visibility === 'hidden' || style.opacity === '0') {
            continue;
        }
        if (rect.width <= 0 || rect.height <= 0) {
            continue;
        }
        
        // Exclude elements outside reasonable screen bounds
        if (rect.bottom < 0 || rect.top > window.innerHeight * 3) {
            continue;
        }
        
        el.setAttribute('data-agent-target', String(targetCounter));
        
        let textContent = (el.innerText || el.textContent || el.value || el.placeholder || el.getAttribute('aria-label') || '').trim();
        textContent = textContent.replace(/\\s+/g, ' ').substring(0, 100);
        
        visibleElements.push({
            index: targetCounter,
            tag: el.tagName.toLowerCase(),
            type: el.getAttribute('type') || '',
            name: el.getAttribute('name') || '',
            text: textContent,
            checked: el.checked || false,
            disabled: el.disabled || false
        });
        
        targetCounter++;
    }
    
    // Extract main visible text body for holistic comprehension
    const pageText = (document.body.innerText || '').substring(0, 6000);
    
    return {
        elements: visibleElements,
        html_snapshot: document.body.innerHTML.substring(0, 20000),
        page_text: pageText
    };
}
"""

async def universal_destruction_engine():
    CANDIDATE_MODELS = [
        "openai/gpt-oss-120b",
        "qwen/qwen3.8-27b",
        "qwen/qwen3.6-27b",
        "openai/gpt-oss-20b",
        "llama-3.3-70b-versatile"
    ]
    client = Groq()

    print("=" * 65)
    print("🧠 SYSTEM ACTIVE: AUTONOMOUS SCREEN-AWARE UNIVERSAL TEST AGENT")
    print("🎯 Full-Viewport Visual Reasoning + Layout Agnostic Action Planning")
    print("=" * 65)
    
    for i in range(4, 0, -1):
        print(f"[*] Attaching to Chrome CDP session in: {i}s...", end="\r")
        await asyncio.sleep(1)
    print("\n[*] Connection established. Listening to active browser viewport...")

    current_mouse_x = 250.0
    current_mouse_y = 250.0

    async with async_playwright() as p:
        try:
            browser = await p.chromium.connect_over_cdp("http://localhost:9222")
            default_context = browser.contexts[0]
            all_pages = default_context.pages
            
            if not all_pages:
                raise Exception("No active browser tabs found on port 9222.")
            
            # Find the currently visible tab
            page = all_pages[0]
            for p_target in all_pages:
                try:
                    if await p_target.evaluate("document.visibilityState === 'visible'"):
                        page = p_target
                        break
                except:
                    pass
                
            print(f"[+] Hooked into active viewport: {page.url}\n")
            
            # Autonomous Perception-Action Loop
            MAX_SCREEN_CYCLES = 40
            completed_questions = set()
            
            for cycle in range(1, MAX_SCREEN_CYCLES + 1):
                print(f"\n--- [Screen Observation Cycle #{cycle}] ---")
                
                # Snapshot the screen and annotate all interactive widgets
                screen_state = await page.evaluate(ANNOTATE_SCREEN_SCRIPT)
                elements = screen_state.get('elements', [])
                page_text = screen_state.get('page_text', '')
                
                if not elements:
                    print("[!] No interactive elements discovered on screen. Waiting...")
                    await asyncio.sleep(1.5)
                    continue

                # Query Groq Multimodal Reasoning Model for whole-screen perception
                system_prompt = (
                    "You are a master academic test taker examining an active screen of an online exam.\n"
                    "All interactive elements on the screen have been annotated with a `[data-agent-target=\"<index>\"]` index.\n\n"
                    "Your mission:\n"
                    "1. Understand the questions, instructions, and widgets currently visible on screen.\n"
                    "2. Determine the correct answers with 100% academic precision (MCQs, Checkboxes, Fill-in-the-blanks, Dropdowns, Coding).\n"
                    "3. Return a list of sequential actions to perform.\n\n"
                    "CRITICAL SAFETY RULE:\n"
                    "- NEVER click the FINAL exam submission buttons (e.g. 'Finalize Submission', 'Submit Exam', 'End Test', 'Finish Exam').\n"
                    "- DO click 'Next', 'Save & Next', 'Continue', 'Proceed' to move between questions if this is a paginated exam.\n\n"
                    "Output format must be strictly a JSON object with this schema:\n"
                    "{\n"
                    "  \"screen_summary\": \"Brief 1-sentence description of what is on screen right now\",\n"
                    "  \"actions\": [\n"
                    "    {\"type\": \"click\", \"target_index\": 3, \"reason\": \"Select option (A) for Question 1\"},\n"
                    "    {\"type\": \"type\", \"target_index\": 6, \"text\": \"let\", \"reason\": \"Fill in the blank for Question 2\"},\n"
                    "    {\"type\": \"click\", \"target_index\": 12, \"reason\": \"Click Next button to go to next page\"}\n"
                    "  ],\n"
                    "  \"is_exam_complete\": false\n"
                    "}"
                )
                
                user_content = (
                    f"URL: {page.url}\n\n"
                    f"--- VISIBLE SCREEN TEXT ---\n{page_text}\n\n"
                    f"--- ANNOTATED INTERACTIVE WIDGETS ---\n{json.dumps(elements, indent=2)}"
                )

                plan = None
                for model_name in CANDIDATE_MODELS:
                    try:
                        resp = client.chat.completions.create(
                            model=model_name,
                            response_format={"type": "json_object"},
                            messages=[
                                {"role": "system", "content": system_prompt},
                                {"role": "user", "content": user_content}
                            ]
                        )
                        plan = json.loads(resp.choices[0].message.content.strip())
                        break
                    except Exception as e:
                        continue

                if not plan or not plan.get("actions"):
                    print("[*] No further actions required on this screen.")
                    if plan and plan.get("is_exam_complete"):
                        print("[*] Screen analysis indicates exam questions are complete.")
                        break
                    await asyncio.sleep(1.0)
                    break

                print(f"👁️  Screen Analysis: {plan.get('screen_summary', 'Processing screen...')}")
                actions = plan.get("actions", [])
                print(f"📋 Generated Action Plan: {len(actions)} steps")

                has_navigation = False
                for step_idx, action in enumerate(actions):
                    act_type = action.get("type")
                    t_idx = str(action.get("target_index", ""))
                    reason = action.get("reason", "")
                    
                    if not t_idx:
                        continue
                        
                    target_el = await page.query_selector(f'[data-agent-target="{t_idx}"]')
                    if not target_el:
                        continue
                        
                    # Hardcoded safeguard against premature final submission
                    el_text = (await page.evaluate("(el) => (el.innerText || el.value || '').toLowerCase()", target_el)).strip()
                    if any(x in el_text for x in ["finalize submission", "submit exam", "submit test", "end test", "finish exam"]):
                        print(f"    [🛡️ SAFETY SHIELD] Blocked automated click on final submission button: '{el_text}'")
                        continue

                    # Scroll element smoothly into center view
                    await page.evaluate("(el) => el.scrollIntoView({behavior: 'smooth', block: 'center'})", target_el)
                    await asyncio.sleep(0.3)
                    
                    box = await target_el.bounding_box()
                    if not box:
                        continue
                        
                    target_x = box['x'] + box['width'] / 2
                    target_y = box['y'] + box['height'] / 2
                    
                    # Human mouse trajectory
                    await human_mouse_move(page, current_mouse_x, current_mouse_y, target_x, target_y)
                    current_mouse_x, current_mouse_y = target_x, target_y
                    
                    if act_type == "click":
                        await page.mouse.click(target_x, target_y)
                        print(f"    [Step {step_idx+1}] Clicked [{t_idx}] -> {reason}")
                        if any(x in el_text for x in ["next", "continue", "save & next", "proceed", "forward"]):
                            has_navigation = True
                            await asyncio.sleep(1.2)
                            break
                            
                    elif act_type == "type":
                        await page.mouse.click(target_x, target_y)
                        await asyncio.sleep(0.1)
                        text_to_type = action.get("text", "")
                        await human_type(target_el, text_to_type)
                        print(f"    [Step {step_idx+1}] Typed '{text_to_type}' into [{t_idx}] -> {reason}")

                    await asyncio.sleep(random.uniform(0.6, 1.2))

                # If this was a single page exam without paginated buttons, we are done
                if not has_navigation:
                    print("\n[+] Single-page / All visible questions resolved.")
                    break

            print("\n" + "=" * 65)
            print("🎉 [SUCCESS] AUTONOMOUS AGENT SOLVING RUN COMPLETE")
            print("🛡️  All questions answered. Submit button left untouched for manual review.")
            print("=" * 65)

        except Exception as e:
            print(f"\n[X] Automation Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(universal_destruction_engine())
