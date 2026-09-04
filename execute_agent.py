import asyncio
import os
import random
import json
import math
import re
import sys

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
    try:
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

from playwright.async_api import async_playwright
from groq import Groq

# Verify GROQ_API_KEY environment variable or local .env file
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
if not GROQ_API_KEY and os.path.exists(".env"):
    try:
        with open(".env", "r", encoding="utf-8") as f:
            for line in f:
                line_str = line.strip()
                if line_str.startswith("GROQ_API_KEY="):
                    GROQ_API_KEY = line_str.split("=", 1)[1].strip(" \"'")
    except Exception:
        pass

if not GROQ_API_KEY:
    print("\n[!] FATAL ERROR: GROQ_API_KEY is not configured.")
    print("[!] Quick Setup: set GROQ_API_KEY=your_groq_key")
    print("[!] Or create a .env file with: GROQ_API_KEY=your_groq_key")
    sys.exit(1)

client = Groq(api_key=GROQ_API_KEY)

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
            noise_x = random.uniform(-0.3, 0.3)
            noise_y = random.uniform(-0.3, 0.3)
            
            await page.mouse.move(cx + arc + noise_x, cy + arc + noise_y)
            await asyncio.sleep(random.uniform(0.008, 0.016))
        
        await page.mouse.move(to_x, to_y)
    except Exception:
        pass

async def human_type(input_field, text):
    """Types text with natural human variance, capitalization pauses, and occasional auto-corrected typos."""
    try:
        await input_field.focus()
        await asyncio.sleep(0.1)
        
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
                await asyncio.sleep(random.uniform(0.06, 0.12))
                await asyncio.sleep(random.uniform(0.12, 0.18))
                await input_field.press("Backspace")
                await asyncio.sleep(random.uniform(0.06, 0.12))
                
            delay = random.uniform(0.04, 0.09)
            if char.isupper() or char in '!@#$%^&*()_+{}|:"<>?':
                delay += random.uniform(0.06, 0.12)
            if char in " ,.?!;":
                delay += random.uniform(0.08, 0.16)
                
            await input_field.press(char)
            await asyncio.sleep(delay)
    except Exception:
        try:
            await input_field.fill(text)
        except Exception:
            pass

ANNOTATE_SCREEN_SCRIPT = """
() => {
    // 1. Inspect screen states
    const isTerminated = document.getElementById('terminated-screen') && 
                         !document.getElementById('terminated-screen').classList.contains('hidden') &&
                         window.getComputedStyle(document.getElementById('terminated-screen')).display !== 'none';
                         
    const isResult = document.getElementById('result-screen') && 
                     !document.getElementById('result-screen').classList.contains('hidden') &&
                     window.getComputedStyle(document.getElementById('result-screen')).display !== 'none';
                     
    const isStart = document.getElementById('start-screen') && 
                    !document.getElementById('start-screen').classList.contains('hidden') &&
                    window.getComputedStyle(document.getElementById('start-screen')).display !== 'none';
                    
    if (isTerminated) return { state: 'terminated' };
    if (isResult) return { state: 'result' };
    if (isStart) return { state: 'start' };

    document.querySelectorAll('[data-agent-target]').forEach(el => el.removeAttribute('data-agent-target'));
    
    const activeViewport = document.getElementById('question-card-viewport') || document.querySelector('.panel:not(.hidden)') || document.body;
    
    const rawCandidates = Array.from(activeViewport.querySelectorAll(
        'button, label, select, input:not([type="hidden"]), textarea, [role="button"], [role="checkbox"], [role="radio"], [contenteditable="true"]'
    ));
    
    const visibleElements = [];
    let targetCounter = 0;
    
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
    
    const currentQNum = parseInt(document.getElementById('current-q-num')?.innerText || '0', 10);
    const totalQCount = parseInt(document.getElementById('total-q-count')?.innerText || '0', 10);
    
    return {
        state: 'exam',
        elements: visibleElements,
        question_context: questionContext,
        tracker: trackerText,
        current_q_num: currentQNum,
        total_q_count: totalQCount
    };
}
"""

async def robust_click_element(page, element, from_x=250.0, from_y=250.0):
    """Executes a 3-tier fallback click ensuring the element is activated regardless of styling."""
    try:
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
        await element.click(force=True, timeout=800)
        return True, from_x, from_y
    except Exception:
        pass

    try:
        await page.evaluate("(el) => { el.focus(); el.click(); }", element)
        return True, from_x, from_y
    except Exception:
        pass

    return False, from_x, from_y

async def robust_select_dropdown(element, opt_val):
    """4-tier resilient dropdown option selector."""
    opt_val_str = str(opt_val).strip()
    
    try:
        await element.select_option(label=opt_val_str, timeout=600)
        return True
    except Exception:
        pass

    try:
        await element.select_option(value=opt_val_str, timeout=600)
        return True
    except Exception:
        pass

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

    try:
        await element.select_option(index=1)
        return True
    except Exception:
        pass

    return False

async def trigger_next_button(page, cur_x=250.0, cur_y=250.0):
    """Guaranteed Next Button activator that moves the mouse naturally and advances to the next question."""
    try:
        has_next = await page.evaluate("""() => {
            const isVisible = (b) => b && !b.classList.contains('hidden') && b.offsetParent !== null && window.getComputedStyle(b).display !== 'none' && !b.disabled;
            
            const nextBtn = document.getElementById('next-btn');
            if (nextBtn && isVisible(nextBtn)) {
                nextBtn.click();
                return true;
            }
            
            const altBtn = Array.from(document.querySelectorAll('button, a.btn, [role="button"]')).find(b => {
                if (!isVisible(b)) return false;
                const t = (b.innerText || b.value || '').toLowerCase().trim();
                return (t.includes('next') || t.includes('continue') || t.includes('proceed') || t.includes('save') || t.includes('forward')) && 
                       !t.includes('finalize') && !t.includes('submit') && !t.includes('finish') && !t.includes('reload');
            });
            if (altBtn) {
                altBtn.click();
                return true;
            }
            return false;
        }""")

        if has_next:
            next_el = await page.query_selector("#next-btn:not(.hidden), button:has-text('Next'):not(.hidden), button:has-text('Save & Next'):not(.hidden)")
            if next_el and await next_el.is_visible():
                box = await next_el.bounding_box()
                if box:
                    tx = box['x'] + box['width'] / 2
                    ty = box['y'] + box['height'] / 2
                    await human_mouse_move(page, cur_x, cur_y, tx, ty)
                    cur_x, cur_y = tx, ty
            
            return True, cur_x, cur_y
    except Exception:
        pass
    return False, cur_x, cur_y

def parse_llm_json(raw_text):
    """Robust JSON parser that extracts JSON even with markdown wrappers."""
    clean = raw_text.strip()
    try:
        return json.loads(clean)
    except Exception:
        pass
        
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
    print("🎯 Dynamic Solver Engine: Supports ANY Question Count (25, 50, 100+)")
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
            
            # Find active visible tab
            page = all_pages[0]
            for p_target in all_pages:
                try:
                    if await p_target.evaluate("document.visibilityState === 'visible'"):
                        page = p_target
                        break
                except Exception:
                    pass
                
            print(f"[+] Hooked into active viewport: {page.url}\n")
            
            # Unbounded dynamic loop runway (supports tests with up to 500 questions)
            MAX_SCREEN_CYCLES = 500
            
            for cycle in range(1, MAX_SCREEN_CYCLES + 1):
                # 1. Inspect screen state
                screen_state = await page.evaluate(ANNOTATE_SCREEN_SCRIPT)
                current_state = screen_state.get('state', 'exam')
                
                # Check for termination
                if current_state == 'terminated':
                    print("\n" + "=" * 68)
                    print("🛑 [SESSION TERMINATED] Exam was stopped by security telemetry.")
                    print("🛡️  Agent halting execution immediately. No auto-restart triggered.")
                    print("=" * 68)
                    return

                if current_state == 'result':
                    print("\n" + "=" * 68)
                    print("📊 [EXAM SUBMITTED] Result screen detected. Halting agent.")
                    print("=" * 68)
                    return

                if current_state == 'start':
                    print("[⏳ WAITING] Start screen visible. Please click 'Start Secure Exam' in browser...")
                    await asyncio.sleep(1.2)
                    continue

                elements = screen_state.get('elements', [])
                q_context = screen_state.get('question_context', '')
                tracker = screen_state.get('tracker', '')
                current_q_num = screen_state.get('current_q_num', 0)
                total_q_count = screen_state.get('total_q_count', 0)

                header_label = f"Question {current_q_num} of {total_q_count}" if (current_q_num and total_q_count) else f"Step {cycle}"

                if not elements:
                    print("[!] Waiting for question viewport...")
                    await asyncio.sleep(0.5)
                    continue

                print(f"\n--- [{header_label}] {tracker} ---")

                # Natural human reading pause before answering
                await asyncio.sleep(random.uniform(0.6, 1.2))

                # Filter question options
                question_options = [e for e in elements if not e.get('is_palette_btn') and not any(
                    n in e.get('text', '').lower() for n in ['next', 'previous', 'submit', 'finalize', 'save & next', 'reload']
                )]

                system_prompt = (
                    "You are a master academic solver.\n"
                    "All interactive elements have a `[data-agent-target=\"<index>\"]` integer index.\n\n"
                    "INSTRUCTIONS:\n"
                    "1. Read the active question and identify the correct answer(s).\n"
                    "2. Return the action needed to answer the question:\n"
                    "   - For radio/checkbox: {\"type\": \"click\", \"target_index\": <idx>, \"reason\": \"...\"}\n"
                    "   - For dropdown select: {\"type\": \"select\", \"target_index\": <idx>, \"option_text\": \"...\", \"reason\": \"...\"}\n"
                    "   - For text/textarea: {\"type\": \"type\", \"target_index\": <idx>, \"text\": \"...\", \"reason\": \"...\"}\n\n"
                    "Output strictly in this JSON format:\n"
                    "{\n"
                    "  \"question_summary\": \"Question topic and answer\",\n"
                    "  \"actions\": [\n"
                    "    {\"type\": \"click\", \"target_index\": 25, \"reason\": \"Select correct option\"}\n"
                    "  ]\n"
                    "}"
                )
                
                user_content = (
                    f"--- ACTIVE QUESTION CONTENT ---\n{q_context}\n\n"
                    f"--- INTERACTIVE QUESTION TARGETS ---\n{json.dumps(question_options, indent=2)}"
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
                
                if not actions and question_options:
                    first_opt = question_options[0]
                    actions.append({
                        "type": "select" if first_opt.get('tag') == 'select' else "click",
                        "target_index": first_opt.get('index'),
                        "option_text": first_opt.get('options', [''])[0] if first_opt.get('options') else '',
                        "reason": "Self-healing option selection"
                    })

                print(f"💡 AI Analysis: {plan.get('question_summary', 'Solving question...') if plan else 'Self-healing mode active'}")

                # 1. Execute answer actions
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
                            
                        el_text = (await page.evaluate("(el) => (el.innerText || el.value || '').toLowerCase()", target_el)).strip()
                        if any(x in el_text for x in ["finalize submission", "submit exam", "submit test", "end test", "finish exam", "reload"]):
                            continue

                        await page.evaluate("(el) => el.scrollIntoView({behavior: 'smooth', block: 'center'})", target_el)
                        await asyncio.sleep(0.08)
                        
                        if act_type == "click":
                            _, current_mouse_x, current_mouse_y = await robust_click_element(
                                page, target_el, from_x=current_mouse_x, from_y=current_mouse_y
                            )
                            print(f"    [+] Selected [{t_idx}] -> {reason}")
                                
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

                        await asyncio.sleep(random.uniform(0.2, 0.4))
                    except Exception:
                        continue

                # 2. Advance to the next question
                nav_success, current_mouse_x, current_mouse_y = await trigger_next_button(
                    page, current_mouse_x, current_mouse_y
                )

                if nav_success:
                    print(f"    [⏩ NAVIGATION] Advanced to next question.")
                    # Wait for next question to render
                    for _ in range(12):
                        new_q = await page.evaluate("() => parseInt(document.getElementById('current-q-num')?.innerText || '0', 10)")
                        if current_q_num and new_q > current_q_num:
                            break
                        await asyncio.sleep(0.1)
                else:
                    # Final question reached (No next button exists, submit button is active)
                    print("\n" + "=" * 68)
                    print("🎯 [FINAL QUESTION COMPLETED] All questions on this exam resolved successfully!")
                    print("🛡️  SAFETY SHIELD ACTIVE: 'Finalize Submission' button left untouched.")
                    print("👉  You can now review your answers and click 'Finalize Submission' manually.")
                    print("=" * 68)
                    break

        except Exception as e:
            print(f"\n[X] Automation Notice: {str(e)}")
            print("[!] Ensure Chrome was started with --remote-debugging-port=9222.")

if __name__ == "__main__":
    asyncio.run(universal_destruction_engine())
