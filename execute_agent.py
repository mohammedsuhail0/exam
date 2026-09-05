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

# Active Groq models for high precision and ultra-fast inference
CANDIDATE_MODELS = [
    "openai/gpt-oss-120b",
    "qwen/qwen3.8-27b",
    "qwen/qwen3.6-27b",
    "openai/gpt-oss-20b",
    "groq/compound"
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
        (fullText.includes('exam result') || fullText.includes('assessment submitted') || fullText.includes('responses have been recorded') || fullText.includes('submission accepted') || fullText.includes('test completed') || fullText.includes('scorecard'))
    );

    if (isTerminated) return { state: 'terminated' };
    if (isResult) return { state: 'result' };

    // Strip previous agent markers
    document.querySelectorAll('[data-agent-target]').forEach(el => el.removeAttribute('data-agent-target'));
    
    const isVisible = (el) => {
        if (!el) return false;
        const style = window.getComputedStyle(el);
        if (style.display === 'none' || style.visibility === 'hidden' || el.classList.contains('hidden')) return false;
        return true;
    };

    const isLoginOrHeader = (el) => {
        const id = (el.id || '').toLowerCase();
        const name = (el.name || '').toLowerCase();
        return id.includes('roll') || id.includes('code') || id.includes('user') || id.includes('login') ||
               name.includes('roll') || name.includes('code') || name.includes('user') || name.includes('login');
    };

    const isNavOrModal = (el) => {
        const text = (el.innerText || el.value || el.id || el.className || '').toLowerCase();
        return text.includes('next') || text.includes('prev') || text.includes('submit') || 
               text.includes('modal') || text.includes('return to fullscreen') || text.includes('cancel') ||
               el.id === 'nextBtn' || el.id === 'prevBtn' || el.id === 'submitBtn';
    };

    const visibleElements = [];
    let targetCounter = 0;

    // Strategy 1: Radio and Checkbox inputs (native)
    const radiosAndChecks = Array.from(document.querySelectorAll('input[type="radio"], input[type="checkbox"]'));
    for (const inp of radiosAndChecks) {
        if (isLoginOrHeader(inp)) continue;
        inp.setAttribute('data-agent-target', String(targetCounter));
        
        let txt = '';
        if (inp.id) {
            const lbl = document.querySelector(`label[for="${inp.id}"]`);
            if (lbl) txt = lbl.innerText;
        }
        if (!txt && inp.closest('label')) txt = inp.closest('label').innerText;
        if (!txt && inp.parentElement) txt = inp.parentElement.innerText;
        if (!txt) txt = inp.value || '';
        txt = txt.trim().replace(/\\s+/g, ' ').substring(0, 180);

        visibleElements.push({
            index: targetCounter,
            tag: inp.tagName.toLowerCase(),
            type: inp.type,
            name: inp.name || '',
            value: inp.value || '',
            text: txt,
            is_custom: false,
            is_checked: inp.checked === true
        });
        targetCounter++;
    }

    // Strategy 2: Custom Option Elements (.option, .choice, .answer, #optionsContainer > *, .options-container > *)
    const customOptions = Array.from(document.querySelectorAll(
        '.option, .choice, .answer, .quiz-option, .options-container > div, #optionsContainer > div, [role="radio"], [role="option"], .list-group-item'
    ));
    for (const opt of customOptions) {
        if (!isVisible(opt) || isNavOrModal(opt) || isLoginOrHeader(opt)) continue;
        if (opt.querySelector('input[type="radio"], input[type="checkbox"]')) continue;
        
        opt.setAttribute('data-agent-target', String(targetCounter));
        const txt = (opt.innerText || opt.textContent || '').trim().replace(/\\s+/g, ' ').substring(0, 180);
        
        visibleElements.push({
            index: targetCounter,
            tag: opt.tagName.toLowerCase(),
            type: 'custom_option',
            name: '',
            value: '',
            text: txt,
            is_custom: true,
            is_checked: opt.classList.contains('selected') || opt.classList.contains('active')
        });
        targetCounter++;
    }

    // Strategy 3: Dropdowns and Text Inputs inside question containers
    const otherInputs = Array.from(document.querySelectorAll('select, textarea, .question-container input[type="text"], #questionText input[type="text"]'));
    for (const inp of otherInputs) {
        if (isLoginOrHeader(inp) || !isVisible(inp)) continue;
        inp.setAttribute('data-agent-target', String(targetCounter));
        
        let optionsList = [];
        if (inp.tagName === 'SELECT') {
            optionsList = Array.from(inp.options).map(o => (o.text || o.value || '').trim()).filter(Boolean);
        }

        visibleElements.push({
            index: targetCounter,
            tag: inp.tagName.toLowerCase(),
            type: inp.type || inp.tagName.toLowerCase(),
            name: inp.name || '',
            value: inp.value || '',
            text: (inp.value || inp.placeholder || '').trim(),
            options: optionsList,
            is_custom: false,
            is_checked: false
        });
        targetCounter++;
    }

    // Question Context & Numbering
    const qTextEl = document.querySelector('#questionText, .question-text, .question, .question-body');
    const qNumEl = document.querySelector('#questionNumber, .question-header, .q-num');
    
    const questionText = (qTextEl ? qTextEl.innerText : document.body.innerText).trim().substring(0, 3000);
    const questionHeader = (qNumEl ? qNumEl.innerText : '').trim();

    let currentQNum = 0;
    let totalQCount = 0;
    const qMatch = (questionHeader + ' ' + questionText).match(/(?:question|problem|q\\.?|item)\\s*(\\d+)\\s*(?:of|\\/|\\-|\\:)\\s*(\\d+)/i);
    if (qMatch) {
        currentQNum = parseInt(qMatch[1], 10);
        totalQCount = parseInt(qMatch[2], 10);
    }
    
    return {
        state: 'exam',
        elements: visibleElements,
        question_context: (questionHeader ? questionHeader + '\\n' : '') + questionText,
        current_q_num: currentQNum,
        total_q_count: totalQCount
    };
}
"""

async def robust_click_element(page, element, from_x=250.0, from_y=250.0):
    """Resilient option selector supporting custom div options, table rows, and native radio inputs."""
    try:
        # Step 1: Scroll into view
        await page.evaluate("(el) => el.scrollIntoView({behavior: 'smooth', block: 'center'})", element)
        await asyncio.sleep(0.08)

        # Step 2: Full DOM state mutation + event cascades
        await page.evaluate("""(el) => {
            if (!el) return;
            
            // 1. Native input
            if (el.tagName === 'INPUT') {
                if (el.type === 'radio') {
                    el.checked = true;
                } else if (el.type === 'checkbox') {
                    el.checked = !el.checked;
                }
            }
            
            // 2. Custom option container (.option, .choice, etc.)
            if (el.classList.contains('option') || el.classList.contains('choice') || el.classList.contains('answer')) {
                // Clear sibling selections if radio-like
                const parent = el.parentElement;
                if (parent) {
                    parent.querySelectorAll('.option, .choice, .answer').forEach(o => {
                        o.classList.remove('selected', 'active');
                    });
                }
                el.classList.add('selected');
            }

            // 3. Native activation & event cascade
            try { el.focus(); } catch(e) {}
            try { el.click(); } catch(e) {}
            
            const evList = ['mousedown', 'mouseup', 'click', 'input', 'change'];
            for (const evName of evList) {
                try {
                    el.dispatchEvent(new MouseEvent(evName, { bubbles: true, cancelable: true, view: window }));
                } catch(e) {
                    try { el.dispatchEvent(new Event(evName, { bubbles: true, cancelable: true })); } catch(e2) {}
                }
            }
        }""", element)

        # Step 3: Natural mouse move & physical CDP click
        box = await element.bounding_box()
        if box and box['width'] > 0 and box['height'] > 0:
            tx = box['x'] + box['width'] / 2
            ty = box['y'] + box['height'] / 2
            await human_mouse_move(page, from_x, from_y, tx, ty)
            await page.mouse.click(tx, ty)
            from_x, from_y = tx, ty

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

    return False

async def trigger_next_button(page, cur_x=250.0, cur_y=250.0, target_q_num=0):
    """Strict Forward Navigation: Guarantees advancing forward (Next) and NEVER clicks Previous/Back or Final Submit."""
    try:
        btn_info = await page.evaluate("""(targetQ) => {
            const isVisible = (b) => {
                if (!b || b.disabled || b.classList.contains('hidden')) return false;
                const style = window.getComputedStyle(b);
                if (style.display === 'none' || style.visibility === 'hidden' || style.opacity === '0') return false;
                const r = b.getBoundingClientRect();
                return r.width > 0 && r.height > 0;
            };

            // Priority 0: Explicit ID #nextBtn
            const directNext = document.getElementById('nextBtn');
            if (directNext && isVisible(directNext)) {
                directNext.focus();
                directNext.click();
                try { directNext.dispatchEvent(new Event('click', { bubbles: true })); } catch(e) {}
                return { clicked: true, text: 'nextBtn', method: 'id' };
            }

            const candidates = Array.from(document.querySelectorAll(
                'button, input[type="submit"], input[type="button"], input[type="image"], a, [role="button"], span.btn, div.btn'
            ));

            // STRICT REJECTION: Reject backward buttons and final submit buttons
            const isStrictlyForbidden = (t) => {
                if (t.includes('prev') || t.includes('back') || t.includes('clear') || 
                    t.includes('reset') || t.includes('review') || t.includes('mark') || 
                    t.includes('cancel') || t.includes('close') || t.includes('exit') || t.includes('fullscreen')) {
                    return true;
                }
                // Reject final submission buttons unless specifically a "Save & Next"
                if ((t.includes('submit') || t.includes('final') || t.includes('finish') || t.includes('end exam') || t.includes('end test') || t.includes('complete')) && !t.includes('next')) {
                    return true;
                }
                return false;
            };

            // PASS 1: Strict Next / Save & Next matches
            for (const b of candidates) {
                if (!isVisible(b)) continue;
                const text = (b.innerText || b.value || b.getAttribute('title') || b.getAttribute('alt') || b.name || b.id || '').toLowerCase().trim();
                
                if (isStrictlyForbidden(text)) continue;

                if (text === 'next' || text.startsWith('next') || text.includes('next >') || 
                    text.includes('next >>') || text.includes('save & next') || text.includes('save and next') || 
                    text.includes('save & continue') || text.includes('save and continue') || 
                    text.includes('next question') || text.includes('btnnext') || text.includes('btnsavenext') ||
                    text.includes('forward') || text === 'save & forward') {
                    
                    b.focus();
                    b.click();
                    try { b.dispatchEvent(new Event('click', { bubbles: true })); } catch(e) {}
                    return { clicked: true, text: text, method: 'next_btn' };
                }
            }

            return { clicked: false };
        }""", target_q_num)

        if btn_info and btn_info.get('clicked'):
            next_el = await page.query_selector("#nextBtn, button:has-text('NEXT'), button:has-text('Next'), input[value*='Next' i]")
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
    print("🎯 Dynamic Solver Engine: Live Battle-Tested on Exam Portals")
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

                elements = screen_state.get('elements', [])
                q_context = screen_state.get('question_context', '')
                current_q_num = screen_state.get('current_q_num', 0)
                total_q_count = screen_state.get('total_q_count', 0)

                header_label = f"Question {current_q_num} of {total_q_count}" if (current_q_num and total_q_count) else f"Assessment Item {cycle}"

                if not elements:
                    print("[!] Waiting for active question elements in viewport...")
                    await asyncio.sleep(0.8)
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
                    tag_type = matched_target_info.get("type", "custom_option")
                    
                    if tag_type in ["radio", "checkbox", "custom_option"] or matched_target_info.get("tag") in ["input", "div", "li", "a", "button"]:
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
                        
                    elif tag_type == "select":
                        opt_val = str(plan.get("selected_option_text", "")) if plan else ""
                        await robust_select_dropdown(target_el, opt_val)
                        print(f"    [+] Selected dropdown option '{opt_val}' on [{target_idx}]")

                await asyncio.sleep(random.uniform(0.4, 0.7))

                # Snapshot old context before advancing
                old_context_snippet = (q_context or '')[:80]
                next_target_q = (current_q_num + 1) if current_q_num > 0 else 0

                # 2. Advance strictly to the next question
                nav_success, current_mouse_x, current_mouse_y = await trigger_next_button(
                    page, current_mouse_x, current_mouse_y, target_q_num=next_target_q
                )

                if nav_success:
                    print(f"    [⏩ ADVANCING] Navigating to next assessment item...")
                    
                    # Resilient wait for page transition / next question render
                    for _ in range(18):
                        await asyncio.sleep(0.15)
                        try:
                            new_context = await page.evaluate("() => (document.querySelector('#questionText, .question-text')?.innerText || document.body.innerText || '').substring(0, 80)")
                            if new_context != old_context_snippet:
                                break
                        except Exception:
                            await asyncio.sleep(0.5)
                            break
                else:
                    # Final question reached (No next button exists, submit button is active)
                    print("\n" + "=" * 68)
                    print("🎯 [ASSESSMENT COMPLETE] All question items in active viewport resolved!")
                    print("🛡️  SAFETY SHIELD ACTIVE: 'Submit Exam' button preserved for manual review.")
                    print("👉  Control passed to human operator for final verification.")
                    print("=" * 68)
                    break

        except Exception as e:
            print(f"\n[X] Automation Notice: {str(e)}")
            print("[!] Ensure Chrome was started with --remote-debugging-port=9222.")

if __name__ == "__main__":
    asyncio.run(universal_destruction_engine())
