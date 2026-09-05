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

async def human_mouse_move(page, from_x, from_y, to_x, to_y, steps=8):
    """Generates physical cubic Bezier curves with micro-tremors to mimic human hand motor dynamics."""
    try:
        for i in range(1, steps + 1):
            t = i / steps
            t_curved = t * t * (3 - 2 * t)
            
            cx = from_x + (to_x - from_x) * t_curved
            cy = from_y + (to_y - from_y) * t_curved
            
            arc = math.sin(t * math.pi) * 4.0 * (random.random() - 0.5)
            noise_x = random.uniform(-0.2, 0.2)
            noise_y = random.uniform(-0.2, 0.2)
            
            await page.mouse.move(cx + arc + noise_x, cy + arc + noise_y)
            await asyncio.sleep(random.uniform(0.006, 0.014))
        
        await page.mouse.move(to_x, to_y)
    except Exception:
        pass

async def human_type(input_field, text):
    """Types text with natural human variance and keystroke timing."""
    try:
        await input_field.focus()
        await asyncio.sleep(0.08)
        
        for char in text:
            delay = random.uniform(0.03, 0.08)
            if char.isupper() or char in '!@#$%^&*()_+{}|:\"<>?':
                delay += random.uniform(0.04, 0.08)
            if char in " ,.?!;":
                delay += random.uniform(0.05, 0.10)
                
            await input_field.press(char)
            await asyncio.sleep(delay)
    except Exception:
        try:
            await input_field.fill(text)
        except Exception:
            pass

ANNOTATE_SCREEN_SCRIPT = """
() => {
    // 1. Universal screen state detection
    const fullText = (document.body.innerText || '').toLowerCase();
    
    // Check for termination / violation screen
    const isTerminated = (
        (document.getElementById('terminated-screen') && !document.getElementById('terminated-screen').classList.contains('hidden') && window.getComputedStyle(document.getElementById('terminated-screen')).display !== 'none') ||
        (fullText.includes('session terminated') || fullText.includes('security violation') || fullText.includes('access revoked') || fullText.includes('exam terminated'))
    );
    
    // Check for results / finished screen
    const isResult = (
        (document.getElementById('result-screen') && !document.getElementById('result-screen').classList.contains('hidden') && window.getComputedStyle(document.getElementById('result-screen')).display !== 'none') ||
        (fullText.includes('exam result') || fullText.includes('assessment submitted') || fullText.includes('responses have been recorded') || fullText.includes('submission accepted') || fullText.includes('test completed'))
    );

    if (isTerminated) return { state: 'terminated' };
    if (isResult) return { state: 'result' };

    // Strip previous agent markers
    document.querySelectorAll('[data-agent-target]').forEach(el => el.removeAttribute('data-agent-target'));
    
    // Helper to check visibility
    const isVisible = (el) => {
        if (!el) return false;
        const style = window.getComputedStyle(el);
        if (style.display === 'none' || style.visibility === 'hidden' || style.opacity === '0' || el.classList.contains('hidden')) return false;
        const rect = el.getBoundingClientRect();
        return rect.width > 0 && rect.height > 0;
    };

    // Helper to find associated text for any input
    const findInputText = (inp) => {
        // 1. Check <label for="id">
        if (inp.id) {
            const lbl = document.querySelector(`label[for="${inp.id}"]`);
            if (lbl && lbl.innerText.trim()) return lbl.innerText.trim();
        }
        // 2. Check enclosing <label>
        const parentLabel = inp.closest('label');
        if (parentLabel && parentLabel.innerText.trim()) return parentLabel.innerText.trim();
        
        // 3. Check enclosing table row <tr>
        const tr = inp.closest('tr');
        if (tr) {
            const cells = Array.from(tr.querySelectorAll('td, th'));
            const cellTexts = cells.map(c => (c.innerText || '').trim()).filter(t => t.length > 0 && t !== inp.value);
            if (cellTexts.length > 0) return cellTexts.join(' ');
        }

        // 4. Check enclosing container (.option, .answer, li, .form-check, div, p)
        const container = inp.closest('.option, .answer, .form-check, .custom-control, .radio, li, p, dd');
        if (container) {
            const txt = (container.innerText || '').trim();
            if (txt.length > 0) return txt;
        }

        // 5. Check next sibling text
        let sibling = inp.nextSibling;
        while (sibling) {
            if (sibling.nodeType === Node.TEXT_NODE && sibling.textContent.trim()) {
                return sibling.textContent.trim();
            }
            if (sibling.nodeType === Node.ELEMENT_NODE && sibling.innerText && sibling.innerText.trim()) {
                return sibling.innerText.trim();
            }
            sibling = sibling.nextSibling;
        }

        // 6. Value or aria attributes
        return (inp.value || inp.getAttribute('aria-label') || inp.placeholder || inp.name || '').trim();
    };

    // 2. Extract Question Inputs (Radios, Checkboxes, Dropdowns, Text Inputs, Textareas)
    const questionInputs = Array.from(document.querySelectorAll(
        'input[type="radio"], input[type="checkbox"], select, textarea, input[type="text"], input:not([type])'
    ));

    const visibleElements = [];
    let targetCounter = 0;

    for (const inp of questionInputs) {
        if (!isVisible(inp) && inp.type !== 'radio' && inp.type !== 'checkbox') continue;
        
        // For radio/checkbox, even if hidden by custom css checkbox UI, parent might be visible
        if ((inp.type === 'radio' || inp.type === 'checkbox') && !isVisible(inp)) {
            const parent = inp.closest('label, tr, .option, .answer, .form-check, div');
            if (!parent || !isVisible(parent)) continue;
        }

        inp.setAttribute('data-agent-target', String(targetCounter));
        
        let textContent = findInputText(inp);
        textContent = textContent.replace(/\\s+/g, ' ').substring(0, 160);

        let optionsList = [];
        if (inp.tagName === 'SELECT') {
            optionsList = Array.from(inp.options).map(o => (o.text || o.value || '').trim()).filter(Boolean);
        }

        visibleElements.push({
            index: targetCounter,
            tag: inp.tagName.toLowerCase(),
            type: inp.type || (inp.tagName === 'SELECT' ? 'select' : 'textarea'),
            name: inp.getAttribute('name') || '',
            value: inp.value || '',
            text: textContent,
            options: optionsList,
            is_checked: inp.checked === true
        });

        targetCounter++;
    }

    // Check if on start/landing page
    if (visibleElements.length === 0 && fullText.match(/(?:start|begin|take|launch|instructions)/i)) {
        return { state: 'standby' };
    }

    // 3. Extract active question context
    const questionContainers = Array.from(document.querySelectorAll(
        '#tblQuestion, #pnlQuestion, .card, article, fieldset, [role="group"], form, main, #question-card-viewport, .question-container, .question-body, .exam-question, table'
    ));
    let bestContainerText = '';
    for (const c of questionContainers) {
        if (isVisible(c)) {
            const txt = (c.innerText || '').trim();
            if (txt.length > 25 && (!bestContainerText || txt.length < bestContainerText.length)) {
                bestContainerText = txt;
            }
        }
    }
    const questionContext = bestContainerText || (document.body.innerText || '').substring(0, 4000);
    
    // 4. Dynamic Question Numbering
    let currentQNum = 0;
    let totalQCount = 0;
    const qMatch = questionContext.match(/(?:question|problem|q\\.?|item)\\s*(\\d+)\\s*(?:of|\\/|\\-|\\:)\\s*(\\d+)/i) ||
                   (document.body.innerText || '').match(/(?:question|problem|q\\.?|item)\\s*(\\d+)\\s*(?:of|\\/|\\-|\\:)\\s*(\\d+)/i);
    if (qMatch) {
        currentQNum = parseInt(qMatch[1], 10);
        totalQCount = parseInt(qMatch[2], 10);
    }
    
    return {
        state: 'exam',
        elements: visibleElements,
        question_context: questionContext,
        current_q_num: currentQNum,
        total_q_count: totalQCount
    };
}
"""

async def robust_click_element(page, element, from_x=250.0, from_y=250.0):
    """Resilient universal option selector supporting any HTML table, div, or custom portal UI."""
    try:
        # Step 1: Scroll element into center view
        await page.evaluate("(el) => el.scrollIntoView({behavior: 'smooth', block: 'center'})", element)
        await asyncio.sleep(0.08)

        # Step 2: Full DOM state mutation + event cascades on the input and all surrounding wrappers
        await page.evaluate("""(el) => {
            if (!el) return;
            
            // Set input state directly
            if (el.tagName === 'INPUT') {
                if (el.type === 'radio') {
                    el.checked = true;
                } else if (el.type === 'checkbox') {
                    el.checked = !el.checked;
                }
            }
            
            // Native element activation
            try { el.focus(); } catch(e) {}
            try { el.click(); } catch(e) {}
            
            // Event cascade for React / Vue / Angular / jQuery / Native HTML forms
            const evList = ['mousedown', 'mouseup', 'click', 'input', 'change'];
            for (const evName of evList) {
                try {
                    el.dispatchEvent(new Event(evName, { bubbles: true, cancelable: true }));
                } catch(e) {}
            }

            // Also click associated <label for="...">
            if (el.id) {
                const lbl = document.querySelector(`label[for="${el.id}"]`);
                if (lbl && lbl !== el) {
                    try { lbl.click(); } catch(e) {}
                }
            }
            const parentLabel = el.closest('label');
            if (parentLabel && parentLabel !== el) {
                try { parentLabel.click(); } catch(e) {}
            }

            // Also click parent container row (tr, li, .option, .answer, .form-check)
            const row = el.closest('tr, li, .option, .answer, .form-check, .custom-control, .option-label');
            if (row && row !== el) {
                try { row.click(); } catch(e) {}
                row.classList.add('active-selected');
            }
        }""", element)

        # Step 3: Natural mouse move & physical CDP click
        box = await element.bounding_box()
        if not box or box['width'] <= 0 or box['height'] <= 0:
            # If input is tiny/hidden by custom CSS, find bounding box of parent label/row
            parent = await element.query_selector("xpath=..")
            if parent:
                box = await parent.bounding_box()

        if box and box['width'] > 0 and box['height'] > 0:
            tx = box['x'] + box['width'] / 2
            ty = box['y'] + box['height'] / 2
            await human_mouse_move(page, from_x, from_y, tx, ty)
            await page.mouse.click(tx, ty)
            from_x, from_y = tx, ty

        # Step 4: Verification - verify input is checked
        is_checked = await page.evaluate("(el) => el.checked === true", element)
        if not is_checked:
            try:
                await element.check(force=True, timeout=500)
            except Exception:
                try:
                    await element.click(force=True, timeout=500)
                except Exception:
                    pass

        return True, from_x, from_y
    except Exception:
        pass

    return False, from_x, from_y

async def robust_select_dropdown(element, opt_val):
    """Resilient dropdown option selector."""
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
    """Universal Next/Save Button finder that works on ASP.NET, PHP, Moodle, and all exam portals."""
    try:
        btn_info = await page.evaluate("""() => {
            const isVisible = (b) => {
                if (!b || b.disabled || b.classList.contains('hidden')) return false;
                const style = window.getComputedStyle(b);
                if (style.display === 'none' || style.visibility === 'hidden' || style.opacity === '0') return false;
                const r = b.getBoundingClientRect();
                return r.width > 0 && r.height > 0;
            };

            const candidates = Array.from(document.querySelectorAll(
                'button, input[type="submit"], input[type="button"], input[type="image"], a, [role="button"], span.btn, div.btn'
            ));

            // Priority 1: Exact Next / Save & Next matches
            for (const b of candidates) {
                if (!isVisible(b)) continue;
                const text = (b.innerText || b.value || b.getAttribute('title') || b.getAttribute('alt') || b.name || b.id || '').toLowerCase().trim();
                
                // Exclude final test submission buttons
                if (text.includes('finalize') || text.includes('finish exam') || text.includes('end exam') || text.includes('end test') || text.includes('submit exam') || text.includes('submit test')) {
                    if (!text.includes('next') && !text.includes('save & next') && !text.includes('save and next')) {
                        continue;
                    }
                }

                if (text.includes('save & next') || text.includes('save and next') || text.includes('save & continue') || 
                    text.includes('next question') || text.includes('next >') || text.includes('next') || 
                    text === 'save' || text.includes('btnnext') || text === 'forward' || text === 'continue' || text === 'proceed') {
                    
                    b.focus();
                    b.click();
                    try { b.dispatchEvent(new Event('click', { bubbles: true })); } catch(e) {}
                    return { clicked: true, text: text };
                }
            }

            return { clicked: false };
        }""")

        if btn_info and btn_info.get('clicked'):
            # Also simulate natural mouse movement to next button area
            next_el = await page.query_selector(
                "input[type='submit'][value*='Next' i], input[type='button'][value*='Next' i], input[type='submit'][value*='Save' i], button:has-text('Next'), button:has-text('Save & Next'), #next-btn, #btnNext"
            )
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
    """Extracts valid JSON from raw LLM output even with markdown or extra text."""
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
    print("🧠 SYSTEM ACTIVE: AUTONOMOUS UNIVERSAL EXAM SOLVER")
    print("🎯 Dynamic Solver Engine: Universally Supports ANY Portal & Question Count")
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
            
            MAX_SCREEN_CYCLES = 500
            
            for cycle in range(1, MAX_SCREEN_CYCLES + 1):
                # 1. Inspect active screen state
                screen_state = await page.evaluate(ANNOTATE_SCREEN_SCRIPT)
                current_state = screen_state.get('state', 'exam')
                
                # Check for termination
                if current_state == 'terminated':
                    print("\n" + "=" * 68)
                    print("🛑 [SESSION TERMINATED] Assessment stopped by security policy.")
                    print("🛡️  Autonomous agent halting execution immediately.")
                    print("=" * 68)
                    return

                if current_state == 'result':
                    print("\n" + "=" * 68)
                    print("📊 [ASSESSMENT COMPLETE] Submission/score screen detected. Halting agent.")
                    print("=" * 68)
                    return

                if current_state == 'standby':
                    print("[⏳ STANDBY] Waiting for active question view in browser viewport...")
                    await asyncio.sleep(1.2)
                    continue

                elements = screen_state.get('elements', [])
                q_context = screen_state.get('question_context', '')
                current_q_num = screen_state.get('current_q_num', 0)
                total_q_count = screen_state.get('total_q_count', 0)

                header_label = f"Question {current_q_num} of {total_q_count}" if (current_q_num and total_q_count) else f"Assessment Item {cycle}"

                if not elements:
                    print("[!] Waiting for active question elements in viewport...")
                    await asyncio.sleep(0.6)
                    continue

                print(f"\n--- [{header_label}] ---")

                # Natural human reading pause before answering
                await asyncio.sleep(random.uniform(0.6, 1.2))

                # Question targets
                question_options = elements

                system_prompt = (
                    "You are a master academic examination solver.\n"
                    "Read the active question context and examine the available input targets.\n"
                    "Select the single best correct option or provide text for the input.\n\n"
                    "Output strictly in this JSON format:\n"
                    "{\n"
                    "  \"question_summary\": \"Brief explanation of question and correct answer\",\n"
                    "  \"selected_target_index\": 0,\n"
                    "  \"selected_option_text\": \"Exact text of the correct option\",\n"
                    "  \"text_to_type\": \"(only for text inputs/textareas)\",\n"
                    "  \"reason\": \"Why this is the correct answer\"\n"
                    "}"
                )
                
                user_content = (
                    f"--- ACTIVE QUESTION CONTENT ---\n{q_context}\n\n"
                    f"--- AVAILABLE QUESTION INPUT TARGETS ---\n{json.dumps(question_options, indent=2)}"
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
                        if plan and (plan.get("selected_target_index") is not None or plan.get("actions") or plan.get("selected_option_text")):
                            break
                    except Exception:
                        continue

                # Fallback matching if target index is ambiguous
                target_idx = None
                if plan:
                    if plan.get("selected_target_index") is not None:
                        target_idx = plan.get("selected_target_index")
                    elif plan.get("actions") and len(plan["actions"]) > 0:
                        target_idx = plan["actions"][0].get("target_index")
                
                # Fuzzy keyword matching fallback
                if target_idx is None or not any(e.get("index") == target_idx for e in question_options):
                    opt_search_text = (plan.get("selected_option_text", "") or plan.get("question_summary", "") or plan.get("reason", "")).lower()
                    matched_elem = None
                    for opt in question_options:
                        o_txt = opt.get("text", "").lower()
                        o_val = opt.get("value", "").lower()
                        if opt_search_text and (opt_search_text in o_txt or o_txt in opt_search_text or (len(o_val) > 0 and o_val == opt_search_text)):
                            matched_elem = opt
                            break
                    
                    if matched_elem:
                        target_idx = matched_elem.get("index")
                    elif question_options:
                        # Safety fallback: always answer first option
                        target_idx = question_options[0].get("index")

                summary_text = plan.get("question_summary", "Solving question...") if plan else "Autonomous solver analysis"
                print(f"💡 AI Analysis: {summary_text}")

                # Execute answer action
                target_el = await page.query_selector(f'[data-agent-target="{target_idx}"]')
                matched_target_info = next((e for e in question_options if e.get("index") == target_idx), {})
                
                if target_el:
                    tag_type = matched_target_info.get("type", "radio")
                    
                    if tag_type in ["radio", "checkbox"] or matched_target_info.get("tag") == "input":
                        _, current_mouse_x, current_mouse_y = await robust_click_element(
                            page, target_el, from_x=current_mouse_x, from_y=current_mouse_y
                        )
                        print(f"    [+] Selected Option [{target_idx}] -> {matched_target_info.get('text', '')}")
                        
                    elif tag_type in ["text", "textarea"]:
                        _, current_mouse_x, current_mouse_y = await robust_click_element(
                            page, target_el, from_x=current_mouse_x, from_y=current_mouse_y
                        )
                        await asyncio.sleep(0.08)
                        val = str(plan.get("text_to_type", plan.get("selected_option_text", ""))) if plan else ""
                        await human_type(target_el, val)
                        print(f"    [+] Typed '{val}' into [{target_idx}]")
                        
                    elif tag_type == "select" or matched_target_info.get("tag") == "select":
                        opt_val = str(plan.get("selected_option_text", "")) if plan else ""
                        await robust_select_dropdown(target_el, opt_val)
                        print(f"    [+] Selected dropdown option '{opt_val}' on [{target_idx}]")

                await asyncio.sleep(random.uniform(0.3, 0.5))

                # Snapshot old context before advancing
                old_context_snippet = (q_context or '')[:80]

                # 2. Advance to the next question
                nav_success, current_mouse_x, current_mouse_y = await trigger_next_button(
                    page, current_mouse_x, current_mouse_y
                )

                if nav_success:
                    print(f"    [⏩ ADVANCING] Navigating to next assessment item...")
                    
                    # Resilient wait for page transition / next question render
                    for _ in range(18):
                        await asyncio.sleep(0.15)
                        try:
                            new_context = await page.evaluate("() => (document.body.innerText || '').substring(0, 80)")
                            if new_context != old_context_snippet:
                                break
                        except Exception:
                            # Page is reloading / navigating
                            await asyncio.sleep(0.5)
                            break
                else:
                    # Final question reached (No next button exists, submit button is active)
                    print("\n" + "=" * 68)
                    print("🎯 [ASSESSMENT COMPLETE] All question items in active viewport resolved!")
                    print("🛡️  SAFETY SHIELD ACTIVE: 'Submit' button preserved for manual review.")
                    print("👉  Control passed to human operator for final verification.")
                    print("=" * 68)
                    break

        except Exception as e:
            print(f"\n[X] Automation Notice: {str(e)}")
            print("[!] Ensure Chrome was started with --remote-debugging-port=9222.")

if __name__ == "__main__":
    asyncio.run(universal_destruction_engine())
