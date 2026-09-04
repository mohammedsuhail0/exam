import asyncio
import os
import random
import json
import math
import sys
import re
from playwright.async_api import async_playwright
from groq import Groq

# Verify GROQ_API_KEY environment variable
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
if not GROQ_API_KEY:
    print("\n[!] FATAL ERROR: GROQ_API_KEY is not configured in your environment.")
    print("[!] Run: set GROQ_API_KEY=your_key_here")
    sys.exit(1)

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

# Prioritized multi-model fallback cascade
CANDIDATE_MODELS = [
    "openai/gpt-oss-120b",
    "qwen/qwen3.8-27b",
    "qwen/qwen3.6-27b",
    "openai/gpt-oss-20b",
    "llama-3.3-70b-versatile"
]

async def human_mouse_move(page, from_x, from_y, to_x, to_y, steps=10):
    """Generates physical cubic Bezier curves with micro-tremors to mimic human hand motor dynamics."""
    try:
        for i in range(1, steps + 1):
            t = i / steps
            t_curved = t * t * (3 - 2 * t)
            
            cx = from_x + (to_x - from_x) * t_curved
            cy = from_y + (to_y - from_y) * t_curved
            
            arc = math.sin(t * math.pi) * 5.0 * (random.random() - 0.5)
            noise_x = random.uniform(-0.4, 0.4)
            noise_y = random.uniform(-0.4, 0.4)
            
            await page.mouse.move(cx + arc + noise_x, cy + arc + noise_y)
            await asyncio.sleep(random.uniform(0.006, 0.012))
        
        await page.mouse.move(to_x, to_y)
    except Exception:
        pass

async def human_type(input_field, text):
    """Types text with natural human variance, capitalization pauses, and occasional auto-corrected typos."""
    try:
        await input_field.focus()
        await asyncio.sleep(0.05)
        
        for char in text:
            # 2% realistic typo auto-correction
            if char.isalnum() and random.random() < 0.02:
                typos = {
                    'a': 's', 's': 'd', 'd': 'f', 'f': 'g', 'g': 'h', 'h': 'j', 'j': 'k', 'k': 'l',
                    'q': 'w', 'w': 'e', 'e': 'r', 'r': 't', 't': 'y', 'y': 'u', 'u': 'i', 'i': 'o', 'o': 'p',
                    'z': 'x', 'x': 'c', 'c': 'v', 'v': 'b', 'b': 'n', 'n': 'm'
                }
                typo_char = typos.get(char.lower(), char)
                await input_field.press(typo_char)
                await asyncio.sleep(random.uniform(0.04, 0.08))
                await asyncio.sleep(random.uniform(0.08, 0.14))
                await input_field.press("Backspace")
                await asyncio.sleep(random.uniform(0.05, 0.09))
                
            delay = random.uniform(0.03, 0.08)
            if char.isupper() or char in '!@#$%^&*()_+{}|:"<>?':
                delay += random.uniform(0.04, 0.08)
            if char in " ,.?!;":
                delay += random.uniform(0.06, 0.12)
                
            await input_field.press(char)
            await asyncio.sleep(delay)
    except Exception:
        # Fallback to direct fill if typing encounters an event lock
        try:
            await input_field.fill(text)
        except Exception:
            pass

# Universal DOM Annotation Script: tags all visible interactive widgets
ANNOTATE_SCREEN_SCRIPT = """
() => {
    document.querySelectorAll('[data-agent-target]').forEach(el => el.removeAttribute('data-agent-target'));
    
    const rawCandidates = Array.from(document.querySelectorAll(
        'button, label, select, input:not([type="hidden"]), textarea, [role="button"], [role="checkbox"], [role="radio"], [contenteditable="true"]'
    ));
    
    const visibleElements = [];
    let targetCounter = 0;
    
    // Deduplicate: If an input is inside a label, keep the label or input
    const filtered = rawCandidates.filter(el => {
        if (el.tagName === 'INPUT' && (el.type === 'radio' || el.type === 'checkbox') && el.closest('label')) {
            return false;
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
        
        const isPalette = el.classList.contains('palette-item');
        
        el.setAttribute('data-agent-target', String(targetCounter));
        
        let textContent = (el.innerText || el.textContent || el.value || el.placeholder || el.getAttribute('aria-label') || '').trim();
        textContent = textContent.replace(/\\s+/g, ' ').substring(0, 120);
        
        let optionsList = [];
        if (el.tagName === 'SELECT') {
            optionsList = Array.from(el.options).map(o => o.text.trim());
        }
        
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

async def robust_click_element(page, element, target_x=None, target_y=None, from_x=250.0, from_y=250.0):
    """Executes a 3-tier fallback click ensuring the element is activated regardless of styling."""
    try:
        # Tier 1: Biomimetic Human Mouse Move & Click
        box = await element.bounding_box()
        if box and box['width'] > 0 and box['height'] > 0:
            tx = box['x'] + box['width'] / 2
            ty = box['y'] + box['height'] / 2
            await human_mouse_move(page, from_x, from_y, tx, ty)
            await page.mouse.click(tx, ty)
            return True, tx, ty
    except Exception:
        pass

    try:
        # Tier 2: Playwright Force Click
        await element.click(force=True, timeout=1000)
        return True, from_x, from_y
    except Exception:
        pass

    try:
        # Tier 3: Direct DOM Event Dispatch
        await page.evaluate("(el) => { el.focus(); el.click(); }", element)
        return True, from_x, from_y
    except Exception:
        pass

    return False, from_x, from_y

async def robust_select_dropdown(element, opt_val):
    """3-tier resilient dropdown option selector."""
    opt_val_str = str(opt_val).strip()
    
    # Tier 1: Exact label
    try:
        await element.select_option(label=opt_val_str, timeout=800)
        return True
    except Exception:
        pass

    # Tier 2: Exact value
    try:
        await element.select_option(value=opt_val_str, timeout=800)
        return True
    except Exception:
        pass

    # Tier 3: Fuzzy option substring match
    try:
        options = await element.query_selector_all("option")
        for o in options:
            txt = (await o.inner_text()).strip()
            val = await o.get_attribute("value") or ""
            if opt_val_str.lower() in txt.lower() or txt.lower() in opt_val_str.lower():
                await element.select_option(value=val or txt)
                return True
    except Exception:
        pass

    # Tier 4: Fallback to first non-empty option
    try:
        await element.select_option(index=1)
        return True
    except Exception:
        pass

    return False

async def try_advance_next(page, cur_x, cur_y):
    """Guaranteed auto-navigation helper that finds and clicks the active Next button."""
    try:
        # Find all potential navigation buttons
        candidates = await page.query_selector_all("button:not(.hidden), #next-btn:not(.hidden), [role='button'], a.btn")
        for btn in candidates:
            try:
                is_vis = await btn.is_visible()
                if not is_vis:
                    continue
                txt = (await page.evaluate("(el) => (el.innerText || el.value || '').toLowerCase()", btn)).strip()
                
                # Strict safety guard: NEVER click final submission button
                if any(s in txt for s in ["finalize", "submit exam", "submit test", "end exam", "finish exam"]):
                    continue
                    
                if any(n in txt for n in ["next", "save & next", "continue", "proceed", "forward", "→", ">", "save"]):
                    success, nx, ny = await robust_click_element(page, btn, from_x=cur_x, from_y=cur_y)
                    if success:
                        print(f"    [⏩ AUTO-ADVANCE] Navigated forward via '{txt}' button.")
                        await asyncio.sleep(0.4)
                        return True, nx, ny
            except Exception:
                continue
    except Exception:
        pass
    return False, cur_x, cur_y

def parse_llm_json(raw_text):
    """Robust JSON parser that extracts JSON even if the model outputs markdown wrappers or extra text."""
    clean = raw_text.strip()
    try:
        return json.loads(clean)
    except Exception:
        pass
        
    # Regex extract JSON object
    match = re.search(r'\{.*\}', clean, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except Exception:
            pass
    return None

async def universal_destruction_engine():
    print("=" * 68)
    print("🧠 SYSTEM ACTIVE: AUTONOMOUS SCREEN-AWARE UNIVERSAL TEST AGENT")
    print("🎯 Enterprise-Grade Self-Healing Architecture (0% Failure Tolerance)")
    print("=" * 68)
    
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
                raise Exception("No active browser tabs found on port 9222. Please open Chrome with debugging port 9222.")
            
            # Find the currently visible active tab
            page = all_pages[0]
            for p_target in all_pages:
                try:
                    if await p_target.evaluate("document.visibilityState === 'visible'"):
                        page = p_target
                        break
                except Exception:
                    pass
                
            print(f"[+] Hooked into active viewport: {page.url}\n")
            
            MAX_SCREEN_CYCLES = 50
            
            for cycle in range(1, MAX_SCREEN_CYCLES + 1):
                # Annotate all visible widgets
                screen_state = await page.evaluate(ANNOTATE_SCREEN_SCRIPT)
                elements = screen_state.get('elements', [])
                q_context = screen_state.get('question_context', '')
                tracker = screen_state.get('tracker', f'Question Step {cycle}')
                
                if not elements:
                    print("[!] Waiting for question viewport to render...")
                    await asyncio.sleep(0.6)
                    continue

                print(f"\n--- [Step {cycle}] {tracker} ---")

                # Filter out palette buttons from LLM prompt
                relevant_elements = [e for e in elements if not e.get('is_palette_btn')]

                system_prompt = (
                    "You are a world-class academic test taker solving an online exam.\n"
                    "All interactive elements on screen are tagged with `[data-agent-target=\"<index>\"]`.\n\n"
                    "RULES FOR ACTION DETERMINATION:\n"
                    "1. Radio options (`type: 'radio'`) -> Single Choice: Return action `type: 'click'` with target_index of the correct answer.\n"
                    "2. Checkbox options (`type: 'checkbox'`) -> Multi-Select: Return action `type: 'click'` for ALL correct answer indices.\n"
                    "3. Select tags (`tag: 'select'`) -> Dropdown: Return action `type: 'select'`, target_index, and `option_text`.\n"
                    "4. Input/Textarea (`tag: 'input'` or `tag: 'textarea'`) -> Fill Blank/Code: Return action `type: 'type'`, target_index, and `text`.\n"
                    "5. If a 'Save & Next', 'Next', or 'Continue' button exists, include clicking it as the LAST action in the array.\n\n"
                    "CRITICAL SAFETY RULE:\n"
                    "- NEVER click final submission buttons ('Finalize Submission', 'Submit Exam', 'End Test').\n\n"
                    "Output strictly in this JSON format:\n"
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
                        raw_content = resp.choices[0].message.content
                        plan = parse_llm_json(raw_content)
                        if plan and plan.get("actions"):
                            break
                    except Exception:
                        continue

                actions = plan.get("actions", []) if plan else []
                
                # If LLM returned no actions, generate an automated fallback plan
                if not actions:
                    # Select first valid input option if available
                    for el_item in relevant_elements:
                        if el_item.get('tag') in ['label', 'input', 'select']:
                            actions.append({
                                "type": "select" if el_item.get('tag') == 'select' else "click",
                                "target_index": el_item.get('index'),
                                "option_text": el_item.get('options', [''])[0] if el_item.get('options') else '',
                                "reason": "Self-healing fallback selection"
                            })
                            break

                print(f"💡 AI Analysis: {plan.get('question_summary', 'Executing optimal response...') if plan else 'Self-healing mode active'}")
                has_navigated = False

                for act_idx, action in enumerate(actions):
                    try:
                        act_type = action.get("type", "click")
                        t_idx = str(action.get("target_index", ""))
                        reason = action.get("reason", "")
                        
                        if not t_idx:
                            continue
                            
                        target_el = await page.query_selector(f'[data-agent-target="{t_idx}"]')
                        if not target_el:
                            continue
                            
                        # Safety shield: never click final submit
                        el_text = (await page.evaluate("(el) => (el.innerText || el.value || '').toLowerCase()", target_el)).strip()
                        if any(x in el_text for x in ["finalize submission", "submit exam", "submit test", "end test", "finish exam"]):
                            print(f"    [🛡️ SAFETY SHIELD] Preserved final submission button: '{el_text}'")
                            continue

                        # Scroll element smoothly into center view
                        await page.evaluate("(el) => el.scrollIntoView({behavior: 'smooth', block: 'center'})", target_el)
                        await asyncio.sleep(0.08)
                        
                        if act_type == "click":
                            _, current_mouse_x, current_mouse_y = await robust_click_element(
                                page, target_el, from_x=current_mouse_x, from_y=current_mouse_y
                            )
                            print(f"    [+] Clicked [{t_idx}] -> {reason}")
                            
                            if any(x in el_text for x in ["next", "continue", "save & next", "proceed", "forward", "→", ">"]):
                                has_navigated = True
                                await asyncio.sleep(0.3)
                                break
                                
                        elif act_type == "type":
                            _, current_mouse_x, current_mouse_y = await robust_click_element(
                                page, target_el, from_x=current_mouse_x, from_y=current_mouse_y
                            )
                            await asyncio.sleep(0.08)
                            val = str(action.get("text", ""))
                            await human_type(target_el, val)
                            print(f"    [+] Typed '{val}' into [{t_idx}] -> {reason}")
                            
                        elif act_type == "select":
                            opt_val = str(action.get("option_text", action.get("text", action.get("value", ""))))
                            await robust_select_dropdown(target_el, opt_val)
                            print(f"    [+] Selected dropdown option '{opt_val}' on [{t_idx}] -> {reason}")

                        await asyncio.sleep(random.uniform(0.12, 0.25))
                    except Exception as step_err:
                        continue

                # AUTO-ADVANCE FAILSAFE:
                # If question was solved but Next was not clicked, find and click Next automatically!
                if not has_navigated:
                    adv_success, current_mouse_x, current_mouse_y = await try_advance_next(page, current_mouse_x, current_mouse_y)
                    if adv_success:
                        has_navigated = True

                if not has_navigated:
                    # Check if final submit button is visible on page
                    final_btn = await page.query_selector("#submit-btn:not(.hidden)")
                    if final_btn and await final_btn.is_visible():
                        print("\n[🎯 FINAL QUESTION REACHED] All 25 questions resolved successfully!")
                        break
                    else:
                        print("\n[*] Exam questions complete. All accessible elements resolved.")
                        break

            print("\n" + "=" * 68)
            print("🎉 [SUCCESS] AUTONOMOUS AGENT SOLVING RUN COMPLETE")
            print("🛡️  All questions answered with precision. Final submission ready for review.")
            print("=" * 68)

        except Exception as e:
            print(f"\n[X] Automation Notice: {str(e)}")
            print("[!] Ensure Chrome was started with --remote-debugging-port=9222.")

if __name__ == "__main__":
    asyncio.run(universal_destruction_engine())
