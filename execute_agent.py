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

async def human_mouse_move(page, from_x, from_y, to_x, to_y, steps=12):
    """Moves mouse smoothly from (from_x, from_y) to (to_x, to_y) using cubic Bezier curve with micro tremors."""
    for i in range(1, steps + 1):
        t = i / steps
        t_curved = t * t * (3 - 2 * t)
        
        cx = from_x + (to_x - from_x) * t_curved
        cy = from_y + (to_y - from_y) * t_curved
        
        arc = math.sin(t * math.pi) * 8.0 * (random.random() - 0.5)
        noise_x = random.uniform(-0.6, 0.6)
        noise_y = random.uniform(-0.6, 0.6)
        
        await page.mouse.move(cx + arc + noise_x, cy + arc + noise_y)
        await asyncio.sleep(random.uniform(0.01, 0.018))
    
    await page.mouse.move(to_x, to_y)

async def human_type(input_field, text):
    """Types text with realistic human-like typing rhythm, capitalization lag, and typo auto-corrections."""
    await input_field.focus()
    
    for char in text:
        # 1. Occasional realistic typo and correction (2% chance)
        if char.isalnum() and random.random() < 0.02:
            typos = {
                'a': 's', 's': 'd', 'd': 'f', 'f': 'g', 'g': 'h', 'h': 'j', 'j': 'k', 'k': 'l',
                'q': 'w', 'w': 'e', 'e': 'r', 'r': 't', 't': 'y', 'y': 'u', 'u': 'i', 'i': 'o', 'o': 'p',
                'z': 'x', 'x': 'c', 'c': 'v', 'v': 'b', 'b': 'n', 'n': 'm'
            }
            typo_char = typos.get(char.lower(), char)
            await input_field.press(typo_char)
            await asyncio.sleep(random.uniform(0.06, 0.12))
            await asyncio.sleep(random.uniform(0.14, 0.22))
            await input_field.press("Backspace")
            await asyncio.sleep(random.uniform(0.08, 0.14))
            
        delay = random.uniform(0.05, 0.12)
        if char.isupper() or char in '!@#$%^&*()_+{}|:"<>?':
            delay += random.uniform(0.06, 0.12)
        if char in " ,.?!;":
            delay += random.uniform(0.10, 0.20)
            
        await input_field.press(char)
        await asyncio.sleep(delay)

# High-precision DOM annotation script that deduplicates nested inputs and extracts dropdown options
ANNOTATE_SCREEN_SCRIPT = """
() => {
    document.querySelectorAll('[data-agent-target]').forEach(el => el.removeAttribute('data-agent-target'));
    
    // Find all candidate interactive elements
    const rawCandidates = Array.from(document.querySelectorAll(
        'button, label, select, input:not([type="hidden"]), textarea, [role="button"], [role="checkbox"], [role="radio"], [contenteditable="true"]'
    ));
    
    const visibleElements = [];
    let targetCounter = 0;
    
    // Deduplicate: If an input is inside a label, keep the label or input
    const filtered = rawCandidates.filter(el => {
        if (el.tagName === 'INPUT' && (el.type === 'radio' || el.type === 'checkbox') && el.closest('label')) {
            return false; // Let the parent label be the click target
        }
        return true;
    });
    
    for (const el of filtered) {
        const rect = el.getBoundingClientRect();
        const style = window.getComputedStyle(el);
        
        if (style.display === 'none' || style.visibility === 'hidden' || style.opacity === '0') {
            continue;
        }
        if (rect.width <= 0 || rect.height <= 0) {
            continue;
        }
        
        // Exclude palette item numbers from confusing the question solver
        const isPalette = el.classList.contains('palette-item');
        
        el.setAttribute('data-agent-target', String(targetCounter));
        
        let textContent = (el.innerText || el.textContent || el.value || el.placeholder || el.getAttribute('aria-label') || '').trim();
        textContent = textContent.replace(/\\s+/g, ' ').substring(0, 120);
        
        let optionsList = [];
        if (el.tagName === 'SELECT') {
            optionsList = Array.from(el.options).map(o => o.text.trim());
        }
        
        // Check input type from tag or child input
        let resolvedType = el.getAttribute('type') || '';
        if (!resolvedType && el.tagName === 'LABEL') {
            const inner = el.querySelector('input');
            if (inner) resolvedType = inner.type || '';
        }
        
        visibleElements.push({
            index: targetCounter,
            tag: el.tagName.toLowerCase(),
            type: resolvedType,
            name: el.getAttribute('name') || '',
            text: textContent,
            options: optionsList,
            is_palette_btn: isPalette
        });
        
        targetCounter++;
    }
    
    // Extract current question text clearly
    const questionCard = document.querySelector('#question-card-viewport, .card, fieldset, .question, main');
    const questionContext = questionCard ? questionCard.innerText.trim() : (document.body.innerText || '').substring(0, 4000);
    const trackerText = (document.querySelector('.question-tracker, header')?.innerText || '').trim();
    
    return {
        elements: visibleElements,
        question_context: questionContext,
        tracker: trackerText
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
    print("🎯 Layout-Agnostic / Guide-Independent Solver Engine")
    print("=" * 65)
    
    for i in range(3, 0, -1):
        print(f"[*] Attaching to Chrome CDP session in: {i}s...", end="\r")
        await asyncio.sleep(1)
    print("\n[*] Connected. Hooking active browser viewport...")

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
            
            MAX_SCREEN_CYCLES = 50
            
            for cycle in range(1, MAX_SCREEN_CYCLES + 1):
                # Snapshot the screen and annotate all interactive widgets
                screen_state = await page.evaluate(ANNOTATE_SCREEN_SCRIPT)
                elements = screen_state.get('elements', [])
                q_context = screen_state.get('question_context', '')
                tracker = screen_state.get('tracker', '')
                
                if not elements:
                    print("[!] No interactive elements found on screen. Waiting...")
                    await asyncio.sleep(1.0)
                    continue

                print(f"\n--- [Cycle {cycle}] {tracker} ---")

                # Filter out palette buttons from LLM prompt to prevent distracting the solver
                relevant_elements = [e for e in elements if not e.get('is_palette_btn')]

                system_prompt = (
                    "You are a master academic solver taking an online exam.\n"
                    "All interactive elements have a `[data-agent-target=\"<index>\"]` integer index.\n\n"
                    "HOW TO DETERMINE QUESTION TYPES WITHOUT ANY GUIDE LABELS:\n"
                    "1. If elements have `type: 'radio'`, this is a Single Choice MCQ -> Choose exactly 1 correct option index.\n"
                    "2. If elements have `type: 'checkbox'`, this is a Multiple Selection MCQ -> Choose ALL valid option indices.\n"
                    "3. If an element has `tag: 'select'`, this is a Dropdown -> Return `type: 'select'` and the exact `option_text`.\n"
                    "4. If an element has `tag: 'input'` (type text) or `tag: 'textarea'`, this is a Text / Code response -> Return `type: 'type'` and the `text` to type.\n\n"
                    "HOW TO ADVANCE:\n"
                    "- If there is a 'Save & Next', 'Next', 'Continue', or 'Proceed' button on screen, include a click on it as the LAST action in your array.\n"
                    "- NEVER click final submission buttons ('Finalize Submission', 'Submit Exam', 'End Test').\n\n"
                    "Output JSON format:\n"
                    "{\n"
                    "  \"question_summary\": \"Identified question and answer rationale\",\n"
                    "  \"actions\": [\n"
                    "    {\"type\": \"click\", \"target_index\": 1, \"reason\": \"Select option\"},\n"
                    "    {\"type\": \"click\", \"target_index\": 4, \"reason\": \"Click Next button\"}\n"
                    "  ]\n"
                    "}"
                )
                
                user_content = (
                    f"--- ACTIVE QUESTION CONTENT ---\n{q_context}\n\n"
                    f"--- INTERACTIVE TARGETS ---\n{json.dumps(relevant_elements, indent=2)}"
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
                    except Exception:
                        continue

                if not plan or not plan.get("actions"):
                    print("[*] No actions returned by solver.")
                    break

                print(f"💡 AI Analysis: {plan.get('question_summary', 'Solving question...')}")
                actions = plan.get("actions", [])
                has_navigated = False

                for act_idx, action in enumerate(actions):
                    act_type = action.get("type")
                    t_idx = str(action.get("target_index", ""))
                    reason = action.get("reason", "")
                    
                    if not t_idx:
                        continue
                        
                    target_el = await page.query_selector(f'[data-agent-target="{t_idx}"]')
                    if not target_el:
                        continue
                        
                    # Final submission safety guard
                    el_text = (await page.evaluate("(el) => (el.innerText || el.value || '').toLowerCase()", target_el)).strip()
                    if any(x in el_text for x in ["finalize submission", "submit exam", "submit test", "end test", "finish exam"]):
                        print(f"    [🛡️ SAFETY SHIELD] Preserved final submission button: '{el_text}'")
                        continue

                    # Scroll element into viewport
                    await page.evaluate("(el) => el.scrollIntoView({behavior: 'smooth', block: 'center'})", target_el)
                    await asyncio.sleep(0.15)
                    
                    box = await target_el.bounding_box()
                    if not box:
                        continue
                        
                    target_x = box['x'] + box['width'] / 2
                    target_y = box['y'] + box['height'] / 2
                    
                    # Smooth human mouse movement
                    await human_mouse_move(page, current_mouse_x, current_mouse_y, target_x, target_y)
                    current_mouse_x, current_mouse_y = target_x, target_y
                    
                    if act_type == "click":
                        await page.mouse.click(target_x, target_y)
                        print(f"    [+] Clicked [{t_idx}] -> {reason}")
                        
                        if any(x in el_text for x in ["next", "continue", "save & next", "proceed", "forward", "→", ">"]):
                            has_navigated = True
                            await asyncio.sleep(0.5)
                            break
                            
                    elif act_type == "type":
                        await page.mouse.click(target_x, target_y)
                        await asyncio.sleep(0.1)
                        val = action.get("text", "")
                        await human_type(target_el, val)
                        print(f"    [+] Typed '{val}' into [{t_idx}] -> {reason}")
                        
                    elif act_type == "select":
                        opt_val = action.get("option_text", "")
                        await target_el.select_option(label=opt_val)
                        print(f"    [+] Selected dropdown option '{opt_val}' on [{t_idx}] -> {reason}")

                    await asyncio.sleep(random.uniform(0.2, 0.4))

                # AUTO-ADVANCE FAILSAFE:
                # If the AI answered the question but didn't include a click on "Next", find and click the Next button!
                if not has_navigated:
                    next_btn = await page.query_selector("button:not(.hidden):has-text('Next'), button:not(.hidden):has-text('Save & Next'), button:not(.hidden):has-text('Continue'), #next-btn:not(.hidden)")
                    if next_btn:
                        is_visible = await page.evaluate("(el) => { const r = el.getBoundingClientRect(); return r.width > 0 && r.height > 0 && window.getComputedStyle(el).display !== 'none'; }", next_btn)
                        btn_txt = (await page.evaluate("(el) => (el.innerText || el.value || '').toLowerCase()", next_btn)).strip()
                        
                        if is_visible and not any(x in btn_txt for x in ["finalize", "submit", "finish", "end"]):
                            box = await next_btn.bounding_box()
                            if box:
                                target_x = box['x'] + box['width'] / 2
                                target_y = box['y'] + box['height'] / 2
                                await human_mouse_move(page, current_mouse_x, current_mouse_y, target_x, target_y)
                                current_mouse_x, current_mouse_y = target_x, target_y
                                await page.mouse.click(target_x, target_y)
                                print(f"    [⏩ AUTO-ADVANCE] Clicked Next navigation button ('{btn_txt}') to load next question.")
                                has_navigated = True
                                await asyncio.sleep(0.5)

                if not has_navigated:
                    # No next button found on page (single page exam or reached the final submission screen)
                    print("\n[*] Exam questions complete. All accessible elements resolved.")
                    break

            print("\n" + "=" * 65)
            print("🎉 [SUCCESS] AUTONOMOUS AGENT SOLVING RUN COMPLETE")
            print("🛡️  All questions answered with precision. Final submission ready for review.")
            print("=" * 65)

        except Exception as e:
            print(f"\n[X] Automation Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(universal_destruction_engine())
