# ==========================================
# DRL (Decision & Reasoning Layer)
# Food Delivery Agentic System
# ==========================================

from typing import Dict
import random
import datetime
import json
import sys

# -----------------------------
# 🧾 MENU DATABASE (LOCAL)
# -----------------------------
MENU = {
    "pizza": {"price": 10, "prep_time": 15},
    "burger": {"price": 7, "prep_time": 10},
    "pasta": {"price": 9, "prep_time": 12},
    "salad": {"price": 6, "prep_time": 8},
    "sushi": {"price": 12, "prep_time": 18}
}

DELIVERY_BASE_TIME = 20  # minutes


# -----------------------------
# 🧍 STEP 1: CUSTOMER INTENT
# -----------------------------
def generate_intent(user_input: str) -> Dict:
    """
    Extract structured intent from raw user input.
    (Simple rule-based parsing for local execution)
    """
    user_input = user_input.lower()

    items = []
    for food in MENU.keys():
        if food in user_input:
            items.append(food)

    if not items:
        items = ["pizza"]  # default fallback

    intent = {
        "goal": "order_food",
        "items": items,
        "preferences": {
            "spice_level": "medium" if "spicy" in user_input else "normal"
        },
        "constraints": {
            "delivery": "fast" if "fast" in user_input else "standard"
        }
    }

    return intent


# -----------------------------
# 🧑‍🍳 STEP 2: WAITER PLANNING
# -----------------------------
def create_plan(intent: Dict) -> Dict:
    """
    Convert intent into execution plan
    """
    items = intent["items"]

    plan = {
        "tasks": [],
        "estimated_cost": 0,
        "estimated_time": 0
    }

    for item in items:
        if item in MENU:
            plan["tasks"].append(f"Prepare {item}")
            plan["estimated_cost"] += MENU[item]["price"]
            plan["estimated_time"] += MENU[item]["prep_time"]

    # Add delivery time
    plan["estimated_time"] += DELIVERY_BASE_TIME

    return plan


# -----------------------------
# 📦 STEP 3: ORDER EXECUTION
# -----------------------------
def execute_order(plan: Dict) -> Dict:
    """
    Simulate order execution
    """
    order_id = f"ORD{random.randint(1000,9999)}"

    confirmation = {
        "order_id": order_id,
        "status": "confirmed",
        "tasks": plan["tasks"],
        "total_cost": plan["estimated_cost"],
        "estimated_delivery_time": f"{plan['estimated_time']} minutes",
        "timestamp": str(datetime.datetime.now())
    }

    return confirmation


# -----------------------------
# 🎯 MASTER PIPELINE
# -----------------------------
def run_agentic_pipeline(user_input: str) -> Dict:
    """
    Full pipeline execution:
    Customer → Waiter → Order
    """
    intent = generate_intent(user_input)
    plan = create_plan(intent)
    result = execute_order(plan)

    return {
        "intent": intent,
        "plan": plan,
        "result": result
    }


def is_streamlit_context() -> bool:
    """
    Detect whether this file is being executed by Streamlit.
    """
    try:
        from streamlit.runtime.scriptrunner import get_script_run_ctx
        return get_script_run_ctx() is not None
    except Exception:
        return False


def run_streamlit_app() -> None:
    """
    Render an attractive Streamlit UI for the DRL pipeline.
    """
    import streamlit as st

    st.set_page_config(page_title="Food Delivery DRL", page_icon="🍽️", layout="wide")
    st.markdown(
        """
        <style>
            .stApp {
                background: linear-gradient(130deg, #fff8ee 0%, #fff1e0 40%, #ffe7d3 100%);
            }
            .hero {
                background: radial-gradient(circle at top right, #ffb36a, #ff8f70 45%, #ff6b6b 100%);
                color: #1f1f1f;
                border-radius: 20px;
                padding: 24px;
                margin-bottom: 18px;
                box-shadow: 0 10px 26px rgba(255, 113, 80, 0.25);
            }
            .hero h1 {
                margin: 0;
                font-size: 2rem;
                letter-spacing: 0.3px;
            }
            .hero p {
                margin: 8px 0 0 0;
                font-size: 1rem;
            }
            .section-title {
                font-size: 1.2rem;
                font-weight: 700;
                margin-bottom: 8px;
            }
            .card {
                background: #ffffffcc;
                border: 1px solid #ffd4b8;
                border-radius: 16px;
                padding: 16px;
                margin-top: 10px;
                box-shadow: 0 6px 16px rgba(215, 95, 53, 0.12);
            }
            .chip {
                display: inline-block;
                padding: 6px 10px;
                margin: 4px 6px 0 0;
                border-radius: 999px;
                background: #ffe8d4;
                border: 1px solid #ffc89f;
                font-size: 0.9rem;
            }
            .line {
                margin: 6px 0;
                font-size: 1rem;
            }
            .order-ok {
                background: #ebfff2;
                border: 1px solid #b6f0c5;
                color: #115a2b;
                border-radius: 14px;
                padding: 12px;
                margin-top: 10px;
                font-weight: 600;
            }
            .muted {
                color: #5b4a42;
                font-size: 0.95rem;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="hero">
            <h1>Food Delivery Decision Engine</h1>
            <p>Type a customer request and get a clean, human-friendly order summary.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    left, right = st.columns([1.1, 1], gap="large")

    with left:
        st.markdown('<div class="section-title">Customer Order</div>', unsafe_allow_html=True)
        st.markdown('<div class="muted">Create your order below. The waiter view updates instantly.</div>', unsafe_allow_html=True)
        customer_name = st.text_input("Customer name", value="Guest")
        selected_items = st.multiselect(
            "Choose items",
            options=list(MENU.keys()),
            default=["pizza"]
        )

        quantities = {}
        if selected_items:
            qcols = st.columns(2)
            for idx, item in enumerate(selected_items):
                with qcols[idx % 2]:
                    quantities[item] = st.number_input(
                        f"{item.title()} quantity",
                        min_value=1,
                        max_value=10,
                        value=1,
                        step=1,
                        key=f"qty_{item}"
                    )
        else:
            st.info("Pick at least one item to continue.")

        spice_level = st.selectbox("Spice preference", ["normal", "medium"])
        fast_delivery = st.toggle("Fast delivery", value=True)
        customer_note = st.text_area("Extra note (optional)", placeholder="No onions, extra sauce, etc.")

    expanded_items = []
    for item, qty in quantities.items():
        expanded_items.extend([item] * int(qty))

    if not expanded_items:
        expanded_items = ["pizza"]

    intent = {
        "goal": "order_food",
        "items": expanded_items,
        "preferences": {"spice_level": spice_level},
        "constraints": {"delivery": "fast" if fast_delivery else "standard"}
    }
    plan = create_plan(intent)
    result = execute_order(plan)

    output = {
        "intent": intent,
        "plan": plan,
        "result": result,
        "customer_name": customer_name,
        "customer_note": customer_note
    }

    with right:
        st.markdown('<div class="section-title">Waiter Desk</div>', unsafe_allow_html=True)
        st.markdown('<div class="muted">Live order summary and kitchen-ready confirmation.</div>', unsafe_allow_html=True)

        pretty_items = []
        for item, qty in quantities.items():
            pretty_items.append(f"<span class=\"chip\">{item.title()} x{qty}</span>")
        items_html = "".join(pretty_items) if pretty_items else '<span class="chip">Pizza x1</span>'

        delivery_note = "Priority" if fast_delivery else "Standard"
        tasks = [task.replace("Prepare ", "").title() for task in plan["tasks"]]
        tasks_text = ", ".join(tasks)

        st.markdown(
            f"""
            <div class="card">
                <h3>Order Overview</h3>
                <div class="line">Customer: <b>{customer_name}</b></div>
                <div class="line">Items:</div>
                <div>{items_html}</div>
                <div class="line">Spice level: <b>{spice_level.title()}</b></div>
                <div class="line">Delivery: <b>{delivery_note}</b></div>
            </div>
            """,
            unsafe_allow_html=True
        )

        a, b, c = st.columns(3)
        a.metric("Total Cost", f"${plan['estimated_cost']}")
        b.metric("Delivery Time", result["estimated_delivery_time"])
        c.metric("Items Count", str(len(intent["items"])))

        st.markdown(
            f"""
            <div class="card">
                <h3>Kitchen Instruction</h3>
                <div class="line">Prepare: <b>{tasks_text}</b></div>
                <div class="line">Special note: <b>{customer_note if customer_note.strip() else 'No special note'}</b></div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="card">
                <h3>Confirmation</h3>
                <div class="order-ok">Order {result['order_id']} is confirmed and in progress.</div>
                <div class="line">Expected arrival: <b>{result['estimated_delivery_time']}</b></div>
                <div class="line">Status: <b>{result['status'].title()}</b></div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with open("drl_output.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    st.caption("Order data is auto-saved to drl_output.json")


def main() -> None:
    """
    CLI entry point for local runs.
    Accepts an optional user query from command line arguments.
    """
    query = " ".join(sys.argv[1:]).strip() or "I want pizza and sushi, make it fast"
    output = run_agentic_pipeline(query)

    print("INTENT:\n", output["intent"], flush=True)
    print("\nPLAN:\n", output["plan"], flush=True)
    print("\nRESULT:\n", output["result"], flush=True)

    # Also persist the latest output for environments where terminal output is hidden.
    with open("drl_output.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    print("\nSaved output to drl_output.json", flush=True)


# -----------------------------
# 🧪 TEST (optional)
# -----------------------------
if __name__ == "__main__":
    if is_streamlit_context():
        run_streamlit_app()
    else:
        main()