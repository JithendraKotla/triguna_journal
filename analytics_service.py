"""
analytics_service.py
Advanced Behavioral Analytics Engine for Triguna Journal.
Implements stability scoring, streak detection, GBI, drift detection,
stress spike detection, heatmap generation, and more.
"""
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from collections import Counter
import plotly.graph_objects as go
import plotly.express as px


# ──────────────────────────────────────────────
# 1. STABILITY SCORE
# ──────────────────────────────────────────────

def calculate_stability(data: list[dict]) -> dict:
    """
    Compute emotional stability as percentage of consecutive days
    where the dominant guna did NOT change.
    
    Args:
        data: list of dicts with keys 'date', 'guna', 'sattva', 'rajas', 'tamas'
    Returns:
        dict with stability_score (0–100), changes, total_days
    """
    if len(data) < 2:
        return {"stability_score": 100, "changes": 0, "total_days": len(data)}
    
    changes = sum(1 for i in range(1, len(data)) if data[i]["guna"] != data[i-1]["guna"])
    stability = round(100 * (1 - changes / (len(data) - 1)), 1)
    return {
        "stability_score": stability,
        "changes": changes,
        "total_days": len(data)
    }


# ──────────────────────────────────────────────
# 2. LONGEST STREAK
# ──────────────────────────────────────────────

def longest_streak(data: list[dict]) -> dict:
    """
    Find the longest consecutive streak for each guna.
    Returns current streak and longest streak per guna.
    """
    if not data:
        return {"Sattva": 0, "Rajas": 0, "Tamas": 0, "current": {"guna": None, "days": 0}}
    
    streaks = {"Sattva": 0, "Rajas": 0, "Tamas": 0}
    max_s = max_r = max_t = 0
    cur_count = 1
    cur_guna = data[0]["guna"]

    for i in range(1, len(data)):
        if data[i]["guna"] == cur_guna:
            cur_count += 1
        else:
            if cur_guna == "Sattva": max_s = max(max_s, cur_count)
            elif cur_guna == "Rajas": max_r = max(max_r, cur_count)
            else: max_t = max(max_t, cur_count)
            cur_guna = data[i]["guna"]
            cur_count = 1

    # Final streak
    if cur_guna == "Sattva": max_s = max(max_s, cur_count)
    elif cur_guna == "Rajas": max_r = max(max_r, cur_count)
    else: max_t = max(max_t, cur_count)

    # Current streak (from end of data)
    current_guna = data[-1]["guna"]
    current_count = 0
    for entry in reversed(data):
        if entry["guna"] == current_guna:
            current_count += 1
        else:
            break

    return {
        "Sattva": max_s,
        "Rajas": max_r,
        "Tamas": max_t,
        "current": {"guna": current_guna, "days": current_count}
    }


# ──────────────────────────────────────────────
# 3. GUNA BALANCE INDEX (GBI)
# ──────────────────────────────────────────────

def guna_balance_index(sattva: float, rajas: float, tamas: float) -> dict:
    """
    GBI = Sattva - (Rajas + Tamas) / 2
    Normalized to -100 to +100 range.
    
    Interpretation:
      +60 to +100 → Highly Balanced / Sattvic
       0 to +60   → Moderately Balanced
      -30 to 0    → Reactive / Restless
      -100 to -30 → Disturbed / Heavy State
    """
    raw = sattva - (rajas + tamas) / 2
    # Theoretical range: -100 to +100 (already in that range given sum=100)
    gbi = max(-100, min(100, raw))
    
    if gbi >= 60:
        label = "Highly Balanced"
        color = "#00d4aa"
        emoji = "🟢"
    elif gbi >= 0:
        label = "Moderately Balanced"
        color = "#f7c948"
        emoji = "🟡"
    elif gbi >= -30:
        label = "Reactive / Restless"
        color = "#ff7043"
        emoji = "🟠"
    else:
        label = "Disturbed State"
        color = "#e53935"
        emoji = "🔴"

    return {"gbi": round(gbi, 1), "label": label, "color": color, "emoji": emoji}


# ──────────────────────────────────────────────
# 4. STRESS SPIKE DETECTOR
# ──────────────────────────────────────────────

def detect_stress_spike(data: list[dict]) -> list[dict]:
    """
    Detect days where Rajas increased > 40% compared to previous day.
    Returns list of spike events with date and delta.
    """
    spikes = []
    for i in range(1, len(data)):
        prev_rajas = data[i-1]["rajas"]
        curr_rajas = data[i]["rajas"]
        if prev_rajas > 0:
            delta = ((curr_rajas - prev_rajas) / prev_rajas) * 100
            if delta >= 40:
                spikes.append({
                    "date": data[i]["date"],
                    "from": round(prev_rajas, 1),
                    "to": round(curr_rajas, 1),
                    "delta": round(delta, 1)
                })
    return spikes


# ──────────────────────────────────────────────
# 5. GUNA DRIFT DETECTOR
# ──────────────────────────────────────────────

def detect_drift(data: list[dict], window: int = 7) -> list[dict]:
    """
    Detect significant personality drift using 7-day moving average.
    Alert triggered when dominant guna shifts between consecutive windows.
    Returns list of drift events.
    """
    if len(data) < window * 2:
        return []
    
    alerts = []
    df = pd.DataFrame(data)
    df["sattva_ma"] = df["sattva"].rolling(window, min_periods=window).mean()
    df["rajas_ma"] = df["rajas"].rolling(window, min_periods=window).mean()
    df["tamas_ma"] = df["tamas"].rolling(window, min_periods=window).mean()

    prev_dominant = None
    for i, row in df.iterrows():
        if pd.isna(row["sattva_ma"]):
            continue
        vals = {"Sattva": row["sattva_ma"], "Rajas": row["rajas_ma"], "Tamas": row["tamas_ma"]}
        current_dominant = max(vals, key=vals.get)
        
        if prev_dominant and current_dominant != prev_dominant:
            alerts.append({
                "date": row["date"],
                "from": prev_dominant,
                "to": current_dominant,
                "message": f"⚠️ Personality shift: {prev_dominant} → {current_dominant} (7-day avg)"
            })
        prev_dominant = current_dominant

    return alerts[-3:] if alerts else []  # Return last 3 most recent


# ──────────────────────────────────────────────
# 6. MENTAL STABILITY VARIANCE
# ──────────────────────────────────────────────

def mental_stability_variance(data: list[dict]) -> dict:
    """
    Compute variance of sattva/rajas/tamas values over time.
    Low variance = stable state. High variance = volatile.
    Returns normalized stability index 0–100.
    """
    if len(data) < 3:
        return {"stability_index": 100, "variance": 0, "label": "Insufficient data"}
    
    s_var = np.var([d["sattva"] for d in data])
    r_var = np.var([d["rajas"] for d in data])
    t_var = np.var([d["tamas"] for d in data])
    
    avg_variance = (s_var + r_var + t_var) / 3
    # Max theoretical variance ~= 1666 (when values swing 0–100)
    stability_index = max(0, round(100 - (avg_variance / 500) * 100, 1))
    stability_index = min(100, stability_index)
    
    if stability_index >= 75:
        label = "Very Stable"
    elif stability_index >= 50:
        label = "Moderately Stable"
    elif stability_index >= 25:
        label = "Somewhat Volatile"
    else:
        label = "Highly Volatile"
    
    return {
        "stability_index": stability_index,
        "variance": round(avg_variance, 2),
        "label": label,
        "sattva_var": round(s_var, 2),
        "rajas_var": round(r_var, 2),
        "tamas_var": round(t_var, 2)
    }


# ──────────────────────────────────────────────
# 7. WEEKLY HEATMAP (GitHub-style)
# ──────────────────────────────────────────────

def build_weekly_heatmap(data: list[dict]) -> go.Figure:
    """
    Build a GitHub contribution-style weekly heatmap.
    X-axis: week number, Y-axis: day of week (Mon–Sun)
    Color: Sattva=green, Rajas=red, Tamas=purple, Empty=dark
    """
    if not data:
        return go.Figure()

    df = pd.DataFrame(data)
    df["datetime"] = pd.to_datetime(df["date"])
    df["week"] = df["datetime"].dt.isocalendar().week.astype(int)
    df["year"] = df["datetime"].dt.isocalendar().year.astype(int)
    df["dayofweek"] = df["datetime"].dt.dayofweek  # 0=Mon, 6=Sun
    df["year_week"] = df["year"].astype(str) + "-W" + df["week"].astype(str).str.zfill(2)

    # Create grid
    min_date = df["datetime"].min()
    max_date = df["datetime"].max()
    all_dates = pd.date_range(min_date, max_date)

    date_guna = {row["date"]: row["guna"] for _, row in df.iterrows()}
    date_sattva = {row["date"]: row["sattva"] for _, row in df.iterrows()}

    color_map = {"Sattva": "#00d4aa", "Rajas": "#ff4757", "Tamas": "#8b5cf6", None: "#1e2130"}

    # Build weekly grid
    weeks = sorted(df["year_week"].unique())
    days_labels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    z_colors = []
    hover_text = []
    for day in range(7):
        row_colors = []
        row_hover = []
        for week in weeks:
            year, w = week.split("-W")
            # Find the date for this week+day
            try:
                d = datetime.strptime(f"{year}-W{int(w):02d}-{day+1}", "%G-W%V-%u")
                d_str = d.strftime("%Y-%m-%d")
                guna = date_guna.get(d_str)
                val = date_sattva.get(d_str, 0) if guna else 0
                row_colors.append(val if guna else -1)
                row_hover.append(f"{d_str}<br>{guna or 'No entry'}" + (f"<br>Sattva: {date_sattva.get(d_str, 0):.0f}%" if guna else ""))
            except:
                row_colors.append(-1)
                row_hover.append("No entry")
        z_colors.append(row_colors)
        hover_text.append(row_hover)

    # Guna color per cell
    cell_colors = []
    for day in range(7):
        row = []
        for week in weeks:
            year, w = week.split("-W")
            try:
                d = datetime.strptime(f"{year}-W{int(w):02d}-{day+1}", "%G-W%V-%u")
                d_str = d.strftime("%Y-%m-%d")
                guna = date_guna.get(d_str)
                row.append(color_map[guna])
            except:
                row.append(color_map[None])
        cell_colors.append(row)

    fig = go.Figure()
    for day_idx in range(7):
        for week_idx, week in enumerate(weeks):
            color = cell_colors[day_idx][week_idx]
            fig.add_trace(go.Scatter(
                x=[week_idx], y=[day_idx],
                mode="markers",
                marker=dict(
                    symbol="square",
                    size=18,
                    color=color,
                    line=dict(color="#0d0f1a", width=2)
                ),
                hovertemplate=hover_text[day_idx][week_idx] + "<extra></extra>",
                showlegend=False
            ))

    fig.update_layout(
        title=dict(text="📅 Activity Heatmap", font=dict(size=16, color="#e0e0e0")),
        xaxis=dict(
            tickvals=list(range(len(weeks))),
            ticktext=[w.split("-W")[1] for w in weeks],
            title="Week",
            showgrid=False,
            color="#888"
        ),
        yaxis=dict(
            tickvals=list(range(7)),
            ticktext=days_labels,
            showgrid=False,
            color="#888"
        ),
        paper_bgcolor="#0d0f1a",
        plot_bgcolor="#0d0f1a",
        height=220,
        margin=dict(l=50, r=20, t=50, b=40),
        font=dict(color="#e0e0e0")
    )

    return fig


# ──────────────────────────────────────────────
# 8. TIME-OF-DAY ANALYSIS
# ──────────────────────────────────────────────

def time_of_day_analysis(data: list[dict]) -> dict:
    """
    Analyze guna patterns based on entry_time (morning/afternoon/evening/night).
    """
    buckets = {"morning": [], "afternoon": [], "evening": [], "night": []}
    
    for d in data:
        t = d.get("entry_time")
        if not t:
            continue
        try:
            hour = int(t.split(":")[0])
            if 5 <= hour < 12:
                buckets["morning"].append(d)
            elif 12 <= hour < 17:
                buckets["afternoon"].append(d)
            elif 17 <= hour < 21:
                buckets["evening"].append(d)
            else:
                buckets["night"].append(d)
        except:
            continue

    patterns = {}
    for period, entries in buckets.items():
        if entries:
            avg_s = np.mean([e["sattva"] for e in entries])
            avg_r = np.mean([e["rajas"] for e in entries])
            avg_t = np.mean([e["tamas"] for e in entries])
            dominant = max({"Sattva": avg_s, "Rajas": avg_r, "Tamas": avg_t}.items(), key=lambda x: x[1])
            patterns[period] = {
                "entries": len(entries),
                "sattva": round(avg_s, 1),
                "rajas": round(avg_r, 1),
                "tamas": round(avg_t, 1),
                "dominant": dominant[0]
            }

    return patterns


# ──────────────────────────────────────────────
# 9. PREDICTIVE MODEL (Moving Average Forecast)
# ──────────────────────────────────────────────

def predict_tomorrow(data: list[dict], window: int = 7) -> dict:
    """
    Predict tomorrow's guna distribution using exponential moving average.
    Falls back to simple moving average if insufficient data.
    """
    if len(data) < 3:
        return {"error": "Need at least 3 entries to predict"}
    
    recent = data[-min(window, len(data)):]
    
    # Exponential weights (more recent = higher weight)
    weights = np.exp(np.linspace(0, 1, len(recent)))
    weights /= weights.sum()
    
    s_pred = np.dot([d["sattva"] for d in recent], weights)
    r_pred = np.dot([d["rajas"] for d in recent], weights)
    t_pred = np.dot([d["tamas"] for d in recent], weights)
    
    # Normalize to 100
    total = s_pred + r_pred + t_pred
    s_pred = round((s_pred / total) * 100, 1)
    r_pred = round((r_pred / total) * 100, 1)
    t_pred = round(100 - s_pred - r_pred, 1)
    
    dominant = max([("Sattva", s_pred), ("Rajas", r_pred), ("Tamas", t_pred)], key=lambda x: x[1])
    
    # Confidence: inverse of recent variance
    variance = np.var([d["sattva"] for d in recent])
    confidence = max(30, round(100 - (variance / 400) * 100, 0))
    
    return {
        "Sattva": s_pred,
        "Rajas": r_pred,
        "Tamas": t_pred,
        "DominantGuna": dominant[0],
        "confidence": int(confidence),
        "method": "Exponential Moving Average",
        "based_on": len(recent)
    }


# ──────────────────────────────────────────────
# 10. GOAL RECOMMENDATION ENGINE
# ──────────────────────────────────────────────

def generate_recommendations(data: list[dict]) -> list[dict]:
    """
    Analyze patterns and generate intelligent recommendations.
    """
    if not data:
        return []
    
    recs = []
    recent = data[-14:] if len(data) >= 14 else data
    last7 = data[-7:] if len(data) >= 7 else data

    # Check Tamas > 50% for 7+ consecutive days
    tamas_dominant_streak = sum(1 for d in last7 if d["guna"] == "Tamas")
    if tamas_dominant_streak >= 5:
        recs.append({
            "type": "warning",
            "icon": "🌙",
            "title": "Tamas Pattern Detected",
            "message": "You've been in a Tamas-dominant state. Physical activity, early rising, and sunlight exposure can help restore Sattva.",
            "actions": ["Take a 20-min morning walk", "Sleep before 10 PM", "Avoid heavy meals at night", "Practice Surya Namaskar"]
        })

    # Check Sattva declining
    if len(data) >= 10:
        first_half_s = np.mean([d["sattva"] for d in data[-10:-5]])
        second_half_s = np.mean([d["sattva"] for d in data[-5:]])
        if second_half_s < first_half_s - 10:
            recs.append({
                "type": "caution",
                "icon": "⬇️",
                "title": "Sattva Declining",
                "message": f"Your Sattva dropped ~{(first_half_s - second_half_s):.0f}% over the last 10 days.",
                "actions": ["Add a 10-min meditation daily", "Read uplifting content", "Reduce social media", "Practice gratitude journaling"]
            })

    # Rajas spike check
    spikes = detect_stress_spike(recent)
    if spikes:
        recs.append({
            "type": "alert",
            "icon": "⚡",
            "title": "Stress Spikes Detected",
            "message": f"Detected {len(spikes)} sudden stress increase(s). Rajas imbalance can lead to burnout.",
            "actions": ["Try box breathing (4-4-4-4)", "Take scheduled breaks", "Limit caffeine after 2 PM", "Spend 15 mins in nature"]
        })

    # Positive reinforcement for Sattva streak
    sattva_streak = sum(1 for d in last7 if d["guna"] == "Sattva")
    if sattva_streak >= 5:
        recs.append({
            "type": "success",
            "icon": "🌟",
            "title": "Excellent Sattvic Streak!",
            "message": f"You've maintained Sattva dominance for {sattva_streak} of the last 7 days. Keep this momentum!",
            "actions": ["Continue your current routine", "Share your practice with others", "Set a new mindfulness goal"]
        })

    # Low variance (very stable)
    stability = mental_stability_variance(recent)
    if stability["stability_index"] >= 80:
        recs.append({
            "type": "info",
            "icon": "🧘",
            "title": "Remarkable Mental Stability",
            "message": f"Your mental state shows exceptional consistency (stability: {stability['stability_index']:.0f}%). This is a strong indicator of emotional maturity.",
            "actions": ["Consider deepening your meditation practice", "Explore advanced philosophical study"]
        })

    return recs[:4]  # Return top 4


# ──────────────────────────────────────────────
# 11. GAMIFICATION — BADGE SYSTEM
# ──────────────────────────────────────────────

def evaluate_badges(data: list[dict], total_entries: int) -> list[dict]:
    """
    Evaluate which badges the user has earned based on their journal data.
    Returns list of earned badge dicts.
    """
    badges = []
    all_badges = [
        {"id": "first_entry",     "name": "First Step",        "icon": "🌱", "desc": "Created your first journal entry",    "threshold": 1},
        {"id": "week_streak",     "name": "7-Day Warrior",      "icon": "🔥", "desc": "Journaled 7 days consecutively",      "threshold": 7},
        {"id": "month_streak",    "name": "30-Entry Scholar",   "icon": "📚", "desc": "Completed 30 journal entries",        "threshold": 30},
        {"id": "sattva_streak",   "name": "Sattvic Soul",       "icon": "✨", "desc": "Sattva dominant for 5+ days in a row", "threshold": 5},
        {"id": "century",         "name": "Century Club",       "icon": "💯", "desc": "100 journal entries milestone",       "threshold": 100},
        {"id": "balanced_mind",   "name": "Balanced Mind",      "icon": "⚖️", "desc": "GBI > 50 for 7 consecutive entries",  "threshold": 7},
    ]

    streaks = longest_streak(data) if data else {}

    for badge in all_badges:
        earned = False
        if badge["id"] == "first_entry" and total_entries >= 1:
            earned = True
        elif badge["id"] == "week_streak":
            earned = streaks.get("current", {}).get("days", 0) >= 7 or any(
                streaks.get(g, 0) >= 7 for g in ["Sattva", "Rajas", "Tamas"]
            )
        elif badge["id"] == "month_streak" and total_entries >= 30:
            earned = True
        elif badge["id"] == "sattva_streak" and streaks.get("Sattva", 0) >= 5:
            earned = True
        elif badge["id"] == "century" and total_entries >= 100:
            earned = True
        elif badge["id"] == "balanced_mind":
            if len(data) >= 7:
                last7 = data[-7:]
                high_gbi = all(guna_balance_index(d["sattva"], d["rajas"], d["tamas"])["gbi"] > 20 for d in last7)
                earned = high_gbi

        badges.append({**badge, "earned": earned})

    return badges


# ──────────────────────────────────────────────
# 12. CORRELATION ENGINE
# ──────────────────────────────────────────────

def compute_correlations(journal_data: list[dict], lifestyle_data: list[dict]) -> dict:
    """
    Compute Pearson correlation between lifestyle factors and guna values.
    """
    if not journal_data or not lifestyle_data:
        return {}
    
    # Merge on date
    j_dict = {d["date"]: d for d in journal_data}
    merged = []
    for ls in lifestyle_data:
        if ls["date"] in j_dict:
            merged.append({**j_dict[ls["date"]], **ls})
    
    if len(merged) < 5:
        return {"error": "Need at least 5 matched days for correlation analysis"}
    
    df = pd.DataFrame(merged)
    factors = ["sleep_hours", "exercise_minutes", "screen_time", "meditation_minutes"]
    gunas = ["sattva", "rajas", "tamas"]
    
    results = {}
    for factor in factors:
        if factor not in df.columns:
            continue
        col = df[factor].dropna()
        if len(col) < 3:
            continue
        results[factor] = {}
        for guna in gunas:
            try:
                # Align indices
                valid_idx = df[factor].dropna().index.intersection(df[guna].dropna().index)
                if len(valid_idx) < 3:
                    continue
                corr = df.loc[valid_idx, factor].corr(df.loc[valid_idx, guna])
                results[factor][guna] = round(corr, 3)
            except:
                pass
    
    return results


# ──────────────────────────────────────────────
# 13. YEARLY SUMMARY
# ──────────────────────────────────────────────

def yearly_summary(data: list[dict]) -> dict:
    """
    Compute per-month averages and dominant gunas for radar + bar charts.
    """
    if not data:
        return {}
    
    df = pd.DataFrame(data)
    df["month"] = pd.to_datetime(df["date"]).dt.month
    df["month_name"] = pd.to_datetime(df["date"]).dt.strftime("%b")
    
    monthly = df.groupby(["month", "month_name"]).agg(
        sattva=("sattva", "mean"),
        rajas=("rajas", "mean"),
        tamas=("tamas", "mean"),
        entries=("guna", "count")
    ).reset_index().sort_values("month")

    result = {
        "months": monthly["month_name"].tolist(),
        "sattva": [round(v, 1) for v in monthly["sattva"]],
        "rajas": [round(v, 1) for v in monthly["rajas"]],
        "tamas": [round(v, 1) for v in monthly["tamas"]],
        "entries": monthly["entries"].tolist(),
        "overall": {
            "sattva": round(df["sattva"].mean(), 1),
            "rajas": round(df["rajas"].mean(), 1),
            "tamas": round(df["tamas"].mean(), 1)
        }
    }
    return result


# ──────────────────────────────────────────────
# 14. MASTER ANALYTICS REPORT
# ──────────────────────────────────────────────

def full_analytics_report(data: list[dict]) -> dict:
    """
    Run all analytics and return structured report dictionary.
    """
    if not data:
        return {}
    
    report = {
        "stability": calculate_stability(data),
        "streaks": longest_streak(data),
        "stress_spikes": detect_stress_spike(data),
        "drift_alerts": detect_drift(data),
        "variance": mental_stability_variance(data),
        "recommendations": generate_recommendations(data),
        "prediction": predict_tomorrow(data)
    }
    
    if data:
        latest = data[-1]
        report["gbi"] = guna_balance_index(latest["sattva"], latest["rajas"], latest["tamas"])
    
    return report
