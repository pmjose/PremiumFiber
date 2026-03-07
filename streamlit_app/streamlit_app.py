import streamlit as st
from textwrap import dedent

try:
    from snowflake.snowpark.context import get_active_session
    session = get_active_session()
except:
    from snowflake.snowpark import Session
    session = Session.builder.config('connection_name', 'default').create()

# ---------------------------------------------------------------------------
# CSS faithfully mirroring PremiumFiber brand
# ---------------------------------------------------------------------------
PREMIUMFIBER_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&display=swap');

/* ── PremiumFiber brand tokens ──────────────────────────────────────── */
:root {
    --mf-blue:        #00A0E3;
    --mf-navy:        #003366;
    --mf-navy-dark:   #001a33;
    --mf-orange:      #FF6B00;
    --mf-orange-hover:#e55d00;
    --mf-dark:        #1a1a2e;
    --mf-light:       #f8f9fa;
    --mf-gray:        #6c757d;
    --mf-border:      #dee2e6;
    --mf-success:     #28a745;
    --mf-danger:      #dc3545;
    --mf-grad-hero:   linear-gradient(135deg, #003366 0%, #001a33 60%, #000d1a 100%);
    --mf-grad-blue:   linear-gradient(135deg, #00A0E3 0%, #003366 100%);
    --mf-grad-card:   linear-gradient(135deg, #00A0E3 0%, #0077b3 100%);
    --mf-grad-recommended: linear-gradient(135deg, #003366 0%, #001a33 100%);
    --mf-shadow-sm:   0 2px 8px rgba(0,0,0,0.08);
    --mf-shadow-md:   0 5px 20px rgba(0,0,0,0.10);
    --mf-shadow-lg:   0 10px 40px rgba(0,0,0,0.15);
    --mf-radius:      16px;
    --mf-radius-sm:   10px;
    --mf-radius-pill:  50px;
}

/* ── Global reset ──────────────────────────────────────────────────── */
html, body, [class*="st-"] {
    font-family: 'Poppins', sans-serif !important;
}

/* Hide Streamlit sidebar collapse controls */
[data-testid="stSidebarCollapseButton"],
[data-testid="collapsedControl"] {
    display: none !important;
}

.stApp {
    background: #f0f2f6;
}

/* Hide Streamlit default header / footer */
header[data-testid="stHeader"] { background: transparent; }
footer { visibility: hidden; }

/* ── Sidebar ───────────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: var(--mf-grad-hero) !important;
    border-right: none;
    overflow-x: hidden;
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h1,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h3,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stRadio label {
    color: #ffffff !important;
}

[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
    color: #ffffff !important;
    background: rgba(255,255,255,0.07);
    border-radius: var(--mf-radius-sm);
    padding: 12px 16px;
    margin: 4px 0;
    transition: all 0.25s ease;
    border: 1px solid rgba(255,255,255,0.06);
    width: 100% !important;
    min-height: 52px;
    box-sizing: border-box;
    display: flex;
    align-items: center;
}

[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label p {
    color: #ffffff !important;
    white-space: normal !important;
    overflow: visible !important;
    text-overflow: clip !important;
    margin: 0 !important;
}

[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {
    background: rgba(0,160,227,0.25);
    border-color: rgba(0,160,227,0.4);
}

[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.12) !important;
}

/* ── Buttons (PremiumFiber orange CTA style) ────────────────────────── */
.stButton > button {
    background: var(--mf-orange) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: var(--mf-radius-pill) !important;
    padding: 12px 32px !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.3px;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(255,107,0,0.3) !important;
}

.stButton > button:hover {
    background: var(--mf-orange-hover) !important;
    transform: translateY(-2px);
    box-shadow: 0 6px 25px rgba(255,107,0,0.45) !important;
}

/* ── Navbar / top bar ──────────────────────────────────────────────── */
.mf-topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: #ffffff;
    padding: 12px 30px;
    border-radius: var(--mf-radius);
    box-shadow: var(--mf-shadow-sm);
    margin-bottom: 24px;
}

.mf-topbar-logo {
    display: flex;
    align-items: center;
    gap: 12px;
}

.mf-topbar-logo img {
    height: 40px;
    border-radius: 10px;
}

.mf-topbar-brand {
    font-size: 1.35rem;
    font-weight: 800;
    color: var(--mf-navy);
    letter-spacing: 0.5px;
}

.mf-topbar-brand span {
    color: var(--mf-blue);
}

.mf-topbar-nav {
    display: flex;
    gap: 24px;
    align-items: center;
}

.mf-topbar-nav a {
    color: var(--mf-navy);
    text-decoration: none;
    font-size: 0.9rem;
    font-weight: 500;
    transition: color 0.2s;
}

.mf-topbar-nav a:hover {
    color: var(--mf-blue);
}

.mf-topbar-phone {
    background: var(--mf-blue);
    color: #fff;
    padding: 8px 20px;
    border-radius: var(--mf-radius-pill);
    font-weight: 600;
    font-size: 0.85rem;
    text-decoration: none;
    transition: background 0.2s;
}

.mf-topbar-phone:hover { background: var(--mf-navy); }

/* ── Hero section (PremiumFiber dark gradient hero) ──────────────────── */
.mf-hero {
    background: var(--mf-grad-hero);
    border-radius: var(--mf-radius);
    padding: 50px 40px;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
    box-shadow: var(--mf-shadow-lg);
}

.mf-hero::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -20%;
    width: 500px;
    height: 500px;
    background: radial-gradient(circle, rgba(0,160,227,0.15) 0%, transparent 70%);
    border-radius: 50%;
}

.mf-hero::after {
    content: '';
    position: absolute;
    bottom: -30%;
    left: -10%;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(0,160,227,0.1) 0%, transparent 70%);
    border-radius: 50%;
}

.mf-hero-content {
    position: relative;
    z-index: 2;
}

.mf-hero h1 {
    color: #ffffff;
    font-size: 2.6rem;
    font-weight: 800;
    margin: 0 0 8px 0;
    line-height: 1.15;
    text-shadow: 0 2px 4px rgba(0,0,0,0.2);
}

.mf-hero h1 span {
    color: var(--mf-blue);
}

.mf-hero p {
    color: rgba(255,255,255,0.8);
    font-size: 1.1rem;
    font-weight: 300;
    margin: 0;
    max-width: 600px;
}

.mf-hero-badge {
    display: inline-block;
    background: var(--mf-orange);
    color: #fff;
    padding: 6px 18px;
    border-radius: var(--mf-radius-pill);
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 16px;
}

/* ── Section headings ──────────────────────────────────────────────── */
.mf-section-title {
    text-align: center;
    margin-bottom: 40px;
}

.mf-section-title h2 {
    color: var(--mf-navy);
    font-size: 2rem;
    font-weight: 700;
    margin: 0 0 8px 0;
}

.mf-section-title p {
    color: var(--mf-gray);
    font-size: 1rem;
    font-weight: 400;
}

.mf-section-title .mf-title-accent {
    display: inline-block;
    width: 60px;
    height: 4px;
    background: var(--mf-blue);
    border-radius: 2px;
    margin-bottom: 16px;
}

/* ── Plan cards (PremiumFiber pricing cards) ─────────────────────────── */
.mf-plans-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap: 24px;
    margin-bottom: 40px;
}

.mf-plan-card {
    background: #ffffff;
    border-radius: var(--mf-radius);
    padding: 32px 24px;
    text-align: center;
    box-shadow: var(--mf-shadow-md);
    border: 2px solid transparent;
    transition: all 0.35s ease;
    position: relative;
    overflow: hidden;
}

.mf-plan-card:hover {
    transform: translateY(-8px);
    box-shadow: var(--mf-shadow-lg);
    border-color: var(--mf-blue);
}

.mf-plan-card.recommended {
    background: var(--mf-grad-recommended);
    color: #ffffff;
    border-color: var(--mf-blue);
    transform: scale(1.03);
}

.mf-plan-card.recommended:hover {
    transform: scale(1.03) translateY(-8px);
}

.mf-plan-card .badge-recommended {
    position: absolute;
    top: 0;
    left: 50%;
    transform: translateX(-50%);
    background: var(--mf-orange);
    color: #fff;
    padding: 6px 24px;
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    border-radius: 0 0 10px 10px;
}

.mf-plan-card .speed-promo {
    font-size: 0.8rem;
    color: var(--mf-gray);
    font-weight: 400;
    margin-bottom: 4px;
}

.mf-plan-card.recommended .speed-promo {
    color: rgba(255,255,255,0.6);
}

.mf-plan-card .speed-main {
    font-size: 2.2rem;
    font-weight: 800;
    color: var(--mf-navy);
    margin: 4px 0;
    line-height: 1.1;
}

.mf-plan-card.recommended .speed-main {
    color: #ffffff;
}

.mf-plan-card .speed-unit {
    font-size: 0.85rem;
    font-weight: 400;
    color: var(--mf-gray);
}

.mf-plan-card.recommended .speed-unit {
    color: rgba(255,255,255,0.7);
}

.mf-plan-card .fiber-label {
    display: inline-block;
    background: rgba(0,160,227,0.1);
    color: var(--mf-blue);
    padding: 4px 14px;
    border-radius: var(--mf-radius-pill);
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin: 12px 0;
}

.mf-plan-card.recommended .fiber-label {
    background: rgba(0,160,227,0.25);
    color: #ffffff;
}

.mf-plan-card .plan-features {
    text-align: left;
    margin: 16px 0;
    padding: 0;
    list-style: none;
    font-size: 0.85rem;
    color: var(--mf-gray);
}

.mf-plan-card.recommended .plan-features {
    color: rgba(255,255,255,0.8);
}

.mf-plan-card .plan-features li {
    padding: 4px 0;
    padding-left: 20px;
    position: relative;
}

.mf-plan-card .plan-features li::before {
    content: '✓';
    position: absolute;
    left: 0;
    color: var(--mf-blue);
    font-weight: 700;
}

.mf-plan-card.recommended .plan-features li::before {
    color: var(--mf-orange);
}

.mf-plan-card .plan-divider {
    border: none;
    height: 1px;
    background: var(--mf-border);
    margin: 16px 0;
}

.mf-plan-card.recommended .plan-divider {
    background: rgba(255,255,255,0.15);
}

.mf-plan-card .plan-price {
    margin: 16px 0 4px;
}

.mf-plan-card .price-currency {
    font-size: 1rem;
    font-weight: 600;
    color: var(--mf-navy);
    vertical-align: top;
}

.mf-plan-card.recommended .price-currency {
    color: #ffffff;
}

.mf-plan-card .price-amount {
    font-size: 2.8rem;
    font-weight: 800;
    color: var(--mf-navy);
    line-height: 1;
}

.mf-plan-card.recommended .price-amount {
    color: #ffffff;
}

.mf-plan-card .price-decimal {
    font-size: 1.2rem;
    font-weight: 600;
    color: var(--mf-navy);
    vertical-align: top;
}

.mf-plan-card.recommended .price-decimal {
    color: #ffffff;
}

.mf-plan-card .price-period {
    display: block;
    font-size: 0.75rem;
    color: var(--mf-gray);
    margin-top: 4px;
}

.mf-plan-card.recommended .price-period {
    color: rgba(255,255,255,0.6);
}

.mf-plan-card .plan-cta {
    display: inline-block;
    background: var(--mf-orange);
    color: #ffffff;
    padding: 12px 32px;
    border-radius: var(--mf-radius-pill);
    font-weight: 600;
    font-size: 0.9rem;
    text-decoration: none;
    margin-top: 16px;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(255,107,0,0.3);
}

.mf-plan-card .plan-cta:hover {
    background: var(--mf-orange-hover);
    transform: translateY(-2px);
    box-shadow: 0 6px 25px rgba(255,107,0,0.45);
}

.mf-plan-card.recommended .plan-cta {
    background: #ffffff;
    color: var(--mf-navy);
}

.mf-plan-card.recommended .plan-cta:hover {
    background: var(--mf-light);
}

.mf-plan-note {
    text-align: center;
    font-size: 0.8rem;
    color: var(--mf-gray);
    margin-top: 8px;
    margin-bottom: 40px;
}

/* ── Benefits section (4-column benefits) ────────────────────────────── */
.mf-benefits-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 24px;
    margin-bottom: 40px;
}

.mf-benefit-card {
    background: #ffffff;
    border-radius: var(--mf-radius);
    padding: 32px 24px;
    text-align: center;
    box-shadow: var(--mf-shadow-sm);
    transition: all 0.3s ease;
    border-top: 4px solid var(--mf-blue);
}

.mf-benefit-card:hover {
    transform: translateY(-6px);
    box-shadow: var(--mf-shadow-md);
}

.mf-benefit-icon {
    font-size: 2.5rem;
    margin-bottom: 16px;
    display: inline-block;
    width: 70px;
    height: 70px;
    line-height: 70px;
    border-radius: 50%;
    background: rgba(0,160,227,0.1);
}

.mf-benefit-card h3 {
    color: var(--mf-navy);
    font-size: 1.1rem;
    font-weight: 700;
    margin: 0 0 8px 0;
}

.mf-benefit-card p {
    color: var(--mf-gray);
    font-size: 0.88rem;
    font-weight: 400;
    line-height: 1.6;
    margin: 0;
}

/* ── Ookla recognition section ─────────────────────────────────────── */
.mf-ookla {
    background: var(--mf-grad-hero);
    border-radius: var(--mf-radius);
    padding: 48px 40px;
    margin-bottom: 32px;
    color: #ffffff;
    text-align: center;
    position: relative;
    overflow: hidden;
}

.mf-ookla::before {
    content: '';
    position: absolute;
    top: -40%;
    right: -15%;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(0,160,227,0.12) 0%, transparent 70%);
    border-radius: 50%;
}

.mf-ookla h3 {
    color: var(--mf-blue);
    font-size: 0.9rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin: 0 0 12px 0;
}

.mf-ookla h2 {
    color: #ffffff;
    font-size: 1.8rem;
    font-weight: 700;
    margin: 0 0 16px 0;
    max-width: 700px;
    margin-left: auto;
    margin-right: auto;
    line-height: 1.3;
}

.mf-ookla p {
    color: rgba(255,255,255,0.75);
    font-size: 0.9rem;
    line-height: 1.7;
    max-width: 750px;
    margin: 0 auto 16px;
}

.mf-ookla-badges {
    display: flex;
    justify-content: center;
    gap: 32px;
    margin: 24px 0;
    flex-wrap: wrap;
}

.mf-ookla-badge {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: var(--mf-radius-sm);
    padding: 20px 28px;
    text-align: center;
    min-width: 180px;
}

.mf-ookla-badge .badge-icon {
    font-size: 2rem;
    margin-bottom: 8px;
}

.mf-ookla-badge .badge-title {
    font-size: 0.85rem;
    font-weight: 600;
    color: #ffffff;
    display: block;
}

.mf-ookla-badge .badge-sub {
    font-size: 0.7rem;
    color: rgba(255,255,255,0.5);
    display: block;
}

.mf-ookla-cta {
    display: inline-block;
    background: var(--mf-orange);
    color: #fff;
    padding: 14px 36px;
    border-radius: var(--mf-radius-pill);
    font-weight: 700;
    font-size: 0.95rem;
    text-decoration: none;
    margin-top: 24px;
    transition: all 0.3s;
    box-shadow: 0 4px 15px rgba(255,107,0,0.3);
}

.mf-ookla-cta:hover {
    background: var(--mf-orange-hover);
    transform: translateY(-2px);
}

/* ── Comparison section (numbered steps) ────────────────────────────── */
.mf-comparison {
    margin-bottom: 40px;
}

.mf-comparison-item {
    display: flex;
    gap: 24px;
    background: #ffffff;
    border-radius: var(--mf-radius);
    padding: 28px;
    margin-bottom: 16px;
    box-shadow: var(--mf-shadow-sm);
    align-items: flex-start;
    transition: all 0.3s ease;
    border-left: 4px solid var(--mf-blue);
}

.mf-comparison-item:hover {
    box-shadow: var(--mf-shadow-md);
    transform: translateX(4px);
}

.mf-comparison-num {
    flex-shrink: 0;
    width: 50px;
    height: 50px;
    background: var(--mf-grad-blue);
    color: #fff;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.2rem;
    font-weight: 800;
}

.mf-comparison-body h3 {
    color: var(--mf-navy);
    font-size: 1.15rem;
    font-weight: 700;
    margin: 0 0 4px 0;
}

.mf-comparison-body .comp-subtitle {
    color: var(--mf-blue);
    font-size: 0.8rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 8px;
    display: block;
}

.mf-comparison-body p {
    color: var(--mf-gray);
    font-size: 0.88rem;
    line-height: 1.6;
    margin: 0;
}

/* ── Dashboard metric cards ────────────────────────────────────────── */
.mf-metrics-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 20px;
    margin-bottom: 32px;
}

.mf-metric-card {
    background: #ffffff;
    border-radius: var(--mf-radius);
    padding: 24px;
    box-shadow: var(--mf-shadow-sm);
    border-left: 4px solid var(--mf-blue);
    transition: all 0.3s ease;
}

.mf-metric-card:hover {
    transform: translateY(-4px);
    box-shadow: var(--mf-shadow-md);
}

.mf-metric-card .metric-icon {
    font-size: 1.5rem;
    margin-bottom: 8px;
}

.mf-metric-card .metric-value {
    font-size: 2rem;
    font-weight: 800;
    color: var(--mf-navy);
    line-height: 1.2;
}

.mf-metric-card .metric-label {
    font-size: 0.8rem;
    color: var(--mf-gray);
    text-transform: uppercase;
    letter-spacing: 0.8px;
    font-weight: 500;
    margin-top: 4px;
}

.mf-metric-card .metric-delta {
    font-size: 0.8rem;
    font-weight: 600;
    margin-top: 8px;
}

.mf-metric-card .metric-delta.positive { color: var(--mf-success); }
.mf-metric-card .metric-delta.negative { color: var(--mf-danger); }

/* ── Empty / placeholder states ────────────────────────────────────── */
.mf-empty {
    text-align: center;
    padding: 60px 40px;
    background: #ffffff;
    border-radius: var(--mf-radius);
    box-shadow: var(--mf-shadow-sm);
}

.mf-empty-icon {
    font-size: 3.5rem;
    margin-bottom: 16px;
}

.mf-empty h3 {
    color: var(--mf-navy);
    font-size: 1.3rem;
    font-weight: 700;
    margin: 0 0 8px 0;
}

.mf-empty p {
    color: var(--mf-gray);
    font-size: 0.95rem;
    margin: 0;
}

/* ── Sidebar logo block ────────────────────────────────────────────── */
.mf-sidebar-logo {
    text-align: center;
    padding: 20px 12px;
    margin-bottom: 16px;
    border-bottom: 1px solid rgba(255,255,255,0.1);
}

.mf-sidebar-logo img {
    max-width: 120px;
    border-radius: 14px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
}

.mf-sidebar-brand {
    color: #ffffff;
    font-size: 1.6rem;
    font-weight: 800;
    margin-top: 10px;
    letter-spacing: 1px;
}

.mf-sidebar-brand span {
    color: var(--mf-blue);
}

.mf-sidebar-tagline {
    color: rgba(255,255,255,0.55);
    font-size: 0.75rem;
    font-weight: 400;
    letter-spacing: 0.5px;
}

@keyframes mfTickerSlide {
    0% { transform: translateX(0%); }
    100% { transform: translateX(-50%); }
}
.mf-sidebar-ticker {
    margin: 4px 6px 12px;
    border: 1px solid rgba(255,255,255,0.16);
    border-radius: 999px;
    background: linear-gradient(135deg, rgba(255,255,255,0.08), rgba(255,255,255,0.04));
    overflow: hidden;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.08);
}
.mf-sidebar-ticker-track {
    display: inline-flex;
    align-items: center;
    gap: 28px;
    min-width: max-content;
    white-space: nowrap;
    padding: 7px 0;
    animation: mfTickerSlide 20s linear infinite;
}
.mf-sidebar-ticker-item {
    color: #FDE68A;
    font-size: 0.66rem;
    font-weight: 600;
    letter-spacing: 0.25px;
}
.mf-sidebar-ticker-item .dot {
    color: #F59E0B;
    margin-right: 6px;
}

.mf-sidebar-badge {
    display: inline-block;
    background: var(--mf-orange);
    color: #fff;
    padding: 4px 14px;
    border-radius: var(--mf-radius-pill);
    font-size: 0.65rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.5px;
}

.mf-sidebar-version {
    color: rgba(255,255,255,0.35);
    font-size: 0.68rem;
    text-align: center;
    margin-top: 24px;
}

.mf-menu-header {
    color: var(--mf-blue) !important;
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin: 20px 0 8px 0;
    padding-left: 4px;
}

/* ── Footer ────────────────────────────────────────────────────────── */
.mf-footer {
    background: var(--mf-grad-hero);
    border-radius: var(--mf-radius);
    padding: 40px 30px;
    margin-top: 48px;
    color: rgba(255,255,255,0.7);
    text-align: center;
}

.mf-footer-brand {
    font-size: 1.5rem;
    font-weight: 800;
    color: #fff;
    margin-bottom: 8px;
}

.mf-footer-brand span {
    color: var(--mf-blue);
}

.mf-footer-links {
    display: flex;
    justify-content: center;
    gap: 24px;
    flex-wrap: wrap;
    margin: 16px 0;
}

.mf-footer-links a {
    color: rgba(255,255,255,0.6);
    text-decoration: none;
    font-size: 0.85rem;
    font-weight: 400;
    transition: color 0.2s;
}

.mf-footer-links a:hover { color: var(--mf-blue); }

.mf-footer-contact {
    margin: 20px 0 0;
    display: flex;
    justify-content: center;
    gap: 32px;
    flex-wrap: wrap;
}

.mf-footer-contact-item {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 0.85rem;
    color: rgba(255,255,255,0.7);
}

.mf-footer-contact-item span.icon {
    font-size: 1.1rem;
}

.mf-footer-divider {
    border: none;
    height: 1px;
    background: rgba(255,255,255,0.1);
    margin: 24px 0 16px;
}

.mf-footer-copy {
    font-size: 0.75rem;
    color: rgba(255,255,255,0.4);
}

/* ── Tabs override ─────────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: transparent;
}

.stTabs [data-baseweb="tab"] {
    background: rgba(0,160,227,0.08);
    border-radius: var(--mf-radius-pill);
    padding: 8px 20px;
    font-weight: 500;
    color: var(--mf-navy);
}

.stTabs [aria-selected="true"] {
    background: var(--mf-blue) !important;
    color: #ffffff !important;
}

/* ── Intro page – Snowflake-style animated dashboard ───────────────── */

/* Keyframe animations */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(30px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes fadeInDown {
    from { opacity: 0; transform: translateY(-20px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes fadeInLeft {
    from { opacity: 0; transform: translateX(-30px); }
    to   { opacity: 1; transform: translateX(0); }
}
@keyframes fadeInRight {
    from { opacity: 0; transform: translateX(30px); }
    to   { opacity: 1; transform: translateX(0); }
}
@keyframes scaleIn {
    from { opacity: 0; transform: scale(0.85); }
    to   { opacity: 1; transform: scale(1); }
}
@keyframes pulseGlow {
    0%, 100% { box-shadow: 0 0 20px rgba(0,160,227,0.15); }
    50%      { box-shadow: 0 0 40px rgba(0,160,227,0.35); }
}
@keyframes float {
    0%, 100% { transform: translateY(0); }
    50%      { transform: translateY(-8px); }
}
@keyframes countUp {
    from { opacity: 0; transform: translateY(10px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes spinSlow {
    from { transform: rotate(0deg); }
    to   { transform: rotate(360deg); }
}
@keyframes slideInScale {
    from { opacity: 0; transform: scale(0.9) translateY(20px); }
    to   { opacity: 1; transform: scale(1) translateY(0); }
}
@keyframes shimmer {
    0%   { background-position: -200% 0; }
    100% { background-position: 200% 0; }
}
@keyframes borderPulse {
    0%, 100% { border-color: rgba(0,160,227,0.2); }
    50%      { border-color: rgba(0,160,227,0.5); }
}

/* ── Intro: Hero hub card ──────────────────────────────────────────── */
.intro-hub {
    background: linear-gradient(135deg, #f0faff 0%, #e6f7ff 50%, #f0f4ff 100%);
    border: 2px solid rgba(0,160,227,0.15);
    border-radius: var(--mf-radius);
    padding: 48px 32px 40px;
    text-align: center;
    margin-bottom: 32px;
    animation: fadeInDown 0.7s ease-out;
    position: relative;
    overflow: hidden;
}
.intro-hub::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 4px;
    background: linear-gradient(90deg, var(--mf-blue), var(--mf-navy), var(--mf-blue));
    background-size: 200% 100%;
    animation: shimmer 3s linear infinite;
}
.intro-hub-title {
    font-size: 1.5rem;
    font-weight: 800;
    color: var(--mf-navy);
    margin: 0 0 4px;
}
.intro-hub-title span { color: var(--mf-blue); }
.intro-hub-sub {
    font-size: 0.85rem;
    color: var(--mf-gray);
    margin-bottom: 28px;
}

/* Hub diagram — circular center + orbiting nodes */
.hub-diagram {
    position: relative;
    width: 260px;
    height: 260px;
    margin: 0 auto 28px;
    animation: scaleIn 0.8s ease-out 0.2s both;
}
.hub-center {
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    width: 90px; height: 90px;
    border-radius: 50%;
    background: var(--mf-grad-blue);
    display: flex; align-items: center; justify-content: center;
    font-size: 2rem;
    color: #fff;
    box-shadow: 0 8px 30px rgba(0,160,227,0.35);
    animation: pulseGlow 3s ease-in-out infinite;
    z-index: 2;
}
.hub-ring {
    position: absolute;
    top: 50%; left: 50%;
    width: 220px; height: 220px;
    transform: translate(-50%, -50%);
    border: 2px dashed rgba(0,160,227,0.2);
    border-radius: 50%;
    animation: spinSlow 60s linear infinite;
}
.hub-node {
    position: absolute;
    width: 52px; height: 52px;
    border-radius: 50%;
    background: #fff;
    border: 2px solid rgba(0,160,227,0.25);
    display: flex; align-items: center; justify-content: center;
    font-size: 0.65rem; font-weight: 600; color: var(--mf-navy);
    box-shadow: var(--mf-shadow-sm);
    transition: all 0.3s ease;
    flex-direction: column;
    line-height: 1.1;
    text-align: center;
}
.hub-node:hover {
    border-color: var(--mf-blue);
    transform: scale(1.12);
    box-shadow: 0 4px 16px rgba(0,160,227,0.25);
}
.hub-node .hub-icon { font-size: 1rem; margin-bottom: 2px; }
/* Positions around circle (6 nodes at 60° intervals) */
.hub-node:nth-child(3) { top: -10px; left: 50%; transform: translateX(-50%); }
.hub-node:nth-child(4) { top: 18%;  right: -10px; }
.hub-node:nth-child(5) { bottom: 18%; right: -10px; }
.hub-node:nth-child(6) { bottom: -10px; left: 50%; transform: translateX(-50%); }
.hub-node:nth-child(7) { bottom: 18%; left: -10px; }
.hub-node:nth-child(8) { top: 18%;  left: -10px; }

/* Hub stats row */
.hub-stats {
    display: flex;
    justify-content: center;
    gap: 40px;
    flex-wrap: wrap;
}
.hub-stat {
    text-align: center;
    animation: countUp 0.6s ease-out both;
}
.hub-stat:nth-child(1) { animation-delay: 0.5s; }
.hub-stat:nth-child(2) { animation-delay: 0.7s; }
.hub-stat:nth-child(3) { animation-delay: 0.9s; }
.hub-stat:nth-child(4) { animation-delay: 1.1s; }
.hub-stat-value {
    font-size: 1.6rem;
    font-weight: 800;
    color: var(--mf-blue);
}
.hub-stat-label {
    font-size: 0.65rem;
    color: var(--mf-gray);
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* ── Intro: section labels ─────────────────────────────────────────── */
.intro-label {
    font-size: 0.75rem;
    font-weight: 600;
    color: var(--mf-blue);
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 16px;
    animation: fadeInLeft 0.5s ease-out both;
}

/* ── Intro: stat cards row ─────────────────────────────────────────── */
.intro-stats {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
    margin-bottom: 32px;
}
.intro-stat-card {
    background: #fff;
    border: 2px solid rgba(0,160,227,0.12);
    border-radius: var(--mf-radius);
    padding: 24px 16px;
    text-align: center;
    animation: slideInScale 0.6s ease-out both;
    transition: all 0.3s ease;
}
.intro-stat-card:nth-child(1) { animation-delay: 0.3s; }
.intro-stat-card:nth-child(2) { animation-delay: 0.45s; }
.intro-stat-card:nth-child(3) { animation-delay: 0.6s; }
.intro-stat-card:nth-child(4) { animation-delay: 0.75s; }
.intro-stat-card:hover {
    border-color: var(--mf-blue);
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(0,160,227,0.12);
}
.intro-stat-val {
    font-size: 2rem;
    font-weight: 800;
    color: var(--mf-navy);
    line-height: 1.1;
}
.intro-stat-val span { color: var(--mf-blue); }
.intro-stat-lbl {
    font-size: 0.72rem;
    color: var(--mf-gray);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-top: 4px;
}

/* ── Intro: 3-column pillar cards ──────────────────────────────────── */
.intro-pillars {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 24px;
    margin-bottom: 32px;
}
.intro-pillar {
    background: #fff;
    border: 2px solid rgba(0,160,227,0.10);
    border-radius: var(--mf-radius);
    padding: 32px 24px;
    text-align: center;
    animation: fadeInUp 0.6s ease-out both;
    transition: all 0.35s ease;
}
.intro-pillar:nth-child(1) { animation-delay: 0.2s; }
.intro-pillar:nth-child(2) { animation-delay: 0.4s; }
.intro-pillar:nth-child(3) { animation-delay: 0.6s; }
.intro-pillar:hover {
    border-color: var(--mf-blue);
    transform: translateY(-6px);
    box-shadow: var(--mf-shadow-md);
}
.intro-pillar .pillar-icon {
    font-size: 2rem;
    margin-bottom: 12px;
    animation: float 4s ease-in-out infinite;
}
.intro-pillar:nth-child(2) .pillar-icon { animation-delay: 0.5s; }
.intro-pillar:nth-child(3) .pillar-icon { animation-delay: 1s; }
.intro-pillar h3 {
    color: var(--mf-navy);
    font-size: 1.05rem;
    font-weight: 700;
    margin: 0 0 8px;
}
.intro-pillar p {
    color: var(--mf-gray);
    font-size: 0.8rem;
    line-height: 1.6;
    margin: 0;
}

/* ── Intro: logo / trust bar ───────────────────────────────────────── */
.intro-trust {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 48px;
    flex-wrap: wrap;
    margin-bottom: 32px;
    padding: 28px 24px;
    background: #fff;
    border: 2px solid rgba(0,160,227,0.08);
    border-radius: var(--mf-radius);
    animation: fadeInUp 0.7s ease-out 0.3s both;
}
.intro-trust-logo {
    font-size: 1.3rem;
    font-weight: 700;
    color: var(--mf-navy);
    opacity: 0.6;
    transition: opacity 0.3s;
    display: flex;
    align-items: center;
    gap: 8px;
}
.intro-trust-logo:hover { opacity: 1; }

/* ── Intro: 2×2 KPI benefit cards ──────────────────────────────────── */
.intro-kpi-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 20px;
    margin-bottom: 32px;
}
.intro-kpi {
    border-radius: var(--mf-radius);
    padding: 28px 24px;
    animation: slideInScale 0.6s ease-out both;
    transition: all 0.3s ease;
    border: 2px solid transparent;
}
.intro-kpi:nth-child(1) { background: linear-gradient(135deg, #e8f8f0 0%, #f0fdf4 100%); border-color: rgba(40,167,69,0.15); animation-delay: 0.2s; }
.intro-kpi:nth-child(2) { background: linear-gradient(135deg, #e6f7ff 0%, #f0faff 100%); border-color: rgba(0,160,227,0.15); animation-delay: 0.35s; }
.intro-kpi:nth-child(3) { background: linear-gradient(135deg, #fff8e6 0%, #fffbf0 100%); border-color: rgba(255,107,0,0.15); animation-delay: 0.5s; }
.intro-kpi:nth-child(4) { background: linear-gradient(135deg, #f0e6ff 0%, #f8f0ff 100%); border-color: rgba(111,66,193,0.15); animation-delay: 0.65s; }
.intro-kpi:hover {
    transform: translateY(-4px);
    box-shadow: var(--mf-shadow-md);
}
.intro-kpi h4 {
    font-size: 1rem;
    font-weight: 700;
    margin: 0 0 12px;
}
.intro-kpi:nth-child(1) h4 { color: #1b7a3d; }
.intro-kpi:nth-child(2) h4 { color: #0077b3; }
.intro-kpi:nth-child(3) h4 { color: #cc5500; }
.intro-kpi:nth-child(4) h4 { color: #6f42c1; }
.intro-kpi ul {
    list-style: none;
    padding: 0;
    margin: 0;
    font-size: 0.82rem;
    color: #555;
    line-height: 1.8;
}
.intro-kpi ul li::before {
    content: '•';
    font-weight: 700;
    margin-right: 8px;
}
.intro-kpi:nth-child(1) ul li::before { color: #28a745; }
.intro-kpi:nth-child(2) ul li::before { color: var(--mf-blue); }
.intro-kpi:nth-child(3) ul li::before { color: var(--mf-orange); }
.intro-kpi:nth-child(4) ul li::before { color: #6f42c1; }
.intro-kpi ul li strong { font-weight: 600; color: #333; }

/* ── Intro: solution cards grid ────────────────────────────────────── */
.intro-solutions {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
    margin-bottom: 16px;
}
.intro-sol {
    background: #fff;
    border: 2px solid rgba(0,160,227,0.10);
    border-radius: var(--mf-radius-sm);
    padding: 22px 20px;
    animation: fadeInUp 0.5s ease-out both;
    transition: all 0.3s ease;
}
.intro-sol:nth-child(1) { animation-delay: 0.1s; }
.intro-sol:nth-child(2) { animation-delay: 0.2s; }
.intro-sol:nth-child(3) { animation-delay: 0.3s; }
.intro-sol:nth-child(4) { animation-delay: 0.4s; }
.intro-sol:nth-child(5) { animation-delay: 0.5s; }
.intro-sol:nth-child(6) { animation-delay: 0.6s; }
.intro-sol:hover {
    border-color: var(--mf-blue);
    transform: translateY(-4px);
    box-shadow: 0 6px 20px rgba(0,160,227,0.10);
}
.intro-sol h5 {
    color: var(--mf-blue);
    font-size: 0.88rem;
    font-weight: 700;
    margin: 0 0 4px;
}
.intro-sol p {
    color: var(--mf-gray);
    font-size: 0.75rem;
    margin: 0;
    line-height: 1.5;
}

/* ── Responsive tweaks ─────────────────────────────────────────────── */
@media (max-width: 768px) {
    .mf-hero { padding: 32px 24px; }
    .mf-hero h1 { font-size: 1.8rem; }
    .mf-plans-grid { grid-template-columns: 1fr; }
    .mf-benefits-grid { grid-template-columns: 1fr 1fr; }
    .mf-ookla { padding: 32px 20px; }
    .mf-ookla h2 { font-size: 1.4rem; }
    .mf-topbar { flex-direction: column; gap: 12px; }
    .mf-comparison-item { flex-direction: column; gap: 16px; }
    .intro-stats { grid-template-columns: repeat(2, 1fr); }
    .intro-pillars { grid-template-columns: 1fr; }
    .intro-kpi-grid { grid-template-columns: 1fr; }
    .intro-solutions { grid-template-columns: 1fr; }
}
</style>
"""

st.set_page_config(
    page_title="PremiumFiber | FTTH Network - Dashboard",
    page_icon="https://premiumfiber.es/wp-content/uploads/PF_horizontal_blanco.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(PREMIUMFIBER_CSS, unsafe_allow_html=True)

LOGO_URL = "https://premiumfiber.es/wp-content/uploads/PF_horizontal_blanco.png"
WA_LINK = "https://api.whatsapp.com/send?phone=34911234567&text=Hola%20PremiumFiber%2C%20quiero%20informaci%C3%B3n%20sobre%20los%20planes%20de%20fibra."

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown(dedent("""
        <div class="mf-sidebar-ticker">
            <div class="mf-sidebar-ticker-track">
                <span class="mf-sidebar-ticker-item"><span class="dot">●</span>Budget churn risk: 78%</span>
                <span class="mf-sidebar-ticker-item"><span class="dot">●</span>€2.4M ARR at risk</span>
                <span class="mf-sidebar-ticker-item"><span class="dot">●</span>Málaga NPS below target</span>
                <span class="mf-sidebar-ticker-item"><span class="dot">●</span>MTTR still above 45 min goal</span>
                <span class="mf-sidebar-ticker-item"><span class="dot">●</span>Budget churn risk: 78%</span>
                <span class="mf-sidebar-ticker-item"><span class="dot">●</span>€2.4M ARR at risk</span>
                <span class="mf-sidebar-ticker-item"><span class="dot">●</span>Málaga NPS below target</span>
                <span class="mf-sidebar-ticker-item"><span class="dot">●</span>MTTR still above 45 min goal</span>
            </div>
        </div>
    """), unsafe_allow_html=True)

    st.markdown(dedent(f"""
        <div class="mf-sidebar-logo">
            <img src="{LOGO_URL}" alt="PremiumFiber">
            <div class="mf-sidebar-tagline">La red FTTH de España</div>
        </div>
    """), unsafe_allow_html=True)

    st.markdown('<p class="mf-menu-header">Dashboard</p>', unsafe_allow_html=True)

    menu_options = [
        "Intro",
        "JV Board View",
        "Tenant SLA",
        "Wholesale Commercial",
        "ESG & Energy",
        "Network Status",
        "Operations & Assets",
        "Data Sharing",
    ]

    selected_menu = st.radio(
        label="Menu",
        options=menu_options,
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown(dedent("""
        <div style="text-align:center; padding: 8px;">
            <span class="mf-sidebar-badge">XGS-PON</span>
        </div>
    """), unsafe_allow_html=True)

    st.markdown('<div class="mf-sidebar-version">v1.0.0 &middot; España &middot; Snowflake</div>', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Page: Intro — Executive Summary (from example.py)
# ---------------------------------------------------------------------------
if selected_menu == "Intro":

    # ── Hub & Spoke Banner with Floating Particles ─────────────────────
    st.markdown("""
<style>
@keyframes hub-pulse { 0%, 100% { transform: scale(1); box-shadow: 0 0 25px rgba(41,181,232,0.5); } 50% { transform: scale(1.08); box-shadow: 0 0 45px rgba(41,181,232,0.8); } }
@keyframes hub-float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-8px); } }
@keyframes hub-arrow { 0%, 100% { opacity: 0.4; transform: translateX(0); } 50% { opacity: 1; transform: translateX(5px); } }
@keyframes particle-drift {
    0% { transform: translateY(0) translateX(0) scale(1); opacity: 0; }
    10% { opacity: 0.8; }
    90% { opacity: 0.8; }
    100% { transform: translateY(-100px) translateX(30px) scale(0.5); opacity: 0; }
}
@keyframes sparkle { 0%, 100% { opacity: 0.3; transform: scale(0.8); } 50% { opacity: 1; transform: scale(1.2); } }
.hub-banner { background: linear-gradient(135deg, #F0F9FF 0%, #E0F2FE 100%); border-radius: 16px; padding: 2rem; margin-bottom: 2rem; position: relative; overflow: hidden; border: 1px solid #BAE6FD; }
.hub-particles { position: absolute; top: 0; left: 0; right: 0; bottom: 0; pointer-events: none; overflow: hidden; }
.hub-particle { position: absolute; width: 6px; height: 6px; background: #29B5E8; border-radius: 50%; animation: particle-drift 4s ease-out infinite; }
.hub-particle.small { width: 4px; height: 4px; background: rgba(41,181,232,0.6); }
.hub-sparkle { position: absolute; width: 8px; height: 8px; background: white; border-radius: 50%; animation: sparkle 2s ease-in-out infinite; }
.hub-title { text-align: center; color: #1B2A4E; font-size: 1.8rem; font-weight: 700; margin-bottom: 0.3rem; position: relative; z-index: 1; }
.hub-subtitle { text-align: center; color: #64748B; font-size: 0.85rem; margin-bottom: 1.5rem; position: relative; z-index: 1; }
.hub-content { display: flex; align-items: center; justify-content: center; gap: 0.8rem; position: relative; z-index: 1; flex-wrap: wrap; }
.hub-sources { display: flex; flex-direction: column; gap: 0.6rem; }
.hub-source { background: white; border-radius: 10px; padding: 0.7rem 1rem; display: flex; align-items: center; gap: 0.6rem; border: 1px solid #E2E8F0; box-shadow: 0 2px 4px rgba(0,0,0,0.05); animation: hub-float 3s ease-in-out infinite; }
.hub-source:nth-child(2) { animation-delay: 0.3s; }
.hub-source:nth-child(3) { animation-delay: 0.6s; }
.hub-source-icon { font-size: 1.3rem; }
.hub-source-label { color: #1B2A4E; font-size: 0.75rem; font-weight: 600; }
.hub-arrows { display: flex; flex-direction: column; gap: 1.2rem; padding: 0 0.5rem; }
.hub-arrow { color: #29B5E8; font-size: 1.2rem; animation: hub-arrow 1.5s ease-in-out infinite; }
.hub-arrow:nth-child(2) { animation-delay: 0.2s; }
.hub-arrow:nth-child(3) { animation-delay: 0.4s; }
.es-hub-center { background: linear-gradient(135deg, #29B5E8, #0EA5E9); border-radius: 50%; width: 120px; height: 120px; display: flex; flex-direction: column; align-items: center; justify-content: center; animation: hub-pulse 2s ease-in-out infinite; flex-shrink: 0; position: relative; }
.es-hub-center::after { content: ''; position: absolute; width: 140px; height: 140px; border: 2px solid rgba(41,181,232,0.3); border-radius: 50%; animation: hub-pulse 2s ease-in-out infinite 0.5s; }
.es-hub-center-icon { font-size: 2.5rem; }
.es-hub-center-label { color: white; font-size: 0.7rem; font-weight: 700; text-transform: uppercase; margin-top: 4px; }
.es-hub-stats { display: flex; justify-content: center; gap: 3rem; margin-top: 1.5rem; position: relative; z-index: 1; flex-wrap: wrap; }
.es-hub-stat { text-align: center; animation: hub-float 3s ease-in-out infinite; }
.es-hub-stat:nth-child(2) { animation-delay: 0.25s; }
.es-hub-stat:nth-child(3) { animation-delay: 0.5s; }
.es-hub-stat:nth-child(4) { animation-delay: 0.75s; }
.es-hub-stat-value { color: #29B5E8; font-size: 1.4rem; font-weight: 700; }
.es-hub-stat-label { color: #64748B; font-size: 0.65rem; text-transform: uppercase; }
@keyframes section-header-fade {
    0% { opacity: 0; transform: translateY(8px); }
    100% { opacity: 1; transform: translateY(0); }
}
@keyframes section-header-shimmer {
    0% { transform: translateX(-120%); opacity: 0; }
    25% { opacity: 1; }
    100% { transform: translateX(220%); opacity: 0; }
}
@keyframes section-header-pulse {
    0%, 100% { box-shadow: 0 0 0 0 rgba(41,181,232,0.32); }
    50% { box-shadow: 0 0 0 6px rgba(41,181,232,0); }
}
.section-header {
    position: relative;
    overflow: hidden;
    display: flex;
    align-items: center;
    gap: 0.55rem;
    font-size: 1.02rem;
    font-weight: 700;
    color: #1B2A4E;
    margin: 1.35rem 0 0.9rem;
    padding: 0.62rem 0.85rem;
    border: 1px solid #DBEAFE;
    border-radius: 12px;
    background: linear-gradient(135deg, #F8FAFF 0%, #EEF5FF 100%);
    animation: section-header-fade 0.45s ease-out both;
}
.section-header::before {
    content: "";
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: linear-gradient(135deg, #29B5E8 0%, #6366F1 100%);
    animation: section-header-pulse 2.2s ease-in-out infinite;
}
.section-header::after {
    content: "";
    position: absolute;
    top: 0;
    left: -30%;
    width: 28%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.85), transparent);
    animation: section-header-shimmer 2.8s ease-in-out infinite;
}
.eo-subtitle {
    position: relative;
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    margin: 0.15rem 0 0.55rem;
    font-size: 0.92rem;
    font-weight: 700;
    color: #1E3A8A;
    letter-spacing: 0.01em;
    animation: section-header-fade 0.35s ease-out both;
}
.eo-subtitle::before {
    content: "";
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: linear-gradient(135deg, #22C1EE 0%, #8B5CF6 100%);
    opacity: 0.95;
}
.metric-card { background: white; border: 1px solid #E5E7EB; border-radius: 12px; padding: 1.25rem; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
.metric-value { font-size: 1.8rem; font-weight: 700; }
.metric-label { font-size: 0.8rem; color: #6B7280; }
.architecture-box { background: white; border: 1px solid #E5E7EB; border-radius: 12px; padding: 1.5rem; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
.architecture-box h4 { color: #1B2A4E; margin-top: 0.5rem; }
.architecture-box p { color: #6B7280; font-size: 0.85rem; line-height: 1.6; }
.talking-point { background: white; border: 1px solid #E5E7EB; border-radius: 10px; padding: 1rem 1.2rem; margin-bottom: 0.5rem; color: #1B2A4E; font-size: 0.9rem; font-weight: 600; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
@keyframes arch-particle { 0% { left: 0%; opacity: 0; } 15% { opacity: 1; } 85% { opacity: 1; } 100% { left: 100%; opacity: 0; } }
@keyframes arch-pulse { 0%, 100% { transform: scale(1); box-shadow: 0 4px 15px rgba(41,181,232,0.3); } 50% { transform: scale(1.02); box-shadow: 0 6px 25px rgba(41,181,232,0.5); } }
@keyframes arch-glow { 0%, 100% { border-color: rgba(41,181,232,0.3); } 50% { border-color: rgba(41,181,232,0.8); } }
.arch-container { background: linear-gradient(180deg, #F8FAFC 0%, #EFF6FF 100%); border-radius: 16px; padding: 2rem; border: 2px solid #E5E7EB; }
.arch-row { display: flex; align-items: center; justify-content: center; gap: 1rem; margin: 1rem 0; flex-wrap: wrap; }
.arch-column { display: flex; flex-direction: column; gap: 0.6rem; min-width: 140px; }
.arch-box { background: white; border: 2px solid #E5E7EB; border-radius: 10px; padding: 0.6rem 1rem; display: flex; align-items: center; gap: 0.5rem; animation: arch-glow 3s ease-in-out infinite; transition: all 0.3s; }
.arch-box:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
.arch-box.source { border-left: 4px solid #F59E0B; }
.arch-box.output { border-left: 4px solid #10B981; }
.arch-icon { font-size: 1.2rem; }
.arch-label { font-size: 0.75rem; font-weight: 600; color: #1B2A4E; }
.arch-sublabel { font-size: 0.6rem; color: #6B7280; }
.arch-center { background: linear-gradient(135deg, #29B5E8 0%, #0EA5E9 100%); border-radius: 16px; padding: 1.5rem 2rem; animation: arch-pulse 3s ease-in-out infinite; min-width: 200px; }
.arch-center-title { color: white; font-size: 1.1rem; font-weight: 700; text-align: center; margin-bottom: 0.3rem; }
.arch-center-sub { color: rgba(255,255,255,0.8); font-size: 0.7rem; text-align: center; }
.arch-center-features { display: flex; flex-wrap: wrap; gap: 0.4rem; justify-content: center; margin-top: 0.8rem; }
.arch-feature { background: rgba(255,255,255,0.2); color: white; padding: 0.2rem 0.6rem; border-radius: 12px; font-size: 0.6rem; }
.arch-pipes { position: relative; width: 60px; height: 200px; }
.arch-pipe { position: absolute; width: 100%; height: 2px; background: linear-gradient(90deg, #F59E0B, #29B5E8); }
.arch-pipe.out { background: linear-gradient(90deg, #29B5E8, #10B981); }
.arch-dot { position: absolute; width: 8px; height: 8px; border-radius: 50%; top: -3px; background: #F59E0B; animation: arch-particle 2.5s linear infinite; }
.arch-pipe.out .arch-dot { background: #10B981; }
.arch-section-label { font-size: 0.65rem; text-transform: uppercase; letter-spacing: 1px; color: #6B7280; margin-bottom: 0.5rem; font-weight: 600; }
</style>
    """, unsafe_allow_html=True)

    # Hub banner HTML (single line to avoid indentation issues)
    st.markdown("""<div class="hub-banner"><div class="hub-particles"><div class="hub-particle" style="left: 10%; top: 80%; animation-delay: 0s;"></div><div class="hub-particle small" style="left: 20%; top: 70%; animation-delay: 0.5s;"></div><div class="hub-particle" style="left: 30%; top: 85%; animation-delay: 1s;"></div><div class="hub-particle small" style="left: 40%; top: 75%; animation-delay: 1.5s;"></div><div class="hub-particle" style="left: 50%; top: 90%; animation-delay: 2s;"></div><div class="hub-particle small" style="left: 60%; top: 80%; animation-delay: 2.5s;"></div><div class="hub-particle" style="left: 70%; top: 85%; animation-delay: 3s;"></div><div class="hub-particle small" style="left: 80%; top: 75%; animation-delay: 3.5s;"></div><div class="hub-particle" style="left: 90%; top: 80%; animation-delay: 0.8s;"></div><div class="hub-sparkle" style="left: 15%; top: 20%; animation-delay: 0s;"></div><div class="hub-sparkle" style="left: 85%; top: 30%; animation-delay: 1s;"></div><div class="hub-sparkle" style="left: 45%; top: 15%; animation-delay: 2s;"></div></div><div class="hub-title">❄️ Snowflake AI Data Cloud</div><div class="hub-subtitle">Breaking Down Data Silos in Real-Time</div><div class="hub-content"><div class="hub-sources"><div class="hub-source"><span class="hub-source-icon">📡</span><span class="hub-source-label">Network</span></div><div class="hub-source"><span class="hub-source-icon">⚙️</span><span class="hub-source-label">OSS/BSS</span></div><div class="hub-source"><span class="hub-source-icon">🏪</span><span class="hub-source-label">Marketplace</span></div></div><div class="hub-arrows"><span class="hub-arrow">→</span><span class="hub-arrow">→</span><span class="hub-arrow">→</span></div><div class="es-hub-center"><span class="es-hub-center-icon">❄️</span><span class="es-hub-center-label">Snowflake</span></div><div class="hub-arrows"><span class="hub-arrow">→</span><span class="hub-arrow">→</span><span class="hub-arrow">→</span></div><div class="hub-sources"><div class="hub-source"><span class="hub-source-icon">📊</span><span class="hub-source-label">Analytics</span></div><div class="hub-source"><span class="hub-source-icon">🤖</span><span class="hub-source-label">AI/ML</span></div><div class="hub-source"><span class="hub-source-icon">💡</span><span class="hub-source-label">Insights</span></div></div></div><div class="es-hub-stats"><div class="es-hub-stat"><div class="es-hub-stat-value">60%</div><div class="es-hub-stat-label">Faster Insights</div></div><div class="es-hub-stat"><div class="es-hub-stat-value">40%</div><div class="es-hub-stat-label">Cost Reduction</div></div><div class="es-hub-stat"><div class="es-hub-stat-value">100%</div><div class="es-hub-stat-label">Data Unified</div></div><div class="es-hub-stat"><div class="es-hub-stat-value">5x</div><div class="es-hub-stat-label">ROI</div></div></div></div>""", unsafe_allow_html=True)

    # ── About Snowflake ────────────────────────────────────────────────
    st.markdown('<div class="section-header">About Snowflake</div>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    metrics = [
        ("11,000+", "Enterprise Customers"),
        ("$3.5B+", "Annual Revenue"),
        ("~50%", "Fortune 500 Companies"),
        ("#1", "Data Cloud Platform"),
    ]
    for col, (value, label) in zip([col1, col2, col3, col4], metrics):
        with col:
            st.markdown(f"""<div class="metric-card" style="text-align: center;"><div class="metric-value" style="color: #29B5E8;">{value}</div><div class="metric-label">{label}</div></div>""", unsafe_allow_html=True)

    # ── Why Snowflake for Telecom ──────────────────────────────────────
    st.markdown('<div class="section-header">Why Snowflake for Telecom</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""<div class="architecture-box" style="min-height: 220px;"><div style="font-size: 2rem; margin-bottom: 0.5rem;">🚀</div><h4>Bring Data & AI to Life</h4><p>Save time on building, configuring and tuning infrastructure with a single, fully managed platform. Streamline workflows, power business-critical use cases and uncover new commercial strategies.</p></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""<div class="architecture-box" style="min-height: 220px;"><div style="font-size: 2rem; margin-bottom: 0.5rem;">🔗</div><h4>Connected Ecosystem</h4><p>Connect with mobile network operators, content providers, network equipment providers, and top data solutions providers. Optimize network performance, enhance customer experiences and monetize services more effectively.</p></div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""<div class="architecture-box" style="min-height: 220px;"><div style="font-size: 2rem; margin-bottom: 0.5rem;">🔒</div><h4>Trusted Governance</h4><p>Govern and protect your data with best-in-class security. Use AI and large language models within Snowflake's security perimeter, with built-in policies, access controls and end-to-end observability.</p></div>""", unsafe_allow_html=True)

    # ── Leading Telcos Trust Snowflake ─────────────────────────────────
    st.markdown('<div class="section-header">Leading Telcos Trust Snowflake</div>', unsafe_allow_html=True)

    customers = [
        {"name": "AT&T", "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/31/AT%26T_logo_2016.svg/200px-AT%26T_logo_2016.svg.png"},
        {"name": "T-Mobile", "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/88/T-Mobile_US_Logo_2022_RGB_Magenta_on_Transparent.svg/500px-T-Mobile_US_Logo_2022_RGB_Magenta_on_Transparent.svg.png"},
        {"name": "Deutsche Telekom", "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Deutsche_Telekom_2022.svg/250px-Deutsche_Telekom_2022.svg.png"},
        {"name": "Vodafone", "logo": "https://upload.wikimedia.org/wikipedia/en/thumb/c/cc/Vodafone_2017_logo.svg/500px-Vodafone_2017_logo.svg.png"},
    ]
    cols = st.columns(4)
    for col, customer in zip(cols, customers):
        with col:
            st.markdown(f"""<div style="background: white; border: 1px solid #E5E7EB; border-radius: 12px; padding: 1.25rem; text-align: center; min-height: 100px; display: flex; flex-direction: column; justify-content: center; align-items: center;"><div style="height: 60px; display: flex; align-items: center; justify-content: center;"><img src="{customer['logo']}" alt="{customer['name']}" style="max-height: 50px; max-width: 120px; object-fit: contain;"></div></div>""", unsafe_allow_html=True)

    # ── Business Benefits & KPIs (animated) ──────────────────────────
    st.markdown("""<style>
@keyframes kpi-slide-up { from { opacity: 0; transform: translateY(24px); } to { opacity: 1; transform: translateY(0); } }
@keyframes kpi-border-glow { 0%,100% { border-color: rgba(0,0,0,0.06); } 50% { border-color: rgba(41,181,232,0.25); } }
@keyframes kpi-icon-bob { 0%,100% { transform: translateY(0) scale(1); } 50% { transform: translateY(-4px) scale(1.08); } }
@keyframes sol-fade { from { opacity: 0; transform: translateY(16px) scale(0.97); } to { opacity: 1; transform: translateY(0) scale(1); } }
.kpi-card { border-radius: 16px; padding: 1.6rem 1.5rem; border: 1.5px solid rgba(0,0,0,0.06); animation: kpi-slide-up 0.6s ease-out both, kpi-border-glow 4s ease-in-out infinite; transition: transform 0.3s ease, box-shadow 0.3s ease; position: relative; overflow: hidden; }
.kpi-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px; border-radius: 16px 16px 0 0; }
.kpi-card:hover { transform: translateY(-4px); box-shadow: 0 12px 32px rgba(0,0,0,0.08); }
.kpi-card.blue { background: linear-gradient(135deg, #EBF8FF 0%, #F0FAFF 100%); }
.kpi-card.blue::before { background: linear-gradient(90deg, #29B5E8, #0EA5E9); }
.kpi-card.green { background: linear-gradient(135deg, #D1FAE5 0%, #ECFDF5 100%); }
.kpi-card.green::before { background: linear-gradient(90deg, #10B981, #34D399); }
.kpi-card.amber { background: linear-gradient(135deg, #FEF3C7 0%, #FFFBEB 100%); }
.kpi-card.amber::before { background: linear-gradient(90deg, #F59E0B, #FBBF24); }
.kpi-card.purple { background: linear-gradient(135deg, #EDE9FE 0%, #F5F3FF 100%); }
.kpi-card.purple::before { background: linear-gradient(90deg, #8B5CF6, #A78BFA); }
.kpi-card .kpi-head { display: flex; align-items: center; gap: 10px; margin-bottom: 14px; }
.kpi-card .kpi-icon { font-size: 1.5rem; animation: kpi-icon-bob 3s ease-in-out infinite; }
.kpi-card .kpi-title { font-size: 1.05rem; font-weight: 700; color: #1B2A4E; }
.kpi-card ul { color: #374151; margin: 0; padding-left: 0; list-style: none; font-size: 0.88rem; line-height: 2; }
.kpi-card ul li { position: relative; padding-left: 18px; }
.kpi-card ul li::before { content: ''; position: absolute; left: 0; top: 50%; transform: translateY(-50%); width: 7px; height: 7px; border-radius: 50%; }
.kpi-card.blue ul li::before { background: #29B5E8; }
.kpi-card.green ul li::before { background: #10B981; }
.kpi-card.amber ul li::before { background: #F59E0B; }
.kpi-card.purple ul li::before { background: #8B5CF6; }
.kpi-card ul li strong { color: #1B2A4E; }
.kpi-card:nth-child(1) { animation-delay: 0.1s; }
.kpi-card:nth-child(2) { animation-delay: 0.2s; }
.sol-card { background: white; border: 1.5px solid #E5E7EB; border-radius: 14px; padding: 1.3rem 1.4rem; min-height: 80px; animation: sol-fade 0.5s ease-out both; transition: all 0.3s ease; position: relative; overflow: hidden; }
.sol-card::after { content: ''; position: absolute; bottom: 0; left: 0; width: 0; height: 2px; background: linear-gradient(90deg, #29B5E8, #0EA5E9); transition: width 0.4s ease; }
.sol-card:hover { border-color: #29B5E8; transform: translateY(-3px); box-shadow: 0 8px 24px rgba(41,181,232,0.10); }
.sol-card:hover::after { width: 100%; }
.sol-card .sol-icon { font-size: 1.6rem; margin-bottom: 8px; display: block; }
.sol-card .sol-title { font-size: 0.92rem; font-weight: 700; color: #1B2A4E; margin-bottom: 4px; }
.sol-card .sol-desc { font-size: 0.8rem; color: #6B7280; line-height: 1.5; }
</style>""", unsafe_allow_html=True)

    st.markdown('<div class="section-header">Business Benefits & KPIs</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""<div class="kpi-card blue"><div class="kpi-head"><span class="kpi-icon">💰</span><span class="kpi-title">Revenue & Growth</span></div><ul><li><strong>15-25%</strong> reduction in customer churn</li><li><strong>20-30%</strong> increase in upsell conversion</li><li><strong>10-15%</strong> ARPU improvement</li><li><strong>$10M+</strong> fraud prevention savings</li></ul></div>""", unsafe_allow_html=True)
        st.markdown("")
        st.markdown("""<div class="kpi-card amber"><div class="kpi-head"><span class="kpi-icon">⚡</span><span class="kpi-title">Operational Excellence</span></div><ul><li><strong>40-60%</strong> faster time-to-insight</li><li><strong>30%</strong> network ops cost reduction</li><li><strong>50%</strong> less data engineering effort</li><li><strong>80%</strong> faster reporting</li></ul></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""<div class="kpi-card green"><div class="kpi-head"><span class="kpi-icon">📈</span><span class="kpi-title">Customer Experience</span></div><ul><li><strong>+15 pts</strong> NPS improvement</li><li><strong>25%</strong> call center volume reduction</li><li><strong>Real-time</strong> network issue detection</li><li><strong>360°</strong> unified customer view</li></ul></div>""", unsafe_allow_html=True)
        st.markdown("")
        st.markdown("""<div class="kpi-card purple"><div class="kpi-head"><span class="kpi-icon">🔒</span><span class="kpi-title">Security & Governance</span></div><ul><li><strong>Single source</strong> of truth</li><li><strong>GDPR/CCPA</strong> compliance built-in</li><li><strong>Row/column</strong> level access control</li><li><strong>Full audit</strong> trail & lineage</li></ul></div>""", unsafe_allow_html=True)

    # ── Join the Connected Future of Telecom (animated) ────────────────
    st.markdown('<div class="section-header">Join the Connected Future of Telecom</div>', unsafe_allow_html=True)

    use_cases = [
        ("🔮", "Churn Prediction", "Identify at-risk customers with ML models"),
        ("📡", "Network Analytics", "Real-time performance monitoring"),
        ("💳", "Revenue Assurance", "Detect billing anomalies and leakage"),
        ("👤", "Customer 360", "Unified cross-channel customer view"),
        ("🛡️", "Fraud Detection", "AI-powered SIM swap detection"),
        ("📶", "5G Monetization", "Optimize 5G pricing and adoption"),
    ]
    cols = st.columns(3)
    for i, (icon, title, desc) in enumerate(use_cases):
        with cols[i % 3]:
            delay = round(0.1 + i * 0.1, 1)
            st.markdown(f"""<div class="sol-card" style="animation-delay: {delay}s;"><span class="sol-icon">{icon}</span><div class="sol-title">{title}</div><div class="sol-desc">{desc}</div></div>""", unsafe_allow_html=True)

    # ── Architecture Overview ──────────────────────────────────────────
    st.markdown('<div class="section-header">Architecture Overview</div>', unsafe_allow_html=True)

    st.markdown("""<div class="arch-container"><div class="arch-row"><div class="arch-column"><div class="arch-section-label">Data Sources</div><div class="arch-box source"><span class="arch-icon">📡</span><div><div class="arch-label">Network Ops</div><div class="arch-sublabel">Performance & Sites</div></div></div><div class="arch-box source"><span class="arch-icon">🚨</span><div><div class="arch-label">Network Alarms</div><div class="arch-sublabel">NOC Events</div></div></div><div class="arch-box source"><span class="arch-icon">📶</span><div><div class="arch-label">FTTH Access Data</div><div class="arch-sublabel">OLT and CPE Telemetry</div></div></div><div class="arch-box source"><span class="arch-icon">💳</span><div><div class="arch-label">Billing</div><div class="arch-sublabel">Revenue & Invoices</div></div></div><div class="arch-box source"><span class="arch-icon">👥</span><div><div class="arch-label">Subscribers</div><div class="arch-sublabel">Customer Records</div></div></div><div class="arch-box source"><span class="arch-icon">🎫</span><div><div class="arch-label">Support Tickets</div><div class="arch-sublabel">Contact Center</div></div></div><div class="arch-box source"><span class="arch-icon">📦</span><div><div class="arch-label">Orders</div><div class="arch-sublabel">Installations and ONTs</div></div></div><div class="arch-box source"><span class="arch-icon">🤝</span><div><div class="arch-label">Partners</div><div class="arch-sublabel">Channel & Retail</div></div></div><div class="arch-box source"><span class="arch-icon">📊</span><div><div class="arch-label">Market Intel</div><div class="arch-sublabel">Competitor Data</div></div></div><div class="arch-box source"><span class="arch-icon">📄</span><div><div class="arch-label">Documents</div><div class="arch-sublabel">Policies & Strategy</div></div></div></div><div class="arch-pipes" style="height: 340px;"><div class="arch-pipe" style="top: 6%;"><div class="arch-dot" style="animation-delay: 0s;"></div></div><div class="arch-pipe" style="top: 16%;"><div class="arch-dot" style="animation-delay: 0.25s;"></div></div><div class="arch-pipe" style="top: 26%;"><div class="arch-dot" style="animation-delay: 0.5s;"></div></div><div class="arch-pipe" style="top: 36%;"><div class="arch-dot" style="animation-delay: 0.75s;"></div></div><div class="arch-pipe" style="top: 46%;"><div class="arch-dot" style="animation-delay: 1s;"></div></div><div class="arch-pipe" style="top: 56%;"><div class="arch-dot" style="animation-delay: 1.25s;"></div></div><div class="arch-pipe" style="top: 66%;"><div class="arch-dot" style="animation-delay: 1.5s;"></div></div><div class="arch-pipe" style="top: 76%;"><div class="arch-dot" style="animation-delay: 1.75s;"></div></div><div class="arch-pipe" style="top: 86%;"><div class="arch-dot" style="animation-delay: 2s;"></div></div><div class="arch-pipe" style="top: 96%;"><div class="arch-dot" style="animation-delay: 2.25s;"></div></div></div><div class="arch-center"><div class="arch-center-title">❄️ Snowflake</div><div class="arch-center-sub">AI Data Cloud</div><div class="arch-center-features"><span class="arch-feature">Cortex AI</span><span class="arch-feature">ML Models</span><span class="arch-feature">Semantic Views</span><span class="arch-feature">Search</span><span class="arch-feature">Notebooks</span><span class="arch-feature">Streamlit</span></div></div><div class="arch-pipes" style="height: 340px;"><div class="arch-pipe out" style="top: 6%;"><div class="arch-dot" style="animation-delay: 0.1s;"></div></div><div class="arch-pipe out" style="top: 16%;"><div class="arch-dot" style="animation-delay: 0.35s;"></div></div><div class="arch-pipe out" style="top: 26%;"><div class="arch-dot" style="animation-delay: 0.6s;"></div></div><div class="arch-pipe out" style="top: 36%;"><div class="arch-dot" style="animation-delay: 0.85s;"></div></div><div class="arch-pipe out" style="top: 46%;"><div class="arch-dot" style="animation-delay: 1.1s;"></div></div><div class="arch-pipe out" style="top: 56%;"><div class="arch-dot" style="animation-delay: 1.35s;"></div></div><div class="arch-pipe out" style="top: 66%;"><div class="arch-dot" style="animation-delay: 1.6s;"></div></div><div class="arch-pipe out" style="top: 76%;"><div class="arch-dot" style="animation-delay: 1.85s;"></div></div><div class="arch-pipe out" style="top: 86%;"><div class="arch-dot" style="animation-delay: 2.1s;"></div></div><div class="arch-pipe out" style="top: 96%;"><div class="arch-dot" style="animation-delay: 2.35s;"></div></div></div><div class="arch-column"><div class="arch-section-label">Intelligence</div><div class="arch-box output"><span class="arch-icon">🧠</span><div><div class="arch-label">Snowflake Intelligence</div><div class="arch-sublabel">Natural Language</div></div></div><div class="arch-box output"><span class="arch-icon">📊</span><div><div class="arch-label">Dashboards</div><div class="arch-sublabel">32 Executive Views</div></div></div><div class="arch-box output"><span class="arch-icon">🔮</span><div><div class="arch-label">Churn Model</div><div class="arch-sublabel">ML Predictions</div></div></div><div class="arch-box output"><span class="arch-icon">📈</span><div><div class="arch-label">Upsell Model</div><div class="arch-sublabel">Propensity Scores</div></div></div><div class="arch-box output"><span class="arch-icon">🔍</span><div><div class="arch-label">Document Search</div><div class="arch-sublabel">7 Collections</div></div></div><div class="arch-box output"><span class="arch-icon">📋</span><div><div class="arch-label">Semantic Views</div><div class="arch-sublabel">34 Business Domains</div></div></div><div class="arch-box output"><span class="arch-icon">💡</span><div><div class="arch-label">Real-time Insights</div><div class="arch-sublabel">Live Analytics</div></div></div><div class="arch-box output"><span class="arch-icon">🎯</span><div><div class="arch-label">Analyst Tools</div><div class="arch-sublabel">41 AI Tools</div></div></div><div class="arch-box output"><span class="arch-icon">📱</span><div><div class="arch-label">Streamlit Apps</div><div class="arch-sublabel">Interactive UI</div></div></div><div class="arch-box output"><span class="arch-icon">📝</span><div><div class="arch-label">Notebooks</div><div class="arch-sublabel">Data Science</div></div></div></div></div></div>""", unsafe_allow_html=True)

    st.markdown("""<div style="text-align: center; margin-top: 2rem; padding: 1rem; color: #6B7280; font-size: 0.8rem;">Learn more at <a href="https://www.snowflake.com/en/solutions/industries/telecom/" target="_blank" style="color: #29B5E8;">snowflake.com/telecom</a></div>""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Page: Executive Overview
# ---------------------------------------------------------------------------
elif selected_menu == "Executive Overview":
    import pandas as pd
    import altair as alt
    import numpy as np

    EXEC_CHART_THEME = {
        "font": "Poppins, sans-serif",
        "title_color": "#0F172A",
        "label_color": "#334155",
        "grid_color": "#E2E8F0",
        "accent_blue": "#29B5E8",
        "accent_indigo": "#6366F1",
        "accent_green": "#10B981",
        "accent_amber": "#F59E0B",
        "accent_purple": "#8B5CF6",
        "accent_red": "#EF4444",
    }

    def style_exec_chart(chart: alt.Chart, height: int = 220) -> alt.Chart:
        return (
            chart.properties(height=height, padding={"left": 6, "top": 10, "right": 8, "bottom": 6})
            .configure(background="#FFFFFF")
            .configure_view(stroke=None)
            .configure_title(
                font=EXEC_CHART_THEME["font"],
                fontSize=15,
                fontWeight=700,
                color=EXEC_CHART_THEME["title_color"],
                anchor="start",
            )
            .configure_axis(
                labelFont=EXEC_CHART_THEME["font"],
                titleFont=EXEC_CHART_THEME["font"],
                labelColor=EXEC_CHART_THEME["label_color"],
                titleColor=EXEC_CHART_THEME["label_color"],
                labelFontSize=11,
                titleFontSize=12,
                domain=False,
                tickColor=EXEC_CHART_THEME["grid_color"],
                gridColor=EXEC_CHART_THEME["grid_color"],
                gridOpacity=0.75,
            )
            .configure_legend(
                labelFont=EXEC_CHART_THEME["font"],
                titleFont=EXEC_CHART_THEME["font"],
                labelColor=EXEC_CHART_THEME["label_color"],
                titleColor=EXEC_CHART_THEME["label_color"],
                orient="top",
                direction="horizontal",
                symbolType="circle",
                symbolSize=110,
                padding=8,
            )
        )

    def render_ai_recommendation(headline: str, insight: str, action: str, impact: str, level: str = "info") -> None:
        st.markdown(
            f"""<div class="ai-rec-card {level}"><div class="ai-rec-head">🤖 AI Recommendation · {headline}</div><div class="ai-rec-line"><strong>Insight:</strong> {insight}</div><div class="ai-rec-line"><strong>Action:</strong> {action}</div><div class="ai-rec-line"><strong>Expected Impact:</strong> {impact}</div></div>""",
            unsafe_allow_html=True,
        )

    # ── Animated CSS for Executive Overview ────────────────────────────
    st.markdown("""<style>
@keyframes pulse-ring { 0%,100% { transform: scale(0.95); opacity: 1; } 50% { transform: scale(1.05); opacity: 0.8; } }
@keyframes value-count { 0% { opacity: 0; transform: translateY(10px); } 100% { opacity: 1; transform: translateY(0); } }
@keyframes trend-arrow { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-3px); } }
@keyframes exec-metric-glow { 0%,100% { box-shadow: 0 2px 4px rgba(0,0,0,0.05); } 50% { box-shadow: 0 4px 20px rgba(41,181,232,0.20); } }
@keyframes icon-bounce { 0%,100% { transform: translateY(0) scale(1); } 50% { transform: translateY(-4px) scale(1.1); } }
@keyframes metric-number-pop { 0% { opacity: 0; transform: scale(0.5) translateY(10px); } 60% { transform: scale(1.1) translateY(-3px); } 100% { opacity: 1; transform: scale(1) translateY(0); } }
@keyframes metric-text-glow { 0%,100% { text-shadow: none; } 50% { text-shadow: 0 0 12px currentColor; } }
@keyframes shimmer-sweep { 0% { left: -100%; } 100% { left: 200%; } }
@keyframes live-pulse { 0%,100% { transform: scale(1); opacity: 0.8; } 50% { transform: scale(1.3); opacity: 1; } }
@keyframes pulse-dot-ring { 0% { transform: scale(1); opacity: 0.8; } 100% { transform: scale(2.5); opacity: 0; } }
@keyframes kpi-accent-pulse { 0%,100% { opacity: 1; } 50% { opacity: 0.6; } }
@keyframes kpi-value-pop { 0% { opacity: 0; transform: scale(0.8); } 100% { opacity: 1; transform: scale(1); } }
@keyframes kpi-line-pulse { 0%,100% { stroke-width: 2; opacity: 0.25; } 50% { stroke-width: 4; opacity: 0.4; } }
@keyframes kpi-fill-pulse { 0%,100% { opacity: 0.2; transform: scaleY(1); } 50% { opacity: 0.35; transform: scaleY(1.05); } }
@keyframes kpi-bar-wave { 0%,100% { transform: scaleY(1); opacity: 0.25; } 50% { transform: scaleY(0.65); opacity: 0.4; } }
@keyframes eo-title-rise { 0% { opacity: 0; transform: translateY(8px); } 100% { opacity: 1; transform: translateY(0); } }
@keyframes eo-title-shimmer { 0% { left: -35%; } 100% { left: 120%; } }
@keyframes eo-dot-pulse { 0%,100% { transform: scale(1); opacity: 0.8; } 50% { transform: scale(1.25); opacity: 1; } }
.eo-title {
    position: relative;
    overflow: hidden;
    display: flex;
    align-items: center;
    gap: 0.6rem;
    margin: 1.3rem 0 0.85rem;
    padding: 0.62rem 0.9rem;
    border-radius: 12px;
    border: 1px solid #DBEAFE;
    background: linear-gradient(135deg, #F0F8FF 0%, #EEF2FF 100%);
    color: #1B2A4E;
    font-weight: 700;
    font-size: 1.04rem;
    letter-spacing: 0.01em;
    animation: eo-title-rise 0.4s ease-out both;
}
.eo-title::before {
    content: "";
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: linear-gradient(135deg, #29B5E8, #6366F1);
    animation: eo-dot-pulse 1.8s ease-in-out infinite;
}
.eo-title::after {
    content: "";
    position: absolute;
    top: 0;
    left: -35%;
    width: 30%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.85), transparent);
    animation: eo-title-shimmer 3.2s ease-in-out infinite;
}
.eo-mini-title {
    display: inline-flex;
    align-items: center;
    gap: 0.45rem;
    margin: 0.15rem 0 0.55rem;
    color: #1E3A8A;
    font-size: 0.93rem;
    font-weight: 700;
    animation: eo-title-rise 0.35s ease-out both;
}
.eo-mini-title::before {
    content: "";
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: linear-gradient(135deg, #22C1EE, #8B5CF6);
}
.business-pulse { background: linear-gradient(135deg, #F8FAFC 0%, #EFF6FF 100%); border-radius: 16px; padding: 1.5rem; margin-bottom: 2rem; border: 1px solid #BFDBFE; position: relative; overflow: hidden; }
.business-pulse::before { content: ''; position: absolute; top: 0; left: -100%; width: 50%; height: 100%; background: linear-gradient(90deg, transparent, rgba(41,181,232,0.1), transparent); animation: shimmer-sweep 3s ease-in-out infinite; }
.pulse-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; position: relative; z-index: 1; }
.pulse-title { color: #1B2A4E; font-size: 1.1rem; font-weight: 600; }
.pulse-live { display: inline-flex; align-items: center; gap: 0.5rem; }
.pulse-dot { width: 10px; height: 10px; background: #10B981; border-radius: 50%; animation: live-pulse 1.5s ease-in-out infinite; position: relative; }
.pulse-dot::after { content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: #10B981; border-radius: 50%; animation: pulse-dot-ring 1.5s ease-out infinite; }
.pulse-period { color: #10B981; font-size: 0.8rem; font-weight: 500; }
.pulse-metrics { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1.5rem; position: relative; z-index: 1; }
.pulse-metric { background: white; border-radius: 12px; padding: 1.25rem; text-align: center; border: 1px solid #E2E8F0; animation: exec-metric-glow 3s ease-in-out infinite; transition: all 0.3s ease; }
.pulse-metric:nth-child(1) { animation-delay: 0s; }
.pulse-metric:nth-child(2) { animation-delay: 0.5s; }
.pulse-metric:nth-child(3) { animation-delay: 1s; }
.pulse-metric:nth-child(4) { animation-delay: 1.5s; }
.pulse-metric:hover { transform: translateY(-4px); box-shadow: 0 8px 25px rgba(41,181,232,0.2); }
.pm-icon { font-size: 1.5rem; margin-bottom: 0.5rem; animation: icon-bounce 2s ease-in-out infinite; display: inline-block; }
.pulse-metric:nth-child(1) .pm-icon { animation-delay: 0s; }
.pulse-metric:nth-child(2) .pm-icon { animation-delay: 0.3s; }
.pulse-metric:nth-child(3) .pm-icon { animation-delay: 0.6s; }
.pulse-metric:nth-child(4) .pm-icon { animation-delay: 0.9s; }
.pm-val { font-size: 1.8rem; font-weight: 700; color: #1B2A4E; animation: metric-number-pop 0.6s ease-out forwards, metric-text-glow 3s ease-in-out 0.6s infinite; opacity: 0; }
.pulse-metric:nth-child(2) .pm-val { animation-delay: 0.15s, 0.75s; }
.pulse-metric:nth-child(3) .pm-val { animation-delay: 0.3s, 0.9s; }
.pulse-metric:nth-child(4) .pm-val { animation-delay: 0.45s, 1.05s; }
.pm-val.revenue { color: #10B981; }
.pm-val.customers { color: #29B5E8; }
.pm-val.nps { color: #F59E0B; }
.pm-val.growth { color: #8B5CF6; }
.pm-name { font-size: 0.75rem; color: #64748B; text-transform: uppercase; letter-spacing: 0.05em; margin-top: 0.25rem; }
.pm-trend { font-size: 0.8rem; margin-top: 0.5rem; display: flex; align-items: center; justify-content: center; gap: 0.25rem; }
.pm-trend.up { color: #10B981; }
.pm-trend.up span { animation: trend-arrow 1s ease-in-out infinite; display: inline-block; }
.eo-kpi-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin-bottom: 1rem; }
.eo-kpi { background: white; border: 1px solid #E5E7EB; border-radius: 12px; padding: 1.25rem; position: relative; overflow: hidden; transition: all 0.3s ease; animation: exec-metric-glow 3s ease-in-out infinite; }
.eo-kpi:nth-child(1) { animation-delay: 0s; }
.eo-kpi:nth-child(2) { animation-delay: 0.4s; }
.eo-kpi:nth-child(3) { animation-delay: 0.8s; }
.eo-kpi:nth-child(4) { animation-delay: 1.2s; }
.eo-kpi:hover { border-color: #29B5E8; box-shadow: 0 8px 25px rgba(41,181,232,0.25) !important; transform: translateY(-4px); }
.eo-kpi::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 4px; background: var(--accent); animation: kpi-accent-pulse 2s ease-in-out infinite; }
.eo-kpi-label { font-size: 0.8rem; color: #6B7280; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.25rem; }
.eo-kpi-value { font-size: 2rem; font-weight: 700; color: #1B2A4E; line-height: 1.1; animation: kpi-value-pop 0.6s ease-out forwards; opacity: 0; }
.eo-kpi:nth-child(2) .eo-kpi-value { animation-delay: 0.1s; }
.eo-kpi:nth-child(3) .eo-kpi-value { animation-delay: 0.2s; }
.eo-kpi:nth-child(4) .eo-kpi-value { animation-delay: 0.3s; }
.eo-kpi-delta { display: inline-flex; align-items: center; font-size: 0.85rem; font-weight: 600; padding: 0.15rem 0.5rem; border-radius: 20px; margin-top: 0.5rem; }
.eo-kpi-delta.positive { background: #D1FAE5; color: #059669; }
.eo-kpi-delta.negative { background: #FEE2E2; color: #DC2626; }
.eo-kpi-delta.neutral { background: #F3F4F6; color: #6B7280; }
.eo-kpi-icon { position: absolute; top: 1rem; right: 1rem; font-size: 1.5rem; opacity: 0.3; }
.eo-kpi .kpi-chart { position: absolute; bottom: 0; left: 0; right: 0; height: 45px; opacity: 0.25; }
.eo-kpi .kpi-chart path[fill="none"] { animation: kpi-line-pulse 2s ease-in-out infinite; }
.eo-kpi .kpi-chart path[fill]:not([fill="none"]) { transform-origin: bottom; animation: kpi-fill-pulse 2.5s ease-in-out infinite; }
.eo-kpi .kpi-chart rect { transform-origin: bottom; animation: kpi-bar-wave 1.5s ease-in-out infinite; }
.exec-summary-shell { margin-top: 0.25rem; }
.exec-summary-hero {
    position: relative;
    overflow: hidden;
    border-radius: 14px;
    border: 1px solid #BFDBFE;
    background: linear-gradient(135deg, #EFF6FF 0%, #F5F3FF 100%);
    padding: 1rem 1.1rem;
    margin-bottom: 0.9rem;
}
.exec-summary-hero::before {
    content: "";
    position: absolute;
    top: 0;
    left: -110%;
    width: 55%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(41,181,232,0.22), transparent);
    animation: shimmer-sweep 3.2s ease-in-out infinite;
}
.exec-summary-title {
    position: relative;
    z-index: 1;
    display: flex;
    align-items: center;
    gap: 0.55rem;
    color: #1E3A8A;
    font-weight: 700;
    font-size: 0.98rem;
}
.exec-summary-sub {
    position: relative;
    z-index: 1;
    margin-top: 0.38rem;
    color: #334155;
    font-size: 0.9rem;
}
.exec-summary-grid {
    display: grid;
    grid-template-columns: 1.45fr 1fr;
    gap: 0.8rem;
}
.exec-summary-panel {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 14px;
    padding: 0.95rem 1rem;
    box-shadow: 0 8px 20px rgba(15, 23, 42, 0.05);
}
.exec-summary-panel h4 {
    margin: 0 0 0.62rem 0;
    color: #1B2A4E;
    font-size: 0.94rem;
    font-weight: 700;
}
.exec-summary-kpis {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.55rem;
}
.exec-summary-kpi {
    background: linear-gradient(135deg, #F8FAFC 0%, #EEF2FF 100%);
    border: 1px solid #E2E8F0;
    border-radius: 10px;
    padding: 0.62rem 0.7rem;
}
.exec-summary-kpi .v {
    color: #0F172A;
    font-size: 1rem;
    font-weight: 700;
    line-height: 1.2;
}
.exec-summary-kpi .l {
    margin-top: 0.12rem;
    color: #64748B;
    font-size: 0.74rem;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}
.exec-summary-list {
    margin: 0;
    padding-left: 1.08rem;
    color: #334155;
}
.exec-summary-list li {
    margin: 0.38rem 0;
    line-height: 1.32;
    font-size: 0.9rem;
}
.exec-summary-actions {
    margin: 0;
    padding-left: 1.05rem;
    color: #1E293B;
}
.exec-summary-actions li {
    margin: 0.42rem 0;
    line-height: 1.35;
    font-size: 0.9rem;
}
@keyframes cxo-fade-up {
    0% { opacity: 0; transform: translateY(12px); }
    100% { opacity: 1; transform: translateY(0); }
}
@keyframes cxo-urgent-pulse {
    0%, 100% { box-shadow: 0 0 0 0 rgba(239,68,68,0.30); }
    50% { box-shadow: 0 0 0 8px rgba(239,68,68,0); }
}
@keyframes cxo-flow {
    0% { left: -35%; }
    100% { left: 120%; }
}
@keyframes cxo-bar-fill {
    0% { width: 0; }
    100% { width: var(--p); }
}
.cxo-snapshot {
    position: relative;
    overflow: hidden;
    background: linear-gradient(130deg, #0F172A 0%, #1E3A8A 62%, #1D4ED8 100%);
    border-radius: 14px;
    border: 1px solid rgba(191, 219, 254, 0.5);
    padding: 1rem 1.1rem;
    margin-bottom: 0.95rem;
    animation: cxo-fade-up 0.5s ease-out both;
}
.cxo-snapshot::after {
    content: "";
    position: absolute;
    top: 0;
    left: -35%;
    width: 30%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.18), transparent);
    animation: cxo-flow 4s ease-in-out infinite;
}
.cxo-snapshot-title {
    color: #DBEAFE;
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 0.35rem;
    position: relative;
    z-index: 1;
}
.cxo-snapshot-text {
    color: #F8FAFC;
    font-size: 0.96rem;
    line-height: 1.4;
    font-weight: 600;
    position: relative;
    z-index: 1;
}
.cxo-snapshot-risk {
    margin-top: 0.6rem;
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.25rem 0.55rem;
    border-radius: 999px;
    background: rgba(239,68,68,0.18);
    color: #FECACA;
    font-size: 0.78rem;
    font-weight: 700;
    border: 1px solid rgba(252,165,165,0.45);
    position: relative;
    z-index: 1;
    animation: cxo-urgent-pulse 2.1s ease-in-out infinite;
}
.cxo-value-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0.7rem;
    margin-bottom: 0.9rem;
}
.cxo-value-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    padding: 0.8rem 0.85rem;
    position: relative;
    overflow: hidden;
    animation: cxo-fade-up 0.45s ease-out both;
}
.cxo-value-card:nth-child(1) { animation-delay: 0.05s; }
.cxo-value-card:nth-child(2) { animation-delay: 0.12s; }
.cxo-value-card:nth-child(3) { animation-delay: 0.2s; }
.cxo-value-card:nth-child(4) { animation-delay: 0.28s; }
.cxo-value-card::before {
    content: "";
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
    height: 3px;
    background: var(--accent);
}
.cxo-value-label {
    color: #64748B;
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    margin-bottom: 0.2rem;
}
.cxo-value-number {
    color: #0F172A;
    font-size: 1.35rem;
    font-weight: 800;
    line-height: 1.2;
}
.cxo-value-note {
    margin-top: 0.25rem;
    color: #334155;
    font-size: 0.78rem;
}
.cxo-value-note.urgent { color: #B91C1C; font-weight: 700; }
.cxo-decision-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.75rem;
    margin-bottom: 0.8rem;
}
.cxo-decision {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    padding: 0.8rem 0.85rem;
    animation: cxo-fade-up 0.45s ease-out both;
}
.cxo-decision:nth-child(1) { animation-delay: 0.08s; }
.cxo-decision:nth-child(2) { animation-delay: 0.16s; }
.cxo-decision:nth-child(3) { animation-delay: 0.24s; }
.cxo-decision-title {
    color: #0F172A;
    font-size: 0.9rem;
    font-weight: 700;
    margin-bottom: 0.4rem;
}
.cxo-decision-meta {
    color: #334155;
    font-size: 0.8rem;
    line-height: 1.36;
}
.cxo-badge {
    display: inline-flex;
    align-items: center;
    padding: 0.18rem 0.46rem;
    border-radius: 999px;
    font-size: 0.68rem;
    font-weight: 700;
    margin-bottom: 0.4rem;
}
.cxo-badge.high { background: #FEE2E2; color: #991B1B; }
.cxo-badge.med { background: #FEF3C7; color: #92400E; }
.cxo-badge.ok { background: #DCFCE7; color: #166534; }
.cxo-initiatives {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.75rem;
}
.cxo-initiative {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    padding: 0.8rem 0.85rem;
    animation: cxo-fade-up 0.45s ease-out both;
}
.cxo-init-head {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.35rem;
}
.cxo-init-title {
    color: #0F172A;
    font-size: 0.88rem;
    font-weight: 700;
}
.cxo-rag {
    font-size: 0.67rem;
    font-weight: 700;
    border-radius: 999px;
    padding: 0.15rem 0.42rem;
}
.cxo-rag.green { background: #DCFCE7; color: #166534; }
.cxo-rag.amber { background: #FEF3C7; color: #92400E; }
.cxo-rag.red { background: #FEE2E2; color: #991B1B; animation: cxo-urgent-pulse 2s ease-in-out infinite; }
.cxo-init-meta {
    color: #475569;
    font-size: 0.76rem;
    margin-bottom: 0.44rem;
}
.cxo-progress {
    width: 100%;
    height: 8px;
    border-radius: 999px;
    background: #E2E8F0;
    overflow: hidden;
    margin-bottom: 0.35rem;
}
.cxo-progress > span {
    display: block;
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, #29B5E8, #1D4ED8);
    width: var(--p);
    animation: cxo-bar-fill 1.2s ease-out both;
}
.cxo-init-foot {
    color: #334155;
    font-size: 0.76rem;
}
.cxo-board {
    background: linear-gradient(135deg, #FFFFFF 0%, #F8FAFC 100%);
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    padding: 0.85rem 0.9rem;
}
.cxo-board-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0.6rem;
}
.cxo-board-cell {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 10px;
    padding: 0.55rem 0.6rem;
}
.cxo-board-cell h5 {
    margin: 0 0 0.2rem 0;
    color: #1E3A8A;
    font-size: 0.76rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
.cxo-board-cell p {
    margin: 0;
    color: #334155;
    font-size: 0.8rem;
    line-height: 1.35;
}
.ai-rec-card {
    margin-top: 0.65rem;
    border-radius: 10px;
    border: 1px solid #D1E9FF;
    background: linear-gradient(135deg, #F8FBFF 0%, #EEF6FF 100%);
    padding: 0.62rem 0.78rem;
    box-shadow: 0 4px 14px rgba(15, 23, 42, 0.05);
    animation: cxo-fade-up 0.35s ease-out both;
}
.ai-rec-card .ai-rec-head {
    color: #1E3A8A;
    font-size: 0.78rem;
    font-weight: 700;
    margin-bottom: 0.28rem;
    letter-spacing: 0.02em;
}
.ai-rec-card .ai-rec-line {
    color: #334155;
    font-size: 0.77rem;
    line-height: 1.34;
    margin: 0.12rem 0;
}
.ai-rec-card.warning {
    border-color: #FCD34D;
    background: linear-gradient(135deg, #FFFBEB 0%, #FEF3C7 100%);
}
.ai-rec-card.warning .ai-rec-head {
    color: #92400E;
}
.ai-rec-card.critical {
    border-color: #FCA5A5;
    background: linear-gradient(135deg, #FEF2F2 0%, #FEE2E2 100%);
}
.ai-rec-card.critical .ai-rec-head {
    color: #991B1B;
}
@media (max-width: 768px) { .pulse-metrics, .eo-kpi-grid { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 980px) { .exec-summary-grid { grid-template-columns: 1fr; } }
@media (max-width: 980px) { .cxo-value-grid, .cxo-decision-grid, .cxo-board-grid { grid-template-columns: 1fr 1fr; } }
@media (max-width: 980px) { .cxo-initiatives { grid-template-columns: 1fr; } }
@media (max-width: 720px) { .cxo-value-grid, .cxo-decision-grid, .cxo-board-grid { grid-template-columns: 1fr; } }
</style>""", unsafe_allow_html=True)

    # -------------------------------------------------------------------
    # Synthetic "warehouse-consistent" dataset for all executive metrics
    # -------------------------------------------------------------------
    db_segment_perf = pd.DataFrame({
        "Segment": ["MasOrange", "Vodafone"],
        "Subscribers": [7000000, 5000000],
        "Monthly Revenue M": [24.5, 17.9],
        "NPS": [58, 54],
        "Churn %": [0.8, 1.1],
    })
    db_risk = pd.DataFrame({
        "Segment": ["Budget", "Standard", "Premium", "VIP"],
        "At Risk": [312, 289, 178, 68],
        "Revenue at Risk K": [95, 78, 51, 16],
        "Avg Propensity": [0.78, 0.65, 0.52, 0.41],
    })
    db_network_regions = pd.DataFrame({
        "Region": ["Madrid Centro", "Barcelona", "Valencia", "Sevilla", "Bilbao", "Málaga"],
        "Network Score": [95.1, 92.4, 90.8, 91.7, 89.9, 88.7],
        "NPS": [54, 49, 45, 47, 42, 39],
        "Incidents": [18, 24, 29, 26, 34, 38],
    })
    db_incident_trend = pd.DataFrame({
        "Week": ["W1", "W2", "W3", "W4", "W5", "W6"],
        "Major Incidents": [22, 20, 18, 19, 16, 14],
        "MTTR Minutes": [62, 59, 57, 55, 52, 49],
    })

    active_subscribers = int(db_segment_perf["Subscribers"].sum())
    monthly_revenue_m = round(float(db_segment_perf["Monthly Revenue M"].sum()), 1)
    quarterly_revenue_m = round(monthly_revenue_m * 3, 1)
    arpu_blended = round((monthly_revenue_m * 1_000_000) / active_subscribers, 2)
    nps_score = int(round((db_segment_perf["NPS"] * db_segment_perf["Subscribers"]).sum() / active_subscribers, 0))
    churn_rate = round(float((db_segment_perf["Churn %"] * db_segment_perf["Subscribers"]).sum() / active_subscribers), 1)
    at_risk_revenue_m = round(float(db_risk["Revenue at Risk K"].sum()) * 12 / 1000, 1)
    at_risk_customers = int(db_risk["At Risk"].sum())
    market_share = 38.2
    net_adds = 125000
    network_availability = 99.7
    support_csat = 4.2
    arpu_delta = "+€0.42"
    value_in_flight_m = 1.6
    protectable_arr_m = round(at_risk_revenue_m * 0.6, 1)

    # ── Real-Time Business Pulse ──────────────────────────────────────
    st.markdown(
        f"""<div class="business-pulse"><div class="pulse-header"><div class="pulse-live"><div class="pulse-dot"></div><span class="pulse-title">📊 Real-Time Business Pulse</span></div><div class="pulse-period">● Live</div></div><div class="pulse-metrics"><div class="pulse-metric"><div class="pm-icon">💰</div><div class="pm-val revenue">€{monthly_revenue_m:.1f}M</div><div class="pm-name">Monthly Revenue</div><div class="pm-trend up"><span>↑</span> +8.4% vs target</div></div><div class="pulse-metric"><div class="pm-icon">🏠</div><div class="pm-val customers">{active_subscribers:,}</div><div class="pm-name">Homes Passed</div><div class="pm-trend up"><span>↑</span> +{net_adds:,} this quarter</div></div><div class="pulse-metric"><div class="pm-icon">⭐</div><div class="pm-val nps">+{nps_score}</div><div class="pm-name">Partner NPS</div><div class="pm-trend up"><span>↑</span> +5 pts QoQ</div></div><div class="pulse-metric"><div class="pm-icon">📈</div><div class="pm-val growth">{market_share:.1f}%</div><div class="pm-name">FTTH Market Share</div><div class="pm-trend up"><span>↑</span> +2.1% YoY</div></div></div></div>""",
        unsafe_allow_html=True,
    )

    overview_tab, ai_summary_tab = st.tabs(["📈 Executive Overview", "🤖 AI Strategy"])

    with overview_tab:
        # ── Business Health at a Glance ───────────────────────────────────
        st.markdown('<div class="eo-title">Business Health at a Glance</div>', unsafe_allow_html=True)

        st.markdown(f"""<div class="eo-kpi-grid"><div class="eo-kpi" style="--accent: #29B5E8;"><div class="eo-kpi-icon">🏠</div><div class="eo-kpi-label">Homes Passed</div><div class="eo-kpi-value">{active_subscribers:,}</div><div class="eo-kpi-delta positive">↑ +5.2% QoQ</div><svg class="kpi-chart" viewBox="0 0 100 40" preserveAspectRatio="none"><path d="M0,35 L15,32 L30,28 L45,25 L60,20 L75,15 L100,8" fill="none" stroke="#29B5E8" stroke-width="2"/><path d="M0,35 L15,32 L30,28 L45,25 L60,20 L75,15 L100,8 L100,40 L0,40 Z" fill="#29B5E8"/></svg></div><div class="eo-kpi" style="--accent: #10B981;"><div class="eo-kpi-icon">💰</div><div class="eo-kpi-label">Quarterly Revenue</div><div class="eo-kpi-value">€{quarterly_revenue_m:.1f}M</div><div class="eo-kpi-delta positive">↑ +8.4% YoY</div><svg class="kpi-chart" viewBox="0 0 100 40" preserveAspectRatio="none"><path d="M0,32 L15,30 L30,26 L45,28 L60,20 L75,14 L100,8" fill="none" stroke="#10B981" stroke-width="2"/><path d="M0,32 L15,30 L30,26 L45,28 L60,20 L75,14 L100,8 L100,40 L0,40 Z" fill="#10B981"/></svg></div><div class="eo-kpi" style="--accent: #8B5CF6;"><div class="eo-kpi-icon">⭐</div><div class="eo-kpi-label">Partner NPS</div><div class="eo-kpi-value">+{nps_score}</div><div class="eo-kpi-delta positive">↑ +5 pts</div><svg class="kpi-chart" viewBox="0 0 100 40" preserveAspectRatio="none"><rect x="5" y="28" width="10" height="12" fill="#8B5CF6"/><rect x="20" y="24" width="10" height="16" fill="#8B5CF6"/><rect x="35" y="26" width="10" height="14" fill="#8B5CF6"/><rect x="50" y="20" width="10" height="20" fill="#8B5CF6"/><rect x="65" y="16" width="10" height="24" fill="#8B5CF6"/><rect x="80" y="12" width="10" height="28" fill="#8B5CF6"/></svg></div><div class="eo-kpi" style="--accent: #F59E0B;"><div class="eo-kpi-icon">📉</div><div class="eo-kpi-label">Partner Churn</div><div class="eo-kpi-value">{churn_rate:.1f}%</div><div class="eo-kpi-delta positive">↓ -0.7%</div><svg class="kpi-chart" viewBox="0 0 100 40" preserveAspectRatio="none"><path d="M0,8 L15,12 L30,16 L45,18 L60,22 L75,28 L100,32" fill="none" stroke="#F59E0B" stroke-width="2"/><path d="M0,8 L15,12 L30,16 L45,18 L60,22 L75,28 L100,32 L100,40 L0,40 Z" fill="#F59E0B"/></svg></div></div>""", unsafe_allow_html=True)

        st.markdown(f"""<div class="eo-kpi-grid"><div class="eo-kpi" style="--accent: #06B6D4;"><div class="eo-kpi-icon">📡</div><div class="eo-kpi-label">Network Availability</div><div class="eo-kpi-value">{network_availability:.1f}%</div><div class="eo-kpi-delta positive">↑ +0.2%</div></div><div class="eo-kpi" style="--accent: #EC4899;"><div class="eo-kpi-icon">📊</div><div class="eo-kpi-label">Revenue per Home</div><div class="eo-kpi-value">€{arpu_blended:.2f}</div><div class="eo-kpi-delta positive">↑ {arpu_delta}</div></div><div class="eo-kpi" style="--accent: #14B8A6;"><div class="eo-kpi-icon">💬</div><div class="eo-kpi-label">Support CSAT</div><div class="eo-kpi-value">{support_csat:.1f}/5</div><div class="eo-kpi-delta positive">↑ +0.3</div></div><div class="eo-kpi" style="--accent: #EF4444;"><div class="eo-kpi-icon">⚠️</div><div class="eo-kpi-label">At-Risk Revenue</div><div class="eo-kpi-value">€{at_risk_revenue_m:.1f}M</div><div class="eo-kpi-delta neutral">{int(db_risk['At Risk'].sum())} customers</div></div></div>""", unsafe_allow_html=True)

        # ── Executive Performance Signals (Altair charts) ──────────────────
        st.markdown('<div class="eo-title">Executive Performance Signals</div>', unsafe_allow_html=True)
        exec_col1, exec_col2 = st.columns(2)

        with exec_col1:
            st.markdown('<div class="eo-mini-title">Revenue Mix by Partner</div>', unsafe_allow_html=True)
            with st.container(border=True):
                seg_df = db_segment_perf[["Segment", "Monthly Revenue M"]].rename(columns={"Monthly Revenue M": "Revenue"})
                seg_bar = (
                    alt.Chart(seg_df)
                    .mark_bar(cornerRadiusTopRight=8, cornerRadiusBottomRight=8, size=22)
                    .encode(
                        x=alt.X('Revenue:Q', title='Revenue (€ M)', axis=alt.Axis(format=".1f", tickCount=6)),
                        y=alt.Y('Segment:N', sort='-x', title=None),
                        color=alt.Color(
                            'Segment:N',
                            scale=alt.Scale(
                                domain=['MasOrange', 'Vodafone'],
                                range=[
                                    "#FF6B00",
                                    "#E60000",
                                ],
                            ),
                            legend=None,
                        ),
                        tooltip=[
                            alt.Tooltip('Segment:N', title='Segment'),
                            alt.Tooltip('Revenue:Q', title='Revenue', format='.2f'),
                        ],
                    )
                )
                seg_text = alt.Chart(seg_df).mark_text(align="left", dx=6, fontSize=11, color="#0F172A").encode(
                    x='Revenue:Q',
                    y=alt.Y('Segment:N', sort='-x'),
                    text=alt.Text('Revenue:Q', format='.1f'),
                )
                st.altair_chart(style_exec_chart(seg_bar + seg_text, height=190), use_container_width=True)
                top_seg = seg_df.loc[seg_df["Revenue"].idxmax()]
                render_ai_recommendation(
                    "Revenue Mix",
                    f"{top_seg['Segment']} contributes the largest wholesale revenue at €{top_seg['Revenue']:.1f}M.",
                    f"Strengthen SLA performance for {top_seg['Segment']} while expanding capacity for growth partners.",
                    "Stabilize core wholesale revenue and add +€1.2M ARR in next quarter.",
                )

        with exec_col2:
            st.markdown('<div class="eo-mini-title">NPS vs Churn Risk</div>', unsafe_allow_html=True)
            with st.container(border=True):
                churn_df = pd.DataFrame({
                    'Segment': db_segment_perf['Segment'],
                    'NPS': db_segment_perf['NPS'],
                    'Churn': db_segment_perf['Churn %'],
                })
                churn_scatter = (
                    alt.Chart(churn_df)
                    .mark_circle(opacity=0.9, stroke="#FFFFFF", strokeWidth=1.8)
                    .encode(
                        x=alt.X('NPS:Q', title='NPS', scale=alt.Scale(domain=[40, 66])),
                        y=alt.Y('Churn:Q', title='Churn %', scale=alt.Scale(domain=[0.8, 2.6])),
                        size=alt.Size('NPS:Q', legend=None, scale=alt.Scale(range=[180, 520])),
                        color=alt.Color(
                            'Segment:N',
                            scale=alt.Scale(
                                domain=['MasOrange', 'Vodafone'],
                                range=[
                                    "#FF6B00",
                                    "#E60000",
                                ],
                            ),
                            legend=alt.Legend(title=None),
                        ),
                        tooltip=[
                            alt.Tooltip('Segment:N', title='Segment'),
                            alt.Tooltip('NPS:Q', title='NPS'),
                            alt.Tooltip('Churn:Q', title='Churn %', format='.1f'),
                        ],
                    )
                )
                trend_line = churn_scatter.transform_regression('NPS', 'Churn').mark_line(
                    strokeDash=[5, 5],
                    color="#64748B",
                    size=2,
                    opacity=0.9,
                )
                point_labels = alt.Chart(churn_df).mark_text(dy=-14, fontSize=10, color="#334155").encode(
                    x='NPS:Q',
                    y='Churn:Q',
                    text='Segment:N',
                )
                st.altair_chart(style_exec_chart(trend_line + churn_scatter + point_labels, height=190), use_container_width=True)
                worst_seg = churn_df.loc[churn_df["Churn"].idxmax()]
                render_ai_recommendation(
                    "NPS vs Churn",
                    f"{worst_seg['Segment']} shows the highest churn ({worst_seg['Churn']:.1f}%) and the lowest relative NPS.",
                    f"Launch a partner-specific retention sprint for {worst_seg['Segment']} with SLA improvement triggers.",
                    "Reduce blended partner churn by ~0.1pp in 60 days.",
                    level="warning",
                )

        # ── Revenue Bridge ─────────────────────────────────────────────────
        st.markdown('<div class="eo-title">Revenue Bridge (YoY)</div>', unsafe_allow_html=True)
        with st.container(border=True):
            bridge_df = pd.DataFrame({
                'Driver': ['Base', 'Volume', 'Price', 'Mix', 'Churn', 'Discounts', 'Current'],
                'Impact': [12.0, 0.9, 0.5, 0.4, -0.4, -0.2, quarterly_revenue_m],
                'Type': ['Total', 'Up', 'Up', 'Up', 'Down', 'Down', 'Total'],
            })
            bridge_df['Label'] = bridge_df['Impact'].apply(lambda v: f"{v:+.1f}M" if v not in [12.0, quarterly_revenue_m] else f"{v:.1f}M")
            bridge_bar = alt.Chart(bridge_df).mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6, size=56).encode(
                x=alt.X('Driver:N', title=None, sort=list(bridge_df['Driver']), axis=alt.Axis(labelAngle=0)),
                y=alt.Y('Impact:Q', title='€ M'),
                color=alt.Color(
                    'Type:N',
                    scale=alt.Scale(
                        domain=['Up', 'Down', 'Total'],
                        range=[
                            EXEC_CHART_THEME["accent_green"],
                            EXEC_CHART_THEME["accent_red"],
                            "#3B82F6",
                        ],
                    ),
                    legend=alt.Legend(title=None),
                ),
                tooltip=[
                    alt.Tooltip('Driver:N', title='Driver'),
                    alt.Tooltip('Impact:Q', title='Impact', format='.1f'),
                    alt.Tooltip('Type:N', title='Type'),
                ],
            )
            bridge_text = alt.Chart(bridge_df).mark_text(dy=-8, fontSize=10, fontWeight='bold').encode(
                x=alt.X('Driver:N', sort=list(bridge_df['Driver'])),
                y='Impact:Q',
                text='Label:N',
                color=alt.value('#1B2A4E'),
            )
            baseline = alt.Chart(pd.DataFrame({"y": [0]})).mark_rule(strokeDash=[4, 4], color="#94A3B8").encode(y="y:Q")
            st.altair_chart(style_exec_chart(baseline + bridge_bar + bridge_text, height=210), use_container_width=True)
            up_driver = bridge_df[bridge_df["Type"] == "Up"].sort_values("Impact", ascending=False).iloc[0]
            down_driver = bridge_df[bridge_df["Type"] == "Down"].sort_values("Impact").iloc[0]
            render_ai_recommendation(
                "Revenue Bridge",
                f"Biggest uplift comes from {up_driver['Driver']} (+€{up_driver['Impact']:.1f}M) while {down_driver['Driver']} is the main drag ({down_driver['Impact']:.1f}M).",
                f"Double down on {up_driver['Driver']} levers and assign an owner to recover losses from {down_driver['Driver']}.",
                "Protect ~€0.4M and improve run-rate predictability.",
            )

        # ── ARPU & Plan Mix ───────────────────────────────────────────────
        st.markdown('<div class="eo-title">ARPU & Plan Mix</div>', unsafe_allow_html=True)
        arpu_col, mix_col = st.columns(2)
        with arpu_col:
            st.markdown('<div class="eo-mini-title">ARPU by Segment</div>', unsafe_allow_html=True)
            with st.container(border=True):
                arpu_df = db_segment_perf.copy()
                arpu_df['ARPU'] = (arpu_df['Monthly Revenue M'] * 1_000_000 / arpu_df['Subscribers']).round(0)
                arpu_df = arpu_df[['Segment', 'ARPU']]
                arpu_bar = (
                    alt.Chart(arpu_df)
                    .mark_bar(cornerRadiusTopRight=8, cornerRadiusBottomRight=8, size=22)
                    .encode(
                        x=alt.X('ARPU:Q', title='ARPU (€)', axis=alt.Axis(tickCount=6)),
                        y=alt.Y('Segment:N', sort='-x', title=None),
                        color=alt.Color(
                            'Segment:N',
                            scale=alt.Scale(
                                domain=['Vodafone', 'MasOrange'],
                                range=["#E60000", "#FF6B00"],
                            ),
                            legend=None,
                        ),
                        tooltip=[
                            alt.Tooltip('Segment:N', title='Segment'),
                            alt.Tooltip('ARPU:Q', title='ARPU', format='.0f'),
                        ],
                    )
                )
                st.altair_chart(style_exec_chart(arpu_bar, height=205), use_container_width=True)
                top_arpu = arpu_df.loc[arpu_df["ARPU"].idxmax()]
                render_ai_recommendation(
                    "Revenue per Home by Partner",
                    f"{top_arpu['Segment']} has the highest revenue per home at €{top_arpu['ARPU']:.2f}.",
                    f"Replicate {top_arpu['Segment']} network efficiency to other partners.",
                    "Increase blended revenue per home by ~€0.08 within a quarter.",
                )
        with mix_col:
            st.markdown('<div class="eo-mini-title">Infrastructure Mix by Type</div>', unsafe_allow_html=True)
            with st.container(border=True):
                plan_df = pd.DataFrame({
                    'Plan': ['FTTH 300Mb', 'FTTH 600Mb', 'FTTH 1Gbps', 'Dark Fiber'],
                    'Share': [35, 32, 25, 8],
                })
                plan_bar = (
                    alt.Chart(plan_df)
                    .mark_bar(cornerRadiusTopRight=8, cornerRadiusBottomRight=8, size=22)
                    .encode(
                        x=alt.X('Share:Q', title='Share %', axis=alt.Axis(tickCount=6)),
                        y=alt.Y('Plan:N', sort='-x', title=None),
                        color=alt.Color(
                            'Plan:N',
                            scale=alt.Scale(
                                domain=['FTTH 300Mb', 'FTTH 600Mb', 'FTTH 1Gbps', 'Dark Fiber'],
                                range=[EXEC_CHART_THEME["accent_indigo"], "#818CF8", "#A5B4FC", "#C7D2FE"],
                            ),
                            legend=None,
                        ),
                        tooltip=[
                            alt.Tooltip('Plan:N', title='Product'),
                            alt.Tooltip('Share:Q', title='Share %', format='.0f'),
                        ],
                    )
                )
                st.altair_chart(style_exec_chart(plan_bar, height=205), use_container_width=True)
                top_plan = plan_df.loc[plan_df["Share"].idxmax()]
                render_ai_recommendation(
                    "Infrastructure Mix",
                    f"{top_plan['Plan']} is the dominant infrastructure type at {top_plan['Share']:.0f}%.",
                    "Increase 1Gbps deployment in high-demand areas to capture premium wholesale pricing.",
                    "Capture +€0.8M monthly incremental revenue.",
                )

        # ── Revenue Mix by Customer Segment ────────────────────────────────
        col_left, col_right = st.columns([1.2, 1])

        with col_left:
            st.markdown('<div class="eo-title">Revenue Mix by Partner</div>', unsafe_allow_html=True)
            revenue_data = db_segment_perf[['Segment', 'Monthly Revenue M']].copy()
            revenue_data['Revenue'] = (revenue_data['Monthly Revenue M'] * 3).round(1)
            revenue_data['Percentage'] = (100 * revenue_data['Revenue'] / revenue_data['Revenue'].sum()).round(0)
            revenue_data = revenue_data[['Segment', 'Revenue', 'Percentage']]
            with st.container(border=True):
                donut = alt.Chart(revenue_data).mark_arc(innerRadius=74, outerRadius=118, cornerRadius=5, stroke="#FFFFFF", strokeWidth=2).encode(
                    theta=alt.Theta('Revenue:Q', stack=True),
                    color=alt.Color(
                        'Segment:N',
                        scale=alt.Scale(domain=['MasOrange', 'Vodafone'], range=['#FF6B00', '#E60000']),
                        legend=alt.Legend(title=None, orient='right'),
                    ),
                    tooltip=[
                        alt.Tooltip('Segment:N', title='Segment'),
                        alt.Tooltip('Revenue:Q', title='Revenue (€ M)', format='.1f'),
                        alt.Tooltip('Percentage:Q', title='Share %', format='.0f'),
                    ],
                    order=alt.Order('Revenue:Q', sort='descending'),
                )
                center_text = alt.Chart(pd.DataFrame({'text': [f'€{quarterly_revenue_m:.1f}M']})).mark_text(fontSize=24, fontWeight='bold', color='#1B2A4E').encode(text='text:N')
                center_sub = alt.Chart(pd.DataFrame({'text': ['Total Revenue']})).mark_text(fontSize=12, color='#6B7280', dy=20).encode(text='text:N')
                st.altair_chart(style_exec_chart(donut + center_text + center_sub, height=272), use_container_width=True)
                dominant_seg = revenue_data.loc[revenue_data["Revenue"].idxmax()]
                render_ai_recommendation(
                    "Partner Revenue Concentration",
                    f"{dominant_seg['Segment']} represents {dominant_seg['Percentage']:.0f}% of quarterly wholesale revenue.",
                    f"Maintain strong SLA performance for both MasOrange and Vodafone networks.",
                    "Ensure balanced growth across both wholesale partners.",
                )

                seg_cols = st.columns(2)
                seg_info = []
                seg_colors = {"MasOrange": "#FF6B00", "Vodafone": "#E60000"}
                seg_growth = {"MasOrange": "+6.8%", "Vodafone": "+8.2%"}
                for _, row in db_segment_perf.iterrows():
                    seg = row["Segment"]
                    q_rev = row["Monthly Revenue M"] * 3
                    share = 100 * q_rev / quarterly_revenue_m
                    seg_arpu = row["Monthly Revenue M"] * 1_000_000 / row["Subscribers"]
                    seg_info.append((seg, seg_colors[seg], f"€{q_rev:.1f}M", f"{share:.0f}%", f"€{seg_arpu:.2f}", seg_growth[seg]))
                for i, (seg, color, rev, share, arpu, growth) in enumerate(seg_info):
                    with seg_cols[i]:
                        st.markdown(f"""<div style="background: linear-gradient(135deg, {color}15 0%, {color}08 100%); border-left: 4px solid {color}; border-radius: 0 8px 8px 0; padding: 0.75rem;"><div style="font-weight: 600; color: {color}; font-size: 0.9rem;">{seg}</div><div style="font-size: 1.2rem; font-weight: 700; color: #1B2A4E;">{rev}</div><div style="color: #6B7280; font-size: 0.75rem;">Rev/Home {arpu} · <span style="color: #10B981;">{growth}</span></div></div>""", unsafe_allow_html=True)

        with col_right:
            st.markdown('<div class="eo-title">At-Risk Customer Analysis</div>', unsafe_allow_html=True)
            with st.container(border=True):
                risk_data = db_risk.rename(columns={"Revenue at Risk K": "Revenue at Risk"})
                lollipop_line = alt.Chart(risk_data).mark_rule(strokeWidth=3).encode(
                    x=alt.X('At Risk:Q', title='Customers at Risk', scale=alt.Scale(domain=[0, 350])),
                    x2=alt.value(0),
                    y=alt.Y('Segment:N', sort=['Budget', 'Standard', 'Premium', 'VIP'], title=None),
                    color=alt.Color('Avg Propensity:Q', scale=alt.Scale(scheme='orangered', domain=[0.4, 0.8]), legend=None),
                )
                lollipop_point = alt.Chart(risk_data).mark_circle(size=300).encode(
                    x='At Risk:Q',
                    y=alt.Y('Segment:N', sort=['Budget', 'Standard', 'Premium', 'VIP']),
                    color=alt.Color('Avg Propensity:Q', scale=alt.Scale(scheme='orangered', domain=[0.4, 0.8]), title='Churn Risk'),
                    tooltip=['Segment', alt.Tooltip('At Risk:Q', title='Customers'), alt.Tooltip('Revenue at Risk:Q', title='Revenue (€ K)', format=',.0f'), alt.Tooltip('Avg Propensity:Q', title='Risk Score', format='.0%')],
                )
                risk_labels = alt.Chart(risk_data).mark_text(align='left', dx=14, fontSize=10, fontWeight='bold', color="#7F1D1D").encode(
                    x='At Risk:Q',
                    y=alt.Y('Segment:N', sort=['Budget', 'Standard', 'Premium', 'VIP']),
                    text=alt.Text('Revenue at Risk:Q', format='€,.0fK'),
                )
                st.altair_chart(style_exec_chart(lollipop_line + lollipop_point + risk_labels, height=190), use_container_width=True)
                highest_risk = risk_data.loc[risk_data["Avg Propensity"].idxmax()]
                render_ai_recommendation(
                    "At-Risk Cohorts",
                    f"{highest_risk['Segment']} has the highest churn propensity ({highest_risk['Avg Propensity']:.0%}) with material revenue exposure.",
                    f"Prioritize save-offers and proactive outreach for {highest_risk['Segment']} in the next 2 billing cycles.",
                    f"Protect up to €{(highest_risk['Revenue at Risk']/1000):.1f}M ARR from this cohort.",
                    level="critical",
                )

                st.markdown(f"""<div style="background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%); border-radius: 8px; padding: 0.75rem; margin-top: 0.5rem; border-left: 4px solid #F59E0B;"><div style="display: flex; align-items: center;"><span style="font-size: 1.5rem; margin-right: 0.5rem;">⚠️</span><div><strong style="color: #92400E;">Urgent: {at_risk_customers} customers at risk</strong><div style="color: #B45309; font-size: 0.85rem;">€{at_risk_revenue_m:.1f}M ARR exposed · Budget segment highest propensity</div></div></div></div>""", unsafe_allow_html=True)

    with ai_summary_tab:
        # ── C-Level AI Executive Cockpit ──────────────────────────────────
        st.markdown('<div class="eo-title">AI Strategy</div>', unsafe_allow_html=True)
        board_view_tab, deep_dive_tab = st.tabs(["🏛️ Board View", "🔍 Deep Dive"])
        st.caption("Board View: decision-ready summary. Deep Dive: diagnostics, scenarios, and risk analytics.")

        with board_view_tab:
            st.markdown(dedent(f"""
            <div class="cxo-snapshot">
                <div class="cxo-snapshot-title">CEO Snapshot · Next 90 Days</div>
                <div class="cxo-snapshot-text">Growth remains on-track, but churn concentration in Budget and Standard segments is putting <strong>€{at_risk_revenue_m:.1f}M ARR</strong> at risk. Fast approval of targeted retention and network quality initiatives can protect ~<strong>€{protectable_arr_m:.1f}M</strong> in the next quarter.</div>
                <div class="cxo-snapshot-risk">⚠ Critical Watch: Churn Concentration + Price Pressure</div>
            </div>
            """), unsafe_allow_html=True)

            st.markdown('<div class="eo-title">North Star, Guardrails, and Value</div>', unsafe_allow_html=True)
            st.markdown(dedent(f"""
            <div class="cxo-value-grid">
                <div class="cxo-value-card" style="--accent: linear-gradient(90deg, #10B981, #34D399);">
                    <div class="cxo-value-label">North Star · Quarterly Revenue</div>
                    <div class="cxo-value-number">€{quarterly_revenue_m:.1f}M</div>
                    <div class="cxo-value-note">Run-rate aligned to growth target</div>
                </div>
                <div class="cxo-value-card" style="--accent: linear-gradient(90deg, #3B82F6, #29B5E8);">
                    <div class="cxo-value-label">Value In Flight</div>
                    <div class="cxo-value-number">€{value_in_flight_m:.1f}M</div>
                    <div class="cxo-value-note">Initiatives in execution this quarter</div>
                </div>
                <div class="cxo-value-card" style="--accent: linear-gradient(90deg, #F59E0B, #FBBF24);">
                    <div class="cxo-value-label">Guardrail · Churn</div>
                    <div class="cxo-value-number">{churn_rate:.1f}%</div>
                    <div class="cxo-value-note">Watchlist if above 2.3%</div>
                </div>
                <div class="cxo-value-card" style="--accent: linear-gradient(90deg, #EF4444, #F87171);">
                    <div class="cxo-value-label">Value At Risk</div>
                    <div class="cxo-value-number">€{at_risk_revenue_m:.1f}M</div>
                    <div class="cxo-value-note urgent">Urgent containment required in 30 days</div>
                </div>
            </div>
            """), unsafe_allow_html=True)

            st.markdown('<div class="eo-title">Network Reliability & Customer Impact</div>', unsafe_allow_html=True)
            net_col1, net_col2 = st.columns(2)

            with net_col1:
                st.markdown('<div class="eo-mini-title">Major Incidents and MTTR Trend</div>', unsafe_allow_html=True)
                with st.container(border=True):
                    incidents_line = alt.Chart(db_incident_trend).mark_line(
                        point=True,
                        strokeWidth=3,
                        color="#EF4444",
                    ).encode(
                        x=alt.X("Week:N", title=None),
                        y=alt.Y("Major Incidents:Q", title="Major Incidents"),
                        tooltip=[alt.Tooltip("Week:N"), alt.Tooltip("Major Incidents:Q")],
                    )
                    mttr_line = alt.Chart(db_incident_trend).mark_line(
                        point=True,
                        strokeWidth=3,
                        color="#29B5E8",
                    ).encode(
                        x=alt.X("Week:N", title=None),
                        y=alt.Y("MTTR Minutes:Q", title="MTTR (min)"),
                        tooltip=[alt.Tooltip("Week:N"), alt.Tooltip("MTTR Minutes:Q")],
                    )
                    st.altair_chart(
                        style_exec_chart(
                            alt.layer(incidents_line, mttr_line).resolve_scale(y="independent"),
                            height=220,
                        ),
                        use_container_width=True,
                    )
                    incident_drop = db_incident_trend["Major Incidents"].iloc[0] - db_incident_trend["Major Incidents"].iloc[-1]
                    mttr_drop = db_incident_trend["MTTR Minutes"].iloc[0] - db_incident_trend["MTTR Minutes"].iloc[-1]
                    render_ai_recommendation(
                        "Network Operations",
                        f"Major incidents improved by {incident_drop} over 6 weeks; MTTR improved by {mttr_drop} minutes.",
                        "Scale proactive fiber maintenance to the two highest-incident clusters to keep trend downward.",
                        "Protect SLA levels and reduce churn pressure in affected zones.",
                    )

            with net_col2:
                st.markdown('<div class="eo-mini-title">Region Network Score vs NPS</div>', unsafe_allow_html=True)
                with st.container(border=True):
                    net_scatter = alt.Chart(db_network_regions).mark_circle(
                        opacity=0.9,
                        stroke="#FFFFFF",
                        strokeWidth=1.4,
                    ).encode(
                        x=alt.X("Network Score:Q", title="Network Score", scale=alt.Scale(domain=[87, 96])),
                        y=alt.Y("NPS:Q", title="NPS", scale=alt.Scale(domain=[36, 56])),
                        size=alt.Size("Incidents:Q", scale=alt.Scale(range=[180, 900]), legend=None),
                        color=alt.Color("Incidents:Q", scale=alt.Scale(scheme="orangered"), legend=None),
                        tooltip=[
                            alt.Tooltip("Region:N"),
                            alt.Tooltip("Network Score:Q", format=".1f"),
                            alt.Tooltip("NPS:Q"),
                            alt.Tooltip("Incidents:Q"),
                        ],
                    )
                    net_labels = alt.Chart(db_network_regions).mark_text(dy=-12, fontSize=9, color="#1E293B").encode(
                        x="Network Score:Q",
                        y="NPS:Q",
                        text="Region:N",
                    )
                    st.altair_chart(style_exec_chart(net_scatter + net_labels, height=220), use_container_width=True)
                    weakest_region = db_network_regions.sort_values(["Network Score", "NPS"]).iloc[0]
                    render_ai_recommendation(
                        "Network Experience Link",
                        f"{weakest_region['Region']} is the weakest node with score {weakest_region['Network Score']:.1f} and NPS {int(weakest_region['NPS'])}.",
                        f"Prioritize SLA restoration and field capacity in {weakest_region['Region']} this month.",
                        "Improve NPS by 2-3 points and reduce local churn risk.",
                        level="warning",
                    )

            st.markdown('<div class="eo-title">Plan vs Actual vs Forecast</div>', unsafe_allow_html=True)
            with st.container(border=True):
                paf_df = pd.DataFrame({
                    "Stage": ["Plan", "Actual to Date", "Forecast"],
                    "Revenue": [15.0, quarterly_revenue_m, 14.6],
                    "Type": ["Plan", "Actual", "Forecast"],
                })
                paf_bar = alt.Chart(paf_df).mark_bar(cornerRadiusTopLeft=7, cornerRadiusTopRight=7, size=64).encode(
                    x=alt.X("Stage:N", title=None),
                    y=alt.Y("Revenue:Q", title="Revenue (€ M)"),
                    color=alt.Color("Type:N", scale=alt.Scale(domain=["Plan", "Actual", "Forecast"], range=["#94A3B8", "#29B5E8", "#10B981"]), legend=None),
                    tooltip=[alt.Tooltip("Stage:N"), alt.Tooltip("Revenue:Q", format=".1f")],
                )
                paf_text = alt.Chart(paf_df).mark_text(dy=-8, fontSize=11, fontWeight="bold", color="#0F172A").encode(
                    x="Stage:N",
                    y="Revenue:Q",
                    text=alt.Text("Revenue:Q", format=".1f"),
                )
                st.altair_chart(style_exec_chart(paf_bar + paf_text, height=220), use_container_width=True)
                variance = 15.0 - quarterly_revenue_m
                render_ai_recommendation(
                    "Plan Variance",
                    f"Current quarter is {variance:.1f}M below plan but forecast suggests partial recovery.",
                    "Fast-track retention and enterprise deals to close remaining plan gap.",
                    "Recover up to €0.6M against plan by quarter close.",
                    level="warning",
                )

            st.markdown('<div class="eo-title">Top Decisions for C-Level Approval</div>', unsafe_allow_html=True)
            st.markdown(dedent("""
            <div class="cxo-decision-grid">
                <div class="cxo-decision">
                    <span class="cxo-badge high">Immediate</span>
                    <div class="cxo-decision-title">Approve targeted save-offers for Budget cohort</div>
                    <div class="cxo-decision-meta"><strong>Impact:</strong> Protect €0.6M ARR<br><strong>Confidence:</strong> 78%<br><strong>Owner:</strong> CCO · <strong>ETA:</strong> 30 days</div>
                </div>
                <div class="cxo-decision">
                    <span class="cxo-badge med">Priority</span>
                    <div class="cxo-decision-title">Accelerate enterprise acquisition package</div>
                    <div class="cxo-decision-meta"><strong>Impact:</strong> +€0.8M ARR<br><strong>Confidence:</strong> 64%<br><strong>Owner:</strong> CRO · <strong>ETA:</strong> 45 days</div>
                </div>
                <div class="cxo-decision">
                    <span class="cxo-badge ok">Monitor</span>
                    <div class="cxo-decision-title">Prioritize 3 low-NPS network clusters</div>
                    <div class="cxo-decision-meta"><strong>Impact:</strong> +2.5 NPS points<br><strong>Confidence:</strong> 71%<br><strong>Owner:</strong> CTO · <strong>ETA:</strong> 60 days</div>
                </div>
            </div>
            """), unsafe_allow_html=True)

            st.markdown('<div class="eo-title">Strategic Initiatives Tracker</div>', unsafe_allow_html=True)
            st.markdown(dedent("""
            <div class="cxo-initiatives">
                <div class="cxo-initiative">
                    <div class="cxo-init-head"><div class="cxo-init-title">Retention War Room</div><span class="cxo-rag amber">At Risk</span></div>
                    <div class="cxo-init-meta">Owner: CCO · Budget used: 62% · Benefit captured: €0.42M</div>
                    <div class="cxo-progress" style="--p: 68%;"><span style="--p: 68%;"></span></div>
                    <div class="cxo-init-foot">Progress: 68% · Next Milestone: Offer rollout for Budget segment</div>
                </div>
                <div class="cxo-initiative">
                    <div class="cxo-init-head"><div class="cxo-init-title">Partner Expansion Sprint</div><span class="cxo-rag green">On Track</span></div>
                    <div class="cxo-init-meta">Owner: CRO · Budget used: 48% · Benefit captured: €2.1M</div>
                    <div class="cxo-progress" style="--p: 74%;"><span style="--p: 74%;"></span></div>
                    <div class="cxo-init-foot">Progress: 74% · Next Milestone: 125K new homes passed deployment</div>
                </div>
                <div class="cxo-initiative">
                    <div class="cxo-init-head"><div class="cxo-init-title">Network Quality Recovery Clusters</div><span class="cxo-rag red">Critical</span></div>
                    <div class="cxo-init-meta">Owner: CTO · Budget used: 39% · Benefit captured: €0.18M</div>
                    <div class="cxo-progress" style="--p: 43%;"><span style="--p: 43%;"></span></div>
                    <div class="cxo-init-foot">Progress: 43% · Next Milestone: stabilize 3 low-NPS zones</div>
                </div>
                <div class="cxo-initiative">
                    <div class="cxo-init-head"><div class="cxo-init-title">Collections and Credit Optimization</div><span class="cxo-rag green">On Track</span></div>
                    <div class="cxo-init-meta">Owner: CFO · Budget used: 54% · Benefit captured: €0.29M</div>
                    <div class="cxo-progress" style="--p: 71%;"><span style="--p: 71%;"></span></div>
                    <div class="cxo-init-foot">Progress: 71% · Next Milestone: reduce failed payments by 1.2pp</div>
                </div>
            </div>
            """), unsafe_allow_html=True)

            st.markdown('<div class="eo-title">Board Narrative</div>', unsafe_allow_html=True)
            st.markdown(dedent(f"""
            <div class="cxo-board">
                <div class="cxo-board-grid">
                    <div class="cxo-board-cell">
                        <h5>What Changed</h5>
                        <p>Revenue and homes passed improved, but partner churn intent rose due to service disruptions.</p>
                    </div>
                    <div class="cxo-board-cell">
                        <h5>Why It Changed</h5>
                        <p>Competitor fiber buildouts and network incidents in two clusters raised attrition risk.</p>
                    </div>
                    <div class="cxo-board-cell">
                        <h5>Next 30 Days</h5>
                        <p>Improve SLA performance, stabilize network hotspots, and accelerate network expansion.</p>
                    </div>
                    <div class="cxo-board-cell">
                        <h5>Expected Impact</h5>
                        <p>Protect up to €{protectable_arr_m:.1f}M ARR and improve churn by 0.2-0.3pp by next quarter.</p>
                    </div>
                </div>
            </div>
            """), unsafe_allow_html=True)

        with deep_dive_tab:
            st.markdown('<div class="eo-title">Scenario Outlook (Next 90 Days)</div>', unsafe_allow_html=True)
            sc_col1, sc_col2 = st.columns(2)

            with sc_col1:
                st.markdown('<div class="eo-mini-title">Revenue Scenarios</div>', unsafe_allow_html=True)
                scenario_df = pd.DataFrame({
                    "Scenario": ["Downside", "Base", "Upside"],
                    "Revenue": [13.9, 14.6, 15.4],
                    "Probability": ["25%", "50%", "25%"],
                })
                sc_bar = alt.Chart(scenario_df).mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6, size=52).encode(
                    x=alt.X("Scenario:N", title=None),
                    y=alt.Y("Revenue:Q", title="Projected Revenue (€ M)"),
                    color=alt.Color(
                        "Scenario:N",
                        scale=alt.Scale(domain=["Downside", "Base", "Upside"], range=["#EF4444", "#3B82F6", "#10B981"]),
                        legend=None,
                    ),
                    tooltip=[
                        alt.Tooltip("Scenario:N"),
                        alt.Tooltip("Revenue:Q", format=".1f"),
                        alt.Tooltip("Probability:N"),
                    ],
                )
                sc_label = alt.Chart(scenario_df).mark_text(dy=-8, fontSize=11, fontWeight="bold", color="#0F172A").encode(
                    x="Scenario:N",
                    y="Revenue:Q",
                    text=alt.Text("Revenue:Q", format=".1f"),
                )
                sc_prob = alt.Chart(scenario_df).mark_text(dy=16, fontSize=10, color="#475569").encode(
                    x="Scenario:N",
                    y=alt.value(0),
                    text="Probability:N",
                )
                st.altair_chart(style_exec_chart(sc_bar + sc_label + sc_prob, height=220), use_container_width=True)
                base_case = scenario_df.loc[scenario_df["Scenario"] == "Base"].iloc[0]
                render_ai_recommendation(
                    "Revenue Scenarios",
                    f"Base scenario projects €{base_case['Revenue']:.1f}M with highest probability ({base_case['Probability']}).",
                    "Commit budget to base-case plan while pre-authorizing contingency spend if downside signals trigger.",
                    "Improve forecast confidence and decision speed.",
                )

            with sc_col2:
                st.markdown('<div class="eo-mini-title">Churn Trend by Scenario</div>', unsafe_allow_html=True)
                churn_fcst = pd.DataFrame({
                    "Month": ["M+1", "M+2", "M+3", "M+1", "M+2", "M+3", "M+1", "M+2", "M+3"],
                    "Scenario": ["Downside", "Downside", "Downside", "Base", "Base", "Base", "Upside", "Upside", "Upside"],
                    "Churn": [2.4, 2.5, 2.6, 2.1, 2.0, 1.95, 1.9, 1.8, 1.7],
                })
                churn_line = alt.Chart(churn_fcst).mark_line(point=True, strokeWidth=3).encode(
                    x=alt.X("Month:N", title=None),
                    y=alt.Y("Churn:Q", title="Projected Churn %", scale=alt.Scale(domain=[1.6, 2.7])),
                    color=alt.Color(
                        "Scenario:N",
                        scale=alt.Scale(domain=["Downside", "Base", "Upside"], range=["#EF4444", "#3B82F6", "#10B981"]),
                        legend=alt.Legend(title=None),
                    ),
                    tooltip=[
                        alt.Tooltip("Scenario:N"),
                        alt.Tooltip("Month:N"),
                        alt.Tooltip("Churn:Q", format=".2f"),
                    ],
                )
                st.altair_chart(style_exec_chart(churn_line, height=220), use_container_width=True)
                upside_m3 = churn_fcst[(churn_fcst["Scenario"] == "Upside") & (churn_fcst["Month"] == "M+3")]["Churn"].iloc[0]
                downside_m3 = churn_fcst[(churn_fcst["Scenario"] == "Downside") & (churn_fcst["Month"] == "M+3")]["Churn"].iloc[0]
                render_ai_recommendation(
                    "Churn Forecast",
                    f"M+3 churn ranges from {upside_m3:.2f}% (upside) to {downside_m3:.2f}% (downside).",
                    "Execute retention playbooks early to steer trajectory toward upside path.",
                    "Potentially avoid ~0.9pp churn deterioration in downside scenario.",
                    level="warning",
                )

            st.markdown('<div class="eo-title">Risk Radar and Leading Indicators</div>', unsafe_allow_html=True)
            rr_col1, rr_col2 = st.columns(2)

            with rr_col1:
                st.markdown('<div class="eo-mini-title">Risk Radar</div>', unsafe_allow_html=True)
                risk_radar_df = pd.DataFrame({
                    "Risk": ["Churn concentration", "Price war", "Network SLA", "Collections", "Brand perception"],
                    "Likelihood": [4.2, 3.9, 3.2, 2.9, 2.7],
                    "Impact": [4.6, 4.0, 4.4, 3.1, 3.3],
                    "Exposure": [2.4, 1.6, 1.9, 0.8, 0.7],
                })
                risk_scatter = alt.Chart(risk_radar_df).mark_circle(opacity=0.88, stroke="#FFFFFF", strokeWidth=1.4).encode(
                    x=alt.X("Likelihood:Q", title="Likelihood (1-5)", scale=alt.Scale(domain=[2.2, 4.6])),
                    y=alt.Y("Impact:Q", title="Impact (1-5)", scale=alt.Scale(domain=[2.8, 4.9])),
                    size=alt.Size("Exposure:Q", title="Exposure (€ M)", scale=alt.Scale(range=[180, 1500])),
                    color=alt.Color("Exposure:Q", scale=alt.Scale(scheme="redpurple"), legend=None),
                    tooltip=[
                        alt.Tooltip("Risk:N"),
                        alt.Tooltip("Likelihood:Q", format=".1f"),
                        alt.Tooltip("Impact:Q", format=".1f"),
                        alt.Tooltip("Exposure:Q", title="Exposure (€ M)", format=".1f"),
                    ],
                )
                risk_labels = alt.Chart(risk_radar_df).mark_text(dy=-11, fontSize=9, color="#1E293B").encode(
                    x="Likelihood:Q",
                    y="Impact:Q",
                    text="Risk:N",
                )
                st.altair_chart(style_exec_chart(risk_scatter + risk_labels, height=235), use_container_width=True)
                top_exposure = risk_radar_df.loc[risk_radar_df["Exposure"].idxmax()]
                render_ai_recommendation(
                    "Risk Radar",
                    f"Highest financial exposure is {top_exposure['Risk']} (€{top_exposure['Exposure']:.1f}M) with high impact/likelihood.",
                    f"Create executive mitigation track for {top_exposure['Risk']} with weekly progress checkpoints.",
                    "Reduce downside exposure and strengthen board-level risk posture.",
                    level="critical",
                )

            with rr_col2:
                st.markdown('<div class="eo-mini-title">Leading Indicators</div>', unsafe_allow_html=True)
                lead_df = pd.DataFrame({
                    "Indicator": ["Downgrade requests", "Payment failure rate", "NOC repeat incidents", "Support backlog age", "Churn intent score"],
                    "Delta": [18, 11, 9, 14, 21],
                    "Status": ["Watch", "Watch", "Stable", "Watch", "Critical"],
                })
                lead_bar = alt.Chart(lead_df).mark_bar(cornerRadiusTopRight=6, cornerRadiusBottomRight=6, size=18).encode(
                    x=alt.X("Delta:Q", title="Change vs baseline (%)", scale=alt.Scale(domain=[0, 24])),
                    y=alt.Y("Indicator:N", sort="-x", title=None),
                    color=alt.Color(
                        "Status:N",
                        scale=alt.Scale(domain=["Stable", "Watch", "Critical"], range=["#10B981", "#F59E0B", "#EF4444"]),
                        legend=alt.Legend(title=None),
                    ),
                    tooltip=[
                        alt.Tooltip("Indicator:N"),
                        alt.Tooltip("Delta:Q", title="Change %"),
                        alt.Tooltip("Status:N"),
                    ],
                )
                lead_text = alt.Chart(lead_df).mark_text(align="left", dx=6, fontSize=10, color="#0F172A").encode(
                    x="Delta:Q",
                    y=alt.Y("Indicator:N", sort="-x"),
                    text=alt.Text("Delta:Q", format=".0f"),
                )
                st.altair_chart(style_exec_chart(lead_bar + lead_text, height=235), use_container_width=True)
                top_lead = lead_df.loc[lead_df["Delta"].idxmax()]
                render_ai_recommendation(
                    "Leading Indicators",
                    f"The fastest-deteriorating signal is {top_lead['Indicator']} (+{top_lead['Delta']:.0f}%).",
                    "Set an automated early-warning threshold and route alert to owner squad immediately.",
                    "Cut reaction time and prevent escalation into churn/revenue loss.",
                    level="warning" if top_lead["Status"] != "Critical" else "critical",
                )

# ---------------------------------------------------------------------------
# Page: JV Board View (Wholesale Fiberco Economics)
# ---------------------------------------------------------------------------
elif selected_menu == "JV Board View":
    import pandas as pd
    import altair as alt
    import pydeck as pdk

    JV_CHART_THEME = {
        "font": "Poppins, sans-serif",
        "title_color": "#0F172A",
        "label_color": "#334155",
        "grid_color": "#E2E8F0",
        "masorange": "#FF6B00",
        "vodafone": "#E60000",
        "accent_blue": "#29B5E8",
        "accent_green": "#10B981",
    }

    def style_jv_chart(chart: alt.Chart, height: int = 220) -> alt.Chart:
        return (
            chart.properties(height=height, padding={"left": 6, "top": 10, "right": 8, "bottom": 6})
            .configure(background="#FFFFFF")
            .configure_view(stroke=None)
            .configure_axis(
                labelFont=JV_CHART_THEME["font"], titleFont=JV_CHART_THEME["font"],
                labelColor=JV_CHART_THEME["label_color"], titleColor=JV_CHART_THEME["title_color"],
                gridColor=JV_CHART_THEME["grid_color"], domainColor=JV_CHART_THEME["grid_color"],
                labelFontSize=10, titleFontSize=11, titleFontWeight=600,
            )
            .configure_legend(labelFont=JV_CHART_THEME["font"], titleFont=JV_CHART_THEME["font"], labelFontSize=10)
        )

    def render_jv_ai_reco(title: str, insight: str, action: str, outcome: str, level: str = "info"):
        color_map = {"info": ("#29B5E8", "#EBF8FF", "#0C4A6E"), "warning": ("#F59E0B", "#FFFBEB", "#92400E"), "critical": ("#EF4444", "#FEF2F2", "#991B1B")}
        accent, bg, text = color_map.get(level, color_map["info"])
        st.markdown(f"""<div style="background: {bg}; border-left: 4px solid {accent}; border-radius: 8px; padding: 0.65rem 0.85rem; margin-top: 0.5rem;">
            <div style="font-weight: 700; color: {text}; font-size: 0.78rem; margin-bottom: 0.2rem;">🤖 {title}</div>
            <div style="color: #334155; font-size: 0.76rem; line-height: 1.4;"><strong>Insight:</strong> {insight}</div>
            <div style="color: #334155; font-size: 0.76rem; line-height: 1.4;"><strong>Action:</strong> {action}</div>
            <div style="color: #059669; font-size: 0.74rem; margin-top: 0.2rem;"><strong>Outcome:</strong> {outcome}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("""<style>
.jv-title { font-size: 1.15rem; font-weight: 800; color: #0F172A; margin: 1.2rem 0 0.6rem; border-bottom: 2px solid #E2E8F0; padding-bottom: 0.4rem; }
.jv-mini-title { font-size: 0.88rem; font-weight: 700; color: #334155; margin-bottom: 0.5rem; }
.jv-pulse { background: linear-gradient(135deg, #003366 0%, #001a33 100%); border-radius: 14px; padding: 1.1rem 1.3rem; margin-bottom: 1rem; }
.jv-pulse-head { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.8rem; }
.jv-pulse-title { color: #FFFFFF; font-size: 1rem; font-weight: 700; }
.jv-pulse-live { background: #10B981; color: white; padding: 2px 10px; border-radius: 12px; font-size: 0.68rem; font-weight: 700; }
.jv-pulse-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 0.8rem; }
.jv-pulse-card { background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.12); border-radius: 10px; padding: 0.7rem; text-align: center; }
.jv-pulse-label { color: rgba(255,255,255,0.7); font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.03em; }
.jv-pulse-value { color: #FFFFFF; font-size: 1.4rem; font-weight: 800; margin-top: 0.15rem; }
.jv-pulse-delta { color: #10B981; font-size: 0.72rem; font-weight: 600; margin-top: 0.1rem; }
.jv-owner-badge { display: inline-block; padding: 3px 10px; border-radius: 12px; font-size: 0.72rem; font-weight: 700; margin-right: 6px; }
.jv-owner-masorange { background: #FF6B00; color: white; }
.jv-owner-vodafone { background: #E60000; color: white; }
.jv-owner-gic { background: #6366F1; color: white; }
@media (max-width: 980px) { .jv-pulse-grid { grid-template-columns: repeat(3, 1fr); } }
</style>""", unsafe_allow_html=True)

    jv_homes_passed = 12_000_000
    jv_homes_connected = 5_000_000
    jv_take_rate = round(jv_homes_connected / jv_homes_passed * 100, 1)
    jv_monthly_revenue_m = 17.8
    jv_ebitda_margin = 42.3
    jv_capex_deployed_m = 892
    jv_capex_planned_m = 156

    jv_cluster_df = pd.DataFrame({
        "Cluster": ["Madrid Centro", "Barcelona", "Valencia", "Sevilla", "Málaga", "Bilbao", "Zaragoza", "Murcia", "Palma", "Alicante", "Granada", "Santander"],
        "Homes Passed K": [1850, 1620, 980, 720, 640, 580, 520, 480, 420, 390, 340, 280],
        "MasOrange Connected K": [680, 590, 360, 265, 235, 214, 192, 177, 155, 144, 125, 103],
        "Vodafone Connected K": [485, 420, 257, 189, 168, 152, 137, 126, 110, 103, 89, 74],
        "Take Rate %": [63.0, 62.3, 63.0, 63.1, 63.0, 63.1, 63.3, 63.1, 63.1, 63.3, 62.9, 63.2],
        "ARPU MasOrange": [3.52, 3.48, 3.45, 3.42, 3.40, 3.55, 3.50, 3.38, 3.62, 3.44, 3.41, 3.58],
        "ARPU Vodafone": [3.60, 3.55, 3.52, 3.48, 3.46, 3.62, 3.58, 3.45, 3.70, 3.50, 3.48, 3.65],
        "Capex Deployed M": [142, 124, 75, 55, 49, 44, 40, 37, 32, 30, 26, 21],
        "Capex Planned M": [18, 22, 14, 12, 11, 10, 9, 8, 7, 6, 5, 4],
        "NPV M": [89, 78, 47, 35, 31, 28, 25, 23, 20, 19, 16, 13],
        "Payback Months": [38, 40, 42, 44, 45, 43, 44, 46, 42, 44, 47, 45],
        "lat": [40.4168, 41.3874, 39.4699, 37.3891, 36.7213, 43.2630, 41.6488, 37.9922, 39.5696, 38.3452, 37.1773, 43.4623],
        "lon": [-3.7038, 2.1686, -0.3763, -5.9845, -4.4214, -2.9350, -0.8891, -1.1307, 2.6502, -0.4810, -3.5986, -3.8100],
    })
    jv_cluster_df["Total Connected K"] = jv_cluster_df["MasOrange Connected K"] + jv_cluster_df["Vodafone Connected K"]
    jv_cluster_df["MasOrange Share %"] = (jv_cluster_df["MasOrange Connected K"] / jv_cluster_df["Total Connected K"] * 100).round(1)
    jv_cluster_df["Vodafone Share %"] = (jv_cluster_df["Vodafone Connected K"] / jv_cluster_df["Total Connected K"] * 100).round(1)
    jv_cluster_df["Monthly Revenue K"] = (jv_cluster_df["MasOrange Connected K"] * jv_cluster_df["ARPU MasOrange"] + jv_cluster_df["Vodafone Connected K"] * jv_cluster_df["ARPU Vodafone"]).round(0)

    jv_ownership = pd.DataFrame({
        "Owner": ["MasOrange", "Vodafone España", "GIC"],
        "Stake %": [58, 17, 25],
        "Type": ["Operator + Investor", "Operator + Investor", "Financial Investor"],
        "Is Tenant": ["Yes", "Yes", "No"],
        "Monthly Revenue Share K": [round(jv_monthly_revenue_m * 1000 * 0.58), round(jv_monthly_revenue_m * 1000 * 0.17), round(jv_monthly_revenue_m * 1000 * 0.25)],
    })

    jv_build_priority = pd.DataFrame({
        "Zone": ["Madrid Este", "Barcelona Nord", "Valencia Sur", "Sevilla Este", "Málaga Costa", "Bilbao Sur"],
        "Homes Target K": [85, 72, 54, 42, 38, 32],
        "Capex Required M": [12.8, 10.9, 8.1, 6.3, 5.7, 4.8],
        "Projected Take Rate %": [58, 55, 52, 50, 48, 54],
        "NPV M": [8.2, 6.8, 4.9, 3.6, 3.1, 2.9],
        "Payback Months": [36, 38, 42, 46, 48, 40],
        "Priority Score": [92, 88, 82, 76, 72, 84],
        "MasOrange Demand": ["High", "High", "Medium", "Medium", "Low", "High"],
        "Vodafone Demand": ["High", "Medium", "High", "Low", "Medium", "Medium"],
    })

    jv_scenario_df = pd.DataFrame({
        "Scenario": ["Conservative", "Base Case", "Aggressive"],
        "New Homes K": [120, 180, 260],
        "Capex M": [36, 54, 78],
        "NPV M": [18, 32, 48],
        "IRR %": [12.4, 15.8, 18.2],
        "Payback Months": [48, 42, 36],
        "Probability": ["25%", "50%", "25%"],
    })

    total_masorange = jv_cluster_df["MasOrange Connected K"].sum()
    total_vodafone = jv_cluster_df["Vodafone Connected K"].sum()
    blended_arpu = round((total_masorange * jv_cluster_df["ARPU MasOrange"].mean() + total_vodafone * jv_cluster_df["ARPU Vodafone"].mean()) / (total_masorange + total_vodafone), 2)

    st.markdown(f"""
    <div class="jv-pulse">
        <div class="jv-pulse-head">
            <span class="jv-pulse-title">📊 JV Economics · Wholesale Fiberco Dashboard</span>
            <span class="jv-pulse-live">Live</span>
        </div>
        <div style="margin-bottom: 0.6rem;">
            <span class="jv-owner-badge jv-owner-masorange">MasOrange 58%</span>
            <span class="jv-owner-badge jv-owner-vodafone">Vodafone 17%</span>
            <span class="jv-owner-badge jv-owner-gic">GIC 25%</span>
        </div>
        <div class="jv-pulse-grid">
            <div class="jv-pulse-card">
                <div class="jv-pulse-label">Homes Passed</div>
                <div class="jv-pulse-value">{jv_homes_passed / 1_000_000:.1f}M</div>
                <div class="jv-pulse-delta">+156K planned</div>
            </div>
            <div class="jv-pulse-card">
                <div class="jv-pulse-label">Homes Connected</div>
                <div class="jv-pulse-value">{jv_homes_connected / 1_000_000:.1f}M</div>
                <div class="jv-pulse-delta">{jv_take_rate}% take rate</div>
            </div>
            <div class="jv-pulse-card">
                <div class="jv-pulse-label">Monthly Revenue</div>
                <div class="jv-pulse-value">€{jv_monthly_revenue_m}M</div>
                <div class="jv-pulse-delta">↑ +3.2% MoM</div>
            </div>
            <div class="jv-pulse-card">
                <div class="jv-pulse-label">EBITDA Margin</div>
                <div class="jv-pulse-value">{jv_ebitda_margin}%</div>
                <div class="jv-pulse-delta">Above target</div>
            </div>
            <div class="jv-pulse-card">
                <div class="jv-pulse-label">Blended ARPU</div>
                <div class="jv-pulse-value">€{blended_arpu}</div>
                <div class="jv-pulse-delta">Per line/month</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    jv_tab_clusters, jv_tab_build, jv_tab_scenarios = st.tabs(["🗺️ Cluster Economics", "🏗️ Build Prioritization", "📈 Investment Scenarios"])

    with jv_tab_clusters:
        st.markdown('<div class="jv-title">Cluster-Level Performance by Tenant</div>', unsafe_allow_html=True)
        cl_col1, cl_col2 = st.columns(2)

        with cl_col1:
            st.markdown('<div class="jv-mini-title">Homes Connected by Tenant</div>', unsafe_allow_html=True)
            with st.container(border=True):
                cluster_long = jv_cluster_df.melt(id_vars=["Cluster"], value_vars=["MasOrange Connected K", "Vodafone Connected K"], var_name="Tenant", value_name="Connected K")
                cluster_long["Tenant"] = cluster_long["Tenant"].str.replace(" Connected K", "")
                tenant_bar = alt.Chart(cluster_long).mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4).encode(
                    x=alt.X("Cluster:N", title=None, sort="-y"),
                    y=alt.Y("Connected K:Q", title="Homes Connected (K)"),
                    color=alt.Color("Tenant:N", scale=alt.Scale(domain=["MasOrange", "Vodafone"], range=["#FF6B00", "#E60000"]), legend=alt.Legend(title=None)),
                    xOffset="Tenant:N",
                    tooltip=["Cluster:N", "Tenant:N", alt.Tooltip("Connected K:Q", format=",.0f")],
                )
                st.altair_chart(style_jv_chart(tenant_bar, height=260), use_container_width=True)
                render_jv_ai_reco(
                    "Tenant Distribution",
                    f"MasOrange has {round(total_masorange/(total_masorange+total_vodafone)*100)}% of connected homes, aligned with ownership stake.",
                    "Monitor cluster-level imbalances to ensure fair network utilization per tenant agreement.",
                    "Maintain JV governance alignment and prevent tenant disputes.",
                )

        with cl_col2:
            st.markdown('<div class="jv-mini-title">ARPU by Tenant and Cluster</div>', unsafe_allow_html=True)
            with st.container(border=True):
                arpu_long = jv_cluster_df.melt(id_vars=["Cluster"], value_vars=["ARPU MasOrange", "ARPU Vodafone"], var_name="Tenant", value_name="ARPU")
                arpu_long["Tenant"] = arpu_long["Tenant"].str.replace("ARPU ", "")
                arpu_line = alt.Chart(arpu_long).mark_line(point=True, strokeWidth=2.5).encode(
                    x=alt.X("Cluster:N", title=None),
                    y=alt.Y("ARPU:Q", title="ARPU (€)", scale=alt.Scale(domain=[3.3, 3.75])),
                    color=alt.Color("Tenant:N", scale=alt.Scale(domain=["MasOrange", "Vodafone"], range=["#FF6B00", "#E60000"]), legend=alt.Legend(title=None)),
                    tooltip=["Cluster:N", "Tenant:N", alt.Tooltip("ARPU:Q", format=".2f")],
                )
                st.altair_chart(style_jv_chart(arpu_line, height=260), use_container_width=True)
                avg_mo = jv_cluster_df["ARPU MasOrange"].mean()
                avg_vf = jv_cluster_df["ARPU Vodafone"].mean()
                render_jv_ai_reco(
                    "ARPU Analysis",
                    f"Vodafone ARPU (€{avg_vf:.2f}) is {((avg_vf-avg_mo)/avg_mo*100):.1f}% higher than MasOrange (€{avg_mo:.2f}).",
                    "Investigate product mix differences; consider whether MasOrange can migrate to higher-value tiers.",
                    "Increase blended ARPU and JV revenue per line.",
                )

        st.markdown('<div class="jv-title">Cluster Investment Economics</div>', unsafe_allow_html=True)
        cl_col3, cl_col4 = st.columns(2)

        with cl_col3:
            st.markdown('<div class="jv-mini-title">NPV vs Payback by Cluster</div>', unsafe_allow_html=True)
            with st.container(border=True):
                npv_scatter = alt.Chart(jv_cluster_df).mark_circle(opacity=0.85, stroke="#FFFFFF", strokeWidth=1.2).encode(
                    x=alt.X("Payback Months:Q", title="Payback (months)", scale=alt.Scale(domain=[36, 50])),
                    y=alt.Y("NPV M:Q", title="NPV (€ M)"),
                    size=alt.Size("Homes Passed K:Q", scale=alt.Scale(range=[200, 1200]), legend=None),
                    color=alt.Color("Take Rate %:Q", scale=alt.Scale(scheme="blues"), legend=alt.Legend(title="Take Rate %")),
                    tooltip=["Cluster:N", alt.Tooltip("NPV M:Q", format=".1f"), alt.Tooltip("Payback Months:Q"), alt.Tooltip("Homes Passed K:Q", format=","), alt.Tooltip("Take Rate %:Q", format=".1f")],
                )
                npv_labels = alt.Chart(jv_cluster_df.head(6)).mark_text(dy=-10, fontSize=9, color="#1E293B").encode(
                    x="Payback Months:Q", y="NPV M:Q", text="Cluster:N"
                )
                st.altair_chart(style_jv_chart(npv_scatter + npv_labels, height=260), use_container_width=True)
                best_cluster = jv_cluster_df.sort_values("NPV M", ascending=False).iloc[0]
                render_jv_ai_reco(
                    "Investment Returns",
                    f"{best_cluster['Cluster']} delivers highest NPV (€{best_cluster['NPV M']:.0f}M) with {best_cluster['Payback Months']} month payback.",
                    "Prioritize incremental build-out in high-NPV clusters before expanding to new territories.",
                    "Maximize JV returns and accelerate investor payback.",
                )

        with cl_col4:
            st.markdown('<div class="jv-mini-title">Capex Deployed vs Planned</div>', unsafe_allow_html=True)
            with st.container(border=True):
                capex_long = jv_cluster_df.melt(id_vars=["Cluster"], value_vars=["Capex Deployed M", "Capex Planned M"], var_name="Type", value_name="Capex M")
                capex_bar = alt.Chart(capex_long).mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4).encode(
                    x=alt.X("Cluster:N", title=None, sort=alt.EncodingSortField(field="Capex M", order="descending")),
                    y=alt.Y("Capex M:Q", title="Capex (€ M)"),
                    color=alt.Color("Type:N", scale=alt.Scale(domain=["Capex Deployed M", "Capex Planned M"], range=["#29B5E8", "#10B981"]), legend=alt.Legend(title=None)),
                    xOffset="Type:N",
                    tooltip=["Cluster:N", "Type:N", alt.Tooltip("Capex M:Q", format=".1f")],
                )
                st.altair_chart(style_jv_chart(capex_bar, height=260), use_container_width=True)
                total_deployed = jv_cluster_df["Capex Deployed M"].sum()
                total_planned = jv_cluster_df["Capex Planned M"].sum()
                render_jv_ai_reco(
                    "Capex Utilization",
                    f"€{total_deployed}M deployed, €{total_planned}M planned ({round(total_planned/(total_deployed+total_planned)*100)}% of total pipeline).",
                    "Ensure planned capex aligns with tenant demand signals and NPV thresholds.",
                    "Optimize capital allocation across JV build program.",
                )

    with jv_tab_build:
        st.markdown('<div class="jv-title">Build Prioritization Matrix</div>', unsafe_allow_html=True)

        bp_col1, bp_col2 = st.columns(2)
        with bp_col1:
            st.markdown('<div class="jv-mini-title">Priority Score vs NPV</div>', unsafe_allow_html=True)
            with st.container(border=True):
                priority_bar = alt.Chart(jv_build_priority).mark_bar(cornerRadiusTopRight=6, cornerRadiusBottomRight=6, size=22).encode(
                    x=alt.X("Priority Score:Q", title="Priority Score"),
                    y=alt.Y("Zone:N", sort="-x", title=None),
                    color=alt.Color("NPV M:Q", scale=alt.Scale(scheme="blues"), legend=alt.Legend(title="NPV (€M)")),
                    tooltip=["Zone:N", "Priority Score:Q", alt.Tooltip("NPV M:Q", format=".1f"), alt.Tooltip("Homes Target K:Q", format=","), alt.Tooltip("Payback Months:Q")],
                )
                st.altair_chart(style_jv_chart(priority_bar, height=240), use_container_width=True)
                top_zone = jv_build_priority.sort_values("Priority Score", ascending=False).iloc[0]
                render_jv_ai_reco(
                    "Build Priority",
                    f"{top_zone['Zone']} has highest priority score ({top_zone['Priority Score']}) with €{top_zone['NPV M']}M NPV.",
                    "Fast-track permitting and contractor allocation for top-priority zones.",
                    "Accelerate high-return deployments and improve JV cash flow.",
                )

        with bp_col2:
            st.markdown('<div class="jv-mini-title">Tenant Demand by Zone</div>', unsafe_allow_html=True)
            with st.container(border=True):
                demand_df = jv_build_priority.melt(id_vars=["Zone"], value_vars=["MasOrange Demand", "Vodafone Demand"], var_name="Tenant", value_name="Demand")
                demand_df["Tenant"] = demand_df["Tenant"].str.replace(" Demand", "")
                demand_df["Demand Score"] = demand_df["Demand"].map({"High": 3, "Medium": 2, "Low": 1})
                demand_heat = alt.Chart(demand_df).mark_rect(cornerRadius=4).encode(
                    x=alt.X("Tenant:N", title=None),
                    y=alt.Y("Zone:N", title=None),
                    color=alt.Color("Demand Score:Q", scale=alt.Scale(domain=[1, 3], range=["#FEF3C7", "#F59E0B", "#DC2626"]), legend=None),
                    tooltip=["Zone:N", "Tenant:N", "Demand:N"],
                )
                demand_text = alt.Chart(demand_df).mark_text(fontSize=10, fontWeight="bold").encode(
                    x="Tenant:N", y="Zone:N", text="Demand:N",
                    color=alt.condition(alt.datum["Demand Score"] == 3, alt.value("white"), alt.value("#1E293B"))
                )
                st.altair_chart(style_jv_chart(demand_heat + demand_text, height=240), use_container_width=True)
                render_jv_ai_reco(
                    "Demand Alignment",
                    "MasOrange shows high demand in Madrid/Barcelona/Bilbao; Vodafone prioritizes Valencia.",
                    "Coordinate build sequencing with tenant commercial teams to maximize early take-up.",
                    "Improve time-to-revenue and reduce idle network capacity.",
                )

        st.markdown('<div class="jv-title">Build Program Economics</div>', unsafe_allow_html=True)
        with st.container(border=True):
            st.dataframe(
                jv_build_priority.style.format({
                    "Homes Target K": "{:,.0f}",
                    "Capex Required M": "€{:.1f}M",
                    "Projected Take Rate %": "{:.0f}%",
                    "NPV M": "€{:.1f}M",
                    "Payback Months": "{:.0f}",
                    "Priority Score": "{:.0f}",
                }).background_gradient(subset=["Priority Score"], cmap="Blues"),
                use_container_width=True,
                hide_index=True,
            )

    with jv_tab_scenarios:
        st.markdown('<div class="jv-title">Investment Scenario Analysis</div>', unsafe_allow_html=True)

        sc_col1, sc_col2 = st.columns(2)
        with sc_col1:
            st.markdown('<div class="jv-mini-title">NPV vs IRR by Scenario</div>', unsafe_allow_html=True)
            with st.container(border=True):
                scenario_scatter = alt.Chart(jv_scenario_df).mark_circle(opacity=0.9, stroke="#FFFFFF", strokeWidth=1.5, size=400).encode(
                    x=alt.X("IRR %:Q", title="IRR (%)", scale=alt.Scale(domain=[10, 20])),
                    y=alt.Y("NPV M:Q", title="NPV (€ M)"),
                    color=alt.Color("Scenario:N", scale=alt.Scale(domain=["Conservative", "Base Case", "Aggressive"], range=["#94A3B8", "#29B5E8", "#10B981"]), legend=alt.Legend(title=None)),
                    tooltip=["Scenario:N", alt.Tooltip("NPV M:Q", format=".1f"), alt.Tooltip("IRR %:Q", format=".1f"), "New Homes K:Q", alt.Tooltip("Capex M:Q", format=".1f"), "Probability:N"],
                )
                scenario_labels = alt.Chart(jv_scenario_df).mark_text(dy=-14, fontSize=10, fontWeight="bold", color="#1E293B").encode(
                    x="IRR %:Q", y="NPV M:Q", text="Scenario:N"
                )
                st.altair_chart(style_jv_chart(scenario_scatter + scenario_labels, height=240), use_container_width=True)
                base_case = jv_scenario_df[jv_scenario_df["Scenario"] == "Base Case"].iloc[0]
                render_jv_ai_reco(
                    "Scenario Outlook",
                    f"Base case yields €{base_case['NPV M']}M NPV at {base_case['IRR %']}% IRR with 50% probability.",
                    "Board should approve base case with contingency triggers for aggressive expansion if take-up exceeds plan.",
                    "Balanced risk-return approach with upside optionality.",
                )

        with sc_col2:
            st.markdown('<div class="jv-mini-title">Capex vs Payback Trade-off</div>', unsafe_allow_html=True)
            with st.container(border=True):
                tradeoff_bar = alt.Chart(jv_scenario_df).mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6, size=50).encode(
                    x=alt.X("Scenario:N", title=None),
                    y=alt.Y("Capex M:Q", title="Capex (€ M)"),
                    color=alt.Color("Scenario:N", scale=alt.Scale(domain=["Conservative", "Base Case", "Aggressive"], range=["#94A3B8", "#29B5E8", "#10B981"]), legend=None),
                    tooltip=["Scenario:N", alt.Tooltip("Capex M:Q", format=".1f"), alt.Tooltip("Payback Months:Q"), alt.Tooltip("New Homes K:Q", format=",")],
                )
                payback_line = alt.Chart(jv_scenario_df).mark_line(point=True, strokeWidth=3, color="#F59E0B").encode(
                    x=alt.X("Scenario:N", title=None),
                    y=alt.Y("Payback Months:Q", title="Payback (months)"),
                    tooltip=["Scenario:N", "Payback Months:Q"],
                )
                st.altair_chart(style_jv_chart(alt.layer(tradeoff_bar, payback_line).resolve_scale(y="independent"), height=240), use_container_width=True)
                render_jv_ai_reco(
                    "Capital Efficiency",
                    "Aggressive scenario requires 2.2x more capex but delivers 2.7x higher NPV.",
                    "If financing conditions remain favorable, consider phased aggressive approach.",
                    "Maximize long-term JV value creation for all shareholders.",
                    level="warning",
                )

        st.markdown('<div class="jv-title">Scenario Summary Table</div>', unsafe_allow_html=True)
        with st.container(border=True):
            st.dataframe(
                jv_scenario_df.style.format({
                    "New Homes K": "{:,.0f}",
                    "Capex M": "€{:.0f}M",
                    "NPV M": "€{:.0f}M",
                    "IRR %": "{:.1f}%",
                    "Payback Months": "{:.0f}",
                }).background_gradient(subset=["NPV M"], cmap="Greens"),
                use_container_width=True,
                hide_index=True,
            )

    st.markdown("""
    <details style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 0.8rem; margin-top: 1rem;">
        <summary style="cursor: pointer; font-weight: 600; color: #334155; font-size: 0.9rem;">▸ Data Sources & Systems</summary>
        <div style="margin-top: 0.8rem; font-size: 0.85rem; color: #475569;">
            <p><strong>This dashboard aggregates data from the following source systems:</strong></p>
            <table style="width: 100%; border-collapse: collapse; margin: 0.5rem 0;">
                <tr style="border-bottom: 1px solid #E2E8F0;"><th style="text-align: left; padding: 0.4rem;">Data Element</th><th style="text-align: left; padding: 0.4rem;">Source System</th><th style="text-align: left; padding: 0.4rem;">Refresh</th></tr>
                <tr><td style="padding: 0.4rem;">Homes Passed / Connected</td><td style="padding: 0.4rem;"><strong>Network Inventory System (NIS)</strong></td><td style="padding: 0.4rem;">Daily</td></tr>
                <tr><td style="padding: 0.4rem;">Partner ownership stakes</td><td style="padding: 0.4rem;"><strong>SAP S/4HANA Finance</strong> - JV Accounting</td><td style="padding: 0.4rem;">Monthly</td></tr>
                <tr><td style="padding: 0.4rem;">Revenue & ARPU metrics</td><td style="padding: 0.4rem;"><strong>Oracle Revenue Management</strong></td><td style="padding: 0.4rem;">Daily</td></tr>
                <tr><td style="padding: 0.4rem;">CAPEX/OPEX figures</td><td style="padding: 0.4rem;"><strong>SAP S/4HANA Controlling</strong></td><td style="padding: 0.4rem;">Monthly</td></tr>
                <tr><td style="padding: 0.4rem;">Fiber deployment clusters</td><td style="padding: 0.4rem;"><strong>GIS Platform (ESRI ArcGIS)</strong></td><td style="padding: 0.4rem;">Weekly</td></tr>
                <tr><td style="padding: 0.4rem;">Connection growth trends</td><td style="padding: 0.4rem;"><strong>CRM (Salesforce)</strong> + Provisioning</td><td style="padding: 0.4rem;">Daily</td></tr>
            </table>
            <p><strong>Key Integrations:</strong></p>
            <ul style="margin: 0.3rem 0; padding-left: 1.2rem;">
                <li>JV partner data via <strong>EDI/API</strong> with MasOrange and Vodafone finance</li>
                <li>Cluster geography from <strong>INE</strong> for population metrics</li>
                <li>Infrastructure valuations from <strong>independent auditor reports</strong> (annual)</li>
            </ul>
        </div>
    </details>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Page: Tenant SLA Dashboard (Wholesale Service Quality)
# ---------------------------------------------------------------------------
elif selected_menu == "Tenant SLA":
    import pandas as pd
    import altair as alt

    SLA_CHART_THEME = {
        "font": "Poppins, sans-serif",
        "masorange": "#FF6B00",
        "vodafone": "#E60000",
    }

    def style_sla_chart(chart: alt.Chart, height: int = 220) -> alt.Chart:
        return (
            chart.properties(height=height, padding={"left": 6, "top": 10, "right": 8, "bottom": 6})
            .configure(background="#FFFFFF")
            .configure_view(stroke=None)
            .configure_axis(labelFontSize=10, titleFontSize=11, gridColor="#E2E8F0", domainColor="#E2E8F0")
            .configure_legend(labelFontSize=10)
        )

    def render_sla_ai_reco(title: str, insight: str, action: str, outcome: str, level: str = "info"):
        color_map = {"info": ("#29B5E8", "#EBF8FF", "#0C4A6E"), "warning": ("#F59E0B", "#FFFBEB", "#92400E"), "critical": ("#EF4444", "#FEF2F2", "#991B1B")}
        accent, bg, text = color_map.get(level, color_map["info"])
        st.markdown(f"""<div style="background: {bg}; border-left: 4px solid {accent}; border-radius: 8px; padding: 0.65rem 0.85rem; margin-top: 0.5rem;">
            <div style="font-weight: 700; color: {text}; font-size: 0.78rem; margin-bottom: 0.2rem;">🤖 {title}</div>
            <div style="color: #334155; font-size: 0.76rem; line-height: 1.4;"><strong>Insight:</strong> {insight}</div>
            <div style="color: #334155; font-size: 0.76rem; line-height: 1.4;"><strong>Action:</strong> {action}</div>
            <div style="color: #059669; font-size: 0.74rem; margin-top: 0.2rem;"><strong>Outcome:</strong> {outcome}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("""<style>
.sla-title { font-size: 1.15rem; font-weight: 800; color: #0F172A; margin: 1.2rem 0 0.6rem; border-bottom: 2px solid #E2E8F0; padding-bottom: 0.4rem; }
.sla-mini-title { font-size: 0.88rem; font-weight: 700; color: #334155; margin-bottom: 0.5rem; }
.sla-pulse { background: linear-gradient(135deg, #1E3A8A 0%, #1E40AF 100%); border-radius: 14px; padding: 1.1rem 1.3rem; margin-bottom: 1rem; }
.sla-pulse-head { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.8rem; }
.sla-pulse-title { color: #FFFFFF; font-size: 1rem; font-weight: 700; }
.sla-tenant-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
.sla-tenant-card { background: rgba(255,255,255,0.1); border-radius: 12px; padding: 1rem; border: 1px solid rgba(255,255,255,0.15); }
.sla-tenant-header { display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.6rem; }
.sla-tenant-name { color: white; font-size: 1.1rem; font-weight: 700; }
.sla-tenant-badge { padding: 2px 8px; border-radius: 8px; font-size: 0.68rem; font-weight: 700; }
.sla-tenant-badge.masorange { background: #FF6B00; color: white; }
.sla-tenant-badge.vodafone { background: #E60000; color: white; }
.sla-metric-row { display: flex; justify-content: space-between; padding: 0.3rem 0; border-bottom: 1px solid rgba(255,255,255,0.1); }
.sla-metric-label { color: rgba(255,255,255,0.7); font-size: 0.75rem; }
.sla-metric-value { color: white; font-size: 0.85rem; font-weight: 700; }
.sla-metric-value.good { color: #34D399; }
.sla-metric-value.warning { color: #FBBF24; }
.sla-metric-value.critical { color: #F87171; }
</style>""", unsafe_allow_html=True)

    sla_monthly = pd.DataFrame({
        "Month": ["2025-09", "2025-10", "2025-11", "2025-12", "2026-01", "2026-02"],
        "MasOrange Availability %": [99.94, 99.92, 99.91, 99.89, 99.93, 99.95],
        "Vodafone Availability %": [99.92, 99.90, 99.88, 99.86, 99.91, 99.93],
        "MasOrange MTTR Min": [42, 45, 48, 52, 46, 43],
        "Vodafone MTTR Min": [44, 47, 51, 55, 48, 45],
        "MasOrange Incidents": [124, 138, 152, 168, 142, 128],
        "Vodafone Incidents": [98, 108, 118, 130, 112, 102],
    })

    sla_by_cause = pd.DataFrame({
        "Cause": ["Fiber Cut", "Power Outage", "OLT Failure", "CPE Issue", "Backhaul Congestion", "Planned Maintenance"],
        "MasOrange Incidents": [42, 28, 18, 52, 12, 8],
        "Vodafone Incidents": [34, 22, 14, 41, 10, 6],
        "MasOrange Downtime Min": [1840, 980, 720, 420, 380, 240],
        "Vodafone Downtime Min": [1520, 810, 590, 340, 310, 195],
    })

    sla_by_region = pd.DataFrame({
        "Region": ["Madrid", "Barcelona", "Valencia", "Sevilla", "Málaga", "Bilbao"],
        "MasOrange SLA Met %": [99.8, 99.6, 99.4, 99.2, 98.9, 99.5],
        "Vodafone SLA Met %": [99.7, 99.5, 99.3, 99.0, 98.7, 99.4],
        "MasOrange Penalty Exposure K": [0, 12, 24, 38, 52, 18],
        "Vodafone Penalty Exposure K": [0, 15, 28, 42, 58, 21],
        "MasOrange Truck Rolls": [180, 165, 142, 128, 118, 105],
        "Vodafone Truck Rolls": [145, 132, 114, 102, 95, 84],
    })

    sla_install = pd.DataFrame({
        "Month": ["2025-09", "2025-10", "2025-11", "2025-12", "2026-01", "2026-02"],
        "MasOrange Install Days": [4.2, 4.5, 4.8, 5.2, 4.6, 4.3],
        "Vodafone Install Days": [4.0, 4.3, 4.6, 5.0, 4.4, 4.1],
        "MasOrange SLA Met %": [94, 92, 88, 82, 90, 93],
        "Vodafone SLA Met %": [95, 93, 89, 84, 91, 94],
    })

    mo_avail = sla_monthly["MasOrange Availability %"].iloc[-1]
    vf_avail = sla_monthly["Vodafone Availability %"].iloc[-1]
    mo_mttr = sla_monthly["MasOrange MTTR Min"].iloc[-1]
    vf_mttr = sla_monthly["Vodafone MTTR Min"].iloc[-1]
    mo_incidents = sla_monthly["MasOrange Incidents"].iloc[-1]
    vf_incidents = sla_monthly["Vodafone Incidents"].iloc[-1]
    mo_penalty = sla_by_region["MasOrange Penalty Exposure K"].sum()
    vf_penalty = sla_by_region["Vodafone Penalty Exposure K"].sum()

    st.markdown(f"""
    <div class="sla-pulse">
        <div class="sla-pulse-head">
            <span class="sla-pulse-title">📊 Tenant SLA Performance · Fiberco → Operator</span>
        </div>
        <div class="sla-tenant-grid">
            <div class="sla-tenant-card">
                <div class="sla-tenant-header">
                    <span class="sla-tenant-badge masorange">TENANT</span>
                    <span class="sla-tenant-name">MasOrange</span>
                </div>
                <div class="sla-metric-row"><span class="sla-metric-label">Network Availability</span><span class="sla-metric-value good">{mo_avail}%</span></div>
                <div class="sla-metric-row"><span class="sla-metric-label">MTTR</span><span class="sla-metric-value {'good' if mo_mttr < 45 else 'warning'}">{mo_mttr} min</span></div>
                <div class="sla-metric-row"><span class="sla-metric-label">Monthly Incidents</span><span class="sla-metric-value">{mo_incidents}</span></div>
                <div class="sla-metric-row"><span class="sla-metric-label">Penalty Exposure</span><span class="sla-metric-value {'good' if mo_penalty < 100 else 'critical'}">€{mo_penalty}K</span></div>
            </div>
            <div class="sla-tenant-card">
                <div class="sla-tenant-header">
                    <span class="sla-tenant-badge vodafone">TENANT</span>
                    <span class="sla-tenant-name">Vodafone</span>
                </div>
                <div class="sla-metric-row"><span class="sla-metric-label">Network Availability</span><span class="sla-metric-value good">{vf_avail}%</span></div>
                <div class="sla-metric-row"><span class="sla-metric-label">MTTR</span><span class="sla-metric-value {'good' if vf_mttr < 45 else 'warning'}">{vf_mttr} min</span></div>
                <div class="sla-metric-row"><span class="sla-metric-label">Monthly Incidents</span><span class="sla-metric-value">{vf_incidents}</span></div>
                <div class="sla-metric-row"><span class="sla-metric-label">Penalty Exposure</span><span class="sla-metric-value {'good' if vf_penalty < 100 else 'critical'}">€{vf_penalty}K</span></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    sla_tab_perf, sla_tab_incidents, sla_tab_install = st.tabs(["📈 SLA Performance", "🔧 Incident Analysis", "🏠 Installation SLA"])

    with sla_tab_perf:
        st.markdown('<div class="sla-title">Network Availability by Tenant</div>', unsafe_allow_html=True)
        perf_col1, perf_col2 = st.columns(2)

        with perf_col1:
            st.markdown('<div class="sla-mini-title">Availability Trend</div>', unsafe_allow_html=True)
            with st.container(border=True):
                avail_long = sla_monthly.melt(id_vars=["Month"], value_vars=["MasOrange Availability %", "Vodafone Availability %"], var_name="Tenant", value_name="Availability %")
                avail_long["Tenant"] = avail_long["Tenant"].str.replace(" Availability %", "")
                avail_line = alt.Chart(avail_long).mark_line(point=True, strokeWidth=2.5).encode(
                    x=alt.X("Month:N", title=None),
                    y=alt.Y("Availability %:Q", title="Availability (%)", scale=alt.Scale(domain=[99.8, 100])),
                    color=alt.Color("Tenant:N", scale=alt.Scale(domain=["MasOrange", "Vodafone"], range=["#FF6B00", "#E60000"]), legend=alt.Legend(title=None)),
                    tooltip=["Month:N", "Tenant:N", alt.Tooltip("Availability %:Q", format=".2f")],
                )
                sla_target = alt.Chart(pd.DataFrame({"y": [99.9]})).mark_rule(strokeDash=[4, 4], color="#10B981").encode(y="y:Q")
                st.altair_chart(style_sla_chart(avail_line + sla_target, height=240), use_container_width=True)
                render_sla_ai_reco(
                    "Availability Trend",
                    f"Both tenants above 99.9% SLA target. MasOrange leads at {mo_avail}%.",
                    "Maintain proactive monitoring to sustain current performance levels.",
                    "Zero SLA penalties and strong tenant satisfaction.",
                )

        with perf_col2:
            st.markdown('<div class="sla-mini-title">MTTR Trend</div>', unsafe_allow_html=True)
            with st.container(border=True):
                mttr_long = sla_monthly.melt(id_vars=["Month"], value_vars=["MasOrange MTTR Min", "Vodafone MTTR Min"], var_name="Tenant", value_name="MTTR Min")
                mttr_long["Tenant"] = mttr_long["Tenant"].str.replace(" MTTR Min", "")
                mttr_line = alt.Chart(mttr_long).mark_line(point=True, strokeWidth=2.5).encode(
                    x=alt.X("Month:N", title=None),
                    y=alt.Y("MTTR Min:Q", title="MTTR (minutes)"),
                    color=alt.Color("Tenant:N", scale=alt.Scale(domain=["MasOrange", "Vodafone"], range=["#FF6B00", "#E60000"]), legend=alt.Legend(title=None)),
                    tooltip=["Month:N", "Tenant:N", alt.Tooltip("MTTR Min:Q")],
                )
                mttr_target = alt.Chart(pd.DataFrame({"y": [45]})).mark_rule(strokeDash=[4, 4], color="#F59E0B").encode(y="y:Q")
                st.altair_chart(style_sla_chart(mttr_line + mttr_target, height=240), use_container_width=True)
                render_sla_ai_reco(
                    "MTTR Analysis",
                    f"MTTR improved from Dec peak. Current: MasOrange {mo_mttr}min, Vodafone {vf_mttr}min.",
                    "Focus on reducing Vodafone MTTR to match MasOrange performance.",
                    "Improved tenant experience and reduced penalty risk.",
                    level="warning" if vf_mttr > 45 else "info",
                )

        st.markdown('<div class="sla-title">Regional SLA Performance</div>', unsafe_allow_html=True)
        with st.container(border=True):
            region_long = sla_by_region.melt(id_vars=["Region"], value_vars=["MasOrange SLA Met %", "Vodafone SLA Met %"], var_name="Tenant", value_name="SLA Met %")
            region_long["Tenant"] = region_long["Tenant"].str.replace(" SLA Met %", "")
            region_bar = alt.Chart(region_long).mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4).encode(
                x=alt.X("Region:N", title=None),
                y=alt.Y("SLA Met %:Q", title="SLA Met (%)", scale=alt.Scale(zero=False, domain=[98.5, 100])),
                color=alt.Color("Tenant:N", scale=alt.Scale(domain=["MasOrange", "Vodafone"], range=["#FF6B00", "#E60000"]), legend=alt.Legend(title=None)),
                xOffset="Tenant:N",
                tooltip=["Region:N", "Tenant:N", alt.Tooltip("SLA Met %:Q", format=".1f")],
            )
            sla_target_line = alt.Chart(pd.DataFrame({"y": [99.5]})).mark_rule(strokeDash=[4, 4], color="#10B981", strokeWidth=2).encode(y="y:Q")
            st.altair_chart(style_sla_chart(region_bar + sla_target_line, height=240), use_container_width=True)
            worst_region = sla_by_region.sort_values("MasOrange SLA Met %").iloc[0]
            render_sla_ai_reco(
                "Regional Risk",
                f"{worst_region['Region']} has lowest SLA compliance ({worst_region['MasOrange SLA Met %']}% MasOrange, {worst_region['Vodafone SLA Met %']}% Vodafone).",
                f"Deploy additional field resources to {worst_region['Region']} and review root causes.",
                "Reduce regional SLA breaches and penalty exposure.",
                level="critical",
            )

    with sla_tab_incidents:
        st.markdown('<div class="sla-title">Incident Analysis by Cause</div>', unsafe_allow_html=True)
        inc_col1, inc_col2 = st.columns(2)

        with inc_col1:
            st.markdown('<div class="sla-mini-title">Incidents by Cause</div>', unsafe_allow_html=True)
            with st.container(border=True):
                cause_long = sla_by_cause.melt(id_vars=["Cause"], value_vars=["MasOrange Incidents", "Vodafone Incidents"], var_name="Tenant", value_name="Incidents")
                cause_long["Tenant"] = cause_long["Tenant"].str.replace(" Incidents", "")
                cause_bar = alt.Chart(cause_long).mark_bar(cornerRadiusTopRight=5, cornerRadiusBottomRight=5, size=16).encode(
                    x=alt.X("Incidents:Q", title="Incidents"),
                    y=alt.Y("Cause:N", title=None, sort="-x"),
                    color=alt.Color("Tenant:N", scale=alt.Scale(domain=["MasOrange", "Vodafone"], range=["#FF6B00", "#E60000"]), legend=alt.Legend(title=None)),
                    yOffset="Tenant:N",
                    tooltip=["Cause:N", "Tenant:N", "Incidents:Q"],
                )
                st.altair_chart(style_sla_chart(cause_bar, height=260), use_container_width=True)
                top_cause = sla_by_cause.sort_values("MasOrange Incidents", ascending=False).iloc[0]
                render_sla_ai_reco(
                    "Top Incident Cause",
                    f"CPE Issues cause most incidents ({top_cause['MasOrange Incidents']} MasOrange, {top_cause['Vodafone Incidents']} Vodafone).",
                    "Review CPE provisioning process and consider proactive replacement program.",
                    "Reduce repeat truck rolls and improve first-time-right rate.",
                )

        with inc_col2:
            st.markdown('<div class="sla-mini-title">Downtime by Cause</div>', unsafe_allow_html=True)
            with st.container(border=True):
                dt_long = sla_by_cause.melt(id_vars=["Cause"], value_vars=["MasOrange Downtime Min", "Vodafone Downtime Min"], var_name="Tenant", value_name="Downtime Min")
                dt_long["Tenant"] = dt_long["Tenant"].str.replace(" Downtime Min", "")
                dt_bar = alt.Chart(dt_long).mark_bar(cornerRadiusTopRight=5, cornerRadiusBottomRight=5, size=16).encode(
                    x=alt.X("Downtime Min:Q", title="Downtime (minutes)"),
                    y=alt.Y("Cause:N", title=None, sort="-x"),
                    color=alt.Color("Tenant:N", scale=alt.Scale(domain=["MasOrange", "Vodafone"], range=["#FF6B00", "#E60000"]), legend=alt.Legend(title=None)),
                    yOffset="Tenant:N",
                    tooltip=["Cause:N", "Tenant:N", alt.Tooltip("Downtime Min:Q", format=",")],
                )
                st.altair_chart(style_sla_chart(dt_bar, height=260), use_container_width=True)
                top_dt = sla_by_cause.sort_values("MasOrange Downtime Min", ascending=False).iloc[0]
                render_sla_ai_reco(
                    "Downtime Impact",
                    f"Fiber Cuts cause highest downtime ({top_dt['MasOrange Downtime Min']} min MasOrange).",
                    "Invest in fiber route hardening and faster splice repair capability.",
                    "Reduce major outage duration and SLA penalty exposure.",
                    level="warning",
                )

        st.markdown('<div class="sla-title">Penalty Exposure by Region</div>', unsafe_allow_html=True)
        with st.container(border=True):
            penalty_long = sla_by_region.melt(id_vars=["Region"], value_vars=["MasOrange Penalty Exposure K", "Vodafone Penalty Exposure K"], var_name="Tenant", value_name="Penalty K")
            penalty_long["Tenant"] = penalty_long["Tenant"].str.replace(" Penalty Exposure K", "")
            penalty_bar = alt.Chart(penalty_long).mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4).encode(
                x=alt.X("Region:N", title=None),
                y=alt.Y("Penalty K:Q", title="Penalty Exposure (€K)"),
                color=alt.Color("Tenant:N", scale=alt.Scale(domain=["MasOrange", "Vodafone"], range=["#FF6B00", "#E60000"]), legend=alt.Legend(title=None)),
                xOffset="Tenant:N",
                tooltip=["Region:N", "Tenant:N", alt.Tooltip("Penalty K:Q", format="€,.0f")],
            )
            st.altair_chart(style_sla_chart(penalty_bar, height=220), use_container_width=True)
            total_penalty = penalty_long["Penalty K"].sum()
            highest_region = penalty_long.groupby("Region")["Penalty K"].sum().idxmax()
            render_sla_ai_reco(
                "Penalty Exposure",
                f"Total penalty exposure: €{total_penalty:.0f}K. {highest_region} has highest risk.",
                "Prioritize SLA improvement investments in high-penalty regions.",
                "Reduce financial exposure and protect JV profitability.",
                level="critical" if total_penalty > 500 else "warning",
            )

    with sla_tab_install:
        st.markdown('<div class="sla-title">Installation Lead Time by Tenant</div>', unsafe_allow_html=True)
        inst_col1, inst_col2 = st.columns(2)

        with inst_col1:
            st.markdown('<div class="sla-mini-title">Install Days Trend</div>', unsafe_allow_html=True)
            with st.container(border=True):
                inst_long = sla_install.melt(id_vars=["Month"], value_vars=["MasOrange Install Days", "Vodafone Install Days"], var_name="Tenant", value_name="Install Days")
                inst_long["Tenant"] = inst_long["Tenant"].str.replace(" Install Days", "")
                inst_line = alt.Chart(inst_long).mark_line(point=True, strokeWidth=2.5).encode(
                    x=alt.X("Month:N", title=None),
                    y=alt.Y("Install Days:Q", title="Install Lead Time (days)"),
                    color=alt.Color("Tenant:N", scale=alt.Scale(domain=["MasOrange", "Vodafone"], range=["#FF6B00", "#E60000"]), legend=alt.Legend(title=None)),
                    tooltip=["Month:N", "Tenant:N", alt.Tooltip("Install Days:Q", format=".1f")],
                )
                st.altair_chart(style_sla_chart(inst_line, height=240), use_container_width=True)
                avg_mo_days = sla_install["MasOrange Install Days"].mean()
                avg_vf_days = sla_install["Vodafone Install Days"].mean()
                render_sla_ai_reco(
                    "Install Speed",
                    f"Avg install time: MasOrange {avg_mo_days:.1f} days, Vodafone {avg_vf_days:.1f} days.",
                    "Reduce variability by pre-staging equipment and optimizing scheduling.",
                    "Faster customer activation and improved tenant experience.",
                )

        with inst_col2:
            st.markdown('<div class="sla-mini-title">Installation SLA Met %</div>', unsafe_allow_html=True)
            with st.container(border=True):
                isla_long = sla_install.melt(id_vars=["Month"], value_vars=["MasOrange SLA Met %", "Vodafone SLA Met %"], var_name="Tenant", value_name="SLA Met %")
                isla_long["Tenant"] = isla_long["Tenant"].str.replace(" SLA Met %", "")
                isla_line = alt.Chart(isla_long).mark_line(point=True, strokeWidth=2.5).encode(
                    x=alt.X("Month:N", title=None),
                    y=alt.Y("SLA Met %:Q", title="SLA Met (%)", scale=alt.Scale(domain=[80, 100])),
                    color=alt.Color("Tenant:N", scale=alt.Scale(domain=["MasOrange", "Vodafone"], range=["#FF6B00", "#E60000"]), legend=alt.Legend(title=None)),
                    tooltip=["Month:N", "Tenant:N", alt.Tooltip("SLA Met %:Q", format=".0f")],
                )
                st.altair_chart(style_sla_chart(isla_line, height=240), use_container_width=True)
                latest_mo_sla = sla_install["MasOrange SLA Met %"].iloc[-1]
                latest_vf_sla = sla_install["Vodafone SLA Met %"].iloc[-1]
                render_sla_ai_reco(
                    "Install SLA Compliance",
                    f"Current install SLA: MasOrange {latest_mo_sla:.0f}%, Vodafone {latest_vf_sla:.0f}%.",
                    "Target 95%+ for both tenants through process standardization.",
                    "Reduce escalations and strengthen tenant relationships.",
                    level="warning" if min(latest_mo_sla, latest_vf_sla) < 90 else "info",
                )

        render_sla_ai_reco(
            "Installation Performance",
            f"Install times recovered from Dec peak. Current: MasOrange {sla_install['MasOrange Install Days'].iloc[-1]} days, Vodafone {sla_install['Vodafone Install Days'].iloc[-1]} days.",
            "Maintain contractor capacity and inventory levels to sustain improvement.",
            "High tenant satisfaction and faster time-to-revenue.",
        )

    st.markdown("""
    <details style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 0.8rem; margin-top: 1rem;">
        <summary style="cursor: pointer; font-weight: 600; color: #334155; font-size: 0.9rem;">▸ Data Sources & Systems</summary>
        <div style="margin-top: 0.8rem; font-size: 0.85rem; color: #475569;">
            <p><strong>This dashboard aggregates data from the following source systems:</strong></p>
            <table style="width: 100%; border-collapse: collapse; margin: 0.5rem 0;">
                <tr style="border-bottom: 1px solid #E2E8F0;"><th style="text-align: left; padding: 0.4rem;">Data Element</th><th style="text-align: left; padding: 0.4rem;">Source System</th><th style="text-align: left; padding: 0.4rem;">Refresh</th></tr>
                <tr><td style="padding: 0.4rem;">Network availability %</td><td style="padding: 0.4rem;"><strong>NOC</strong> - Monitoring Platform</td><td style="padding: 0.4rem;">Real-time</td></tr>
                <tr><td style="padding: 0.4rem;">MTTR metrics</td><td style="padding: 0.4rem;"><strong>ServiceNow ITSM</strong> - Incident Mgmt</td><td style="padding: 0.4rem;">Real-time</td></tr>
                <tr><td style="padding: 0.4rem;">Incident counts</td><td style="padding: 0.4rem;"><strong>ServiceNow</strong> + Alarm Correlation</td><td style="padding: 0.4rem;">Real-time</td></tr>
                <tr><td style="padding: 0.4rem;">Regional SLA performance</td><td style="padding: 0.4rem;"><strong>NOC</strong> + GIS Platform</td><td style="padding: 0.4rem;">Hourly</td></tr>
                <tr><td style="padding: 0.4rem;">Penalty exposure</td><td style="padding: 0.4rem;"><strong>Contract Management</strong> + Finance</td><td style="padding: 0.4rem;">Daily</td></tr>
                <tr><td style="padding: 0.4rem;">Installation times</td><td style="padding: 0.4rem;"><strong>Workforce Management (WFM)</strong></td><td style="padding: 0.4rem;">Daily</td></tr>
            </table>
            <p><strong>Key Integrations:</strong></p>
            <ul style="margin: 0.3rem 0; padding-left: 1.2rem;">
                <li>SLA thresholds from <strong>Master Service Agreements (MSA)</strong></li>
                <li>Incident sync with <strong>MasOrange/Vodafone ticketing</strong></li>
                <li>Penalty calculations from <strong>contractual SLA matrices</strong></li>
            </ul>
        </div>
    </details>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Page: Wholesale Commercial (Product & Pricing Strategy)
# ---------------------------------------------------------------------------
elif selected_menu == "Wholesale Commercial":
    import pandas as pd
    import altair as alt

    def style_ws_chart(chart: alt.Chart, height: int = 220) -> alt.Chart:
        return (
            chart.properties(height=height, padding={"left": 6, "top": 10, "right": 8, "bottom": 6})
            .configure(background="#FFFFFF")
            .configure_view(stroke=None)
            .configure_axis(labelFontSize=10, titleFontSize=11, gridColor="#E2E8F0", domainColor="#E2E8F0")
            .configure_legend(labelFontSize=10)
        )

    def render_ws_ai_reco(title: str, insight: str, action: str, outcome: str, level: str = "info"):
        color_map = {"info": ("#29B5E8", "#EBF8FF", "#0C4A6E"), "warning": ("#F59E0B", "#FFFBEB", "#92400E"), "critical": ("#EF4444", "#FEF2F2", "#991B1B")}
        accent, bg, text = color_map.get(level, color_map["info"])
        st.markdown(f"""<div style="background: {bg}; border-left: 4px solid {accent}; border-radius: 8px; padding: 0.65rem 0.85rem; margin-top: 0.5rem;">
            <div style="font-weight: 700; color: {text}; font-size: 0.78rem; margin-bottom: 0.2rem;">🤖 {title}</div>
            <div style="color: #334155; font-size: 0.76rem; line-height: 1.4;"><strong>Insight:</strong> {insight}</div>
            <div style="color: #334155; font-size: 0.76rem; line-height: 1.4;"><strong>Action:</strong> {action}</div>
            <div style="color: #059669; font-size: 0.74rem; margin-top: 0.2rem;"><strong>Outcome:</strong> {outcome}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("""<style>
.ws-title { font-size: 1.15rem; font-weight: 800; color: #0F172A; margin: 1.2rem 0 0.6rem; border-bottom: 2px solid #E2E8F0; padding-bottom: 0.4rem; }
.ws-mini-title { font-size: 0.88rem; font-weight: 700; color: #334155; margin-bottom: 0.5rem; }
.ws-pulse { background: linear-gradient(135deg, #065F46 0%, #047857 100%); border-radius: 14px; padding: 1.1rem 1.3rem; margin-bottom: 1rem; }
.ws-pulse-head { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.8rem; }
.ws-pulse-title { color: #FFFFFF; font-size: 1rem; font-weight: 700; }
.ws-pulse-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 0.8rem; }
.ws-pulse-card { background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.15); border-radius: 10px; padding: 0.7rem; text-align: center; }
.ws-pulse-label { color: rgba(255,255,255,0.7); font-size: 0.68rem; text-transform: uppercase; }
.ws-pulse-value { color: #FFFFFF; font-size: 1.4rem; font-weight: 800; margin-top: 0.15rem; }
.ws-pulse-delta { color: #34D399; font-size: 0.72rem; font-weight: 600; margin-top: 0.1rem; }
</style>""", unsafe_allow_html=True)

    ws_products = pd.DataFrame({
        "Product": ["Bitstream 300Mb", "Bitstream 600Mb", "Bitstream 1Gb", "Bitstream 2.5Gb", "Enterprise Dedicated", "Dark Fiber"],
        "MasOrange Lines K": [1820, 2340, 1680, 420, 85, 12],
        "Vodafone Lines K": [1290, 1680, 1240, 310, 62, 8],
        "Price €/mo": [2.80, 3.20, 3.80, 4.50, 12.00, 45.00],
        "Cost €/mo": [1.85, 2.10, 2.50, 3.10, 7.20, 18.00],
        "Margin %": [33.9, 34.4, 34.2, 31.1, 40.0, 60.0],
        "YoY Growth %": [-8, 12, 28, 45, 18, 22],
    })
    ws_products["Total Lines K"] = ws_products["MasOrange Lines K"] + ws_products["Vodafone Lines K"]
    ws_products["Monthly Revenue K"] = (ws_products["Total Lines K"] * ws_products["Price €/mo"]).round(0)
    ws_products["Gross Profit K"] = (ws_products["Total Lines K"] * (ws_products["Price €/mo"] - ws_products["Cost €/mo"])).round(0)

    ws_margin_waterfall = pd.DataFrame({
        "Step": ["Gross Revenue", "Network Costs", "Field Ops", "Energy", "SLA Credits", "Net Margin"],
        "Value M": [17.8, -7.2, -2.4, -1.8, -0.3, 6.1],
        "Cumulative M": [17.8, 10.6, 8.2, 6.4, 6.1, 6.1],
    })

    ws_pricing_scenario = pd.DataFrame({
        "Scenario": ["Current", "+5% Price", "+10% Price", "-5% Price"],
        "Monthly Revenue M": [17.8, 18.7, 19.6, 16.9],
        "Volume Impact %": [0, -2, -5, 3],
        "EBITDA M": [6.1, 6.8, 7.2, 5.6],
        "Tenant Risk": ["Low", "Medium", "High", "Low"],
    })

    ws_monthly_trend = pd.DataFrame({
        "Month": ["2025-09", "2025-10", "2025-11", "2025-12", "2026-01", "2026-02"],
        "MasOrange Revenue M": [9.8, 10.0, 10.2, 10.1, 10.3, 10.5],
        "Vodafone Revenue M": [6.9, 7.0, 7.1, 7.0, 7.2, 7.3],
    })

    total_revenue_m = ws_products["Monthly Revenue K"].sum() / 1000
    total_lines_k = ws_products["Total Lines K"].sum()
    blended_margin = round(ws_products["Gross Profit K"].sum() / ws_products["Monthly Revenue K"].sum() * 100, 1)
    avg_arpu = round(total_revenue_m * 1000 / total_lines_k, 2)

    st.markdown(f"""
    <div class="ws-pulse">
        <div class="ws-pulse-head">
            <span class="ws-pulse-title">📦 Wholesale Product & Pricing · B2B Strategy</span>
        </div>
        <div class="ws-pulse-grid">
            <div class="ws-pulse-card">
                <div class="ws-pulse-label">Monthly Revenue</div>
                <div class="ws-pulse-value">€{total_revenue_m:.1f}M</div>
                <div class="ws-pulse-delta">↑ +3.2% MoM</div>
            </div>
            <div class="ws-pulse-card">
                <div class="ws-pulse-label">Active Lines</div>
                <div class="ws-pulse-value">{total_lines_k/1000:.1f}M</div>
                <div class="ws-pulse-delta">Both tenants</div>
            </div>
            <div class="ws-pulse-card">
                <div class="ws-pulse-label">Blended Margin</div>
                <div class="ws-pulse-value">{blended_margin}%</div>
                <div class="ws-pulse-delta">Above target</div>
            </div>
            <div class="ws-pulse-card">
                <div class="ws-pulse-label">Avg ARPU</div>
                <div class="ws-pulse-value">€{avg_arpu}</div>
                <div class="ws-pulse-delta">Per line/month</div>
            </div>
            <div class="ws-pulse-card">
                <div class="ws-pulse-label">Products</div>
                <div class="ws-pulse-value">{len(ws_products)}</div>
                <div class="ws-pulse-delta">In portfolio</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    ws_tab_portfolio, ws_tab_margin, ws_tab_pricing = st.tabs(["📦 Product Portfolio", "💰 Margin Analysis", "📊 Pricing Scenarios"])

    with ws_tab_portfolio:
        st.markdown('<div class="ws-title">Product Portfolio by Tenant</div>', unsafe_allow_html=True)
        port_col1, port_col2 = st.columns(2)

        with port_col1:
            st.markdown('<div class="ws-mini-title">Lines by Product and Tenant</div>', unsafe_allow_html=True)
            with st.container(border=True):
                prod_long = ws_products.melt(id_vars=["Product"], value_vars=["MasOrange Lines K", "Vodafone Lines K"], var_name="Tenant", value_name="Lines K")
                prod_long["Tenant"] = prod_long["Tenant"].str.replace(" Lines K", "")
                prod_bar = alt.Chart(prod_long).mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4).encode(
                    x=alt.X("Product:N", title=None, sort="-y"),
                    y=alt.Y("Lines K:Q", title="Lines (K)"),
                    color=alt.Color("Tenant:N", scale=alt.Scale(domain=["MasOrange", "Vodafone"], range=["#FF6B00", "#E60000"]), legend=alt.Legend(title=None)),
                    xOffset="Tenant:N",
                    tooltip=["Product:N", "Tenant:N", alt.Tooltip("Lines K:Q", format=",")],
                )
                st.altair_chart(style_ws_chart(prod_bar, height=260), use_container_width=True)
                top_prod = ws_products.sort_values("Total Lines K", ascending=False).iloc[0]
                render_ws_ai_reco(
                    "Product Mix",
                    f"{top_prod['Product']} is highest volume ({top_prod['Total Lines K']:,.0f}K lines, {top_prod['Total Lines K']/total_lines_k*100:.0f}% share).",
                    "Monitor migration from 300Mb to higher tiers; declining legacy products.",
                    "Optimize product mix toward higher-margin tiers.",
                )

        with port_col2:
            st.markdown('<div class="ws-mini-title">Revenue vs Margin by Product</div>', unsafe_allow_html=True)
            with st.container(border=True):
                rev_margin = alt.Chart(ws_products).mark_circle(opacity=0.85, stroke="#FFFFFF", strokeWidth=1.2).encode(
                    x=alt.X("Monthly Revenue K:Q", title="Monthly Revenue (€K)"),
                    y=alt.Y("Margin %:Q", title="Margin (%)"),
                    size=alt.Size("Total Lines K:Q", scale=alt.Scale(range=[200, 1000]), legend=None),
                    color=alt.Color("YoY Growth %:Q", scale=alt.Scale(scheme="redyellowgreen", domainMid=0), legend=alt.Legend(title="YoY Growth")),
                    tooltip=["Product:N", alt.Tooltip("Monthly Revenue K:Q", format="€,.0f"), alt.Tooltip("Margin %:Q", format=".1f"), alt.Tooltip("YoY Growth %:Q", format="+.0f"), alt.Tooltip("Total Lines K:Q", format=",")],
                )
                rev_labels = alt.Chart(ws_products).mark_text(dy=-12, fontSize=9, color="#1E293B").encode(
                    x="Monthly Revenue K:Q", y="Margin %:Q", text="Product:N"
                )
                st.altair_chart(style_ws_chart(rev_margin + rev_labels, height=260), use_container_width=True)
                low_margin = ws_products.sort_values("Margin %").iloc[0]
                render_ws_ai_reco(
                    "Margin Optimization",
                    f"{low_margin['Product']} has lowest margin ({low_margin['Margin %']:.1f}%) but strong growth ({low_margin['YoY Growth %']:+.0f}%).",
                    "Review cost structure for 2.5Gb tier; consider price adjustment or cost reduction.",
                    "Improve margin as volumes scale.",
                    level="warning",
                )

        st.markdown('<div class="ws-title">Product Portfolio Details</div>', unsafe_allow_html=True)
        with st.container(border=True):
            st.dataframe(
                ws_products.style.format({
                    "MasOrange Lines K": "{:,.0f}",
                    "Vodafone Lines K": "{:,.0f}",
                    "Total Lines K": "{:,.0f}",
                    "Price €/mo": "€{:.2f}",
                    "Cost €/mo": "€{:.2f}",
                    "Margin %": "{:.1f}%",
                    "YoY Growth %": "{:+.0f}%",
                    "Monthly Revenue K": "€{:,.0f}",
                    "Gross Profit K": "€{:,.0f}",
                }).background_gradient(subset=["Margin %"], cmap="Greens"),
                use_container_width=True,
                hide_index=True,
            )

    with ws_tab_margin:
        st.markdown('<div class="ws-title">Margin Waterfall Analysis</div>', unsafe_allow_html=True)
        with st.container(border=True):
            wf = ws_margin_waterfall.copy()
            wf["Type"] = wf["Value M"].apply(lambda v: "Revenue" if v > 10 else "Profit" if v > 0 else "Cost")
            wf_bar = alt.Chart(wf).mark_bar(cornerRadiusTopLeft=5, cornerRadiusTopRight=5, size=50).encode(
                x=alt.X("Step:N", title=None, sort=list(wf["Step"])),
                y=alt.Y("Value M:Q", title="€ Million"),
                color=alt.Color("Type:N", scale=alt.Scale(domain=["Revenue", "Cost", "Profit"], range=["#29B5E8", "#EF4444", "#10B981"]), legend=None),
                tooltip=["Step:N", alt.Tooltip("Value M:Q", format="+.1f"), alt.Tooltip("Cumulative M:Q", format=".1f")],
            )
            wf_text = alt.Chart(wf).mark_text(dy=-8, fontSize=10, fontWeight="bold", color="#0F172A").encode(
                x=alt.X("Step:N", sort=list(wf["Step"])),
                y="Value M:Q",
                text=alt.Text("Value M:Q", format="+.1f"),
            )
            st.altair_chart(style_ws_chart(wf_bar + wf_text, height=280), use_container_width=True)
            network_pct = round(abs(ws_margin_waterfall[ws_margin_waterfall["Step"] == "Network Costs"]["Value M"].iloc[0]) / ws_margin_waterfall[ws_margin_waterfall["Step"] == "Gross Revenue"]["Value M"].iloc[0] * 100, 1)
            render_ws_ai_reco(
                "Cost Structure",
                f"Network costs are {network_pct}% of revenue, the largest cost driver.",
                "Focus optimization on network efficiency and vendor renegotiations.",
                "Improve net margin from current 34% toward 38% target.",
            )

        st.markdown('<div class="ws-title">Revenue Trend by Tenant</div>', unsafe_allow_html=True)
        with st.container(border=True):
            trend_long = ws_monthly_trend.melt(id_vars=["Month"], value_vars=["MasOrange Revenue M", "Vodafone Revenue M"], var_name="Tenant", value_name="Revenue M")
            trend_long["Tenant"] = trend_long["Tenant"].str.replace(" Revenue M", "")
            trend_line = alt.Chart(trend_long).mark_area(opacity=0.7).encode(
                x=alt.X("Month:N", title=None),
                y=alt.Y("Revenue M:Q", title="Revenue (€ M)", stack=True),
                color=alt.Color("Tenant:N", scale=alt.Scale(domain=["MasOrange", "Vodafone"], range=["#FF6B00", "#E60000"]), legend=alt.Legend(title=None)),
                tooltip=["Month:N", "Tenant:N", alt.Tooltip("Revenue M:Q", format=".1f")],
            )
            st.altair_chart(style_ws_chart(trend_line, height=220), use_container_width=True)
            mo_growth = (ws_monthly_trend["MasOrange Revenue M"].iloc[-1] - ws_monthly_trend["MasOrange Revenue M"].iloc[0]) / ws_monthly_trend["MasOrange Revenue M"].iloc[0] * 100
            vf_growth = (ws_monthly_trend["Vodafone Revenue M"].iloc[-1] - ws_monthly_trend["Vodafone Revenue M"].iloc[0]) / ws_monthly_trend["Vodafone Revenue M"].iloc[0] * 100
            render_ws_ai_reco(
                "Revenue Trend",
                f"6-month growth: MasOrange {mo_growth:+.1f}%, Vodafone {vf_growth:+.1f}%.",
                "Sustain growth momentum through upselling and network expansion.",
                "Achieve €24M+ monthly revenue target by Q4.",
            )

    with ws_tab_pricing:
        st.markdown('<div class="ws-title">Pricing Scenario Analysis</div>', unsafe_allow_html=True)
        pr_col1, pr_col2 = st.columns(2)

        with pr_col1:
            st.markdown('<div class="ws-mini-title">Revenue vs EBITDA by Scenario</div>', unsafe_allow_html=True)
            with st.container(border=True):
                scenario_bar = alt.Chart(ws_pricing_scenario).mark_bar(cornerRadiusTopLeft=5, cornerRadiusTopRight=5, size=40).encode(
                    x=alt.X("Scenario:N", title=None),
                    y=alt.Y("Monthly Revenue M:Q", title="Monthly Revenue (€ M)"),
                    color=alt.Color("Tenant Risk:N", scale=alt.Scale(domain=["Low", "Medium", "High"], range=["#10B981", "#F59E0B", "#EF4444"]), legend=alt.Legend(title="Tenant Risk")),
                    tooltip=["Scenario:N", alt.Tooltip("Monthly Revenue M:Q", format=".1f"), alt.Tooltip("EBITDA M:Q", format=".1f"), "Volume Impact %:Q", "Tenant Risk:N"],
                )
                ebitda_line = alt.Chart(ws_pricing_scenario).mark_line(point=True, strokeWidth=3, color="#6366F1").encode(
                    x=alt.X("Scenario:N", title=None),
                    y=alt.Y("EBITDA M:Q", title="EBITDA (€ M)"),
                    tooltip=["Scenario:N", alt.Tooltip("EBITDA M:Q", format=".1f")],
                )
                st.altair_chart(style_ws_chart(alt.layer(scenario_bar, ebitda_line).resolve_scale(y="independent"), height=250), use_container_width=True)
                render_ws_ai_reco(
                    "Pricing Strategy",
                    "+5% price increase yields €0.7M EBITDA uplift with moderate tenant risk.",
                    "Propose +5% adjustment in next contract renewal cycle with enhanced SLA commitment.",
                    "Balance margin improvement with tenant relationship stability.",
                    level="warning",
                )

        with pr_col2:
            st.markdown('<div class="ws-mini-title">Volume Impact Trade-off</div>', unsafe_allow_html=True)
            with st.container(border=True):
                vol_scatter = alt.Chart(ws_pricing_scenario).mark_circle(size=300, opacity=0.85, stroke="#FFFFFF", strokeWidth=1.5).encode(
                    x=alt.X("Volume Impact %:Q", title="Volume Impact (%)"),
                    y=alt.Y("EBITDA M:Q", title="EBITDA (€ M)"),
                    color=alt.Color("Scenario:N", legend=alt.Legend(title=None)),
                    tooltip=["Scenario:N", "Volume Impact %:Q", alt.Tooltip("EBITDA M:Q", format=".1f"), alt.Tooltip("Monthly Revenue M:Q", format=".1f")],
                )
                vol_labels = alt.Chart(ws_pricing_scenario).mark_text(dy=-14, fontSize=10, fontWeight="bold", color="#1E293B").encode(
                    x="Volume Impact %:Q", y="EBITDA M:Q", text="Scenario:N"
                )
                st.altair_chart(style_ws_chart(vol_scatter + vol_labels, height=250), use_container_width=True)
                render_ws_ai_reco(
                    "Elasticity Analysis",
                    "Price elasticity suggests -2% volume per +5% price, acceptable trade-off.",
                    "Monitor churn signals closely if implementing price increases.",
                    "Optimize revenue without triggering tenant contract disputes.",
                )

    st.markdown("""
    <details style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 0.8rem; margin-top: 1rem;">
        <summary style="cursor: pointer; font-weight: 600; color: #334155; font-size: 0.9rem;">▸ Data Sources & Systems</summary>
        <div style="margin-top: 0.8rem; font-size: 0.85rem; color: #475569;">
            <p><strong>This dashboard aggregates data from the following source systems:</strong></p>
            <table style="width: 100%; border-collapse: collapse; margin: 0.5rem 0;">
                <tr style="border-bottom: 1px solid #E2E8F0;"><th style="text-align: left; padding: 0.4rem;">Data Element</th><th style="text-align: left; padding: 0.4rem;">Source System</th><th style="text-align: left; padding: 0.4rem;">Refresh</th></tr>
                <tr><td style="padding: 0.4rem;">Product portfolio & speeds</td><td style="padding: 0.4rem;"><strong>Salesforce CPQ</strong></td><td style="padding: 0.4rem;">On change</td></tr>
                <tr><td style="padding: 0.4rem;">Wholesale pricing</td><td style="padding: 0.4rem;"><strong>SAP S/4HANA Pricing</strong></td><td style="padding: 0.4rem;">Monthly</td></tr>
                <tr><td style="padding: 0.4rem;">Revenue by product</td><td style="padding: 0.4rem;"><strong>Oracle Revenue Management</strong></td><td style="padding: 0.4rem;">Daily</td></tr>
                <tr><td style="padding: 0.4rem;">Tenant order volumes</td><td style="padding: 0.4rem;"><strong>Order Management (OMS)</strong></td><td style="padding: 0.4rem;">Real-time</td></tr>
                <tr><td style="padding: 0.4rem;">Margin calculations</td><td style="padding: 0.4rem;"><strong>SAP BPC</strong> Finance Analytics</td><td style="padding: 0.4rem;">Monthly</td></tr>
                <tr><td style="padding: 0.4rem;">Pricing scenarios</td><td style="padding: 0.4rem;"><strong>Revenue Optimization Model</strong></td><td style="padding: 0.4rem;">On demand</td></tr>
            </table>
            <p><strong>Key Integrations:</strong></p>
            <ul style="margin: 0.3rem 0; padding-left: 1.2rem;">
                <li>Pricing agreements in <strong>Contract Lifecycle Management (CLM)</strong></li>
                <li>Competitor intel from <strong>market research feeds</strong></li>
                <li>Volume forecasts from <strong>SAP IBP Demand Planning</strong></li>
            </ul>
        </div>
    </details>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Page: ESG & Energy Efficiency
# ---------------------------------------------------------------------------
elif selected_menu == "ESG & Energy":
    import pandas as pd
    import altair as alt

    def style_esg_chart(chart: alt.Chart, height: int = 220) -> alt.Chart:
        return (
            chart.properties(height=height, padding={"left": 6, "top": 10, "right": 8, "bottom": 6})
            .configure(background="#FFFFFF")
            .configure_view(stroke=None)
            .configure_axis(labelFontSize=10, titleFontSize=11, gridColor="#E2E8F0", domainColor="#E2E8F0")
            .configure_legend(labelFontSize=10)
        )

    def render_esg_ai_reco(title: str, insight: str, action: str, outcome: str, level: str = "info"):
        color_map = {"info": ("#10B981", "#ECFDF5", "#065F46"), "warning": ("#F59E0B", "#FFFBEB", "#92400E"), "critical": ("#EF4444", "#FEF2F2", "#991B1B")}
        accent, bg, text = color_map.get(level, color_map["info"])
        st.markdown(f"""<div style="background: {bg}; border-left: 4px solid {accent}; border-radius: 8px; padding: 0.65rem 0.85rem; margin-top: 0.5rem;">
            <div style="font-weight: 700; color: {text}; font-size: 0.78rem; margin-bottom: 0.2rem;">🌱 {title}</div>
            <div style="color: #334155; font-size: 0.76rem; line-height: 1.4;"><strong>Insight:</strong> {insight}</div>
            <div style="color: #334155; font-size: 0.76rem; line-height: 1.4;"><strong>Action:</strong> {action}</div>
            <div style="color: #059669; font-size: 0.74rem; margin-top: 0.2rem;"><strong>Outcome:</strong> {outcome}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("""<style>
.esg-title { font-size: 1.15rem; font-weight: 800; color: #0F172A; margin: 1.2rem 0 0.6rem; border-bottom: 2px solid #E2E8F0; padding-bottom: 0.4rem; }
.esg-mini-title { font-size: 0.88rem; font-weight: 700; color: #334155; margin-bottom: 0.5rem; }
.esg-pulse { background: linear-gradient(135deg, #065F46 0%, #059669 100%); border-radius: 14px; padding: 1.1rem 1.3rem; margin-bottom: 1rem; }
.esg-pulse-head { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.8rem; }
.esg-pulse-title { color: #FFFFFF; font-size: 1rem; font-weight: 700; }
.esg-pulse-badge { background: #34D399; color: #065F46; padding: 2px 10px; border-radius: 12px; font-size: 0.68rem; font-weight: 700; }
.esg-pulse-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 0.8rem; }
.esg-pulse-card { background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.15); border-radius: 10px; padding: 0.7rem; text-align: center; }
.esg-pulse-label { color: rgba(255,255,255,0.7); font-size: 0.68rem; text-transform: uppercase; }
.esg-pulse-value { color: #FFFFFF; font-size: 1.4rem; font-weight: 800; margin-top: 0.15rem; }
.esg-pulse-delta { color: #34D399; font-size: 0.72rem; font-weight: 600; margin-top: 0.1rem; }
</style>""", unsafe_allow_html=True)

    esg_energy_monthly = pd.DataFrame({
        "Month": ["2025-09", "2025-10", "2025-11", "2025-12", "2026-01", "2026-02"],
        "Energy MWh": [4280, 4320, 4450, 4580, 4420, 4350],
        "Active Lines M": [4.82, 4.88, 4.92, 4.96, 5.00, 5.02],
        "Traffic PB": [12.4, 13.1, 14.2, 15.8, 14.6, 13.8],
        "Cost K€": [385, 389, 401, 412, 398, 391],
    })
    esg_energy_monthly["kWh per Line"] = (esg_energy_monthly["Energy MWh"] * 1000 / (esg_energy_monthly["Active Lines M"] * 1_000_000)).round(3)
    esg_energy_monthly["kWh per TB"] = (esg_energy_monthly["Energy MWh"] / (esg_energy_monthly["Traffic PB"] * 1000)).round(4)

    esg_by_site = pd.DataFrame({
        "Site Type": ["Core PoP", "Transport Node", "OLT Cabinet", "Field Junction", "Office"],
        "Sites": [8, 42, 302, 1120, 6],
        "Energy MWh/mo": [1420, 980, 1280, 520, 150],
        "Renewable %": [78, 65, 42, 28, 92],
        "PUE": [1.45, 1.62, 1.85, 2.10, 1.35],
    })
    esg_by_site["Energy per Site MWh"] = (esg_by_site["Energy MWh/mo"] / esg_by_site["Sites"]).round(1)

    esg_carbon = pd.DataFrame({
        "Month": ["2025-09", "2025-10", "2025-11", "2025-12", "2026-01", "2026-02"],
        "Scope 1 tCO2": [42, 44, 46, 48, 45, 43],
        "Scope 2 tCO2": [1285, 1297, 1336, 1375, 1327, 1306],
        "Scope 3 tCO2": [420, 435, 448, 462, 445, 432],
    })
    esg_carbon["Total tCO2"] = esg_carbon["Scope 1 tCO2"] + esg_carbon["Scope 2 tCO2"] + esg_carbon["Scope 3 tCO2"]

    esg_copper_migration = pd.DataFrame({
        "Year": ["2023", "2024", "2025", "2026 (Plan)"],
        "Copper Lines K": [320, 180, 85, 25],
        "Fiber Lines K": [4200, 4650, 4920, 5100],
        "Energy Saved MWh": [0, 2800, 4200, 5100],
        "Carbon Avoided tCO2": [0, 840, 1260, 1530],
    })

    esg_initiatives = pd.DataFrame({
        "Initiative": ["Solar PV at Core Sites", "OLT Power Optimization", "Fleet EV Transition", "Office LED Retrofit", "Cooling Efficiency Upgrade"],
        "Status": ["In Progress", "Completed", "In Progress", "Completed", "Planned"],
        "Investment K€": [420, 85, 280, 45, 320],
        "Annual Savings K€": [95, 38, 62, 12, 78],
        "Carbon Reduction tCO2": [380, 145, 95, 28, 185],
        "Payback Years": [4.4, 2.2, 4.5, 3.8, 4.1],
    })

    current_energy = esg_energy_monthly["Energy MWh"].iloc[-1]
    current_kwh_line = esg_energy_monthly["kWh per Line"].iloc[-1]
    current_carbon = esg_carbon["Total tCO2"].iloc[-1]
    renewable_pct = round((esg_by_site["Energy MWh/mo"] * esg_by_site["Renewable %"] / 100).sum() / esg_by_site["Energy MWh/mo"].sum() * 100, 1)
    yoy_carbon_reduction = round((esg_carbon["Total tCO2"].iloc[0] - current_carbon) / esg_carbon["Total tCO2"].iloc[0] * 100, 1)

    st.markdown(f"""
    <div class="esg-pulse">
        <div class="esg-pulse-head">
            <span class="esg-pulse-title">🌍 ESG & Energy Efficiency Dashboard</span>
            <span class="esg-pulse-badge">Sustainability Report</span>
        </div>
        <div class="esg-pulse-grid">
            <div class="esg-pulse-card">
                <div class="esg-pulse-label">Monthly Energy</div>
                <div class="esg-pulse-value">{current_energy:,}</div>
                <div class="esg-pulse-delta">MWh</div>
            </div>
            <div class="esg-pulse-card">
                <div class="esg-pulse-label">kWh per Line</div>
                <div class="esg-pulse-value">{current_kwh_line}</div>
                <div class="esg-pulse-delta">↓ -4% YoY</div>
            </div>
            <div class="esg-pulse-card">
                <div class="esg-pulse-label">Carbon Footprint</div>
                <div class="esg-pulse-value">{current_carbon:,}</div>
                <div class="esg-pulse-delta">tCO2/month</div>
            </div>
            <div class="esg-pulse-card">
                <div class="esg-pulse-label">Renewable Energy</div>
                <div class="esg-pulse-value">{renewable_pct}%</div>
                <div class="esg-pulse-delta">↑ +8pp YoY</div>
            </div>
            <div class="esg-pulse-card">
                <div class="esg-pulse-label">Carbon Reduction</div>
                <div class="esg-pulse-value">{abs(yoy_carbon_reduction)}%</div>
                <div class="esg-pulse-delta">vs baseline</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    esg_tab_energy, esg_tab_carbon, esg_tab_migration = st.tabs(["⚡ Energy Efficiency", "🌱 Carbon Footprint", "🔄 Copper Migration"])

    with esg_tab_energy:
        st.markdown('<div class="esg-title">Energy Consumption Analysis</div>', unsafe_allow_html=True)
        en_col1, en_col2 = st.columns(2)

        with en_col1:
            st.markdown('<div class="esg-mini-title">Energy vs Traffic Trend</div>', unsafe_allow_html=True)
            with st.container(border=True):
                energy_line = alt.Chart(esg_energy_monthly).mark_line(point=True, strokeWidth=2.5, color="#10B981").encode(
                    x=alt.X("Month:N", title=None),
                    y=alt.Y("Energy MWh:Q", title="Energy (MWh)"),
                    tooltip=["Month:N", alt.Tooltip("Energy MWh:Q", format=","), alt.Tooltip("Traffic PB:Q", format=".1f")],
                )
                traffic_line = alt.Chart(esg_energy_monthly).mark_line(point=True, strokeWidth=2.5, color="#6366F1").encode(
                    x=alt.X("Month:N", title=None),
                    y=alt.Y("Traffic PB:Q", title="Traffic (PB)"),
                )
                st.altair_chart(style_esg_chart(alt.layer(energy_line, traffic_line).resolve_scale(y="independent"), height=240), use_container_width=True)
                render_esg_ai_reco(
                    "Energy Efficiency",
                    "Energy consumption stable while traffic grew 11%, indicating improved efficiency.",
                    "Continue network optimization and equipment refresh programs.",
                    "Achieve 2026 target of 15% efficiency improvement.",
                )

        with en_col2:
            st.markdown('<div class="esg-mini-title">kWh per Line Trend</div>', unsafe_allow_html=True)
            with st.container(border=True):
                kwh_line = alt.Chart(esg_energy_monthly).mark_area(opacity=0.6, color="#10B981", line={"color": "#059669", "strokeWidth": 2}).encode(
                    x=alt.X("Month:N", title=None),
                    y=alt.Y("kWh per Line:Q", title="kWh per Line", scale=alt.Scale(domain=[0.85, 0.92])),
                    tooltip=["Month:N", alt.Tooltip("kWh per Line:Q", format=".3f")],
                )
                st.altair_chart(style_esg_chart(kwh_line, height=240), use_container_width=True)
                render_esg_ai_reco(
                    "Per-Line Efficiency",
                    f"Current kWh/line ({current_kwh_line}) is 4% below 2025 baseline.",
                    "Target 0.80 kWh/line by end of 2026 through OLT optimization.",
                    "Reduce operating costs and carbon intensity per customer.",
                )

        st.markdown('<div class="esg-title">Energy by Site Type</div>', unsafe_allow_html=True)
        site_col1, site_col2 = st.columns(2)

        with site_col1:
            st.markdown('<div class="esg-mini-title">Energy Distribution</div>', unsafe_allow_html=True)
            with st.container(border=True):
                site_donut = alt.Chart(esg_by_site).mark_arc(innerRadius=55, outerRadius=95).encode(
                    theta=alt.Theta("Energy MWh/mo:Q", stack=True),
                    color=alt.Color("Site Type:N", scale=alt.Scale(range=["#10B981", "#3B82F6", "#F59E0B", "#EF4444", "#8B5CF6"]), legend=alt.Legend(title=None)),
                    tooltip=["Site Type:N", alt.Tooltip("Energy MWh/mo:Q", format=","), alt.Tooltip("Renewable %:Q", format=".0f"), alt.Tooltip("PUE:Q", format=".2f")],
                )
                st.altair_chart(style_esg_chart(site_donut, height=240), use_container_width=True)
                top_consumer = esg_by_site.sort_values("Energy MWh/mo", ascending=False).iloc[0]
                render_esg_ai_reco(
                    "Energy Concentration",
                    f"{top_consumer['Site Type']} consumes highest energy ({top_consumer['Energy MWh/mo']:,} MWh/mo).",
                    "Focus efficiency upgrades on high-consumption site types.",
                    "Reduce peak energy demand 15% through targeted optimization.",
                )

        with site_col2:
            st.markdown('<div class="esg-mini-title">Renewable % by Site Type</div>', unsafe_allow_html=True)
            with st.container(border=True):
                renew_bar = alt.Chart(esg_by_site).mark_bar(cornerRadiusTopRight=5, cornerRadiusBottomRight=5, size=20).encode(
                    x=alt.X("Renewable %:Q", title="Renewable Energy (%)", scale=alt.Scale(domain=[0, 100])),
                    y=alt.Y("Site Type:N", title=None, sort="-x"),
                    color=alt.Color("Renewable %:Q", scale=alt.Scale(scheme="greens"), legend=None),
                    tooltip=["Site Type:N", alt.Tooltip("Renewable %:Q", format=".0f"), alt.Tooltip("Energy MWh/mo:Q", format=",")],
                )
                st.altair_chart(style_esg_chart(renew_bar, height=240), use_container_width=True)
                low_renew = esg_by_site.sort_values("Renewable %").iloc[0]
                render_esg_ai_reco(
                    "Renewable Opportunity",
                    f"{low_renew['Site Type']} has lowest renewable share ({low_renew['Renewable %']}%).",
                    "Prioritize solar/battery deployment at field junction sites.",
                    "Increase overall renewable mix toward 70% target.",
                    level="warning",
                )

    with esg_tab_carbon:
        st.markdown('<div class="esg-title">Carbon Footprint Tracking</div>', unsafe_allow_html=True)
        c_col1, c_col2 = st.columns(2)

        with c_col1:
            st.markdown('<div class="esg-mini-title">Emissions by Scope</div>', unsafe_allow_html=True)
            with st.container(border=True):
                carbon_long = esg_carbon.melt(id_vars=["Month"], value_vars=["Scope 1 tCO2", "Scope 2 tCO2", "Scope 3 tCO2"], var_name="Scope", value_name="tCO2")
                carbon_area = alt.Chart(carbon_long).mark_area(opacity=0.7).encode(
                    x=alt.X("Month:N", title=None),
                    y=alt.Y("tCO2:Q", title="tCO2", stack=True),
                    color=alt.Color("Scope:N", scale=alt.Scale(domain=["Scope 1 tCO2", "Scope 2 tCO2", "Scope 3 tCO2"], range=["#EF4444", "#F59E0B", "#3B82F6"]), legend=alt.Legend(title=None)),
                    tooltip=["Month:N", "Scope:N", alt.Tooltip("tCO2:Q", format=",")],
                )
                st.altair_chart(style_esg_chart(carbon_area, height=240), use_container_width=True)
                scope2_pct = round(esg_carbon["Scope 2 tCO2"].iloc[-1] / current_carbon * 100, 0)
                render_esg_ai_reco(
                    "Carbon Breakdown",
                    f"Scope 2 (purchased electricity) represents {scope2_pct}% of emissions.",
                    "Accelerate renewable energy procurement and PPA agreements.",
                    "Reduce Scope 2 emissions 25% by 2027.",
                )

        with c_col2:
            st.markdown('<div class="esg-mini-title">Total Carbon Trend</div>', unsafe_allow_html=True)
            with st.container(border=True):
                total_line = alt.Chart(esg_carbon).mark_line(point=True, strokeWidth=3, color="#10B981").encode(
                    x=alt.X("Month:N", title=None),
                    y=alt.Y("Total tCO2:Q", title="Total tCO2"),
                    tooltip=["Month:N", alt.Tooltip("Total tCO2:Q", format=",")],
                )
                target_rule = alt.Chart(pd.DataFrame({"y": [1600]})).mark_rule(strokeDash=[4, 4], color="#EF4444").encode(y="y:Q")
                st.altair_chart(style_esg_chart(total_line + target_rule, height=240), use_container_width=True)
                render_esg_ai_reco(
                    "Carbon Target",
                    f"Current emissions ({current_carbon:,} tCO2) below 1,600 monthly target.",
                    "Maintain trajectory; prepare for SBTi commitment reporting.",
                    "Achieve carbon neutral operations by 2030.",
                )

        st.markdown('<div class="esg-title">ESG Initiatives Portfolio</div>', unsafe_allow_html=True)
        with st.container(border=True):
            st.dataframe(
                esg_initiatives.style.format({
                    "Investment K€": "€{:,.0f}",
                    "Annual Savings K€": "€{:,.0f}",
                    "Carbon Reduction tCO2": "{:,.0f}",
                    "Payback Years": "{:.1f}",
                }).background_gradient(subset=["Carbon Reduction tCO2"], cmap="Greens"),
                use_container_width=True,
                hide_index=True,
            )

    with esg_tab_migration:
        st.markdown('<div class="esg-title">Copper to Fiber Migration Impact</div>', unsafe_allow_html=True)
        mig_col1, mig_col2 = st.columns(2)

        with mig_col1:
            st.markdown('<div class="esg-mini-title">Line Migration Progress</div>', unsafe_allow_html=True)
            with st.container(border=True):
                mig_long = esg_copper_migration.melt(id_vars=["Year"], value_vars=["Copper Lines K", "Fiber Lines K"], var_name="Type", value_name="Lines K")
                mig_bar = alt.Chart(mig_long).mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4).encode(
                    x=alt.X("Year:N", title=None),
                    y=alt.Y("Lines K:Q", title="Lines (K)"),
                    color=alt.Color("Type:N", scale=alt.Scale(domain=["Copper Lines K", "Fiber Lines K"], range=["#94A3B8", "#10B981"]), legend=alt.Legend(title=None)),
                    xOffset="Type:N",
                    tooltip=["Year:N", "Type:N", alt.Tooltip("Lines K:Q", format=",")],
                )
                st.altair_chart(style_esg_chart(mig_bar, height=240), use_container_width=True)
                copper_reduction = round((320 - 25) / 320 * 100, 0)
                render_esg_ai_reco(
                    "Migration Progress",
                    f"Copper lines reduced {copper_reduction}% since 2023 (320K → 25K planned).",
                    "Complete final copper sunset in 2027 for full fiber network.",
                    "Eliminate legacy infrastructure costs and energy waste.",
                )

        with mig_col2:
            st.markdown('<div class="esg-mini-title">Environmental Benefits</div>', unsafe_allow_html=True)
            with st.container(border=True):
                benefit_long = esg_copper_migration.melt(id_vars=["Year"], value_vars=["Energy Saved MWh", "Carbon Avoided tCO2"], var_name="Metric", value_name="Value")
                benefit_line = alt.Chart(benefit_long).mark_line(point=True, strokeWidth=2.5).encode(
                    x=alt.X("Year:N", title=None),
                    y=alt.Y("Value:Q", title="Value"),
                    color=alt.Color("Metric:N", scale=alt.Scale(domain=["Energy Saved MWh", "Carbon Avoided tCO2"], range=["#3B82F6", "#10B981"]), legend=alt.Legend(title=None)),
                    tooltip=["Year:N", "Metric:N", alt.Tooltip("Value:Q", format=",")],
                )
                st.altair_chart(style_esg_chart(benefit_line, height=240), use_container_width=True)
                total_saved = esg_copper_migration["Energy Saved MWh"].sum()
                total_avoided = esg_copper_migration["Carbon Avoided tCO2"].sum()
                render_esg_ai_reco(
                    "Migration Benefits",
                    f"Cumulative: {total_saved:,} MWh saved, {total_avoided:,} tCO2 avoided.",
                    "Highlight migration benefits in ESG reporting and investor communications.",
                    "Strengthen sustainability credentials with stakeholders.",
                )

    st.markdown("""
    <details style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 0.8rem; margin-top: 1rem;">
        <summary style="cursor: pointer; font-weight: 600; color: #334155; font-size: 0.9rem;">▸ Data Sources & Systems</summary>
        <div style="margin-top: 0.8rem; font-size: 0.85rem; color: #475569;">
            <p><strong>This dashboard aggregates data from the following source systems:</strong></p>
            <table style="width: 100%; border-collapse: collapse; margin: 0.5rem 0;">
                <tr style="border-bottom: 1px solid #E2E8F0;"><th style="text-align: left; padding: 0.4rem;">Data Element</th><th style="text-align: left; padding: 0.4rem;">Source System</th><th style="text-align: left; padding: 0.4rem;">Refresh</th></tr>
                <tr><td style="padding: 0.4rem;">Energy consumption</td><td style="padding: 0.4rem;"><strong>BMS</strong> + Smart meters</td><td style="padding: 0.4rem;">Hourly</td></tr>
                <tr><td style="padding: 0.4rem;">Carbon emissions</td><td style="padding: 0.4rem;"><strong>Salesforce Net Zero</strong></td><td style="padding: 0.4rem;">Monthly</td></tr>
                <tr><td style="padding: 0.4rem;">PUE metrics</td><td style="padding: 0.4rem;"><strong>DCIM</strong> Infrastructure Mgmt</td><td style="padding: 0.4rem;">Real-time</td></tr>
                <tr><td style="padding: 0.4rem;">Renewable energy %</td><td style="padding: 0.4rem;"><strong>Energy procurement</strong> + Grid</td><td style="padding: 0.4rem;">Daily</td></tr>
                <tr><td style="padding: 0.4rem;">Copper migration</td><td style="padding: 0.4rem;"><strong>Network Inventory (NIS)</strong></td><td style="padding: 0.4rem;">Weekly</td></tr>
                <tr><td style="padding: 0.4rem;">Environmental savings</td><td style="padding: 0.4rem;"><strong>ESG Calculation Engine</strong></td><td style="padding: 0.4rem;">Monthly</td></tr>
            </table>
            <p><strong>Key Integrations:</strong></p>
            <ul style="margin: 0.3rem 0; padding-left: 1.2rem;">
                <li>Energy data from <strong>Iberdrola/Endesa</strong> utility APIs</li>
                <li>Carbon factors from <strong>IDAE</strong></li>
                <li>Reporting aligned with <strong>GRI Standards</strong> and <strong>CDP Climate</strong></li>
                <li>Third-party verification by <strong>Bureau Veritas</strong></li>
            </ul>
        </div>
    </details>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Page: Subscribers (now after new wholesale pages)
# ---------------------------------------------------------------------------
elif selected_menu == "Subscribers":
    import pandas as pd
    import altair as alt

    SUB_CHART_THEME = {
        "font": "Poppins, sans-serif",
        "title_color": "#0F172A",
        "label_color": "#334155",
        "grid_color": "#E2E8F0",
        "accent_blue": "#29B5E8",
        "accent_green": "#10B981",
        "accent_indigo": "#6366F1",
        "accent_amber": "#F59E0B",
        "accent_red": "#EF4444",
        "accent_purple": "#8B5CF6",
    }

    def style_sub_chart(chart: alt.Chart, height: int = 220) -> alt.Chart:
        return (
            chart.properties(height=height, padding={"left": 6, "top": 10, "right": 8, "bottom": 6})
            .configure(background="#FFFFFF")
            .configure_view(stroke=None)
            .configure_axis(
                labelFont=SUB_CHART_THEME["font"],
                titleFont=SUB_CHART_THEME["font"],
                labelColor=SUB_CHART_THEME["label_color"],
                titleColor=SUB_CHART_THEME["label_color"],
                labelFontSize=11,
                titleFontSize=12,
                domain=False,
                gridColor=SUB_CHART_THEME["grid_color"],
                gridOpacity=0.75,
            )
            .configure_legend(
                labelFont=SUB_CHART_THEME["font"],
                titleFont=SUB_CHART_THEME["font"],
                labelColor=SUB_CHART_THEME["label_color"],
                titleColor=SUB_CHART_THEME["label_color"],
                orient="top",
                direction="horizontal",
                symbolType="circle",
                symbolSize=100,
            )
        )

    def render_sub_ai_reco(headline: str, insight: str, action: str, impact: str, level: str = "info") -> None:
        st.markdown(
            f"""<div class="sub-ai-card {level}"><div class="sub-ai-head">🤖 AI Recommendation · {headline}</div><div class="sub-ai-line"><strong>Insight:</strong> {insight}</div><div class="sub-ai-line"><strong>Action:</strong> {action}</div><div class="sub-ai-line"><strong>Expected Impact:</strong> {impact}</div></div>""",
            unsafe_allow_html=True,
        )

    st.markdown("""<style>
@keyframes sub-fade-up { 0% { opacity: 0; transform: translateY(10px); } 100% { opacity: 1; transform: translateY(0); } }
@keyframes sub-shimmer { 0% { left: -40%; } 100% { left: 120%; } }
@keyframes sub-pulse-dot { 0%,100% { transform: scale(1); opacity: 0.7; } 50% { transform: scale(1.25); opacity: 1; } }
.sub-title { position: relative; overflow: hidden; display: flex; align-items: center; gap: 0.55rem; margin: 1.2rem 0 0.8rem; padding: 0.6rem 0.85rem; border-radius: 12px; border: 1px solid #DBEAFE; background: linear-gradient(135deg, #F0F8FF 0%, #EEF2FF 100%); color: #1B2A4E; font-size: 1rem; font-weight: 700; animation: sub-fade-up 0.4s ease-out both; }
.sub-title::before { content: ""; width: 8px; height: 8px; border-radius: 50%; background: linear-gradient(135deg, #29B5E8, #6366F1); animation: sub-pulse-dot 1.8s ease-in-out infinite; }
.sub-title::after { content: ""; position: absolute; top: 0; left: -40%; width: 34%; height: 100%; background: linear-gradient(90deg, transparent, rgba(255,255,255,0.85), transparent); animation: sub-shimmer 3.2s ease-in-out infinite; }
.sub-mini-title { display: inline-flex; align-items: center; gap: 0.4rem; margin: 0.15rem 0 0.55rem; font-size: 0.9rem; font-weight: 700; color: #1E3A8A; }
.sub-mini-title::before { content: ""; width: 7px; height: 7px; border-radius: 50%; background: linear-gradient(135deg, #22C1EE, #8B5CF6); }
.sub-pulse { position: relative; overflow: hidden; border-radius: 14px; border: 1px solid #BFDBFE; background: linear-gradient(135deg, #EFF6FF 0%, #ECFEFF 100%); padding: 1rem 1.1rem; margin-bottom: 1rem; }
.sub-pulse::before { content: ""; position: absolute; top: 0; left: -50%; width: 40%; height: 100%; background: linear-gradient(90deg, transparent, rgba(41,181,232,0.2), transparent); animation: sub-shimmer 3s ease-in-out infinite; }
.sub-pulse-head { position: relative; z-index: 1; display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.75rem; }
.sub-pulse-title { color: #1E3A8A; font-weight: 700; font-size: 0.92rem; }
.sub-pulse-live { color: #10B981; font-size: 0.74rem; font-weight: 700; display: inline-flex; align-items: center; gap: 0.35rem; }
.sub-pulse-live::before { content: ""; width: 8px; height: 8px; border-radius: 50%; background: #10B981; animation: sub-pulse-dot 1.2s ease-in-out infinite; }
.sub-pulse-grid { position: relative; z-index: 1; display: grid; grid-template-columns: repeat(5, 1fr); gap: 0.65rem; }
.sub-pulse-card { background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 10px; padding: 0.65rem 0.72rem; animation: sub-fade-up 0.4s ease-out both; }
.sub-pulse-card:nth-child(1) { animation-delay: 0.05s; } .sub-pulse-card:nth-child(2) { animation-delay: 0.12s; } .sub-pulse-card:nth-child(3) { animation-delay: 0.2s; } .sub-pulse-card:nth-child(4) { animation-delay: 0.28s; } .sub-pulse-card:nth-child(5) { animation-delay: 0.36s; }
.sub-pulse-label { color: #64748B; font-size: 0.66rem; text-transform: uppercase; letter-spacing: 0.04em; margin-bottom: 0.2rem; }
.sub-pulse-value { color: #0F172A; font-size: 1.28rem; font-weight: 800; line-height: 1.15; }
.sub-pulse-delta { margin-top: 0.2rem; color: #059669; font-size: 0.74rem; font-weight: 700; }
.sub-ai-card { margin-top: 0.6rem; border-radius: 10px; border: 1px solid #D1E9FF; background: linear-gradient(135deg, #F8FBFF 0%, #EEF6FF 100%); padding: 0.62rem 0.78rem; box-shadow: 0 4px 14px rgba(15, 23, 42, 0.05); animation: sub-fade-up 0.35s ease-out both; }
.sub-ai-card.warning { border-color: #FCD34D; background: linear-gradient(135deg, #FFFBEB 0%, #FEF3C7 100%); }
.sub-ai-card.critical { border-color: #FCA5A5; background: linear-gradient(135deg, #FEF2F2 0%, #FEE2E2 100%); }
.sub-ai-head { color: #1E3A8A; font-size: 0.78rem; font-weight: 700; margin-bottom: 0.28rem; }
.sub-ai-card.warning .sub-ai-head { color: #92400E; }
.sub-ai-card.critical .sub-ai-head { color: #991B1B; }
.sub-ai-line { color: #334155; font-size: 0.77rem; line-height: 1.34; margin: 0.12rem 0; }
.sub-kpi-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.6rem; margin-bottom: 0.75rem; }
.sub-kpi-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 10px;
    padding: 0.55rem 0.62rem;
    box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
    animation: sub-fade-up 0.35s ease-out both;
}
.sub-kpi-card .k {
    color: #64748B;
    font-size: 0.64rem;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}
.sub-kpi-card .v {
    color: #0F172A;
    font-size: 1.02rem;
    font-weight: 800;
    margin-top: 0.12rem;
    line-height: 1.15;
}
.sub-kpi-card .d {
    color: #059669;
    font-size: 0.68rem;
    font-weight: 700;
    margin-top: 0.14rem;
}
.sub-kpi-card.warn .d { color: #B45309; }
.sub-kpi-card.crit .d { color: #B91C1C; }
@media (max-width: 980px) { .sub-pulse-grid { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 980px) { .sub-kpi-grid { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 640px) { .sub-pulse-grid { grid-template-columns: 1fr; } }
@media (max-width: 640px) { .sub-kpi-grid { grid-template-columns: 1fr; } }
</style>""", unsafe_allow_html=True)

    # -------------------------------------------------------------------
    # Synthetic and internally consistent subscriber dataset
    # -------------------------------------------------------------------
    sub_monthly = pd.DataFrame({
        "Month": ["2025-09", "2025-10", "2025-11", "2025-12", "2026-01", "2026-02"],
        "Adds": [820, 790, 870, 830, 860, 900],
        "Churned": [610, 610, 620, 640, 640, 643],
    })
    sub_monthly["Net Adds"] = sub_monthly["Adds"] - sub_monthly["Churned"]
    starting_base = 28940
    sub_monthly["Base"] = starting_base + sub_monthly["Net Adds"].cumsum()
    sub_monthly["Churn %"] = (sub_monthly["Churned"] / (sub_monthly["Base"] - sub_monthly["Net Adds"]) * 100).round(2)

    sub_segments = pd.DataFrame({
        "Segment": ["MasOrange", "Vodafone"],
        "Subscribers": [7000000, 5000000],
        "NPS": [58, 54],
        "ARPU": [3.50, 3.58],
    })

    sub_risk = pd.DataFrame({
        "Segment": ["Budget", "Standard", "Premium", "VIP"],
        "At Risk": [312, 289, 178, 68],
        "Revenue at Risk K": [95, 78, 51, 16],
        "Propensity": [0.78, 0.65, 0.52, 0.41],
    })

    funnel_df = pd.DataFrame({
        "Stage": ["Leads", "Qualified", "Orders", "Installed", "Activated"],
        "Users": [6200, 4100, 2900, 2480, 2310],
    })

    support_df = pd.DataFrame({
        "Queue": ["Billing", "Tech L1", "Tech L2", "Install", "Retention"],
        "Resolution Hrs": [7.2, 5.4, 10.6, 6.8, 4.1],
        "CSAT": [4.1, 4.4, 3.8, 4.2, 4.5],
        "Tickets": [920, 1280, 510, 640, 430],
    })

    retention_df = pd.DataFrame({
        "Campaign": ["Save Offer A", "Save Offer B", "Proactive NOC", "VIP Concierge"],
        "Contacted": [480, 390, 260, 120],
        "Saved": [228, 156, 123, 66],
    })
    retention_df["Save Rate"] = (retention_df["Saved"] / retention_df["Contacted"] * 100).round(1)
    retention_df["Value Saved K"] = [420, 280, 190, 120]

    churn_type_df = pd.DataFrame({
        "Month": sub_monthly["Month"],
        "Voluntary": [430, 425, 432, 438, 436, 430],
        "Involuntary": [180, 185, 188, 202, 204, 213],
    })

    reactivation_df = pd.DataFrame({
        "Month": sub_monthly["Month"],
        "Reactivated": [105, 112, 118, 121, 126, 133],
    })

    tenure_df = pd.DataFrame({
        "Tenure Band": ["0-3m", "4-6m", "7-12m", "13-24m", "25m+"],
        "Subscribers": [4200, 5200, 7800, 6900, 6147],
        "Churn %": [4.8, 3.4, 2.3, 1.6, 1.1],
    })

    channel_df = pd.DataFrame({
        "Channel": ["PF Web Leads", "Referidos PF", "Tiendas PF", "Fuerza Comercial FTTH", "Canal Constructoras"],
        "Leads": [2400, 1100, 1700, 1200, 900],
        "Activations": [920, 560, 610, 470, 340],
    })
    channel_df["Conversion %"] = (channel_df["Activations"] / channel_df["Leads"] * 100).round(1)

    channel_econ_df = pd.DataFrame({
        "Channel": ["PF Web Leads", "Referidos PF", "Tiendas PF", "Fuerza Comercial FTTH", "Canal Constructoras"],
        "CAC": [128, 74, 112, 156, 138],
        "LTV": [468, 512, 472, 520, 495],
    })
    channel_econ_df["LTV/CAC"] = (channel_econ_df["LTV"] / channel_econ_df["CAC"]).round(2)

    csat_contact_df = pd.DataFrame({
        "Contact Type": ["Chat", "Phone", "Email", "App", "Field Visit"],
        "CSAT": [4.5, 4.1, 4.0, 4.6, 3.9],
    })

    digital_df = pd.DataFrame({
        "Month": sub_monthly["Month"],
        "SelfService Users": [9800, 10150, 10420, 10810, 11120, 11560],
    })

    complaint_df = pd.DataFrame({
        "Reason": ["Slow speed", "Billing disputes", "Service downtime", "Installation delays", "WiFi issues"],
        "Volume": [420, 310, 280, 190, 260],
    })

    risk_score_df = pd.DataFrame({
        "Band": ["0.0-0.2", "0.2-0.4", "0.4-0.6", "0.6-0.8", "0.8-1.0"],
        "Customers": [9600, 8400, 6200, 4200, 1847],
    })

    total_subs = int(sub_segments["Subscribers"].sum())
    latest = sub_monthly.iloc[-1]
    prev = sub_monthly.iloc[-2]
    qoq_ref = sub_monthly.iloc[-4]
    latest_net = int(latest["Net Adds"])
    latest_churn = float(latest["Churn %"])
    latest_base = int(latest["Base"])
    prev_base = int(prev["Base"])
    adds_last = int(latest["Adds"])
    churned_last = int(latest["Churned"])
    weighted_nps = int(round((sub_segments["NPS"] * sub_segments["Subscribers"]).sum() / total_subs, 0))
    blended_arpu = round((sub_segments["ARPU"] * sub_segments["Subscribers"]).sum() / total_subs, 2)
    risk_customers = int(sub_risk["At Risk"].sum())
    risk_arr_m = round(sub_risk["Revenue at Risk K"].sum() * 12 / 1000, 1)
    growth_mom = round((latest_base - prev_base) / prev_base * 100, 2)
    growth_qoq = round((latest_base - int(qoq_ref["Base"])) / int(qoq_ref["Base"]) * 100, 2)
    voluntary_pct = round(churn_type_df.iloc[-1]["Voluntary"] / churned_last * 100, 1)
    involuntary_pct = round(churn_type_df.iloc[-1]["Involuntary"] / churned_last * 100, 1)
    early_life_churn = float(tenure_df.loc[tenure_df["Tenure Band"] == "0-3m", "Churn %"].iloc[0])
    save_rate_overall = round(retention_df["Saved"].sum() / retention_df["Contacted"].sum() * 100, 1)
    risk_coverage = round(retention_df["Contacted"].sum() / risk_customers * 100, 1)
    reactivation_rate = round(reactivation_df.iloc[-1]["Reactivated"] / churned_last * 100, 1)
    avg_tenure_months = round((tenure_df["Subscribers"] * pd.Series([2, 5, 9, 18, 36])).sum() / tenure_df["Subscribers"].sum(), 1)
    long_tenure_mix = round((tenure_df.loc[tenure_df["Tenure Band"].isin(["13-24m", "25m+"]), "Subscribers"].sum() / total_subs) * 100, 1)
    fcr = 78.4
    avg_resolution = round((support_df["Resolution Hrs"] * support_df["Tickets"]).sum() / support_df["Tickets"].sum(), 1)
    complaint_rate = round(complaint_df["Volume"].sum() / total_subs * 1000, 1)
    install_to_activation = round((funnel_df.loc[funnel_df["Stage"] == "Activated", "Users"].iloc[0] / funnel_df.loc[funnel_df["Stage"] == "Installed", "Users"].iloc[0]) * 100, 1)
    activation_lead_days = 2.8
    digital_adoption = round(digital_df.iloc[-1]["SelfService Users"] / total_subs * 100, 1)
    arpu_uplift = "+€3.8"
    churn_cost_avoided_m = round(retention_df["Value Saved K"].sum() / 1000, 2)
    ltv_cac_blended = round(channel_econ_df["LTV/CAC"].mean(), 2)
    predictive_churn_index = round(sub_risk["Propensity"].mean() * 100, 1)

    st.markdown(dedent(f"""
    <div class="sub-pulse">
        <div class="sub-pulse-head">
            <span class="sub-pulse-title">👥 Subscriber Pulse · Key Customer Metrics</span>
            <span class="sub-pulse-live">Live</span>
        </div>
        <div class="sub-pulse-grid">
            <div class="sub-pulse-card">
                <div class="sub-pulse-label">Total Subscribers</div>
                <div class="sub-pulse-value">{total_subs:,}</div>
                <div class="sub-pulse-delta">↑ +{latest_net} net adds</div>
            </div>
            <div class="sub-pulse-card">
                <div class="sub-pulse-label">New Adds (Month)</div>
                <div class="sub-pulse-value">{adds_last:,}</div>
                <div class="sub-pulse-delta">↑ +{int(latest['Adds']-prev['Adds'])} vs prior month</div>
            </div>
            <div class="sub-pulse-card">
                <div class="sub-pulse-label">Churn Rate</div>
                <div class="sub-pulse-value">{latest_churn:.1f}%</div>
                <div class="sub-pulse-delta">↓ {(prev['Churn %']-latest_churn):.1f}pp improvement</div>
            </div>
            <div class="sub-pulse-card">
                <div class="sub-pulse-label">NPS</div>
                <div class="sub-pulse-value">+{weighted_nps}</div>
                <div class="sub-pulse-delta">Strong CX momentum</div>
            </div>
            <div class="sub-pulse-card">
                <div class="sub-pulse-label">At-Risk Base</div>
                <div class="sub-pulse-value">{risk_customers}</div>
                <div class="sub-pulse-delta">€{risk_arr_m:.1f}M ARR exposed</div>
            </div>
        </div>
    </div>
    """), unsafe_allow_html=True)

    sub_tab_overview, sub_tab_journey, sub_tab_risk = st.tabs(
        ["📈 Subscriber Overview", "🧭 Journey & Experience", "⚠️ Risk & Retention"]
    )

    with sub_tab_overview:
        st.markdown('<div class="sub-title">Subscriber Growth Momentum</div>', unsafe_allow_html=True)
        st.markdown(dedent(f"""
            <div class="sub-kpi-grid">
                <div class="sub-kpi-card"><div class="k">Gross Adds</div><div class="v">{adds_last:,}</div><div class="d">Monthly intake</div></div>
                <div class="sub-kpi-card"><div class="k">Churned Subs</div><div class="v">{churned_last:,}</div><div class="d">Monthly exits</div></div>
                <div class="sub-kpi-card"><div class="k">Net Adds</div><div class="v">{latest_net:,}</div><div class="d">Positive momentum</div></div>
                <div class="sub-kpi-card"><div class="k">Growth MoM</div><div class="v">{growth_mom:.2f}%</div><div class="d">Base acceleration</div></div>
                <div class="sub-kpi-card"><div class="k">Growth QoQ</div><div class="v">{growth_qoq:.2f}%</div><div class="d">Quarter trend</div></div>
                <div class="sub-kpi-card"><div class="k">Voluntary Churn</div><div class="v">{voluntary_pct:.1f}%</div><div class="d">Of total churn</div></div>
                <div class="sub-kpi-card warn"><div class="k">Involuntary Churn</div><div class="v">{involuntary_pct:.1f}%</div><div class="d">Billing-driven exits</div></div>
                <div class="sub-kpi-card crit"><div class="k">Early-Life Churn</div><div class="v">{early_life_churn:.1f}%</div><div class="d">0-3 month risk</div></div>
                <div class="sub-kpi-card"><div class="k">Average Tenure</div><div class="v">{avg_tenure_months:.1f}m</div><div class="d">Customer maturity</div></div>
                <div class="sub-kpi-card"><div class="k">Long Tenure Mix</div><div class="v">{long_tenure_mix:.1f}%</div><div class="d">13+ months</div></div>
                <div class="sub-kpi-card"><div class="k">NPS (Weighted)</div><div class="v">+{weighted_nps}</div><div class="d">Brand loyalty</div></div>
                <div class="sub-kpi-card"><div class="k">ARPU (Blended)</div><div class="v">€{blended_arpu:.2f}</div><div class="d">{arpu_uplift} vs last qtr</div></div>
            </div>
        """), unsafe_allow_html=True)
        ov_col1, ov_col2 = st.columns(2)

        with ov_col1:
            st.markdown('<div class="sub-mini-title">Adds vs Churn vs Base Trend</div>', unsafe_allow_html=True)
            with st.container(border=True):
                bars = alt.Chart(sub_monthly).transform_fold(
                    ["Adds", "Churned"], as_=["Metric", "Count"]
                ).mark_bar(opacity=0.82, cornerRadiusTopLeft=5, cornerRadiusTopRight=5).encode(
                    x=alt.X("Month:N", title=None),
                    y=alt.Y("Count:Q", title="Adds / Churn"),
                    color=alt.Color("Metric:N", scale=alt.Scale(domain=["Adds", "Churned"], range=["#29B5E8", "#EF4444"]), legend=alt.Legend(title=None)),
                    xOffset="Metric:N",
                    tooltip=[alt.Tooltip("Month:N"), alt.Tooltip("Metric:N"), alt.Tooltip("Count:Q")],
                )
                base_line = alt.Chart(sub_monthly).mark_line(point=True, color="#10B981", strokeWidth=3).encode(
                    x=alt.X("Month:N", title=None),
                    y=alt.Y("Base:Q", title="Subscriber Base"),
                    tooltip=[alt.Tooltip("Month:N"), alt.Tooltip("Base:Q", format=",")],
                )
                st.altair_chart(style_sub_chart(alt.layer(bars, base_line).resolve_scale(y="independent"), height=230), use_container_width=True)
                net_total = int(sub_monthly["Net Adds"].sum())
                render_sub_ai_reco(
                    "Growth Momentum",
                    f"Subscriber base grew by {net_total:,} over the last 6 months with stable monthly additions.",
                    "Maintain acquisition pace while tightening early-life churn controls in first 30 days.",
                    "Sustain positive net adds and improve growth quality.",
                )

        with ov_col2:
            st.markdown('<div class="sub-mini-title">Partner Mix, NPS and Revenue/Home</div>', unsafe_allow_html=True)
            with st.container(border=True):
                seg_bubble = alt.Chart(sub_segments).mark_circle(opacity=0.88, stroke="#FFFFFF", strokeWidth=1.4).encode(
                    x=alt.X("Subscribers:Q", title="Homes Passed"),
                    y=alt.Y("NPS:Q", title="NPS", scale=alt.Scale(domain=[50, 66])),
                    size=alt.Size("ARPU:Q", title="Rev/Home", scale=alt.Scale(range=[300, 1600])),
                    color=alt.Color("Segment:N", scale=alt.Scale(domain=["MasOrange", "Vodafone"], range=["#FF6B00", "#E60000"]), legend=alt.Legend(title=None)),
                    tooltip=["Segment:N", alt.Tooltip("Subscribers:Q", format=",", title="Homes Passed"), "NPS:Q", alt.Tooltip("ARPU:Q", format=".2f", title="Rev/Home")],
                )
                seg_labels = alt.Chart(sub_segments).mark_text(dy=-12, fontSize=10, color="#1E293B").encode(
                    x="Subscribers:Q", y="NPS:Q", text="Segment:N"
                )
                st.altair_chart(style_sub_chart(seg_bubble + seg_labels, height=230), use_container_width=True)
                top_seg = sub_segments.loc[sub_segments["Subscribers"].idxmax()]
                render_sub_ai_reco(
                    "Partner Quality",
                    f"{top_seg['Segment']} has the largest footprint. Focus on network reliability for both partners.",
                    "Expand network capacity in high-demand regions and maintain SLA excellence.",
                    "Increase homes passed while maintaining partner satisfaction.",
                )

        st.markdown('<div class="sub-mini-title">Voluntary vs Involuntary Churn Split</div>', unsafe_allow_html=True)
        with st.container(border=True):
            split_latest = churn_type_df.iloc[-1]
            churn_split_df = pd.DataFrame({
                "Type": ["Voluntary", "Involuntary"],
                "Customers": [int(split_latest["Voluntary"]), int(split_latest["Involuntary"])],
            })
            churn_donut = alt.Chart(churn_split_df).mark_arc(innerRadius=58, outerRadius=100, cornerRadius=4, stroke="#FFFFFF", strokeWidth=2).encode(
                theta=alt.Theta("Customers:Q", stack=True),
                color=alt.Color("Type:N", scale=alt.Scale(domain=["Voluntary", "Involuntary"], range=["#29B5E8", "#EF4444"]), legend=alt.Legend(title=None)),
                tooltip=["Type:N", alt.Tooltip("Customers:Q", format=",")],
            )
            churn_center = alt.Chart(pd.DataFrame({"t": [f"{churned_last}"]})).mark_text(fontSize=22, fontWeight="bold", color="#0F172A").encode(text="t:N")
            churn_sub = alt.Chart(pd.DataFrame({"t": ["Total Churn"]})).mark_text(fontSize=11, dy=18, color="#64748B").encode(text="t:N")
            st.altair_chart(style_sub_chart(churn_donut + churn_center + churn_sub, height=230), use_container_width=True)
            render_sub_ai_reco(
                "Churn Type Mix",
                f"Involuntary churn is {involuntary_pct:.1f}% of monthly churn, indicating a billing/process component.",
                "Introduce proactive payment reminders + auto-retry flows before suspension events.",
                "Recover 4-6% of involuntary churners monthly.",
                level="warning",
            )

        st.markdown('<div class="sub-mini-title">Tenure Profile and Churn Risk Curve</div>', unsafe_allow_html=True)
        with st.container(border=True):
            tenure_bar = alt.Chart(tenure_df).mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6, color="#29B5E8", opacity=0.85).encode(
                x=alt.X("Tenure Band:N", title=None),
                y=alt.Y("Subscribers:Q", title="Subscribers"),
                tooltip=["Tenure Band:N", alt.Tooltip("Subscribers:Q", format=",")],
            )
            tenure_line = alt.Chart(tenure_df).mark_line(point=True, strokeWidth=3, color="#EF4444").encode(
                x=alt.X("Tenure Band:N", title=None),
                y=alt.Y("Churn %:Q", title="Churn %"),
                tooltip=["Tenure Band:N", alt.Tooltip("Churn %:Q", format=".1f")],
            )
            st.altair_chart(style_sub_chart(alt.layer(tenure_bar, tenure_line).resolve_scale(y="independent"), height=240), use_container_width=True)
            early_churn = tenure_df.loc[tenure_df["Tenure Band"] == "0-3m", "Churn %"].iloc[0]
            mature_churn = tenure_df.loc[tenure_df["Tenure Band"] == "25m+", "Churn %"].iloc[0]
            render_sub_ai_reco(
                "Tenure Risk",
                f"Churn drops from {early_churn:.1f}% in first 3 months to {mature_churn:.1f}% in mature base.",
                "Prioritize first-90-day onboarding quality checks and proactive welcome interventions.",
                "Reduce early-life churn by 0.6-0.9pp and improve lifetime value.",
                level="warning",
            )

    with sub_tab_journey:
        st.markdown('<div class="sub-title">Customer Journey & Experience</div>', unsafe_allow_html=True)
        st.markdown(dedent(f"""
            <div class="sub-kpi-grid">
                <div class="sub-kpi-card"><div class="k">Install→Activation</div><div class="v">{install_to_activation:.1f}%</div><div class="d">Operational conversion</div></div>
                <div class="sub-kpi-card"><div class="k">Activation Lead Time</div><div class="v">{activation_lead_days:.1f}d</div><div class="d">Order to live</div></div>
                <div class="sub-kpi-card"><div class="k">First Contact Resolution</div><div class="v">{fcr:.1f}%</div><div class="d">Support effectiveness</div></div>
                <div class="sub-kpi-card"><div class="k">Avg Resolution</div><div class="v">{avg_resolution:.1f}h</div><div class="d">Across all queues</div></div>
                <div class="sub-kpi-card warn"><div class="k">Complaint Rate</div><div class="v">{complaint_rate:.1f}</div><div class="d">Per 1,000 subs</div></div>
                <div class="sub-kpi-card"><div class="k">Digital Adoption</div><div class="v">{digital_adoption:.1f}%</div><div class="d">Self-service users</div></div>
                <div class="sub-kpi-card"><div class="k">Best Contact CSAT</div><div class="v">{csat_contact_df['CSAT'].max():.1f}</div><div class="d">{csat_contact_df.loc[csat_contact_df['CSAT'].idxmax(), 'Contact Type']}</div></div>
                <div class="sub-kpi-card crit"><div class="k">Weakest Contact CSAT</div><div class="v">{csat_contact_df['CSAT'].min():.1f}</div><div class="d">{csat_contact_df.loc[csat_contact_df['CSAT'].idxmin(), 'Contact Type']}</div></div>
            </div>
        """), unsafe_allow_html=True)
        jr_col1, jr_col2 = st.columns(2)

        with jr_col1:
            st.markdown('<div class="sub-mini-title">Onboarding Funnel Conversion</div>', unsafe_allow_html=True)
            with st.container(border=True):
                funnel = alt.Chart(funnel_df).mark_bar(cornerRadiusTopRight=8, cornerRadiusBottomRight=8, size=26).encode(
                    x=alt.X("Users:Q", title="Customers"),
                    y=alt.Y("Stage:N", sort=list(funnel_df["Stage"]), title=None),
                    color=alt.value("#29B5E8"),
                    tooltip=["Stage:N", alt.Tooltip("Users:Q", format=",")],
                )
                funnel_labels = alt.Chart(funnel_df).mark_text(align="left", dx=6, fontSize=10, color="#0F172A").encode(
                    x="Users:Q", y=alt.Y("Stage:N", sort=list(funnel_df["Stage"])), text=alt.Text("Users:Q", format=",")
                )
                st.altair_chart(style_sub_chart(funnel + funnel_labels, height=230), use_container_width=True)
                conv = 100 * funnel_df.iloc[-1]["Users"] / funnel_df.iloc[0]["Users"]
                render_sub_ai_reco(
                    "Onboarding Funnel",
                    f"End-to-end conversion is {conv:.1f}% from lead to activation.",
                    "Target the biggest drop between Qualified and Orders with assisted checkout nudges.",
                    "Increase activation volume by 6-8% without extra media spend.",
                    level="warning",
                )

        with jr_col2:
            st.markdown('<div class="sub-mini-title">Resolution Time vs CSAT by Queue</div>', unsafe_allow_html=True)
            with st.container(border=True):
                support_scatter = alt.Chart(support_df).mark_circle(opacity=0.88, stroke="#FFFFFF", strokeWidth=1.4).encode(
                    x=alt.X("Resolution Hrs:Q", title="Avg Resolution (hrs)"),
                    y=alt.Y("CSAT:Q", title="CSAT", scale=alt.Scale(domain=[3.6, 4.7])),
                    size=alt.Size("Tickets:Q", scale=alt.Scale(range=[220, 1400]), legend=None),
                    color=alt.Color("Queue:N", scale=alt.Scale(range=["#29B5E8", "#6366F1", "#EF4444", "#10B981", "#F59E0B"]), legend=alt.Legend(title=None)),
                    tooltip=["Queue:N", "Resolution Hrs:Q", "CSAT:Q", alt.Tooltip("Tickets:Q", format=",")],
                )
                support_labels = alt.Chart(support_df).mark_text(dy=-12, fontSize=9, color="#1E293B").encode(
                    x="Resolution Hrs:Q", y="CSAT:Q", text="Queue:N"
                )
                st.altair_chart(style_sub_chart(support_scatter + support_labels, height=230), use_container_width=True)
                worst_queue = support_df.sort_values(["CSAT", "Resolution Hrs"]).iloc[0]
                render_sub_ai_reco(
                    "Experience Operations",
                    f"{worst_queue['Queue']} has the weakest experience profile (CSAT {worst_queue['CSAT']:.1f}, {worst_queue['Resolution Hrs']:.1f}h resolution).",
                    f"Deploy specialist queue optimization in {worst_queue['Queue']} and first-response SLA triggers.",
                    "Improve CSAT by 0.2-0.3 and reduce repeat contacts.",
                    level="warning",
                )

        st.markdown('<div class="sub-mini-title">Acquisition Channel Efficiency</div>', unsafe_allow_html=True)
        with st.container(border=True):
            channel_bars = alt.Chart(channel_df).mark_bar(cornerRadiusTopRight=7, cornerRadiusBottomRight=7, size=20).encode(
                x=alt.X("Leads:Q", title="Leads"),
                y=alt.Y("Channel:N", sort="-x", title=None),
                color=alt.value("#94A3B8"),
                tooltip=["Channel:N", alt.Tooltip("Leads:Q", format=",")],
            )
            channel_acts = alt.Chart(channel_df).mark_bar(cornerRadiusTopRight=7, cornerRadiusBottomRight=7, size=12).encode(
                x=alt.X("Activations:Q", title="Leads / Activations"),
                y=alt.Y("Channel:N", sort="-x", title=None),
                color=alt.value("#10B981"),
                tooltip=["Channel:N", alt.Tooltip("Activations:Q", format=","), alt.Tooltip("Conversion %:Q", format=".1f")],
            )
            channel_conv = alt.Chart(channel_df).mark_text(align="left", dx=6, fontSize=10, color="#0F172A").encode(
                x="Leads:Q",
                y=alt.Y("Channel:N", sort="-x"),
                text=alt.Text("Conversion %:Q", format=".1f"),
            )
            st.altair_chart(style_sub_chart(channel_bars + channel_acts + channel_conv, height=240), use_container_width=True)
            best_channel = channel_df.loc[channel_df["Conversion %"].idxmax()]
            render_sub_ai_reco(
                "Channel ROI",
                f"{best_channel['Channel']} has the strongest conversion at {best_channel['Conversion %']:.1f}%.",
                f"Reallocate 10-15% spend from low-converting channels into {best_channel['Channel']} and referrals.",
                "Increase activations by 120-180/month at similar CAC.",
            )

        st.markdown('<div class="sub-mini-title">CSAT by Contact Type</div>', unsafe_allow_html=True)
        with st.container(border=True):
            csat_plot_df = csat_contact_df.copy()
            csat_plot_df["Baseline"] = 3.6
            csat_stems = alt.Chart(csat_plot_df).mark_bar(
                size=12,
                opacity=0.85,
                cornerRadiusTopRight=7,
                cornerRadiusBottomRight=7,
            ).encode(
                x=alt.X("Baseline:Q", title="CSAT", scale=alt.Scale(domain=[3.6, 4.8])),
                x2=alt.X2("CSAT:Q"),
                y=alt.Y("Contact Type:N", sort="-x", title=None),
                color=alt.Color("Contact Type:N", legend=None, scale=alt.Scale(range=["#29B5E8", "#6366F1", "#10B981", "#F59E0B", "#EF4444"])),
                tooltip=["Contact Type:N", alt.Tooltip("CSAT:Q", format=".1f")],
            )
            csat_points = alt.Chart(csat_contact_df).mark_circle(size=220, opacity=0.95, stroke="#FFFFFF", strokeWidth=1.6).encode(
                x=alt.X("CSAT:Q", title="CSAT", scale=alt.Scale(domain=[3.6, 4.8])),
                y=alt.Y("Contact Type:N", sort="-x", title=None),
                color=alt.Color("Contact Type:N", legend=None, scale=alt.Scale(range=["#29B5E8", "#6366F1", "#10B981", "#F59E0B", "#EF4444"])),
                tooltip=["Contact Type:N", alt.Tooltip("CSAT:Q", format=".1f")],
            )
            csat_label = alt.Chart(csat_contact_df).mark_text(
                align="left",
                dx=6,
                fontSize=10,
                color="#0F172A",
            ).encode(
                x="CSAT:Q",
                y=alt.Y("Contact Type:N", sort="-x"),
                text=alt.Text("CSAT:Q", format=".1f"),
            )
            st.altair_chart(style_sub_chart(csat_stems + csat_points + csat_label, height=220), use_container_width=True)
            weakest_contact = csat_contact_df.loc[csat_contact_df["CSAT"].idxmin()]
            render_sub_ai_reco(
                "Contact Experience",
                f"{weakest_contact['Contact Type']} has the lowest CSAT ({weakest_contact['CSAT']:.1f}).",
                f"Create focused quality program for {weakest_contact['Contact Type']} interactions and script optimization.",
                "Raise blended CSAT and reduce repeat contacts.",
                level="warning",
            )

    with sub_tab_risk:
        st.markdown('<div class="sub-title">Churn Risk & Retention Performance</div>', unsafe_allow_html=True)
        st.markdown(dedent(f"""
            <div class="sub-kpi-grid">
                <div class="sub-kpi-card crit"><div class="k">At-Risk Subscribers</div><div class="v">{risk_customers:,}</div><div class="d">High-priority cohort</div></div>
                <div class="sub-kpi-card crit"><div class="k">Revenue at Risk</div><div class="v">€{risk_arr_m:.1f}M</div><div class="d">ARR exposure</div></div>
                <div class="sub-kpi-card"><div class="k">Save Rate</div><div class="v">{save_rate_overall:.1f}%</div><div class="d">Campaign effectiveness</div></div>
                <div class="sub-kpi-card warn"><div class="k">Risk Coverage</div><div class="v">{risk_coverage:.1f}%</div><div class="d">At-risk contacted</div></div>
                <div class="sub-kpi-card"><div class="k">Reactivation Rate</div><div class="v">{reactivation_rate:.1f}%</div><div class="d">Win-back performance</div></div>
                <div class="sub-kpi-card"><div class="k">Churn Cost Avoided</div><div class="v">€{churn_cost_avoided_m:.2f}M</div><div class="d">Retention value saved</div></div>
                <div class="sub-kpi-card"><div class="k">LTV/CAC (Blended)</div><div class="v">{ltv_cac_blended:.2f}x</div><div class="d">Acquisition efficiency</div></div>
                <div class="sub-kpi-card warn"><div class="k">Predictive Churn Index</div><div class="v">{predictive_churn_index:.1f}</div><div class="d">Model pressure score</div></div>
            </div>
        """), unsafe_allow_html=True)
        rk_col1, rk_col2 = st.columns(2)

        with rk_col1:
            st.markdown('<div class="sub-mini-title">At-Risk Cohorts by Segment</div>', unsafe_allow_html=True)
            with st.container(border=True):
                risk_lolli_line = alt.Chart(sub_risk).mark_rule(strokeWidth=3).encode(
                    x=alt.X("At Risk:Q", title="Customers at Risk"),
                    x2=alt.value(0),
                    y=alt.Y("Segment:N", sort=["Budget", "Standard", "Premium", "VIP"], title=None),
                    color=alt.Color("Propensity:Q", scale=alt.Scale(scheme="orangered"), legend=None),
                )
                risk_lolli_point = alt.Chart(sub_risk).mark_circle(size=330).encode(
                    x="At Risk:Q",
                    y=alt.Y("Segment:N", sort=["Budget", "Standard", "Premium", "VIP"]),
                    color=alt.Color("Propensity:Q", scale=alt.Scale(scheme="orangered"), legend=alt.Legend(title="Churn Risk")),
                    tooltip=["Segment:N", "At Risk:Q", alt.Tooltip("Revenue at Risk K:Q", title="Revenue at Risk (€ K)", format=",.0f"), alt.Tooltip("Propensity:Q", format=".0%")],
                )
                st.altair_chart(style_sub_chart(risk_lolli_line + risk_lolli_point, height=230), use_container_width=True)
                high_risk = sub_risk.loc[sub_risk["Propensity"].idxmax()]
                render_sub_ai_reco(
                    "Risk Concentration",
                    f"{high_risk['Segment']} is the most vulnerable cohort ({high_risk['Propensity']:.0%} propensity).",
                    f"Activate a 2-step save journey for {high_risk['Segment']} with bill-credit + quality assurance callback.",
                    f"Protect up to €{(high_risk['Revenue at Risk K']*12/1000):.1f}M ARR from this cohort.",
                    level="critical",
                )

        with rk_col2:
            st.markdown('<div class="sub-mini-title">Retention Campaign Efficiency</div>', unsafe_allow_html=True)
            with st.container(border=True):
                camp_bars = alt.Chart(retention_df).transform_fold(
                    ["Contacted", "Saved"], as_=["Metric", "Value"]
                ).mark_bar(opacity=0.82, cornerRadiusTopLeft=5, cornerRadiusTopRight=5).encode(
                    x=alt.X("Campaign:N", title=None),
                    y=alt.Y("Value:Q", title="Customers"),
                    color=alt.Color("Metric:N", scale=alt.Scale(domain=["Contacted", "Saved"], range=["#94A3B8", "#10B981"]), legend=alt.Legend(title=None)),
                    xOffset="Metric:N",
                    tooltip=["Campaign:N", "Metric:N", "Value:Q"],
                )
                save_rate = alt.Chart(retention_df).mark_line(point=True, color="#F59E0B", strokeWidth=3).encode(
                    x=alt.X("Campaign:N", title=None),
                    y=alt.Y("Save Rate:Q", title="Save Rate %"),
                    tooltip=["Campaign:N", alt.Tooltip("Save Rate:Q", format=".1f")],
                )
                st.altair_chart(style_sub_chart(alt.layer(camp_bars, save_rate).resolve_scale(y="independent"), height=230), use_container_width=True)
                best_campaign = retention_df.loc[retention_df["Save Rate"].idxmax()]
                render_sub_ai_reco(
                    "Retention ROI",
                    f"{best_campaign['Campaign']} is the best performer with {best_campaign['Save Rate']:.1f}% save rate.",
                    f"Scale targeting logic from {best_campaign['Campaign']} across high-propensity standard and budget users.",
                    "Increase saves by 80-120 accounts per cycle at similar cost.",
                )

        st.markdown('<div class="sub-mini-title">Risk Score Distribution and Complaint Pressure</div>', unsafe_allow_html=True)
        rrk_col1, rrk_col2 = st.columns(2)
        with rrk_col1:
            with st.container(border=True):
                risk_hist = alt.Chart(risk_score_df).mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6, color="#EF4444", opacity=0.82).encode(
                    x=alt.X("Band:N", title="Risk Score Band"),
                    y=alt.Y("Customers:Q", title="Customers"),
                    tooltip=["Band:N", alt.Tooltip("Customers:Q", format=",")],
                )
                st.altair_chart(style_sub_chart(risk_hist, height=240), use_container_width=True)
            high_band = risk_score_df.iloc[-1]
            band_share = (high_band["Customers"] / risk_score_df["Customers"].sum()) * 100
            render_sub_ai_reco(
                "Risk Band Severity",
                f"{high_band['Customers']:,} subscribers are concentrated in the highest risk score band ({band_share:.1f}% of monitored base).",
                "Prioritize save-offer triggers for this band and enforce proactive outreach 7-10 days before billing date.",
                "Reduce near-term churn exposure and stabilize retention over the next cycle.",
                level="critical",
            )
        with rrk_col2:
            with st.container(border=True):
                complaint_bar = alt.Chart(complaint_df).mark_bar(cornerRadiusTopRight=7, cornerRadiusBottomRight=7, size=18, color="#F59E0B").encode(
                    x=alt.X("Volume:Q", title="Complaint Volume"),
                    y=alt.Y("Reason:N", sort="-x", title=None),
                    tooltip=["Reason:N", "Volume:Q"],
                )
                st.altair_chart(style_sub_chart(complaint_bar, height=240), use_container_width=True)
            top_reason = complaint_df.sort_values("Volume", ascending=False).iloc[0]
            render_sub_ai_reco(
                "Escalation Drivers",
                f"Top complaint driver is {top_reason['Reason']} with {top_reason['Volume']:,} cases in the latest window.",
                f"Trigger targeted remediation for {top_reason['Reason']} before next billing cycle and prioritize high-risk cohort outreach.",
                "Lower complaint-driven churn and reduce near-term attrition pressure.",
                level="critical",
            )

        st.markdown('<div class="sub-mini-title">LTV/CAC by Acquisition Channel</div>', unsafe_allow_html=True)
        with st.container(border=True):
            ltvcac_bar = alt.Chart(channel_econ_df).mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6, size=24).encode(
                x=alt.X("Channel:N", title=None),
                y=alt.Y("LTV/CAC:Q", title="LTV/CAC Ratio"),
                color=alt.Color("Channel:N", legend=None, scale=alt.Scale(range=["#29B5E8", "#10B981", "#6366F1", "#F59E0B", "#EF4444"])),
                tooltip=["Channel:N", alt.Tooltip("LTV/CAC:Q", format=".2f"), "CAC:Q", "LTV:Q"],
            )
            ltv_target = alt.Chart(pd.DataFrame({"y": [3.0]})).mark_rule(color="#94A3B8", strokeDash=[4, 4]).encode(y="y:Q")
            st.altair_chart(style_sub_chart(ltvcac_bar + ltv_target, height=220), use_container_width=True)
            worst_ratio = channel_econ_df.loc[channel_econ_df["LTV/CAC"].idxmin()]
            render_sub_ai_reco(
                "Acquisition Economics",
                f"{worst_ratio['Channel']} is the weakest economics channel at {worst_ratio['LTV/CAC']:.2f}x.",
                f"Tighten spend efficiency in {worst_ratio['Channel']} and shift acquisition mix toward higher-ratio channels.",
                "Improve blended LTV/CAC and protect payback timelines.",
                level="warning",
            )

        st.markdown(dedent(f"""
            <div style="background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%); border-radius: 10px; padding: 0.82rem 0.95rem; margin-top: 0.55rem; border-left: 4px solid #F59E0B;">
                <div style="display: flex; align-items: center;">
                    <span style="font-size: 1.35rem; margin-right: 0.55rem;">⚠️</span>
                    <div>
                        <strong style="color: #92400E;">Urgent: {risk_customers} subscribers at risk</strong>
                        <div style="color: #B45309; font-size: 0.84rem;">€{risk_arr_m:.1f}M ARR exposed · Budget segment highest propensity</div>
                    </div>
                </div>
            </div>
        """), unsafe_allow_html=True)

elif selected_menu == "Revenue Analytics":
    import pandas as pd
    import altair as alt
    import pydeck as pdk

    REV_CHART_THEME = {
        "font": "Poppins, sans-serif",
        "label_color": "#334155",
        "grid_color": "#E2E8F0",
    }

    def style_rev_chart(chart: alt.Chart, height: int = 220) -> alt.Chart:
        return (
            chart.properties(height=height, padding={"left": 6, "top": 10, "right": 8, "bottom": 6})
            .configure(background="#FFFFFF")
            .configure_view(stroke=None)
            .configure_axis(
                labelFont=REV_CHART_THEME["font"],
                titleFont=REV_CHART_THEME["font"],
                labelColor=REV_CHART_THEME["label_color"],
                titleColor=REV_CHART_THEME["label_color"],
                labelFontSize=11,
                titleFontSize=12,
                domain=False,
                gridColor=REV_CHART_THEME["grid_color"],
                gridOpacity=0.75,
            )
            .configure_legend(
                labelFont=REV_CHART_THEME["font"],
                titleFont=REV_CHART_THEME["font"],
                labelColor=REV_CHART_THEME["label_color"],
                titleColor=REV_CHART_THEME["label_color"],
                orient="top",
                direction="horizontal",
                symbolType="circle",
                symbolSize=100,
            )
        )

    def render_rev_ai_reco(headline: str, insight: str, action: str, impact: str, level: str = "info") -> None:
        st.markdown(
            f"""<div class="rev-ai-card {level}"><div class="rev-ai-head">🤖 AI Recommendation · {headline}</div><div class="rev-ai-line"><strong>Insight:</strong> {insight}</div><div class="rev-ai-line"><strong>Action:</strong> {action}</div><div class="rev-ai-line"><strong>Expected Impact:</strong> {impact}</div></div>""",
            unsafe_allow_html=True,
        )

    st.markdown("""<style>
@keyframes rev-fade-up { 0% { opacity: 0; transform: translateY(10px); } 100% { opacity: 1; transform: translateY(0); } }
@keyframes rev-shimmer { 0% { left: -40%; } 100% { left: 120%; } }
@keyframes rev-pulse-dot { 0%,100% { transform: scale(1); opacity: 0.7; } 50% { transform: scale(1.25); opacity: 1; } }
.rev-title { position: relative; overflow: hidden; display: flex; align-items: center; gap: 0.55rem; margin: 1.2rem 0 0.8rem; padding: 0.6rem 0.85rem; border-radius: 12px; border: 1px solid #DBEAFE; background: linear-gradient(135deg, #F0F8FF 0%, #EEF2FF 100%); color: #1B2A4E; font-size: 1rem; font-weight: 700; animation: rev-fade-up 0.4s ease-out both; }
.rev-title::before { content: ""; width: 8px; height: 8px; border-radius: 50%; background: linear-gradient(135deg, #29B5E8, #6366F1); animation: rev-pulse-dot 1.8s ease-in-out infinite; }
.rev-title::after { content: ""; position: absolute; top: 0; left: -40%; width: 34%; height: 100%; background: linear-gradient(90deg, transparent, rgba(255,255,255,0.85), transparent); animation: rev-shimmer 3.2s ease-in-out infinite; }
.rev-mini-title { display: inline-flex; align-items: center; gap: 0.4rem; margin: 0.15rem 0 0.55rem; font-size: 0.9rem; font-weight: 700; color: #1E3A8A; }
.rev-mini-title::before { content: ""; width: 7px; height: 7px; border-radius: 50%; background: linear-gradient(135deg, #22C1EE, #8B5CF6); }
.rev-pulse { position: relative; overflow: hidden; border-radius: 14px; border: 1px solid #BFDBFE; background: linear-gradient(135deg, #EFF6FF 0%, #ECFEFF 100%); padding: 1rem 1.1rem; margin-bottom: 1rem; }
.rev-pulse::before { content: ""; position: absolute; top: 0; left: -50%; width: 40%; height: 100%; background: linear-gradient(90deg, transparent, rgba(41,181,232,0.2), transparent); animation: rev-shimmer 3s ease-in-out infinite; }
.rev-pulse-head { position: relative; z-index: 1; display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.75rem; }
.rev-pulse-title { color: #1E3A8A; font-weight: 700; font-size: 0.92rem; }
.rev-pulse-live { color: #10B981; font-size: 0.74rem; font-weight: 700; display: inline-flex; align-items: center; gap: 0.35rem; }
.rev-pulse-live::before { content: ""; width: 8px; height: 8px; border-radius: 50%; background: #10B981; animation: rev-pulse-dot 1.2s ease-in-out infinite; }
.rev-pulse-grid { position: relative; z-index: 1; display: grid; grid-template-columns: repeat(6, 1fr); gap: 0.6rem; }
.rev-pulse-card { background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 10px; padding: 0.62rem 0.7rem; animation: rev-fade-up 0.35s ease-out both; }
.rev-pulse-card:nth-child(1){animation-delay:.05s}.rev-pulse-card:nth-child(2){animation-delay:.1s}.rev-pulse-card:nth-child(3){animation-delay:.16s}.rev-pulse-card:nth-child(4){animation-delay:.22s}.rev-pulse-card:nth-child(5){animation-delay:.28s}.rev-pulse-card:nth-child(6){animation-delay:.34s}
.rev-pulse-label { color: #64748B; font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.04em; margin-bottom: 0.2rem; }
.rev-pulse-value { color: #0F172A; font-size: 1.2rem; font-weight: 800; line-height: 1.15; }
.rev-pulse-delta { margin-top: 0.2rem; color: #059669; font-size: 0.72rem; font-weight: 700; }
.rev-kpi-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.6rem; margin-bottom: 0.75rem; }
.rev-kpi-card { background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 10px; padding: 0.55rem 0.62rem; box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04); animation: rev-fade-up 0.35s ease-out both; }
.rev-kpi-card .k { color: #64748B; font-size: 0.64rem; text-transform: uppercase; letter-spacing: 0.04em; }
.rev-kpi-card .v { color: #0F172A; font-size: 1.02rem; font-weight: 800; margin-top: 0.12rem; line-height: 1.15; }
.rev-kpi-card .d { color: #059669; font-size: 0.68rem; font-weight: 700; margin-top: 0.14rem; }
.rev-kpi-card.warn .d { color: #B45309; }
.rev-kpi-card.crit .d { color: #B91C1C; }
.rev-ai-card { margin-top: 0.6rem; border-radius: 10px; border: 1px solid #D1E9FF; background: linear-gradient(135deg, #F8FBFF 0%, #EEF6FF 100%); padding: 0.62rem 0.78rem; box-shadow: 0 4px 14px rgba(15, 23, 42, 0.05); animation: rev-fade-up 0.35s ease-out both; }
.rev-ai-card.warning { border-color: #FCD34D; background: linear-gradient(135deg, #FFFBEB 0%, #FEF3C7 100%); }
.rev-ai-card.critical { border-color: #FCA5A5; background: linear-gradient(135deg, #FEF2F2 0%, #FEE2E2 100%); }
.rev-ai-head { color: #1E3A8A; font-size: 0.78rem; font-weight: 700; margin-bottom: 0.28rem; }
.rev-ai-card.warning .rev-ai-head { color: #92400E; }
.rev-ai-card.critical .rev-ai-head { color: #991B1B; }
.rev-ai-line { color: #334155; font-size: 0.77rem; line-height: 1.34; margin: 0.12rem 0; }
@media (max-width: 980px) { .rev-pulse-grid { grid-template-columns: repeat(3, 1fr); } .rev-kpi-grid { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 640px) { .rev-pulse-grid, .rev-kpi-grid { grid-template-columns: 1fr; } }
</style>""", unsafe_allow_html=True)

    # -------------------------------------------------------------------
    # Synthetic and internally consistent revenue dataset
    # -------------------------------------------------------------------
    rev_monthly = pd.DataFrame({
        "Month": ["2025-09", "2025-10", "2025-11", "2025-12", "2026-01", "2026-02"],
        "Invoiced M": [4.56, 4.62, 4.68, 4.66, 4.74, 4.82],
        "Collected M": [4.38, 4.43, 4.49, 4.47, 4.56, 4.64],
        "Discounts M": [0.28, 0.29, 0.30, 0.30, 0.30, 0.31],
        "COGS M": [2.03, 2.05, 2.08, 2.07, 2.10, 2.12],
    })
    rev_monthly["Net Revenue M"] = rev_monthly["Invoiced M"] - rev_monthly["Discounts M"]
    rev_monthly["Gross Margin %"] = ((rev_monthly["Net Revenue M"] - rev_monthly["COGS M"]) / rev_monthly["Net Revenue M"] * 100).round(1)
    rev_monthly["Collection %"] = (rev_monthly["Collected M"] / rev_monthly["Invoiced M"] * 100).round(1)

    rev_segments = pd.DataFrame({
        "Segment": ["MasOrange", "Vodafone"],
        "Revenue M": [24.5, 17.9],
        "Growth %": [6.8, 8.2],
        "Margin %": [52.1, 50.8],
    })

    rev_plans = pd.DataFrame({
        "Plan": ["FTTH 300Mb", "FTTH 600Mb", "FTTH 1Gbps", "FTTH Business", "Dark Fiber"],
        "Subs": [4200000, 3800000, 2100000, 1200000, 700000],
        "ARPU": [2.85, 3.42, 4.20, 5.80, 8.50],
    })
    rev_plans["Revenue M"] = (rev_plans["Subs"] * rev_plans["ARPU"] / 1_000_000).round(3)

    rev_aging = pd.DataFrame({
        "Bucket": ["Current", "1-30", "31-60", "61-90", "90+"],
        "Amount M": [4.1, 1.2, 0.7, 0.4, 0.28],
    })

    rev_channels = pd.DataFrame({
        "Channel": ["PF Web", "Referidos PF", "Tiendas PF", "Fuerza Comercial FTTH", "Canal Constructoras"],
        "Revenue M": [1.45, 0.82, 0.94, 0.68, 0.61],
        "Cost M": [0.39, 0.20, 0.31, 0.26, 0.22],
    })
    rev_channels["ROI x"] = ((rev_channels["Revenue M"] - rev_channels["Cost M"]) / rev_channels["Cost M"]).round(2)

    rev_risk = pd.DataFrame({
        "Risk Driver": ["Delinquency", "Discount Leakage", "Partner Churn", "Downgrades", "Disputes"],
        "Exposure M": [0.95, 0.62, 0.47, 0.31, 0.19],
        "Likelihood": [4.2, 3.8, 3.1, 2.9, 2.7],
    })

    rev_scenario = pd.DataFrame({
        "Scenario": ["Downside", "Base", "Upside"],
        "Quarter Revenue M": [12.8, 13.2, 13.7],
        "Probability": ["25%", "50%", "25%"],
    })
    sales_monthly = pd.DataFrame({
        "Month": rev_monthly["Month"],
        "B2C Sales M": [2.64, 2.69, 2.73, 2.71, 2.78, 2.84],
        "B2B Sales M": [1.22, 1.25, 1.28, 1.30, 1.33, 1.37],
        "Digital Sales M": [1.46, 1.49, 1.52, 1.54, 1.58, 1.62],
        "Retail Stores M": [1.18, 1.20, 1.22, 1.23, 1.25, 1.27],
        "Field Sales M": [0.88, 0.90, 0.93, 0.91, 0.94, 0.96],
        "Partner Sales M": [0.34, 0.35, 0.34, 0.33, 0.34, 0.36],
    })
    sales_monthly["Total Sales M"] = sales_monthly["B2C Sales M"] + sales_monthly["B2B Sales M"]
    sales_monthly["Blended Margin %"] = [51.2, 51.5, 51.8, 52.1, 52.4, 52.8]

    sales_channel_mix = pd.DataFrame({
        "Channel": ["PF Web", "Tiendas PF", "Fuerza Comercial FTTH", "Canal Constructoras"],
        "Motion": ["Digital", "Retail Stores", "Field Sales", "Partners"],
        "B2C Sales M": [1.28, 0.92, 0.52, 0.12],
        "B2B Sales M": [0.34, 0.35, 0.44, 0.24],
        "Orders K": [7.1, 5.8, 3.2, 1.2],
        "Margin %": [55.8, 49.7, 52.3, 57.1],
    })
    sales_channel_mix["Total Sales M"] = sales_channel_mix["B2C Sales M"] + sales_channel_mix["B2B Sales M"]

    sales_region = pd.DataFrame({
        "Region": ["Madrid Metro", "Norte", "Sur", "Centro", "Este"],
        "B2C Sales M": [1.66, 0.42, 0.33, 0.27, 0.16],
        "B2B Sales M": [0.78, 0.20, 0.15, 0.13, 0.11],
        "Retail Stores": [34, 12, 8, 9, 5],
        "Margin %": [53.2, 51.0, 50.4, 49.9, 48.7],
    })
    sales_region["Total Sales M"] = sales_region["B2C Sales M"] + sales_region["B2B Sales M"]

    sales_reps = pd.DataFrame({
        "Sales Pod": ["Pod Madrid Premium", "Pod Empresas Centro", "Pod Norte FTTH", "Pod Sur Expansions", "Pod Este Build"],
        "Region": ["Madrid Metro", "Madrid Metro", "Norte", "Sur", "Este"],
        "Sales M": [0.94, 0.81, 0.56, 0.49, 0.31],
        "New Logos": [42, 28, 23, 19, 11],
        "Win Rate %": [38.4, 35.1, 33.8, 31.6, 29.7],
    })

    sales_product_mix = pd.DataFrame({
        "Product": ["PF Hogar 300", "PF Hogar 600", "PF Gamer 1G", "PF Empresas Pro", "PF Mesh Plus", "PF TV App"],
        "B2C Sales M": [1.18, 0.94, 0.56, 0.00, 0.31, 0.21],
        "B2B Sales M": [0.00, 0.00, 0.00, 1.36, 0.07, 0.00],
        "Attach Rate %": [0, 0, 0, 0, 36.0, 42.0],
    })
    sales_product_mix["Total Sales M"] = sales_product_mix["B2C Sales M"] + sales_product_mix["B2B Sales M"]
    sales_pipeline = pd.DataFrame({
        "Stage": ["MQL", "SQL", "Proposal", "Negotiation", "Closed Won"],
        "B2C K": [3.5, 2.6, 1.7, 1.0, 0.43],
        "B2B K": [1.1, 0.8, 0.56, 0.34, 0.14],
        "Avg Age Days": [5, 8, 12, 16, 4],
    })
    sales_pipeline["Total K"] = sales_pipeline["B2C K"] + sales_pipeline["B2B K"]

    sales_quota = pd.DataFrame({
        "Dimension": ["PF Web", "Tiendas PF", "Fuerza Comercial FTTH", "Canal Constructoras", "Madrid Metro", "Norte", "Sur", "Centro", "Este"],
        "Type": ["Channel", "Channel", "Channel", "Channel", "Region", "Region", "Region", "Region", "Region"],
        "Target M": [1.55, 1.25, 1.00, 0.42, 2.55, 0.66, 0.57, 0.47, 0.35],
        "Actual M": [1.62, 1.27, 0.96, 0.36, 2.44, 0.62, 0.48, 0.40, 0.27],
    })
    sales_quota["Attainment %"] = (sales_quota["Actual M"] / sales_quota["Target M"] * 100).round(1)
    sales_quota["Gap M"] = (sales_quota["Actual M"] - sales_quota["Target M"]).round(2)

    sales_forecast = pd.DataFrame({
        "Month": ["2025-11", "2025-12", "2026-01", "2026-02"],
        "Fcst -90d M": [3.72, 3.78, 3.90, 4.02],
        "Fcst -30d M": [3.84, 3.88, 4.00, 4.12],
        "Actual M": [4.01, 4.03, 4.11, 4.21],
    })
    sales_forecast["Error -90d %"] = ((sales_forecast["Actual M"] - sales_forecast["Fcst -90d M"]) / sales_forecast["Actual M"] * 100).round(1)
    sales_forecast["Error -30d %"] = ((sales_forecast["Actual M"] - sales_forecast["Fcst -30d M"]) / sales_forecast["Actual M"] * 100).round(1)

    sales_waterfall = pd.DataFrame({
        "Step": ["Gross Bookings", "Discounts", "Commercial Credits", "Churn Reversals", "Net Sales"],
        "Value M": [4.74, -0.31, -0.12, -0.10, 4.21],
    })
    sales_waterfall["Cumulative M"] = sales_waterfall["Value M"].cumsum()

    sales_cohort = pd.DataFrame({
        "Cohort": ["2025-09", "2025-10", "2025-11", "2025-12", "2026-01", "2026-02"],
        "Retention 30d %": [97.8, 97.5, 97.2, 97.0, 96.8, 96.7],
        "Retention 60d %": [95.9, 95.6, 95.2, 95.0, 94.8, 94.6],
        "Retention 90d %": [94.2, 93.9, 93.5, 93.2, 93.0, 92.8],
    })

    sales_install_sla = pd.DataFrame({
        "Region": ["Madrid Metro", "Norte", "Sur", "Centro", "Este"],
        "Sale to Install Days": [2.6, 3.4, 3.8, 4.1, 4.9],
        "Install to First Invoice Days": [3.2, 3.9, 4.0, 4.4, 5.1],
        "SLA Met %": [95.6, 91.8, 89.7, 88.4, 84.2],
    })

    sales_productivity = pd.DataFrame({
        "Motion": ["B2C Hunters", "B2B Hunters", "Farmers / Upsell"],
        "Revenue per Rep K": [112, 164, 138],
        "Win Rate %": [33.8, 29.4, 41.7],
        "Avg Deal Size K": [3.8, 14.2, 6.4],
        "Cycle Days": [8.5, 22.1, 11.7],
        "Activity to Close %": [12.8, 9.3, 18.5],
    })

    sales_deals = pd.DataFrame({
        "Deal": ["Madrid Corporate Multi-site", "Salamanca Residencial Tower", "Zaragoza SME Cluster", "Palma Hospitality Bundle", "Málaga Industrial Park", "Sevilla Port Offices"],
        "Status": ["Won", "Won", "Won", "Lost", "Lost", "Lost"],
        "Value K": [220, 178, 146, 132, 128, 115],
        "Region": ["Madrid Metro", "Madrid Metro", "Norte", "Sur", "Sur", "Madrid Metro"],
        "Reason": ["Price-value fit", "Fast install SLA", "Partner-led conversion", "Competitor discount", "Long install lead time", "Procurement delay"],
    })

    madrid_sales_map = pd.DataFrame({
        "Neighborhood": ["Salamanca", "Chamberí", "Retiro", "Chamartín", "Arganzuela", "Moncloa", "Latina", "Usera", "Carabanchel", "Villaverde", "Vallecas", "Hortaleza"],
        "lat": [40.4260, 40.4350, 40.4140, 40.4620, 40.3950, 40.4340, 40.4020, 40.3850, 40.3770, 40.3460, 40.3880, 40.4730],
        "lon": [-3.6830, -3.7060, -3.6830, -3.6900, -3.6960, -3.7250, -3.7420, -3.7060, -3.7420, -3.7060, -3.6520, -3.6530],
        "Sales M": [0.41, 0.38, 0.35, 0.29, 0.27, 0.21, 0.23, 0.19, 0.20, 0.18, 0.20, 0.17],
        "B2B Share %": [62, 54, 41, 39, 48, 36, 44, 32, 35, 46, 29, 25],
        "Margin %": [56.8, 55.4, 53.2, 52.7, 53.8, 50.1, 51.5, 49.8, 50.4, 52.0, 48.4, 47.2],
    })
    madrid_sales_map["radius"] = (madrid_sales_map["Sales M"] * 9000).round(0)
    madrid_sales_map["r"] = madrid_sales_map["Margin %"].apply(lambda v: 16 if v >= 53 else 41 if v >= 50 else 245)
    madrid_sales_map["g"] = madrid_sales_map["Margin %"].apply(lambda v: 185 if v >= 53 else 121 if v >= 50 else 158)
    madrid_sales_map["b"] = madrid_sales_map["Margin %"].apply(lambda v: 129 if v >= 53 else 255 if v >= 50 else 11)

    latest = rev_monthly.iloc[-1]
    prev = rev_monthly.iloc[-2]
    mrr = float(latest["Net Revenue M"])
    arr = mrr * 12
    gross_margin = float(latest["Gross Margin %"])
    collection_rate = float(latest["Collection %"])
    mrr_growth = (latest["Net Revenue M"] - prev["Net Revenue M"]) / prev["Net Revenue M"] * 100
    arpu_blended = round((rev_plans["Revenue M"].sum() * 1_000_000) / rev_plans["Subs"].sum(), 2)
    at_risk_rev_m = rev_risk["Exposure M"].sum()

    st.markdown(dedent(f"""
    <div class="rev-pulse">
        <div class="rev-pulse-head">
            <span class="rev-pulse-title">💰 Revenue Pulse · Key Financial Metrics</span>
            <span class="rev-pulse-live">Live</span>
        </div>
        <div class="rev-pulse-grid">
            <div class="rev-pulse-card"><div class="rev-pulse-label">MRR</div><div class="rev-pulse-value">€{mrr:.2f}M</div><div class="rev-pulse-delta">↑ {mrr_growth:.2f}% MoM</div></div>
            <div class="rev-pulse-card"><div class="rev-pulse-label">ARR</div><div class="rev-pulse-value">€{arr:.1f}M</div><div class="rev-pulse-delta">Annualized run-rate</div></div>
            <div class="rev-pulse-card"><div class="rev-pulse-label">Gross Margin</div><div class="rev-pulse-value">{gross_margin:.1f}%</div><div class="rev-pulse-delta">Healthy unit economics</div></div>
            <div class="rev-pulse-card"><div class="rev-pulse-label">Collection Rate</div><div class="rev-pulse-value">{collection_rate:.1f}%</div><div class="rev-pulse-delta">Cash discipline</div></div>
            <div class="rev-pulse-card"><div class="rev-pulse-label">Blended ARPU</div><div class="rev-pulse-value">€{arpu_blended:.2f}</div><div class="rev-pulse-delta">↑ +€2.1 QoQ</div></div>
            <div class="rev-pulse-card"><div class="rev-pulse-label">Revenue at Risk</div><div class="rev-pulse-value">€{at_risk_rev_m:.2f}M</div><div class="rev-pulse-delta">Watchlist exposure</div></div>
        </div>
    </div>
    """), unsafe_allow_html=True)

    rev_tab_overview, rev_tab_ops, rev_tab_sales, rev_tab_risk = st.tabs(
        ["📈 Revenue Overview", "🧭 Revenue Operations", "🛍️ Sales", "⚠️ Risk & Strategy"]
    )

    with rev_tab_overview:
        st.markdown('<div class="rev-title">Revenue Growth and Mix</div>', unsafe_allow_html=True)
        st.markdown(dedent(f"""
            <div class="rev-kpi-grid">
                <div class="rev-kpi-card"><div class="k">MRR Growth (MoM)</div><div class="v">{mrr_growth:.2f}%</div><div class="d">Top-line acceleration</div></div>
                <div class="rev-kpi-card"><div class="k">Gross Margin %</div><div class="v">{gross_margin:.1f}%</div><div class="d">Margin efficiency</div></div>
                <div class="rev-kpi-card"><div class="k">ARPU (Blended)</div><div class="v">€{arpu_blended:.2f}</div><div class="d">Value quality</div></div>
                <div class="rev-kpi-card warn"><div class="k">Discount Impact</div><div class="v">€{latest['Discounts M']:.2f}M</div><div class="d">Revenue dilution</div></div>
                <div class="rev-kpi-card"><div class="k">Best Growth Segment</div><div class="v">{rev_segments.loc[rev_segments['Growth %'].idxmax(), 'Segment']}</div><div class="d">{rev_segments['Growth %'].max():.1f}% growth</div></div>
                <div class="rev-kpi-card"><div class="k">Highest Margin Segment</div><div class="v">{rev_segments.loc[rev_segments['Margin %'].idxmax(), 'Segment']}</div><div class="d">{rev_segments['Margin %'].max():.1f}% margin</div></div>
                <div class="rev-kpi-card"><div class="k">Quarter Revenue</div><div class="v">€{(rev_monthly.tail(3)['Net Revenue M'].sum()):.2f}M</div><div class="d">Last 3 months</div></div>
                <div class="rev-kpi-card crit"><div class="k">Revenue at Risk</div><div class="v">€{at_risk_rev_m:.2f}M</div><div class="d">Needs mitigation</div></div>
            </div>
        """), unsafe_allow_html=True)

        rv_col1, rv_col2 = st.columns(2)
        with rv_col1:
            st.markdown('<div class="rev-mini-title">MRR vs Collections Trend</div>', unsafe_allow_html=True)
            with st.container(border=True):
                mrr_line = alt.Chart(rev_monthly).mark_line(point=True, strokeWidth=3, color="#29B5E8").encode(
                    x=alt.X("Month:N", title=None),
                    y=alt.Y("Net Revenue M:Q", title="Revenue (€ M)"),
                    tooltip=["Month:N", alt.Tooltip("Net Revenue M:Q", format=".2f"), alt.Tooltip("Collected M:Q", format=".2f")],
                )
                coll_line = alt.Chart(rev_monthly).mark_line(point=True, strokeWidth=3, color="#10B981").encode(
                    x=alt.X("Month:N", title=None),
                    y=alt.Y("Collected M:Q", title="Revenue (€ M)"),
                )
                st.altair_chart(style_rev_chart(mrr_line + coll_line, height=230), use_container_width=True)
                gap = latest["Net Revenue M"] - latest["Collected M"]
                render_rev_ai_reco(
                    "Cash Conversion",
                    f"Current month cash gap is €{gap:.2f}M between net revenue and collections.",
                    "Tighten collections for 1-30 day bucket and auto-reminder cadence.",
                    "Lift collection rate by 0.8-1.2pp in one cycle.",
                    level="warning",
                )

        with rv_col2:
            st.markdown('<div class="rev-mini-title">Revenue Mix by Partner</div>', unsafe_allow_html=True)
            with st.container(border=True):
                seg_donut = alt.Chart(rev_segments).mark_arc(innerRadius=66, outerRadius=108, cornerRadius=4, stroke="#FFFFFF", strokeWidth=2).encode(
                    theta=alt.Theta("Revenue M:Q", stack=True),
                    color=alt.Color("Segment:N", scale=alt.Scale(domain=["MasOrange", "Vodafone"], range=["#FF6B00", "#E60000"]), legend=alt.Legend(title=None)),
                    tooltip=["Segment:N", alt.Tooltip("Revenue M:Q", format=".2f"), alt.Tooltip("Growth %:Q", format=".1f")],
                )
                seg_center = alt.Chart(pd.DataFrame({"t": [f"€{rev_segments['Revenue M'].sum():.1f}M"]})).mark_text(fontSize=22, fontWeight="bold", color="#0F172A").encode(text="t:N")
                seg_sub = alt.Chart(pd.DataFrame({"t": ["Monthly Wholesale"]})).mark_text(fontSize=11, dy=18, color="#64748B").encode(text="t:N")
                st.altair_chart(style_rev_chart(seg_donut + seg_center + seg_sub, height=230), use_container_width=True)
                dom = rev_segments.loc[rev_segments["Revenue M"].idxmax()]
                render_rev_ai_reco(
                    "Mix Concentration",
                    f"{dom['Segment']} contributes the highest revenue share at €{dom['Revenue M']:.2f}M.",
                    "Maintain balanced growth across both MasOrange and Vodafone networks.",
                    "Strengthen wholesale revenue stability with both partners.",
                )

        st.markdown('<div class="rev-mini-title">Margin vs Growth by Partner</div>', unsafe_allow_html=True)
        with st.container(border=True):
            mg_scatter = alt.Chart(rev_segments).mark_circle(opacity=0.88, stroke="#FFFFFF", strokeWidth=1.4).encode(
                x=alt.X("Growth %:Q", title="Growth %"),
                y=alt.Y("Margin %:Q", title="Margin %"),
                size=alt.Size("Revenue M:Q", scale=alt.Scale(range=[250, 1400]), legend=None),
                color=alt.Color("Segment:N", scale=alt.Scale(domain=["MasOrange", "Vodafone"], range=["#FF6B00", "#E60000"]), legend=alt.Legend(title=None)),
                tooltip=["Segment:N", alt.Tooltip("Growth %:Q", format=".1f"), alt.Tooltip("Margin %:Q", format=".1f"), alt.Tooltip("Revenue M:Q", format=".2f")],
            )
            mg_labels = alt.Chart(rev_segments).mark_text(dy=-12, fontSize=9, color="#1E293B").encode(
                x="Growth %:Q", y="Margin %:Q", text="Segment:N"
            )
            st.altair_chart(style_rev_chart(mg_scatter + mg_labels, height=235), use_container_width=True)
            best_quad = rev_segments.sort_values(["Growth %", "Margin %"], ascending=False).iloc[0]
            render_rev_ai_reco(
                "Growth Quality",
                f"{best_quad['Segment']} sits in the strongest growth-margin quadrant.",
                f"Prioritize network expansion in {best_quad['Segment']} deployment regions.",
                "Maximize profitable infrastructure growth with partner alignment.",
            )

    with rev_tab_ops:
        st.markdown('<div class="rev-title">Revenue Operations and Efficiency</div>', unsafe_allow_html=True)
        st.markdown(dedent(f"""
            <div class="rev-kpi-grid">
                <div class="rev-kpi-card"><div class="k">Collection Rate</div><div class="v">{collection_rate:.1f}%</div><div class="d">Latest month</div></div>
                <div class="rev-kpi-card warn"><div class="k">90+ Aging</div><div class="v">€{rev_aging.loc[rev_aging['Bucket']=='90+', 'Amount M'].iloc[0]:.2f}M</div><div class="d">Delinquency risk</div></div>
                <div class="rev-kpi-card"><div class="k">Best ROI Channel</div><div class="v">{rev_channels.loc[rev_channels['ROI x'].idxmax(), 'Channel']}</div><div class="d">{rev_channels['ROI x'].max():.2f}x</div></div>
                <div class="rev-kpi-card crit"><div class="k">Weak ROI Channel</div><div class="v">{rev_channels.loc[rev_channels['ROI x'].idxmin(), 'Channel']}</div><div class="d">{rev_channels['ROI x'].min():.2f}x</div></div>
                <div class="rev-kpi-card"><div class="k">Plan Mix ARPU</div><div class="v">€{arpu_blended:.2f}</div><div class="d">Weighted across plans</div></div>
                <div class="rev-kpi-card"><div class="k">Discount Ratio</div><div class="v">{(latest['Discounts M']/latest['Invoiced M']*100):.1f}%</div><div class="d">Promotion intensity</div></div>
                <div class="rev-kpi-card"><div class="k">Gross Margin Trend</div><div class="v">{(rev_monthly['Gross Margin %'].iloc[-1]-rev_monthly['Gross Margin %'].iloc[0]):+.1f}pp</div><div class="d">6-month move</div></div>
                <div class="rev-kpi-card warn"><div class="k">Cash Gap</div><div class="v">€{(latest['Net Revenue M']-latest['Collected M']):.2f}M</div><div class="d">Needs cash focus</div></div>
            </div>
        """), unsafe_allow_html=True)

        op_col1, op_col2 = st.columns(2)
        with op_col1:
            st.markdown('<div class="rev-mini-title">Receivables Aging Waterfall</div>', unsafe_allow_html=True)
            with st.container(border=True):
                aging_bar = alt.Chart(rev_aging).mark_bar(cornerRadiusTopRight=7, cornerRadiusBottomRight=7, size=22).encode(
                    x=alt.X("Amount M:Q", title="Amount (€ M)"),
                    y=alt.Y("Bucket:N", sort=["Current", "1-30", "31-60", "61-90", "90+"], title=None),
                    color=alt.Color("Bucket:N", legend=None, scale=alt.Scale(range=["#10B981", "#29B5E8", "#6366F1", "#F59E0B", "#EF4444"])),
                    tooltip=["Bucket:N", alt.Tooltip("Amount M:Q", format=".2f")],
                )
                st.altair_chart(style_rev_chart(aging_bar, height=230), use_container_width=True)
                over_60 = rev_aging.loc[rev_aging["Bucket"].isin(["61-90", "90+"]), "Amount M"].sum()
                render_rev_ai_reco(
                    "Receivables Health",
                    f"Over-60-day receivables are at €{over_60:.2f}M.",
                    "Start escalation workflow for 61+ buckets with account-level prioritization.",
                    "Improve cash collection and reduce bad-debt risk.",
                    level="warning",
                )

        with op_col2:
            st.markdown('<div class="rev-mini-title">Channel Revenue vs Cost (ROI)</div>', unsafe_allow_html=True)
            with st.container(border=True):
                ch_bars = alt.Chart(rev_channels).transform_fold(["Revenue M", "Cost M"], as_=["Metric", "Amount"]).mark_bar(opacity=0.82, cornerRadiusTopLeft=5, cornerRadiusTopRight=5).encode(
                    x=alt.X("Channel:N", title=None),
                    y=alt.Y("Amount:Q", title="€ M"),
                    color=alt.Color("Metric:N", scale=alt.Scale(domain=["Revenue M", "Cost M"], range=["#29B5E8", "#94A3B8"]), legend=alt.Legend(title=None)),
                    xOffset="Metric:N",
                    tooltip=["Channel:N", "Metric:N", alt.Tooltip("Amount:Q", format=".2f")],
                )
                roi_line = alt.Chart(rev_channels).mark_line(point=True, color="#10B981", strokeWidth=3).encode(
                    x=alt.X("Channel:N", title=None),
                    y=alt.Y("ROI x:Q", title="ROI x"),
                    tooltip=["Channel:N", alt.Tooltip("ROI x:Q", format=".2f")],
                )
                st.altair_chart(style_rev_chart(alt.layer(ch_bars, roi_line).resolve_scale(y="independent"), height=230), use_container_width=True)
                weak = rev_channels.loc[rev_channels["ROI x"].idxmin()]
                render_rev_ai_reco(
                    "Channel Efficiency",
                    f"{weak['Channel']} is the weakest channel at {weak['ROI x']:.2f}x ROI.",
                    f"Rebalance spend from {weak['Channel']} to higher-ROI channels next cycle.",
                    "Improve blended channel profitability by 8-12%.",
                    level="warning",
                )

        st.markdown('<div class="rev-mini-title">Plan ARPU vs Subscriber Base</div>', unsafe_allow_html=True)
        with st.container(border=True):
            plan_scatter = alt.Chart(rev_plans).mark_circle(opacity=0.88, stroke="#FFFFFF", strokeWidth=1.4).encode(
                x=alt.X("Subs:Q", title="Subscribers"),
                y=alt.Y("ARPU:Q", title="ARPU (€)"),
                size=alt.Size("Revenue M:Q", scale=alt.Scale(range=[220, 1400]), legend=None),
                color=alt.Color("Plan:N", legend=alt.Legend(title=None), scale=alt.Scale(range=["#29B5E8", "#6366F1", "#10B981", "#F59E0B", "#EF4444"])),
                tooltip=["Plan:N", alt.Tooltip("Subs:Q", format=","), alt.Tooltip("ARPU:Q", format=".0f"), alt.Tooltip("Revenue M:Q", format=".3f")],
            )
            plan_labels = alt.Chart(rev_plans).mark_text(dy=-12, fontSize=9, color="#1E293B").encode(
                x="Subs:Q", y="ARPU:Q", text="Plan:N"
            )
            st.altair_chart(style_rev_chart(plan_scatter + plan_labels, height=235), use_container_width=True)
            top_arpu_plan = rev_plans.loc[rev_plans["ARPU"].idxmax()]
            render_rev_ai_reco(
                "Plan Monetization",
                f"{top_arpu_plan['Plan']} has the highest ARPU at €{top_arpu_plan['ARPU']:.0f}.",
                f"Use migration offers from PF Hogar 300 into {top_arpu_plan['Plan']} tiers where feasible.",
                "Increase blended ARPU while preserving retention.",
            )

    with rev_tab_sales:
        st.markdown('<div class="rev-title">Sales Performance Command Center</div>', unsafe_allow_html=True)
        sales_latest = sales_monthly.iloc[-1]
        sales_prev = sales_monthly.iloc[-2]
        sales_growth = (sales_latest["Total Sales M"] - sales_prev["Total Sales M"]) / sales_prev["Total Sales M"] * 100
        b2c_share = (sales_latest["B2C Sales M"] / sales_latest["Total Sales M"]) * 100
        b2b_share = (sales_latest["B2B Sales M"] / sales_latest["Total Sales M"]) * 100
        best_sales_channel = sales_channel_mix.loc[sales_channel_mix["Total Sales M"].idxmax()]
        best_sales_region = sales_region.loc[sales_region["Total Sales M"].idxmax()]
        top_pod = sales_reps.loc[sales_reps["Sales M"].idxmax()]
        sales_top_product = sales_product_mix.loc[sales_product_mix["Total Sales M"].idxmax()]
        digital_share = (sales_latest["Digital Sales M"] / sales_latest["Total Sales M"]) * 100
        retail_share = (sales_latest["Retail Stores M"] / sales_latest["Total Sales M"]) * 100

        st.markdown(dedent(f"""
            <div class="rev-pulse">
                <div class="rev-pulse-head">
                    <span class="rev-pulse-title">🛍️ Sales Pulse · PF Commercial KPIs</span>
                    <span class="rev-pulse-live">Live</span>
                </div>
                <div class="rev-pulse-grid">
                    <div class="rev-pulse-card"><div class="rev-pulse-label">Total Sales</div><div class="rev-pulse-value">€{sales_latest['Total Sales M']:.2f}M</div><div class="rev-pulse-delta">{sales_growth:+.2f}% MoM</div></div>
                    <div class="rev-pulse-card"><div class="rev-pulse-label">B2C Sales</div><div class="rev-pulse-value">€{sales_latest['B2C Sales M']:.2f}M</div><div class="rev-pulse-delta">{b2c_share:.1f}% mix</div></div>
                    <div class="rev-pulse-card"><div class="rev-pulse-label">B2B Sales</div><div class="rev-pulse-value">€{sales_latest['B2B Sales M']:.2f}M</div><div class="rev-pulse-delta">{b2b_share:.1f}% mix</div></div>
                    <div class="rev-pulse-card"><div class="rev-pulse-label">Digital Sales</div><div class="rev-pulse-value">€{sales_latest['Digital Sales M']:.2f}M</div><div class="rev-pulse-delta">{digital_share:.1f}% of sales</div></div>
                    <div class="rev-pulse-card"><div class="rev-pulse-label">Retail Stores</div><div class="rev-pulse-value">€{sales_latest['Retail Stores M']:.2f}M</div><div class="rev-pulse-delta">{retail_share:.1f}% of sales</div></div>
                    <div class="rev-pulse-card"><div class="rev-pulse-label">Blended Sales Margin</div><div class="rev-pulse-value">{sales_latest['Blended Margin %']:.1f}%</div><div class="rev-pulse-delta">Margin expansion trend</div></div>
                </div>
            </div>
        """), unsafe_allow_html=True)

        st.markdown(dedent(f"""
            <div class="rev-kpi-grid">
                <div class="rev-kpi-card"><div class="k">Top Channel</div><div class="v">{best_sales_channel['Channel']}</div><div class="d">€{best_sales_channel['Total Sales M']:.2f}M</div></div>
                <div class="rev-kpi-card"><div class="k">Top Region</div><div class="v">{best_sales_region['Region']}</div><div class="d">€{best_sales_region['Total Sales M']:.2f}M sales</div></div>
                <div class="rev-kpi-card"><div class="k">Top Sales Pod</div><div class="v">{top_pod['Sales Pod']}</div><div class="d">{top_pod['Win Rate %']:.1f}% win rate</div></div>
                <div class="rev-kpi-card warn"><div class="k">Lowest Margin Region</div><div class="v">{sales_region.loc[sales_region['Margin %'].idxmin(), 'Region']}</div><div class="d">{sales_region['Margin %'].min():.1f}% margin</div></div>
                <div class="rev-kpi-card"><div class="k">Best Product</div><div class="v">{sales_top_product['Product']}</div><div class="d">€{sales_top_product['Total Sales M']:.2f}M sales</div></div>
                <div class="rev-kpi-card"><div class="k">B2C/B2B Balance</div><div class="v">{b2c_share:.0f}% / {b2b_share:.0f}%</div><div class="d">Latest month mix</div></div>
                <div class="rev-kpi-card"><div class="k">Store Footprint</div><div class="v">{int(sales_region['Retail Stores'].sum())}</div><div class="d">Active retail points</div></div>
                <div class="rev-kpi-card crit"><div class="k">Sales Concentration</div><div class="v">{(best_sales_region['Total Sales M']/sales_region['Total Sales M'].sum()*100):.1f}%</div><div class="d">Top-region dependence</div></div>
            </div>
        """), unsafe_allow_html=True)

        sl_col1, sl_col2 = st.columns(2)
        with sl_col1:
            st.markdown('<div class="rev-mini-title">B2C vs B2B Monthly Sales</div>', unsafe_allow_html=True)
            with st.container(border=True):
                b2c_line = alt.Chart(sales_monthly).mark_line(point=True, strokeWidth=3, color="#29B5E8").encode(
                    x=alt.X("Month:N", title=None),
                    y=alt.Y("B2C Sales M:Q", title="Sales (€ M)"),
                    tooltip=["Month:N", alt.Tooltip("B2C Sales M:Q", format=".2f"), alt.Tooltip("B2B Sales M:Q", format=".2f"), alt.Tooltip("Total Sales M:Q", format=".2f")],
                )
                b2b_line = alt.Chart(sales_monthly).mark_line(point=True, strokeWidth=3, color="#6366F1").encode(
                    x=alt.X("Month:N", title=None),
                    y=alt.Y("B2B Sales M:Q", title="Sales (€ M)"),
                )
                st.altair_chart(style_rev_chart(b2c_line + b2b_line, height=230), use_container_width=True)
                render_rev_ai_reco(
                    "Commercial Balance",
                    f"B2C leads with {b2c_share:.1f}% share while B2B contributes {b2b_share:.1f}% at higher ticket size.",
                    "Keep B2C volume engine in digital channels and scale B2B hunting in Madrid Metro and Norte.",
                    "Sustain top-line momentum while improving sales quality.",
                )

        with sl_col2:
            st.markdown('<div class="rev-mini-title">Digital, Retail, Field and Partner Sales</div>', unsafe_allow_html=True)
            with st.container(border=True):
                motion_df = sales_monthly[["Month", "Digital Sales M", "Retail Stores M", "Field Sales M", "Partner Sales M"]].copy()
                motion_long = motion_df.melt("Month", var_name="Motion", value_name="Sales M")
                motion_bar = alt.Chart(motion_long).mark_bar(opacity=0.85).encode(
                    x=alt.X("Month:N", title=None),
                    y=alt.Y("Sales M:Q", title="Sales (€ M)"),
                    color=alt.Color("Motion:N", scale=alt.Scale(domain=["Digital Sales M", "Retail Stores M", "Field Sales M", "Partner Sales M"], range=["#29B5E8", "#10B981", "#6366F1", "#F59E0B"]), legend=alt.Legend(title=None)),
                    tooltip=["Month:N", "Motion:N", alt.Tooltip("Sales M:Q", format=".2f")],
                )
                margin_line = alt.Chart(sales_monthly).mark_line(point=True, strokeWidth=3, color="#EF4444").encode(
                    x=alt.X("Month:N", title=None),
                    y=alt.Y("Blended Margin %:Q", title="Margin %"),
                    tooltip=["Month:N", alt.Tooltip("Blended Margin %:Q", format=".1f")],
                )
                st.altair_chart(style_rev_chart(alt.layer(motion_bar, margin_line).resolve_scale(y="independent"), height=230), use_container_width=True)
                render_rev_ai_reco(
                    "Channel Mix and Margin",
                    f"Digital is the largest motion at {digital_share:.1f}% of current sales while margins improved to {sales_latest['Blended Margin %']:.1f}%.",
                    "Increase conversion spend in PF Web and protect margin guardrails in retail promotions.",
                    "Lift sales throughput without diluting profitability.",
                )

        sl_col3, sl_col4 = st.columns(2)
        with sl_col3:
            st.markdown('<div class="rev-mini-title">B2C vs B2B by Region</div>', unsafe_allow_html=True)
            with st.container(border=True):
                reg_long = sales_region.melt(id_vars=["Region"], value_vars=["B2C Sales M", "B2B Sales M"], var_name="Segment", value_name="Sales M")
                reg_bar = alt.Chart(reg_long).mark_bar(opacity=0.84, cornerRadiusTopLeft=5, cornerRadiusTopRight=5).encode(
                    x=alt.X("Region:N", title=None),
                    y=alt.Y("Sales M:Q", title="Sales (€ M)"),
                    color=alt.Color("Segment:N", scale=alt.Scale(domain=["B2C Sales M", "B2B Sales M"], range=["#29B5E8", "#6366F1"]), legend=alt.Legend(title=None)),
                    xOffset="Segment:N",
                    tooltip=["Region:N", "Segment:N", alt.Tooltip("Sales M:Q", format=".2f")],
                )
                st.altair_chart(style_rev_chart(reg_bar, height=230), use_container_width=True)
                render_rev_ai_reco(
                    "Regional Segment Focus",
                    f"{best_sales_region['Region']} is the strongest sales region with balanced B2C and B2B pull.",
                    f"Replicate {best_sales_region['Region']} playbook in Centro and Este through targeted field coverage.",
                    "Improve regional productivity and reduce concentration risk.",
                )

        with sl_col4:
            st.markdown('<div class="rev-mini-title">Top Sales Regions and Margin</div>', unsafe_allow_html=True)
            with st.container(border=True):
                top_region = sales_region.sort_values("Total Sales M", ascending=False)
                top_reg_bar = alt.Chart(top_region).mark_bar(cornerRadiusTopRight=7, cornerRadiusBottomRight=7, size=22).encode(
                    x=alt.X("Total Sales M:Q", title="Total Sales (€ M)"),
                    y=alt.Y("Region:N", sort="-x", title=None),
                    color=alt.Color("Margin %:Q", scale=alt.Scale(scheme="blues"), legend=alt.Legend(title="Margin %")),
                    tooltip=["Region:N", alt.Tooltip("Total Sales M:Q", format=".2f"), alt.Tooltip("Margin %:Q", format=".1f"), "Retail Stores:Q"],
                )
                st.altair_chart(style_rev_chart(top_reg_bar, height=230), use_container_width=True)
                low_margin_region = sales_region.loc[sales_region["Margin %"].idxmin()]
                render_rev_ai_reco(
                    "Regional Margin Management",
                    f"{low_margin_region['Region']} has the lowest sales margin at {low_margin_region['Margin %']:.1f}%.",
                    f"Tighten discount policy and improve bundle attach in {low_margin_region['Region']}.",
                    "Recover 1-2pp margin while maintaining local sales velocity.",
                    level="warning",
                )

        sl_col5, sl_col6 = st.columns(2)
        with sl_col5:
            st.markdown('<div class="rev-mini-title">Top Sales Pods Performance</div>', unsafe_allow_html=True)
            with st.container(border=True):
                pod_scatter = alt.Chart(sales_reps).mark_circle(opacity=0.9, stroke="#FFFFFF", strokeWidth=1.2).encode(
                    x=alt.X("Win Rate %:Q", title="Win Rate %"),
                    y=alt.Y("Sales M:Q", title="Sales (€ M)"),
                    size=alt.Size("New Logos:Q", scale=alt.Scale(range=[240, 1300]), legend=alt.Legend(title="New Logos")),
                    color=alt.Color("Region:N", legend=alt.Legend(title=None), scale=alt.Scale(range=["#29B5E8", "#6366F1", "#10B981", "#F59E0B", "#EF4444"])),
                    tooltip=["Sales Pod:N", "Region:N", alt.Tooltip("Sales M:Q", format=".2f"), alt.Tooltip("Win Rate %:Q", format=".1f"), "New Logos:Q"],
                )
                pod_labels = alt.Chart(sales_reps).mark_text(dy=-10, fontSize=9, color="#1E293B").encode(
                    x="Win Rate %:Q", y="Sales M:Q", text="Sales Pod:N"
                )
                st.altair_chart(style_rev_chart(pod_scatter + pod_labels, height=235), use_container_width=True)
                render_rev_ai_reco(
                    "Top Sales Execution",
                    f"{top_pod['Sales Pod']} leads with €{top_pod['Sales M']:.2f}M and {top_pod['Win Rate %']:.1f}% win rate.",
                    "Codify this pod's discovery and closing framework for other regional teams.",
                    "Increase close rates across the sales organization.",
                )

        with sl_col6:
            st.markdown('<div class="rev-mini-title">Sales by PF Product</div>', unsafe_allow_html=True)
            with st.container(border=True):
                prod_donut = alt.Chart(sales_product_mix).mark_arc(innerRadius=62, outerRadius=105, stroke="#FFFFFF", strokeWidth=2).encode(
                    theta=alt.Theta("Total Sales M:Q", stack=True),
                    color=alt.Color("Product:N", scale=alt.Scale(range=["#29B5E8", "#6366F1", "#10B981", "#F59E0B", "#EF4444", "#14B8A6"]), legend=alt.Legend(title=None)),
                    tooltip=["Product:N", alt.Tooltip("Total Sales M:Q", format=".2f"), alt.Tooltip("B2C Sales M:Q", format=".2f"), alt.Tooltip("B2B Sales M:Q", format=".2f"), alt.Tooltip("Attach Rate %:Q", format=".1f")],
                )
                prod_center = alt.Chart(pd.DataFrame({"t": [f"€{sales_product_mix['Total Sales M'].sum():.1f}M"]})).mark_text(fontSize=21, fontWeight="bold", color="#0F172A").encode(text="t:N")
                prod_sub = alt.Chart(pd.DataFrame({"t": ["Product Sales Mix"]})).mark_text(fontSize=11, dy=18, color="#64748B").encode(text="t:N")
                st.altair_chart(style_rev_chart(prod_donut + prod_center + prod_sub, height=235), use_container_width=True)
                render_rev_ai_reco(
                    "Portfolio Sales Priorities",
                    f"{sales_top_product['Product']} is the strongest product by sales at €{sales_top_product['Total Sales M']:.2f}M.",
                    "Push attach bundles (Mesh Plus and TV App) into high-volume plans and B2B migrations.",
                    "Increase ARPU and raise cross-sell contribution.",
                )

        st.markdown('<div class="rev-title">Sales Pipeline, Targets and Forecast Discipline</div>', unsafe_allow_html=True)
        pp_col1, pp_col2 = st.columns(2)
        with pp_col1:
            st.markdown('<div class="rev-mini-title">Pipeline Health by Stage (B2C + B2B)</div>', unsafe_allow_html=True)
            with st.container(border=True):
                pipe_long = sales_pipeline.melt(id_vars=["Stage", "Avg Age Days"], value_vars=["B2C K", "B2B K"], var_name="Segment", value_name="Volume K")
                pipe_bar = alt.Chart(pipe_long).mark_bar(opacity=0.85, cornerRadiusTopLeft=5, cornerRadiusTopRight=5).encode(
                    x=alt.X("Stage:N", title=None),
                    y=alt.Y("Volume K:Q", title="Volume (K)"),
                    color=alt.Color("Segment:N", scale=alt.Scale(domain=["B2C K", "B2B K"], range=["#29B5E8", "#6366F1"]), legend=alt.Legend(title=None)),
                    xOffset="Segment:N",
                    tooltip=["Stage:N", "Segment:N", alt.Tooltip("Volume K:Q", format=".2f"), "Avg Age Days:Q"],
                )
                age_line = alt.Chart(sales_pipeline).mark_line(point=True, strokeWidth=3, color="#F59E0B").encode(
                    x=alt.X("Stage:N", title=None),
                    y=alt.Y("Avg Age Days:Q", title="Avg Age (days)"),
                    tooltip=["Stage:N", alt.Tooltip("Avg Age Days:Q", format=".0f")],
                )
                st.altair_chart(style_rev_chart(alt.layer(pipe_bar, age_line).resolve_scale(y="independent"), height=235), use_container_width=True)
                neg_age = sales_pipeline.loc[sales_pipeline["Stage"] == "Negotiation", "Avg Age Days"].iloc[0]
                render_rev_ai_reco(
                    "Pipeline Flow",
                    f"Negotiation stage aging reached {neg_age:.0f} days and is the main close-speed constraint.",
                    "Launch weekly deal review for negotiation-stage opportunities with pricing and legal fast-track.",
                    "Improve close velocity and reduce carry-over risk.",
                    level="warning",
                )

        with pp_col2:
            st.markdown('<div class="rev-mini-title">Target vs Actual Attainment</div>', unsafe_allow_html=True)
            with st.container(border=True):
                quota_chart = alt.Chart(sales_quota).mark_bar(cornerRadiusTopLeft=5, cornerRadiusTopRight=5, opacity=0.85).encode(
                    x=alt.X("Dimension:N", title=None),
                    y=alt.Y("Actual M:Q", title="Sales (€ M)"),
                    color=alt.Color("Type:N", scale=alt.Scale(domain=["Channel", "Region"], range=["#29B5E8", "#10B981"]), legend=alt.Legend(title=None)),
                    tooltip=["Dimension:N", "Type:N", alt.Tooltip("Target M:Q", format=".2f"), alt.Tooltip("Actual M:Q", format=".2f"), alt.Tooltip("Attainment %:Q", format=".1f")],
                )
                target_rule = alt.Chart(sales_quota).mark_tick(color="#334155", thickness=2, size=20).encode(
                    x=alt.X("Dimension:N", title=None),
                    y="Target M:Q",
                )
                st.altair_chart(style_rev_chart(quota_chart + target_rule, height=235), use_container_width=True)
                low_att = sales_quota.loc[sales_quota["Attainment %"].idxmin()]
                render_rev_ai_reco(
                    "Quota Attainment",
                    f"{low_att['Dimension']} is the lowest attainment point at {low_att['Attainment %']:.1f}%.",
                    f"Deploy focused recovery plan for {low_att['Dimension']} with weekly target checkpoints.",
                    "Close target gap faster before quarter end.",
                    level="warning",
                )

        ff_col1, ff_col2 = st.columns(2)
        with ff_col1:
            st.markdown('<div class="rev-mini-title">Forecast Accuracy (Snapshot vs Actual)</div>', unsafe_allow_html=True)
            with st.container(border=True):
                fcst_long = sales_forecast.melt(id_vars=["Month", "Actual M"], value_vars=["Fcst -90d M", "Fcst -30d M"], var_name="Forecast", value_name="Forecast M")
                fcst_line = alt.Chart(fcst_long).mark_line(point=True, strokeWidth=3).encode(
                    x=alt.X("Month:N", title=None),
                    y=alt.Y("Forecast M:Q", title="Sales (€ M)"),
                    color=alt.Color("Forecast:N", scale=alt.Scale(domain=["Fcst -90d M", "Fcst -30d M"], range=["#94A3B8", "#29B5E8"]), legend=alt.Legend(title=None)),
                    tooltip=["Month:N", "Forecast:N", alt.Tooltip("Forecast M:Q", format=".2f")],
                )
                actual_line = alt.Chart(sales_forecast).mark_line(point=True, strokeWidth=3, color="#10B981").encode(
                    x=alt.X("Month:N", title=None),
                    y=alt.Y("Actual M:Q", title="Sales (€ M)"),
                    tooltip=["Month:N", alt.Tooltip("Actual M:Q", format=".2f"), alt.Tooltip("Error -30d %:Q", format=".1f"), alt.Tooltip("Error -90d %:Q", format=".1f")],
                )
                st.altair_chart(style_rev_chart(fcst_line + actual_line, height=235), use_container_width=True)
                err30 = sales_forecast["Error -30d %"].abs().mean()
                render_rev_ai_reco(
                    "Forecast Reliability",
                    f"Average 30-day forecast error is {err30:.1f}% across recent closes.",
                    "Tighten stage probability calibration and enforce forecast commit criteria by pod.",
                    "Improve forecast confidence for board-level planning.",
                )

        with ff_col2:
            st.markdown('<div class="rev-mini-title">Price and Discount Waterfall</div>', unsafe_allow_html=True)
            with st.container(border=True):
                wf = sales_waterfall.copy()
                wf["Type"] = wf["Value M"].apply(lambda v: "Up" if v >= 0 else "Down")
                wf_bar = alt.Chart(wf).mark_bar(cornerRadiusTopLeft=5, cornerRadiusTopRight=5, size=44).encode(
                    x=alt.X("Step:N", title=None),
                    y=alt.Y("Value M:Q", title="Impact (€ M)"),
                    color=alt.Color("Type:N", scale=alt.Scale(domain=["Up", "Down"], range=["#10B981", "#EF4444"]), legend=None),
                    tooltip=["Step:N", alt.Tooltip("Value M:Q", format="+.2f"), alt.Tooltip("Cumulative M:Q", format=".2f")],
                )
                zero_rule = alt.Chart(pd.DataFrame({"y": [0]})).mark_rule(color="#94A3B8", strokeDash=[4, 4]).encode(y="y:Q")
                st.altair_chart(style_rev_chart(zero_rule + wf_bar, height=235), use_container_width=True)
                discount_impact = abs(float(sales_waterfall.loc[sales_waterfall["Step"] == "Discounts", "Value M"].iloc[0]))
                render_rev_ai_reco(
                    "Discount Discipline",
                    f"Discount drag is €{discount_impact:.2f}M in the latest month waterfall.",
                    "Set discount guardrails by product and require approval above threshold levels.",
                    "Protect margin while sustaining close rates.",
                    level="warning",
                )

        st.markdown('<div class="rev-title">Retention Quality, SLA and Productivity</div>', unsafe_allow_html=True)
        rq_col1, rq_col2 = st.columns(2)
        with rq_col1:
            st.markdown('<div class="rev-mini-title">30/60/90-Day Retention by Sales Cohort</div>', unsafe_allow_html=True)
            with st.container(border=True):
                cohort_long = sales_cohort.melt(id_vars=["Cohort"], value_vars=["Retention 30d %", "Retention 60d %", "Retention 90d %"], var_name="Window", value_name="Retention %")
                cohort_line = alt.Chart(cohort_long).mark_line(point=True, strokeWidth=3).encode(
                    x=alt.X("Cohort:N", title=None),
                    y=alt.Y("Retention %:Q", title="Retention %"),
                    color=alt.Color("Window:N", scale=alt.Scale(domain=["Retention 30d %", "Retention 60d %", "Retention 90d %"], range=["#10B981", "#29B5E8", "#6366F1"]), legend=alt.Legend(title=None)),
                    tooltip=["Cohort:N", "Window:N", alt.Tooltip("Retention %:Q", format=".1f")],
                )
                st.altair_chart(style_rev_chart(cohort_line, height=230), use_container_width=True)
                latest_90 = sales_cohort.iloc[-1]["Retention 90d %"]
                render_rev_ai_reco(
                    "Sales Quality Cohorts",
                    f"Latest cohort 90-day retention is {latest_90:.1f}%, signaling good post-sale quality.",
                    "Prioritize proactive care journeys for lower-retention cohorts immediately after activation.",
                    "Reduce early-life churn and protect realized sales value.",
                )

        with rq_col2:
            st.markdown('<div class="rev-mini-title">Install-to-Revenue SLA by Region</div>', unsafe_allow_html=True)
            with st.container(border=True):
                sla_bar = alt.Chart(sales_install_sla).mark_bar(cornerRadiusTopLeft=5, cornerRadiusTopRight=5, opacity=0.84).encode(
                    x=alt.X("Region:N", title=None),
                    y=alt.Y("Sale to Install Days:Q", title="Days"),
                    color=alt.Color("SLA Met %:Q", scale=alt.Scale(scheme="tealblues"), legend=alt.Legend(title="SLA Met %")),
                    tooltip=["Region:N", alt.Tooltip("Sale to Install Days:Q", format=".1f"), alt.Tooltip("Install to First Invoice Days:Q", format=".1f"), alt.Tooltip("SLA Met %:Q", format=".1f")],
                )
                invoice_line = alt.Chart(sales_install_sla).mark_line(point=True, strokeWidth=3, color="#F59E0B").encode(
                    x=alt.X("Region:N", title=None),
                    y=alt.Y("Install to First Invoice Days:Q", title="Days"),
                )
                st.altair_chart(style_rev_chart(alt.layer(sla_bar, invoice_line).resolve_scale(y="independent"), height=230), use_container_width=True)
                slow_region = sales_install_sla.loc[sales_install_sla["Sale to Install Days"].idxmax()]
                render_rev_ai_reco(
                    "Order-to-Cash SLA",
                    f"{slow_region['Region']} has the longest sale-to-install cycle at {slow_region['Sale to Install Days']:.1f} days.",
                    f"Prioritize installation slots and first-invoice automation in {slow_region['Region']}.",
                    "Accelerate revenue recognition and customer activation experience.",
                    level="warning",
                )

        st.markdown('<div class="rev-mini-title">Sales Productivity by Motion</div>', unsafe_allow_html=True)
        with st.container(border=True):
            prod_scatter = alt.Chart(sales_productivity).mark_circle(opacity=0.9, stroke="#FFFFFF", strokeWidth=1.2).encode(
                x=alt.X("Cycle Days:Q", title="Sales Cycle (days)"),
                y=alt.Y("Revenue per Rep K:Q", title="Revenue per Rep (€ K)"),
                size=alt.Size("Avg Deal Size K:Q", scale=alt.Scale(range=[300, 1800]), legend=alt.Legend(title="Avg Deal Size K")),
                color=alt.Color("Motion:N", scale=alt.Scale(range=["#29B5E8", "#6366F1", "#10B981"]), legend=alt.Legend(title=None)),
                tooltip=["Motion:N", alt.Tooltip("Revenue per Rep K:Q", format=".0f"), alt.Tooltip("Win Rate %:Q", format=".1f"), alt.Tooltip("Activity to Close %:Q", format=".1f")],
            )
            prod_label = alt.Chart(sales_productivity).mark_text(dy=-10, fontSize=9, color="#1E293B").encode(
                x="Cycle Days:Q", y="Revenue per Rep K:Q", text="Motion:N"
            )
            st.altair_chart(style_rev_chart(prod_scatter + prod_label, height=235), use_container_width=True)
            top_motion = sales_productivity.loc[sales_productivity["Revenue per Rep K"].idxmax()]
            render_rev_ai_reco(
                "Productivity Focus",
                f"{top_motion['Motion']} delivers the highest productivity at €{top_motion['Revenue per Rep K']:.0f}K per rep.",
                "Scale playbooks from top motion and rebalance capacity from lower-efficiency motions.",
                "Lift overall sales productivity and shorten cycle times.",
            )

        st.markdown('<div class="rev-title">Madrid Neighborhood Sales Heatmap</div>', unsafe_allow_html=True)
        with st.container(border=True):
            madrid_layers = [
                pdk.Layer(
                    "ScatterplotLayer",
                    data=madrid_sales_map,
                    get_position="[lon, lat]",
                    get_radius="radius",
                    get_fill_color="[r, g, b, 165]",
                    get_line_color="[255, 255, 255, 220]",
                    line_width_min_pixels=1.2,
                    stroked=True,
                    pickable=True,
                ),
                pdk.Layer(
                    "TextLayer",
                    data=madrid_sales_map,
                    get_position="[lon, lat]",
                    get_text="Neighborhood",
                    get_size=12,
                    get_color=[15, 23, 42, 230],
                    get_alignment_baseline="'top'",
                    get_pixel_offset=[0, 14],
                    pickable=False,
                ),
            ]
            madrid_deck = pdk.Deck(
                layers=madrid_layers,
                initial_view_state=pdk.ViewState(latitude=40.42, longitude=-3.70, zoom=11.6, pitch=8),
                map_style="https://basemaps.cartocdn.com/gl/positron-gl-style/style.json",
                tooltip={
                    "html": "<b>{Neighborhood}</b><br/>Sales: €{Sales M}M<br/>B2B Share: {B2B Share %}%<br/>Margin: {Margin %}%"
                },
            )
            st.pydeck_chart(madrid_deck, use_container_width=True)
            st.markdown(dedent("""
                <div style="margin-top:0.4rem; display:flex; flex-wrap:wrap; gap:0.4rem;">
                    <span style="display:inline-flex; align-items:center; gap:0.34rem; background:#F8FAFC; border:1px solid #E2E8F0; border-radius:999px; padding:0.16rem 0.5rem; font-size:0.72rem; color:#334155; font-weight:700;">
                        <span style="width:10px; height:10px; border-radius:50%; background:#10B981; display:inline-block;"></span> High Margin / High Sales
                    </span>
                    <span style="display:inline-flex; align-items:center; gap:0.34rem; background:#F8FAFC; border:1px solid #E2E8F0; border-radius:999px; padding:0.16rem 0.5rem; font-size:0.72rem; color:#334155; font-weight:700;">
                        <span style="width:10px; height:10px; border-radius:50%; background:#2979FF; display:inline-block;"></span> Medium Margin
                    </span>
                    <span style="display:inline-flex; align-items:center; gap:0.34rem; background:#F8FAFC; border:1px solid #E2E8F0; border-radius:999px; padding:0.16rem 0.5rem; font-size:0.72rem; color:#334155; font-weight:700;">
                        <span style="width:10px; height:10px; border-radius:50%; background:#F59E0B; display:inline-block;"></span> Low Margin Priority
                    </span>
                </div>
            """), unsafe_allow_html=True)
            top_madrid = madrid_sales_map.loc[madrid_sales_map["Sales M"].idxmax()]
            low_madrid = madrid_sales_map.loc[madrid_sales_map["Margin %"].idxmin()]
            render_rev_ai_reco(
                "Madrid Neighborhood White-Space",
                f"{top_madrid['Neighborhood']} is the top Madrid sales pocket at €{top_madrid['Sales M']:.2f}M, while {low_madrid['Neighborhood']} has the lowest margin.",
                f"Keep high-intent investment in {top_madrid['Neighborhood']} and run pricing/attach correction in {low_madrid['Neighborhood']}.",
                "Grow Madrid revenue while improving unit economics by district.",
                level="warning",
            )

        st.markdown('<div class="rev-title">Top Deals, Loss Insights and Action Queue</div>', unsafe_allow_html=True)
        td_col1, td_col2 = st.columns(2)
        with td_col1:
            st.markdown('<div class="rev-mini-title">Top Won and Lost Deals</div>', unsafe_allow_html=True)
            with st.container(border=True):
                deals_bar = alt.Chart(sales_deals).mark_bar(cornerRadiusTopLeft=5, cornerRadiusTopRight=5).encode(
                    x=alt.X("Deal:N", title=None),
                    y=alt.Y("Value K:Q", title="Deal Value (€ K)"),
                    color=alt.Color("Status:N", scale=alt.Scale(domain=["Won", "Lost"], range=["#10B981", "#EF4444"]), legend=alt.Legend(title=None)),
                    tooltip=["Deal:N", "Status:N", "Region:N", alt.Tooltip("Value K:Q", format=".0f"), "Reason:N"],
                )
                st.altair_chart(style_rev_chart(deals_bar, height=230), use_container_width=True)
                lost_top = sales_deals[sales_deals["Status"] == "Lost"].sort_values("Value K", ascending=False).iloc[0]
                render_rev_ai_reco(
                    "Top Loss Recovery",
                    f"Highest lost deal is {lost_top['Deal']} at €{lost_top['Value K']:.0f}K, mostly due to {lost_top['Reason'].lower()}.",
                    "Build dedicated save-kit for high-value loss reasons (pricing, SLA, procurement).",
                    "Recover strategic deals and improve win-rate in enterprise opportunities.",
                    level="warning",
                )

        with td_col2:
            st.markdown('<div class="rev-mini-title">Sales Alert and Action Queue</div>', unsafe_allow_html=True)
            weak_att = sales_quota.loc[sales_quota["Attainment %"].idxmin()]
            aging_peak = sales_pipeline.loc[sales_pipeline["Avg Age Days"].idxmax()]
            sla_low = sales_install_sla.loc[sales_install_sla["SLA Met %"].idxmin()]
            st.markdown(dedent(f"""
                <div class="rev-ai-card warning">
                    <div class="rev-ai-head">🚦 This Week Priority Queue</div>
                    <div class="rev-ai-line"><strong>Target Risk:</strong> {weak_att['Dimension']} is at {weak_att['Attainment %']:.1f}% attainment ({weak_att['Gap M']:+.2f}M gap).</div>
                    <div class="rev-ai-line"><strong>Pipeline Risk:</strong> {aging_peak['Stage']} stage is aging at {aging_peak['Avg Age Days']:.0f} days.</div>
                    <div class="rev-ai-line"><strong>Execution Risk:</strong> {sla_low['Region']} SLA compliance is {sla_low['SLA Met %']:.1f}%.</div>
                </div>
            """), unsafe_allow_html=True)
            render_rev_ai_reco(
                "Action Queue",
                "Three risks are active: target gap, stage aging, and install SLA slippage.",
                "Run daily huddle with sales + operations for the flagged dimensions until normalized.",
                "Faster tactical recovery and stronger month-end close predictability.",
                level="critical",
            )

    with rev_tab_risk:
        st.markdown('<div class="rev-title">Revenue Risk and Strategy</div>', unsafe_allow_html=True)
        st.markdown(dedent(f"""
            <div class="rev-kpi-grid">
                <div class="rev-kpi-card crit"><div class="k">Revenue at Risk</div><div class="v">€{at_risk_rev_m:.2f}M</div><div class="d">Current exposure</div></div>
                <div class="rev-kpi-card warn"><div class="k">Top Risk Driver</div><div class="v">{rev_risk.loc[rev_risk['Exposure M'].idxmax(), 'Risk Driver']}</div><div class="d">Highest exposure line</div></div>
                <div class="rev-kpi-card"><div class="k">Base Scenario (Q)</div><div class="v">€{rev_scenario.loc[rev_scenario['Scenario']=='Base', 'Quarter Revenue M'].iloc[0]:.1f}M</div><div class="d">Highest probability</div></div>
                <div class="rev-kpi-card"><div class="k">Upside Potential</div><div class="v">€{(rev_scenario.iloc[-1]['Quarter Revenue M']-rev_scenario.iloc[1]['Quarter Revenue M']):.1f}M</div><div class="d">vs base scenario</div></div>
                <div class="rev-kpi-card warn"><div class="k">Downside Gap</div><div class="v">€{(rev_scenario.iloc[1]['Quarter Revenue M']-rev_scenario.iloc[0]['Quarter Revenue M']):.1f}M</div><div class="d">vs base scenario</div></div>
                <div class="rev-kpi-card"><div class="k">Risk Coverage</div><div class="v">{(1 - rev_risk['Exposure M'].sum()/arr):.1%}</div><div class="d">ARR protected</div></div>
                <div class="rev-kpi-card"><div class="k">Collection Quality</div><div class="v">{collection_rate:.1f}%</div><div class="d">Cash resilience</div></div>
                <div class="rev-kpi-card crit"><div class="k">Delinquency Exposure</div><div class="v">€{rev_risk.loc[rev_risk['Risk Driver']=='Delinquency', 'Exposure M'].iloc[0]:.2f}M</div><div class="d">Critical watch</div></div>
            </div>
        """), unsafe_allow_html=True)

        rk_col1, rk_col2 = st.columns(2)
        with rk_col1:
            st.markdown('<div class="rev-mini-title">Revenue Risk Drivers</div>', unsafe_allow_html=True)
            with st.container(border=True):
                risk_bar = alt.Chart(rev_risk).mark_bar(cornerRadiusTopRight=7, cornerRadiusBottomRight=7, size=20).encode(
                    x=alt.X("Exposure M:Q", title="Exposure (€ M)"),
                    y=alt.Y("Risk Driver:N", sort="-x", title=None),
                    color=alt.Color("Likelihood:Q", scale=alt.Scale(scheme="orangered"), legend=None),
                    tooltip=["Risk Driver:N", alt.Tooltip("Exposure M:Q", format=".2f"), alt.Tooltip("Likelihood:Q", format=".1f")],
                )
                risk_labels = alt.Chart(rev_risk).mark_text(align="left", dx=6, fontSize=10, color="#0F172A").encode(
                    x="Exposure M:Q",
                    y=alt.Y("Risk Driver:N", sort="-x"),
                    text=alt.Text("Exposure M:Q", format=".2f"),
                )
                st.altair_chart(style_rev_chart(risk_bar + risk_labels, height=230), use_container_width=True)
                top_risk = rev_risk.loc[rev_risk["Exposure M"].idxmax()]
                render_rev_ai_reco(
                    "Risk Prioritization",
                    f"{top_risk['Risk Driver']} is the highest exposure risk at €{top_risk['Exposure M']:.2f}M.",
                    f"Assign cross-functional mitigation sprint for {top_risk['Risk Driver']} with weekly governance.",
                    "Reduce downside risk and improve forecast confidence.",
                    level="critical",
                )

        with rk_col2:
            st.markdown('<div class="rev-mini-title">Quarter Revenue Scenarios</div>', unsafe_allow_html=True)
            with st.container(border=True):
                sc_bar = alt.Chart(rev_scenario).mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6, size=56).encode(
                    x=alt.X("Scenario:N", title=None),
                    y=alt.Y("Quarter Revenue M:Q", title="Revenue (€ M)"),
                    color=alt.Color("Scenario:N", scale=alt.Scale(domain=["Downside", "Base", "Upside"], range=["#EF4444", "#3B82F6", "#10B981"]), legend=None),
                    tooltip=["Scenario:N", alt.Tooltip("Quarter Revenue M:Q", format=".1f"), "Probability:N"],
                )
                sc_labels = alt.Chart(rev_scenario).mark_text(dy=-8, fontSize=11, fontWeight="bold", color="#0F172A").encode(
                    x="Scenario:N",
                    y="Quarter Revenue M:Q",
                    text=alt.Text("Quarter Revenue M:Q", format=".1f"),
                )
                st.altair_chart(style_rev_chart(sc_bar + sc_labels, height=230), use_container_width=True)
                base_q = rev_scenario.loc[rev_scenario["Scenario"] == "Base", "Quarter Revenue M"].iloc[0]
                render_rev_ai_reco(
                    "Scenario Planning",
                    f"Base scenario is €{base_q:.1f}M with balanced probability weight.",
                    "Pre-authorize tactical levers for downside triggers and expansion offers for upside capture.",
                    "Shorten reaction time and stabilize quarter-close outcomes.",
                )

        st.markdown('<div class="rev-title">Interactive What-If Analysis</div>', unsafe_allow_html=True)
        whatif_presets = {
            "Defensive": {"churn": 1.2, "price": -0.5, "collection": -0.4, "discount": 1.6},
            "Base": {"churn": 0.4, "price": 0.8, "collection": 0.4, "discount": 0.3},
            "Growth": {"churn": 0.1, "price": 2.0, "collection": 0.9, "discount": 0.1},
            "Stretch": {"churn": -0.2, "price": 3.2, "collection": 1.4, "discount": -0.4},
        }

        # Keep widget state owned by session_state to avoid key/default conflicts.
        st.session_state.setdefault("rev_whatif_churn", whatif_presets["Base"]["churn"])
        st.session_state.setdefault("rev_whatif_price", whatif_presets["Base"]["price"])
        st.session_state.setdefault("rev_whatif_collection", whatif_presets["Base"]["collection"])
        st.session_state.setdefault("rev_whatif_discount", whatif_presets["Base"]["discount"])

        st.markdown('<div class="rev-mini-title">Scenario Presets</div>', unsafe_allow_html=True)
        preset_col1, preset_col2, preset_col3, preset_col4 = st.columns(4)
        with preset_col1:
            if st.button("🛡️ Defensive", use_container_width=True, key="rev_preset_defensive"):
                st.session_state["rev_whatif_churn"] = whatif_presets["Defensive"]["churn"]
                st.session_state["rev_whatif_price"] = whatif_presets["Defensive"]["price"]
                st.session_state["rev_whatif_collection"] = whatif_presets["Defensive"]["collection"]
                st.session_state["rev_whatif_discount"] = whatif_presets["Defensive"]["discount"]
        with preset_col2:
            if st.button("⚖️ Base", use_container_width=True, key="rev_preset_base"):
                st.session_state["rev_whatif_churn"] = whatif_presets["Base"]["churn"]
                st.session_state["rev_whatif_price"] = whatif_presets["Base"]["price"]
                st.session_state["rev_whatif_collection"] = whatif_presets["Base"]["collection"]
                st.session_state["rev_whatif_discount"] = whatif_presets["Base"]["discount"]
        with preset_col3:
            if st.button("🚀 Growth", use_container_width=True, key="rev_preset_growth"):
                st.session_state["rev_whatif_churn"] = whatif_presets["Growth"]["churn"]
                st.session_state["rev_whatif_price"] = whatif_presets["Growth"]["price"]
                st.session_state["rev_whatif_collection"] = whatif_presets["Growth"]["collection"]
                st.session_state["rev_whatif_discount"] = whatif_presets["Growth"]["discount"]
        with preset_col4:
            if st.button("🏆 Stretch", use_container_width=True, key="rev_preset_stretch"):
                st.session_state["rev_whatif_churn"] = whatif_presets["Stretch"]["churn"]
                st.session_state["rev_whatif_price"] = whatif_presets["Stretch"]["price"]
                st.session_state["rev_whatif_collection"] = whatif_presets["Stretch"]["collection"]
                st.session_state["rev_whatif_discount"] = whatif_presets["Stretch"]["discount"]

        ctrl_col1, ctrl_col2, ctrl_col3, ctrl_col4 = st.columns(4)
        with ctrl_col1:
            churn_shock_pp = st.slider("Churn Shock (pp)", -1.0, 2.0, step=0.1, key="rev_whatif_churn")
        with ctrl_col2:
            price_uplift_pct = st.slider("Price Uplift (%)", -3.0, 5.0, step=0.1, key="rev_whatif_price")
        with ctrl_col3:
            collection_improve_pp = st.slider("Collection Delta (pp)", -1.0, 2.0, step=0.1, key="rev_whatif_collection")
        with ctrl_col4:
            discount_change_pp = st.slider("Discount Pressure (pp)", -2.0, 3.0, step=0.1, key="rev_whatif_discount")

        base_q_whatif = float(rev_scenario.loc[rev_scenario["Scenario"] == "Base", "Quarter Revenue M"].iloc[0])
        churn_impact_m = -base_q_whatif * (churn_shock_pp * 0.012)
        price_impact_m = base_q_whatif * (price_uplift_pct / 100) * 0.85
        collection_impact_m = base_q_whatif * (collection_improve_pp / 100) * 0.35
        discount_impact_m = -base_q_whatif * (discount_change_pp / 100) * 0.75
        scenario_q_m = base_q_whatif + churn_impact_m + price_impact_m + collection_impact_m + discount_impact_m
        delta_q_m = scenario_q_m - base_q_whatif

        scenario_margin = gross_margin + (0.6 * price_uplift_pct) - (0.8 * discount_change_pp) - (0.5 * churn_shock_pp) + (0.2 * collection_improve_pp)
        scenario_margin = max(35.0, min(65.0, scenario_margin))

        st.markdown(dedent(f"""
            <div class="rev-kpi-grid">
                <div class="rev-kpi-card"><div class="k">Base Quarter</div><div class="v">€{base_q_whatif:.2f}M</div><div class="d">Reference case</div></div>
                <div class="rev-kpi-card {'crit' if delta_q_m < 0 else ''}"><div class="k">What-If Quarter</div><div class="v">€{scenario_q_m:.2f}M</div><div class="d">{delta_q_m:+.2f}M vs base</div></div>
                <div class="rev-kpi-card {'warn' if scenario_margin < gross_margin else ''}"><div class="k">What-If Margin</div><div class="v">{scenario_margin:.1f}%</div><div class="d">{(scenario_margin-gross_margin):+.1f}pp vs current</div></div>
                <div class="rev-kpi-card {'crit' if delta_q_m < -0.3 else 'warn' if delta_q_m < 0 else ''}"><div class="k">Scenario Health</div><div class="v">{'At Risk' if delta_q_m < -0.3 else 'Watch' if delta_q_m < 0 else 'Favorable'}</div><div class="d">Composite result</div></div>
            </div>
        """), unsafe_allow_html=True)

        wf_col1, wf_col2 = st.columns(2)
        with wf_col1:
            st.markdown('<div class="rev-mini-title">Driver Impact Decomposition</div>', unsafe_allow_html=True)
            with st.container(border=True):
                driver_df = pd.DataFrame({
                    "Driver": ["Churn", "Pricing", "Collections", "Discounts"],
                    "Impact M": [churn_impact_m, price_impact_m, collection_impact_m, discount_impact_m],
                })
                driver_df["Type"] = driver_df["Impact M"].apply(lambda v: "Up" if v >= 0 else "Down")
                d_bar = alt.Chart(driver_df).mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6, size=46).encode(
                    x=alt.X("Driver:N", title=None),
                    y=alt.Y("Impact M:Q", title="Impact (€ M)"),
                    color=alt.Color("Type:N", scale=alt.Scale(domain=["Up", "Down"], range=["#10B981", "#EF4444"]), legend=None),
                    tooltip=["Driver:N", alt.Tooltip("Impact M:Q", format=".2f")],
                )
                d_text = alt.Chart(driver_df).mark_text(dy=-8, fontSize=10, fontWeight="bold", color="#0F172A").encode(
                    x="Driver:N",
                    y="Impact M:Q",
                    text=alt.Text("Impact M:Q", format="+.2f"),
                )
                d_zero = alt.Chart(pd.DataFrame({"y": [0]})).mark_rule(color="#94A3B8", strokeDash=[4, 4]).encode(y="y:Q")
                st.altair_chart(style_rev_chart(d_zero + d_bar + d_text, height=220), use_container_width=True)

        with wf_col2:
            st.markdown('<div class="rev-mini-title">Base vs What-If Outcome</div>', unsafe_allow_html=True)
            with st.container(border=True):
                compare_df = pd.DataFrame({
                    "Case": ["Base", "What-If"],
                    "Revenue M": [base_q_whatif, scenario_q_m],
                })
                c_bar = alt.Chart(compare_df).mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6, size=58).encode(
                    x=alt.X("Case:N", title=None),
                    y=alt.Y("Revenue M:Q", title="Quarter Revenue (€ M)"),
                    color=alt.Color("Case:N", scale=alt.Scale(domain=["Base", "What-If"], range=["#3B82F6", "#10B981" if delta_q_m >= 0 else "#EF4444"]), legend=None),
                    tooltip=["Case:N", alt.Tooltip("Revenue M:Q", format=".2f")],
                )
                c_text = alt.Chart(compare_df).mark_text(dy=-8, fontSize=11, fontWeight="bold", color="#0F172A").encode(
                    x="Case:N",
                    y="Revenue M:Q",
                    text=alt.Text("Revenue M:Q", format=".2f"),
                )
                st.altair_chart(style_rev_chart(c_bar + c_text, height=220), use_container_width=True)

        if delta_q_m >= 0:
            render_rev_ai_reco(
                "What-If Outcome",
                f"This scenario improves quarter revenue by €{delta_q_m:.2f}M with margin at {scenario_margin:.1f}%.",
                "Proceed with pricing and collections levers; keep discount expansion controlled.",
                "Higher quarter close with stable profitability.",
            )
        else:
            render_rev_ai_reco(
                "What-If Outcome",
                f"This scenario reduces quarter revenue by €{abs(delta_q_m):.2f}M and margin shifts to {scenario_margin:.1f}%.",
                "Trigger mitigation playbook: protect collections, limit discounting, and prioritize churn containment.",
                "Contain downside and recover part of the revenue gap before close.",
                level="critical" if delta_q_m < -0.3 else "warning",
            )

        st.markdown(dedent(f"""
            <div style="background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%); border-radius: 10px; padding: 0.82rem 0.95rem; margin-top: 0.55rem; border-left: 4px solid #F59E0B;">
                <div style="display: flex; align-items: center;">
                    <span style="font-size: 1.35rem; margin-right: 0.55rem;">⚠️</span>
                    <div>
                        <strong style="color: #92400E;">Urgent: €{at_risk_rev_m:.2f}M revenue exposure</strong>
                        <div style="color: #B45309; font-size: 0.84rem;">Top driver: {rev_risk.loc[rev_risk['Exposure M'].idxmax(), 'Risk Driver']} · prioritize mitigation in next cycle</div>
                    </div>
                </div>
            </div>
        """), unsafe_allow_html=True)

elif selected_menu == "Network Status":
    import pandas as pd
    import altair as alt
    import pydeck as pdk
    import math
    import random
    import time

    NET_CHART_THEME = {
        "bg": "#F8FAFF",
        "title": "#1E3A8A",
        "axis": "#334155",
        "grid": "#E2E8F0",
        "font": "Inter",
    }

    def style_net_chart(chart: alt.Chart, height: int = 220) -> alt.Chart:
        return (
            chart.properties(height=height, padding={"left": 10, "right": 10, "top": 8, "bottom": 4})
            .configure(background=NET_CHART_THEME["bg"])
            .configure_view(stroke=None, cornerRadius=10)
            .configure_title(color=NET_CHART_THEME["title"], fontSize=13, font=NET_CHART_THEME["font"], anchor="start")
            .configure_axis(
                labelColor=NET_CHART_THEME["axis"],
                titleColor=NET_CHART_THEME["axis"],
                gridColor=NET_CHART_THEME["grid"],
                labelFont=NET_CHART_THEME["font"],
                titleFont=NET_CHART_THEME["font"],
            )
            .configure_legend(
                labelColor=NET_CHART_THEME["axis"],
                titleColor=NET_CHART_THEME["axis"],
                labelFont=NET_CHART_THEME["font"],
                titleFont=NET_CHART_THEME["font"],
            )
        )

    def render_net_ai_reco(headline: str, insight: str, action: str, impact: str, level: str = "info") -> None:
        level_class = "crit" if level == "critical" else "warn" if level == "warning" else ""
        icon = "🚨" if level == "critical" else "⚠️" if level == "warning" else "🤖"
        st.markdown(dedent(f"""
            <div class="net-ai-card {level_class}">
                <div class="h">{icon} {headline}</div>
                <div class="b"><strong>Insight:</strong> {insight}</div>
                <div class="b"><strong>Action:</strong> {action}</div>
                <div class="b"><strong>Expected Impact:</strong> {impact}</div>
            </div>
        """), unsafe_allow_html=True)

    st.markdown(dedent("""
        <style>
            @keyframes net-fade-up {
                from { opacity: 0; transform: translateY(8px); }
                to { opacity: 1; transform: translateY(0); }
            }
            @keyframes net-pulse-glow {
                0%, 100% { box-shadow: 0 0 0 0 rgba(37, 99, 235, 0.12); }
                50% { box-shadow: 0 0 0 8px rgba(37, 99, 235, 0.03); }
            }
            .net-title {
                font-size: 1.08rem;
                font-weight: 800;
                color: #1E3A8A;
                letter-spacing: 0.01em;
                margin: 0.3rem 0 0.6rem 0;
                animation: net-fade-up 0.45s ease-out both;
            }
            .net-mini-title {
                font-size: 0.92rem;
                font-weight: 700;
                color: #334155;
                margin: 0.12rem 0 0.5rem 0;
                animation: net-fade-up 0.45s ease-out both;
            }
            .net-pulse {
                border-radius: 12px;
                border: 1px solid #DBEAFE;
                background: linear-gradient(135deg, #EFF6FF 0%, #E0F2FE 100%);
                padding: 0.8rem 0.95rem;
                margin-bottom: 0.65rem;
                animation: net-fade-up 0.45s ease-out both, net-pulse-glow 2.8s ease-in-out infinite;
            }
            .net-pulse-grid, .net-kpi-grid {
                display: grid;
                grid-template-columns: repeat(4, minmax(0, 1fr));
                gap: 0.48rem;
            }
            .net-pulse-card, .net-kpi-card {
                border-radius: 10px;
                background: rgba(255, 255, 255, 0.88);
                border: 1px solid #E2E8F0;
                padding: 0.52rem 0.62rem;
            }
            .net-pulse-card .k, .net-kpi-card .k {
                font-size: 0.69rem;
                color: #64748B;
                text-transform: uppercase;
                letter-spacing: 0.03em;
                font-weight: 700;
            }
            .net-pulse-card .v, .net-kpi-card .v {
                font-size: 1.04rem;
                color: #0F172A;
                font-weight: 800;
                line-height: 1.1;
                margin-top: 0.08rem;
            }
            .net-pulse-card .d, .net-kpi-card .d {
                font-size: 0.74rem;
                color: #475569;
                margin-top: 0.12rem;
            }
            .net-kpi-card.warn { border-left: 4px solid #F59E0B; }
            .net-kpi-card.crit { border-left: 4px solid #EF4444; }
            .net-ai-card {
                border-radius: 10px;
                border-left: 4px solid #3B82F6;
                background: #EFF6FF;
                padding: 0.62rem 0.72rem;
                margin-top: 0.46rem;
                animation: net-fade-up 0.42s ease-out both;
            }
            .net-ai-card.warn { border-left-color: #F59E0B; background: #FFFBEB; }
            .net-ai-card.crit { border-left-color: #EF4444; background: #FEF2F2; }
            .net-ai-card .h {
                font-size: 0.83rem;
                font-weight: 800;
                color: #1E293B;
                margin-bottom: 0.28rem;
            }
            .net-ai-card .b {
                font-size: 0.78rem;
                color: #334155;
                line-height: 1.42;
            }
            @media (max-width: 1200px) {
                .net-pulse-grid, .net-kpi-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
            }
        </style>
    """), unsafe_allow_html=True)

    net_hourly = pd.DataFrame({
        "Hour": ["00:00", "04:00", "08:00", "12:00", "16:00", "20:00"],
        "Latency ms": [19, 21, 23, 27, 25, 22],
        "Utilization %": [54, 58, 69, 82, 76, 63],
        "Packet Loss %": [0.18, 0.21, 0.27, 0.36, 0.31, 0.24],
        "Availability %": [99.96, 99.95, 99.93, 99.88, 99.90, 99.94],
        "Incidents": [1, 1, 2, 4, 3, 2],
    })
    net_regions = pd.DataFrame({
        "Region": ["Madrid Centro", "Barcelona", "Valencia", "Málaga", "Bilbao", "Zaragoza"],
        "Availability %": [99.94, 99.91, 99.90, 99.86, 99.88, 99.84],
        "NPS": [57, 54, 53, 49, 50, 47],
        "Active OLTs": [82, 63, 58, 36, 34, 29],
        "MTTR Min": [44, 47, 48, 55, 52, 59],
    })
    net_incident_trend = pd.DataFrame({
        "Month": ["2025-09", "2025-10", "2025-11", "2025-12", "2026-01", "2026-02"],
        "Incidents": [62, 58, 55, 51, 49, 46],
        "MTTR Min": [56, 54, 52, 50, 48, 46],
    })
    net_queue = pd.DataFrame({
        "Queue": ["Core", "Access", "Field", "Transport", "CPE"],
        "Open Tickets": [22, 34, 31, 17, 28],
        "SLA Breach %": [7.5, 10.4, 9.8, 5.1, 8.9],
        "Avg Age Hr": [9.2, 12.1, 10.8, 7.4, 9.9],
    })
    net_risk = pd.DataFrame({
        "Risk Driver": ["Backbone Saturation", "Power Instability", "Fiber Cuts", "Vendor Delay", "Config Drift"],
        "Exposure Hr": [94, 71, 86, 49, 44],
        "Likelihood": [3.8, 3.1, 3.6, 2.9, 2.7],
    })
    net_scenario = pd.DataFrame({
        "Scenario": ["Downside", "Base", "Upside"],
        "Availability %": [99.80, 99.91, 99.96],
        "Avoided Churn K": [1.8, 2.4, 3.1],
        "Recovery Cost K": [102, 88, 76],
        "Probability": ["25%", "50%", "25%"],
    })
    net_map_nodes = pd.DataFrame({
        "Node": ["Madrid Centro", "Barcelona", "Valencia", "Málaga", "Bilbao", "Zaragoza", "Murcia", "Palma"],
        "lat": [40.4168, 41.3874, 39.4699, 36.7213, 43.2630, 41.6488, 37.9922, 39.5696],
        "lon": [-3.7038, 2.1686, -0.3763, -4.4214, -2.9350, -0.8891, -1.1307, 2.6502],
        "Availability %": [99.94, 99.91, 99.90, 99.86, 99.88, 99.84, 99.87, 99.89],
        "Utilization %": [72, 76, 74, 68, 66, 71, 67, 64],
        "Open Incidents": [5, 7, 6, 9, 8, 10, 7, 6],
        "Status": ["Healthy", "Watch", "Watch", "At Risk", "Watch", "At Risk", "Watch", "Healthy"],
    })
    net_incident_points = pd.DataFrame({
        "lat": [40.42, 40.40, 41.39, 39.47, 36.72, 36.70, 43.26, 43.28, 41.65, 41.63, 37.99, 39.57],
        "lon": [-3.70, -3.68, 2.17, -0.38, -4.42, -4.40, -2.94, -2.91, -0.89, -0.87, -1.13, 2.65],
        "weight": [4, 3, 3, 2, 5, 4, 3, 2, 5, 4, 3, 2],
        "Type": ["Fiber Cut", "Power", "Congestion", "Config", "Fiber Cut", "Power", "Congestion", "Config", "Fiber Cut", "Power", "Congestion", "Config"],
    })
    # Expand sparse map points into realistic synthetic clusters for richer visuals.
    rng = random.Random(17)
    net_node_density_records = []
    node_offsets = [(0.00, 0.00), (0.06, 0.02), (-0.05, 0.03), (0.03, -0.05), (-0.04, -0.04), (0.07, -0.01), (-0.07, 0.00)]
    for _, row in net_map_nodes.iterrows():
        cluster_size = min(13, 4 + int(row["Open Incidents"]))
        base_color = {
            "Healthy": (16, 185, 129),
            "Watch": (245, 158, 11),
            "At Risk": (239, 68, 68),
        }[row["Status"]]
        for i in range(cluster_size):
            off_lon, off_lat = node_offsets[i % len(node_offsets)]
            scale = 0.35 + 0.08 * (i // len(node_offsets))
            net_node_density_records.append({
                "Node": row["Node"],
                "Status": row["Status"],
                "lat": row["lat"] + off_lat * scale + rng.uniform(-0.004, 0.004),
                "lon": row["lon"] + off_lon * scale + rng.uniform(-0.004, 0.004),
                "r": base_color[0],
                "g": base_color[1],
                "b": base_color[2],
                "radius": 2000 + (220 * i),
            })
    net_node_density = pd.DataFrame(net_node_density_records)

    net_incident_density_records = []
    incident_offsets = [(0.00, 0.00), (0.04, 0.02), (-0.04, 0.02), (0.03, -0.03), (-0.03, -0.03), (0.06, -0.01), (-0.06, -0.01), (0.00, 0.05)]
    for _, row in net_incident_points.iterrows():
        cluster_size = int(row["weight"] * 3)
        for i in range(cluster_size):
            off_lon, off_lat = incident_offsets[i % len(incident_offsets)]
            scale = 0.28 + 0.08 * (i // len(incident_offsets))
            net_incident_density_records.append({
                "Type": row["Type"],
                "lat": row["lat"] + off_lat * scale + rng.uniform(-0.003, 0.003),
                "lon": row["lon"] + off_lon * scale + rng.uniform(-0.003, 0.003),
                "weight": max(1.0, row["weight"] - 0.15 * (i % 3)),
            })
    net_incident_density = pd.DataFrame(net_incident_density_records)
    net_access_points_records = []
    for _, row in net_map_nodes.iterrows():
        site_count = 24 + int(row["Utilization %"] / 4)
        for _ in range(site_count):
            theta = rng.uniform(0, 2 * math.pi)
            radius = rng.uniform(0.008, 0.11)
            lat = row["lat"] + radius * math.sin(theta)
            lon = row["lon"] + radius * math.cos(theta) * 0.92
            traffic = max(22.0, min(95.0, row["Utilization %"] + rng.uniform(-20, 16)))
            net_access_points_records.append({
                "Node": row["Node"],
                "lat": lat,
                "lon": lon,
                "Traffic": traffic,
            })
    net_access_points = pd.DataFrame(net_access_points_records)
    net_access_points["r"] = net_access_points["Traffic"].apply(lambda v: 239 if v >= 82 else 245 if v >= 66 else 37)
    net_access_points["g"] = net_access_points["Traffic"].apply(lambda v: 68 if v >= 82 else 158 if v >= 66 else 99)
    net_access_points["b"] = net_access_points["Traffic"].apply(lambda v: 68 if v >= 82 else 11 if v >= 66 else 235)
    net_access_points["radius"] = net_access_points["Traffic"].apply(lambda v: 500 if v >= 82 else 420 if v >= 66 else 360)
    net_access_points["Tier"] = net_access_points["Traffic"].apply(lambda v: "Critical" if v >= 82 else "Watch" if v >= 66 else "Stable")
    node_sites = net_access_points.groupby("Node", as_index=False).size().rename(columns={"size": "Access Sites"})
    net_node_labels = net_map_nodes.merge(node_sites, on="Node", how="left")
    net_node_labels["Label"] = net_node_labels["Node"] + " • " + net_node_labels["Access Sites"].astype(int).astype(str) + " sites"
    net_fiber_paths = pd.DataFrame({
        "from_lon": [-3.70, -3.70, -3.70, -3.70, -2.94],
        "from_lat": [40.42, 40.42, 40.42, 40.42, 43.26],
        "to_lon": [-2.94, -4.42, -0.89, 2.65, -1.13],
        "to_lat": [43.26, 36.72, 41.65, 39.57, 37.99],
        "Cuts": [7, 9, 8, 6, 5],
    })
    net_backbone_flows = pd.DataFrame({
        "source_lon": [-3.70, -3.70, -3.70, -3.70, -3.70],
        "source_lat": [40.42, 40.42, 40.42, 40.42, 40.42],
        "target_lon": [-2.94, -4.42, -0.89, -1.13, 2.65],
        "target_lat": [43.26, 36.72, 41.65, 37.99, 39.57],
        "Utilization %": [77, 71, 83, 68, 64],
    })
    net_sla_geo = pd.DataFrame({
        "City": ["Madrid", "Bilbao", "Málaga", "Zaragoza", "Murcia", "Palma"],
        "lat": [40.4168, 43.2630, 36.7213, 41.6488, 37.9922, 39.5696],
        "lon": [-3.7038, -2.9350, -4.4214, -0.8891, -1.1307, 2.6502],
        "SLA Risk": [31, 38, 43, 48, 36, 34],
    })
    net_opportunity_geo = pd.DataFrame({
        "Zone": ["Madrid Este", "Barcelona", "Valencia", "Bilbao Sur", "Zaragoza Norte", "Málaga Norte", "Murcia Centro", "Palma Valle"],
        "lat": [40.44, 41.40, 39.48, 43.24, 41.67, 36.74, 37.98, 39.55],
        "lon": [-3.65, 2.18, -0.36, -2.96, -0.87, -4.40, -1.12, 2.63],
        "Demand Index": [84, 73, 70, 68, 75, 66, 64, 62],
        "Coverage Gap %": [18, 14, 12, 16, 19, 13, 11, 10],
        "ARR Risk M": [1.40, 1.05, 0.92, 0.86, 1.22, 0.79, 0.67, 0.58],
        "Capex M": [1.10, 0.84, 0.78, 0.73, 1.04, 0.70, 0.62, 0.56],
        "Payback Mo": [15, 13, 12, 14, 16, 12, 11, 10],
        "Priority Score": [88, 81, 77, 79, 86, 74, 72, 70],
    })
    net_major_cities_geo = pd.DataFrame({
        "City": [
            "Madrid", "Sevilla", "Málaga", "Bilbao", "Zaragoza", "Murcia", "Palma", "Valladolid",
            "Alicante", "Córdoba", "Vigo", "Gijón", "Granada", "Santander", "San Sebastián", "Pamplona",
            "Almería", "Badajoz", "León", "Tarragona", "Castellón", "Vitoria", "Logroño", "Oviedo",
        ],
        "lat": [
            40.4168, 37.3891, 36.7213, 43.2630, 41.6488, 37.9922, 39.5696, 41.6520,
            38.3452, 37.8882, 42.2406, 43.5322, 37.1773, 43.4623, 43.3183, 42.8125,
            36.8381, 38.8794, 42.5987, 41.1189, 39.9864, 42.8467, 42.4627, 43.3614,
        ],
        "lon": [
            -3.7038, -5.9845, -4.4214, -2.9350, -0.8891, -1.1307, 2.6502, -4.7286,
            -0.4810, -4.7794, -8.7207, -5.6611, -3.5986, -3.8100, -1.9812, -1.6458,
            -2.4637, -6.9706, -5.5671, 1.2445, -0.0376, -2.6726, -2.4449, -5.8593,
        ],
        "City Tier": [
            "Core Hub", "Core Hub", "Core Hub", "Core Hub", "Growth Node", "Growth Node", "Growth Node", "Growth Node",
            "Growth Node", "Growth Node", "Emerging Node", "Emerging Node", "Growth Node", "Emerging Node", "Emerging Node", "Emerging Node",
            "Emerging Node", "Emerging Node", "Emerging Node", "Growth Node", "Emerging Node", "Growth Node", "Growth Node", "Emerging Node",
        ],
        "Investment Signal": [97, 92, 90, 88, 86, 84, 83, 81, 80, 79, 77, 76, 82, 74, 73, 72, 71, 70, 69, 78, 68, 81, 85, 67],
    })
    net_major_cities_geo["r"] = net_major_cities_geo["City Tier"].apply(lambda v: 37 if v == "Core Hub" else 16 if v == "Growth Node" else 245)
    net_major_cities_geo["g"] = net_major_cities_geo["City Tier"].apply(lambda v: 99 if v == "Core Hub" else 185 if v == "Growth Node" else 158)
    net_major_cities_geo["b"] = net_major_cities_geo["City Tier"].apply(lambda v: 235 if v == "Core Hub" else 129 if v == "Growth Node" else 11)
    net_major_cities_geo["radius"] = net_major_cities_geo["City Tier"].apply(lambda v: 13500 if v == "Core Hub" else 11000 if v == "Growth Node" else 9500)
    net_infra_assets = pd.DataFrame({
        "Domain": ["Core", "Transport", "Access OLT", "Field Fiber", "CPE Edge"],
        "Sites": [18, 42, 302, 1120, 640],
        "Capacity Gbps": [520, 710, 910, 640, 480],
        "Utilization %": [68, 74, 79, 66, 61],
        "Redundancy %": [96, 92, 88, 81, 76],
        "Health Score": [91, 87, 83, 79, 82],
    })
    net_maintenance = pd.DataFrame({
        "Asset Type": ["Core Routers", "Transport Links", "OLT Shelves", "Fiber Junctions", "Power Units"],
        "Open Workorders": [16, 24, 38, 45, 29],
        "Critical %": [14, 17, 20, 23, 19],
        "Avg Delay Hr": [6.2, 7.4, 8.6, 9.1, 7.8],
    })
    net_upgrade_program = pd.DataFrame({
        "Initiative": ["PF Core Madrid Refresh", "PF Northern Backbone Ring", "PF OLT Densification Wave 2", "PF South Fiber Hardening", "PF Critical Site Power Backup"],
        "Domain": ["Core", "Transport", "Access OLT", "Field Fiber", "Power"],
        "Capex M": [1.6, 1.9, 1.3, 1.5, 1.1],
        "Impact Score": [89, 92, 84, 81, 78],
        "Delivery Risk": [2.4, 2.8, 2.1, 2.6, 2.2],
        "Quarter": ["Q1", "Q2", "Q2", "Q3", "Q1"],
    })
    net_spof = pd.DataFrame({
        "Region": ["Barcelona", "Valencia", "Málaga", "Bilbao", "Zaragoza"],
        "SPOF Count": [4, 3, 5, 4, 6],
        "Subscribers K": [52, 48, 35, 31, 29],
        "Criticality": [3.2, 2.9, 3.5, 3.1, 3.8],
    })
    net_resilience_sites = pd.DataFrame({
        "Region": ["Madrid Centro", "Barcelona", "Valencia", "Málaga", "Bilbao", "Zaragoza"],
        "Backup Autonomy Hr": [8.8, 7.6, 7.1, 6.2, 6.5, 5.8],
        "Power Events / Mo": [2.3, 2.8, 2.9, 3.6, 3.1, 3.8],
        "Critical Sites": [24, 19, 18, 12, 11, 10],
    })
    net_enterprise_geo = pd.DataFrame({
        "City": ["Madrid", "Sevilla", "Bilbao", "Zaragoza", "Málaga", "Palma", "Murcia", "Alicante"],
        "lat": [40.4168, 37.3891, 43.2630, 41.6488, 36.7213, 39.5696, 37.9922, 38.3452],
        "lon": [-3.7038, -5.9845, -2.9350, -0.8891, -4.4214, 2.6502, -1.1307, -0.4810],
        "Accounts": [190, 122, 74, 66, 59, 48, 44, 37],
        "Priority": ["Tier 1", "Tier 1", "Tier 2", "Tier 2", "Tier 2", "Tier 3", "Tier 3", "Tier 3"],
    })
    net_enterprise_geo["radius"] = (net_enterprise_geo["Accounts"] * 30).clip(lower=1200, upper=7200)
    net_weather_risk_geo = pd.DataFrame({
        "Zone": ["Barcelona", "Valencia", "Bilbao Norte", "Zaragoza Este", "Málaga Centro", "Palma Sur"],
        "lat": [41.40, 39.48, 43.28, 41.66, 36.73, 39.55],
        "lon": [2.18, -0.36, -2.91, -0.87, -4.40, 2.63],
        "Weather Risk": [72, 66, 78, 84, 63, 57],
    })
    net_weather_risk_geo["radius"] = net_weather_risk_geo["Weather Risk"] * 150
    net_build_corridors = pd.DataFrame({
        "from_lon": [-3.7038, -3.7038, -3.7038, -3.7038],
        "from_lat": [40.4168, 40.4168, 40.4168, 40.4168],
        "to_lon": [-2.9350, -0.8891, -4.4214, 2.6502],
        "to_lat": [43.2630, 41.6488, 36.7213, 39.5696],
        "Phase": ["Wave 1", "Wave 1", "Wave 2", "Wave 2"],
        "Capex M": [0.88, 1.04, 0.96, 0.74],
    })
    net_build_corridors["width"] = net_build_corridors["Phase"].map({"Wave 1": 4.8, "Wave 2": 3.6})
    net_service_impact = pd.DataFrame({
        "Incident Type": ["Fiber Cut", "Power", "Congestion", "Config Drift", "Vendor Fault"],
        "Subs Impacted K": [3.4, 2.6, 2.1, 1.2, 0.9],
        "ARR at Risk M": [0.38, 0.31, 0.24, 0.16, 0.11],
        "Enterprise Accounts": [12, 9, 7, 4, 3],
        "Avg Restore Hr": [3.8, 3.1, 2.5, 2.0, 2.4],
    })
    net_sla_command = pd.DataFrame({
        "Day": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        "SLA Actual %": [98.9, 99.1, 98.8, 99.0, 98.7, 99.2, 99.0],
        "SLA Forecast %": [98.9, 99.1, 98.8, 99.0, 98.7, 98.9, 98.8],
        "SLA Target %": [99.2, 99.2, 99.2, 99.2, 99.2, 99.2, 99.2],
    })
    net_change_monitor = pd.DataFrame({
        "Week": ["W1", "W2", "W3", "W4", "W5", "W6"],
        "Planned Changes": [26, 31, 28, 35, 33, 29],
        "Failed Changes": [2, 3, 2, 4, 3, 2],
        "Incidents": [11, 13, 12, 16, 14, 12],
    })
    net_capacity_forecast = pd.DataFrame({
        "Horizon": ["30d", "60d", "90d"] * 4,
        "Corridor": ["North Backbone"] * 3 + ["South Backbone"] * 3 + ["Metro Core"] * 3 + ["Regional Edge"] * 3,
        "Projected Util %": [74, 79, 84, 69, 73, 77, 81, 86, 91, 66, 70, 74],
    })
    net_critical_sites = pd.DataFrame({
        "Site": ["MAD-CORE-01", "ZGZ-EDGE-04", "MLG-TR-02", "BIO-ACC-05", "MAD-ACC-09", "PMI-TR-01", "MUR-ACC-03", "MAD-TR-07", "ZGZ-ACC-02", "MLG-ACC-06"],
        "Region": ["Madrid", "Zaragoza", "Málaga", "Bilbao", "Madrid", "Palma", "Murcia", "Madrid", "Zaragoza", "Málaga"],
        "Criticality": [94, 92, 90, 88, 87, 85, 84, 83, 82, 81],
        "Subscribers Impact K": [46, 38, 29, 27, 25, 22, 20, 19, 18, 17],
        "MTTR Min": [62, 68, 58, 56, 54, 52, 50, 49, 48, 47],
        "Owner": ["Core Ops", "Field Ops", "Transport", "Access", "Access", "Transport", "Access", "Transport", "Field Ops", "Access"],
    })
    net_mitigation_tracker = pd.DataFrame({
        "Initiative": ["Backbone Ring Redundancy", "Power Hardening North", "Fiber Route Diversification", "Config Guardrails", "Priority Queue Automation"],
        "Owner": ["Transport", "Field Ops", "Core Ops", "NOC", "Service Ops"],
        "ETA": ["Q2", "Q2", "Q3", "Q1", "Q1"],
        "Progress %": [58, 46, 34, 72, 64],
        "Risk Reduced %": [26, 18, 21, 14, 12],
        "Status": ["On Track", "Watch", "Watch", "On Track", "On Track"],
    })
    net_customer_link = pd.DataFrame({
        "Region": ["Madrid Centro", "Barcelona", "Valencia", "Málaga", "Bilbao", "Zaragoza"],
        "Latency ms": [20.5, 22.8, 23.2, 25.4, 24.7, 26.2],
        "Packet Loss %": [0.19, 0.24, 0.26, 0.31, 0.29, 0.34],
        "NPS": [57, 54, 53, 49, 50, 47],
        "Churn %": [2.2, 2.5, 2.6, 3.0, 2.9, 3.3],
    })
    net_outage_timeline = pd.DataFrame({
        "Hour": list(range(24)),
        "Incidents": [1, 1, 1, 1, 1, 2, 2, 3, 4, 4, 5, 6, 5, 5, 4, 4, 5, 6, 5, 4, 3, 2, 2, 1],
        "Subs Impacted K": [1, 1, 1, 1, 2, 2, 3, 4, 5, 6, 7, 8, 7, 7, 6, 6, 7, 8, 7, 6, 4, 3, 2, 1],
    })
    net_resilience_score = pd.DataFrame({
        "Month": ["2025-09", "2025-10", "2025-11", "2025-12", "2026-01", "2026-02"],
        "Core Score": [82, 84, 85, 86, 87, 88],
        "Access Score": [74, 75, 76, 78, 79, 80],
        "Field Score": [71, 72, 73, 74, 75, 77],
    })

    active_olts = int(net_regions["Active OLTs"].sum())
    avg_availability = net_hourly["Availability %"].mean()
    avg_latency = net_hourly["Latency ms"].mean()
    open_tickets = int(net_queue["Open Tickets"].sum())
    p95_utilization = net_hourly["Utilization %"].quantile(0.95)
    mttr_current = net_incident_trend.iloc[-1]["MTTR Min"]
    packet_loss_avg = net_hourly["Packet Loss %"].mean()
    breach_rate = net_queue["SLA Breach %"].mean()
    highest_risk = net_risk.loc[net_risk["Exposure Hr"].idxmax()]
    weakest_region = net_regions.loc[net_regions["Availability %"].idxmin()]
    infra_total_capacity = net_infra_assets["Capacity Gbps"].sum()
    infra_weighted_util = (net_infra_assets["Capacity Gbps"] * net_infra_assets["Utilization %"]).sum() / infra_total_capacity
    infra_health_avg = net_infra_assets["Health Score"].mean()
    infra_redundancy_avg = net_infra_assets["Redundancy %"].mean()

    st.markdown('<div class="net-title">Network Pulse</div>', unsafe_allow_html=True)
    st.markdown(dedent(f"""
        <div class="net-pulse">
            <div class="net-pulse-grid">
                <div class="net-pulse-card"><div class="k">Network Availability</div><div class="v">{avg_availability:.2f}%</div><div class="d">Last 24h blended uptime</div></div>
                <div class="net-pulse-card"><div class="k">Active OLTs</div><div class="v">{active_olts:,}</div><div class="d">Live access nodes</div></div>
                <div class="net-pulse-card"><div class="k">Avg Latency</div><div class="v">{avg_latency:.1f} ms</div><div class="d">Core-to-edge performance</div></div>
                <div class="net-pulse-card"><div class="k">Open Tickets</div><div class="v">{open_tickets}</div><div class="d">Operations workload</div></div>
                <div class="net-pulse-card"><div class="k">P95 Utilization</div><div class="v">{p95_utilization:.1f}%</div><div class="d">Capacity pressure</div></div>
                <div class="net-pulse-card"><div class="k">Current MTTR</div><div class="v">{mttr_current:.0f} min</div><div class="d">Incident recovery speed</div></div>
            </div>
        </div>
    """), unsafe_allow_html=True)

    net_tab_overview, net_tab_map, net_tab_ops, net_tab_impact, net_tab_exec, net_tab_risk, net_tab_aiml = st.tabs([
        "📈 Network Overview",
        "🗺️ Network Map",
        "🧭 Network Operations",
        "💼 Service Impact",
        "🧩 Execution & Playbooks",
        "⚠️ Risk & Strategy",
        "🤖 AI/ML Predictive",
    ])

    with net_tab_overview:
        st.markdown('<div class="net-title">Network Performance Overview</div>', unsafe_allow_html=True)
        st.markdown(dedent(f"""
            <div class="net-kpi-grid">
                <div class="net-kpi-card"><div class="k">Availability</div><div class="v">{avg_availability:.2f}%</div><div class="d">Service reliability baseline</div></div>
                <div class="net-kpi-card {'warn' if avg_latency > 24 else ''}"><div class="k">Average Latency</div><div class="v">{avg_latency:.1f} ms</div><div class="d">Customer experience proxy</div></div>
                <div class="net-kpi-card {'warn' if packet_loss_avg > 0.28 else ''}"><div class="k">Packet Loss</div><div class="v">{packet_loss_avg:.2f}%</div><div class="d">Quality consistency</div></div>
                <div class="net-kpi-card {'crit' if weakest_region['Availability %'] < 99.86 else 'warn'}"><div class="k">Lowest Region Uptime</div><div class="v">{weakest_region['Region']}</div><div class="d">{weakest_region['Availability %']:.2f}% availability</div></div>
            </div>
        """), unsafe_allow_html=True)

        ov_col1, ov_col2 = st.columns(2)
        with ov_col1:
            st.markdown('<div class="net-mini-title">Latency and Utilization by Hour</div>', unsafe_allow_html=True)
            with st.container(border=True):
                lat_line = alt.Chart(net_hourly).mark_line(point=True, strokeWidth=3, color="#2563EB").encode(
                    x=alt.X("Hour:N", title=None),
                    y=alt.Y("Latency ms:Q", title="Latency (ms)"),
                    tooltip=["Hour:N", alt.Tooltip("Latency ms:Q", format=".1f"), alt.Tooltip("Utilization %:Q", format=".1f"), alt.Tooltip("Incidents:Q", format=".0f")],
                )
                util_line = alt.Chart(net_hourly).mark_line(point=True, strokeWidth=3, color="#10B981").encode(
                    x=alt.X("Hour:N", title=None),
                    y=alt.Y("Utilization %:Q", title="Utilization (%)"),
                )
                st.altair_chart(style_net_chart(alt.layer(lat_line, util_line).resolve_scale(y="independent"), height=235), use_container_width=True)
                render_net_ai_reco(
                    "Load Pattern",
                    f"Peak utilization reaches {p95_utilization:.1f}% around demand-heavy windows, while latency expands in the same periods.",
                    "Apply dynamic traffic steering and pre-scale transport capacity before the midday peak.",
                    "Reduce congestion events and stabilize customer experience in peak windows.",
                )

        with ov_col2:
            st.markdown('<div class="net-mini-title">Regional Availability vs NPS</div>', unsafe_allow_html=True)
            with st.container(border=True):
                regional_scatter = alt.Chart(net_regions).mark_circle(opacity=0.85, stroke="#FFFFFF", strokeWidth=1.3).encode(
                    x=alt.X("Availability %:Q", title="Availability (%)"),
                    y=alt.Y("NPS:Q", title="NPS"),
                    size=alt.Size("Active OLTs:Q", scale=alt.Scale(range=[260, 1400]), legend=None),
                    color=alt.Color("MTTR Min:Q", scale=alt.Scale(scheme="orangered"), legend=alt.Legend(title="MTTR (min)")),
                    tooltip=["Region:N", alt.Tooltip("Availability %:Q", format=".2f"), alt.Tooltip("NPS:Q", format=".0f"), alt.Tooltip("MTTR Min:Q", format=".0f"), alt.Tooltip("Active OLTs:Q", format=",")],
                )
                region_label = alt.Chart(net_regions).mark_text(dy=-10, fontSize=9, color="#1E293B").encode(
                    x="Availability %:Q", y="NPS:Q", text="Region:N"
                )
                st.altair_chart(style_net_chart(regional_scatter + region_label, height=235), use_container_width=True)
                render_net_ai_reco(
                    "Regional Reliability",
                    f"{weakest_region['Region']} shows the weakest uptime at {weakest_region['Availability %']:.2f}% with visible NPS drag.",
                    f"Prioritize preventive maintenance and redundancy hardening in {weakest_region['Region']} corridors.",
                    "Lift regional service quality and protect customer sentiment in vulnerable zones.",
                    level="warning",
                )

        ov_col3, ov_col4 = st.columns(2)
        with ov_col3:
            st.markdown('<div class="net-mini-title">Packet Loss and Incident Pressure</div>', unsafe_allow_html=True)
            with st.container(border=True):
                loss_line = alt.Chart(net_hourly).mark_line(point=True, strokeWidth=3, color="#F59E0B").encode(
                    x=alt.X("Hour:N", title=None),
                    y=alt.Y("Packet Loss %:Q", title="Packet Loss (%)"),
                    tooltip=["Hour:N", alt.Tooltip("Packet Loss %:Q", format=".2f"), alt.Tooltip("Incidents:Q", format=".0f"), alt.Tooltip("Latency ms:Q", format=".1f")],
                )
                inc_bar_hourly = alt.Chart(net_hourly).mark_bar(cornerRadiusTopLeft=5, cornerRadiusTopRight=5, opacity=0.45, color="#EF4444", size=24).encode(
                    x=alt.X("Hour:N", title=None),
                    y=alt.Y("Incidents:Q", title="Incidents"),
                )
                st.altair_chart(style_net_chart(alt.layer(inc_bar_hourly, loss_line).resolve_scale(y="independent"), height=235), use_container_width=True)
                peak_loss_hour = net_hourly.loc[net_hourly["Packet Loss %"].idxmax()]
                render_net_ai_reco(
                    "Quality Degradation Window",
                    f"Highest packet loss appears at {peak_loss_hour['Hour']} ({peak_loss_hour['Packet Loss %']:.2f}%) alongside elevated incident pressure.",
                    "Pre-stage troubleshooting teams during this window and trigger proactive congestion balancing.",
                    "Reduce visible quality dips and prevent avoidable complaint spikes.",
                    level="warning",
                )

        with ov_col4:
            st.markdown('<div class="net-mini-title">Regional Resilience Index</div>', unsafe_allow_html=True)
            with st.container(border=True):
                resilience_df = net_regions.copy()
                resilience_df["Resilience Index"] = (
                    (resilience_df["Availability %"] - 99.70) * 320
                    + (60 - resilience_df["MTTR Min"]) * 0.9
                    + (resilience_df["NPS"] - 45) * 0.8
                ).clip(lower=45, upper=98)
                res_bar = alt.Chart(resilience_df).mark_bar(cornerRadiusTopRight=7, cornerRadiusBottomRight=7, size=20).encode(
                    x=alt.X("Resilience Index:Q", title="Resilience Index"),
                    y=alt.Y("Region:N", sort="-x", title=None),
                    color=alt.Color("Resilience Index:Q", scale=alt.Scale(scheme="blues"), legend=None),
                    tooltip=["Region:N", alt.Tooltip("Resilience Index:Q", format=".1f"), alt.Tooltip("Availability %:Q", format=".2f"), alt.Tooltip("MTTR Min:Q", format=".0f"), alt.Tooltip("NPS:Q", format=".0f")],
                )
                res_text = alt.Chart(resilience_df).mark_text(align="left", dx=6, fontSize=10, color="#0F172A").encode(
                    x="Resilience Index:Q",
                    y=alt.Y("Region:N", sort="-x"),
                    text=alt.Text("Resilience Index:Q", format=".1f"),
                )
                st.altair_chart(style_net_chart(res_bar + res_text, height=235), use_container_width=True)
                weakest_res = resilience_df.loc[resilience_df["Resilience Index"].idxmin()]
                render_net_ai_reco(
                    "Resilience Benchmark",
                    f"{weakest_res['Region']} has the lowest resilience score at {weakest_res['Resilience Index']:.1f}.",
                    f"Bundle reliability and recovery initiatives in {weakest_res['Region']} under a single recovery OKR.",
                    "Lift structural reliability and narrow regional performance dispersion.",
                    level="warning",
                )

        st.markdown('<div class="net-title">Infrastructure Footprint and Capacity</div>', unsafe_allow_html=True)
        st.markdown(dedent(f"""
            <div class="net-kpi-grid">
                <div class="net-kpi-card"><div class="k">Total Network Capacity</div><div class="v">{infra_total_capacity:,.0f} Gbps</div><div class="d">Across core, transport, access, edge</div></div>
                <div class="net-kpi-card {'warn' if infra_weighted_util > 75 else ''}"><div class="k">Weighted Utilization</div><div class="v">{infra_weighted_util:.1f}%</div><div class="d">Capacity load profile</div></div>
                <div class="net-kpi-card {'warn' if infra_redundancy_avg < 85 else ''}"><div class="k">Average Redundancy</div><div class="v">{infra_redundancy_avg:.1f}%</div><div class="d">Failover preparedness</div></div>
                <div class="net-kpi-card {'warn' if infra_health_avg < 84 else ''}"><div class="k">Infrastructure Health</div><div class="v">{infra_health_avg:.1f}</div><div class="d">Asset quality score</div></div>
            </div>
        """), unsafe_allow_html=True)

        inf_col1, inf_col2 = st.columns(2)
        with inf_col1:
            st.markdown('<div class="net-mini-title">Capacity and Utilization by Domain</div>', unsafe_allow_html=True)
            with st.container(border=True):
                infra_cap = net_infra_assets.copy()
                infra_cap["Used Gbps"] = (infra_cap["Capacity Gbps"] * infra_cap["Utilization %"] / 100).round(1)
                cap_bar = alt.Chart(infra_cap).mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6, size=32, color="#60A5FA").encode(
                    x=alt.X("Domain:N", title=None),
                    y=alt.Y("Capacity Gbps:Q", title="Capacity (Gbps)"),
                    tooltip=["Domain:N", alt.Tooltip("Capacity Gbps:Q", format=".0f"), alt.Tooltip("Used Gbps:Q", format=".1f"), alt.Tooltip("Utilization %:Q", format=".1f")],
                )
                used_line = alt.Chart(infra_cap).mark_line(point=True, strokeWidth=3, color="#F59E0B").encode(
                    x="Domain:N",
                    y=alt.Y("Used Gbps:Q", title="Used (Gbps)"),
                )
                st.altair_chart(style_net_chart(alt.layer(cap_bar, used_line).resolve_scale(y="independent"), height=235), use_container_width=True)
                hottest_domain = infra_cap.loc[infra_cap["Utilization %"].idxmax()]
                render_net_ai_reco(
                    "Capacity Load Balance",
                    f"{hottest_domain['Domain']} is the hottest domain at {hottest_domain['Utilization %']:.1f}% utilization.",
                    f"Prioritize near-term capacity augmentation in {hottest_domain['Domain']} to avoid saturation spillover.",
                    "Preserves headroom for growth and reduces performance degradation risk.",
                    level="warning",
                )

        with inf_col2:
            st.markdown('<div class="net-mini-title">Asset Health vs Redundancy</div>', unsafe_allow_html=True)
            with st.container(border=True):
                infra_health = alt.Chart(net_infra_assets).mark_circle(opacity=0.88, stroke="#FFFFFF", strokeWidth=1.2).encode(
                    x=alt.X("Redundancy %:Q", title="Redundancy (%)"),
                    y=alt.Y("Health Score:Q", title="Health Score"),
                    size=alt.Size("Sites:Q", scale=alt.Scale(range=[280, 1400]), legend=None),
                    color=alt.Color("Domain:N", legend=alt.Legend(title=None), scale=alt.Scale(range=["#3B82F6", "#10B981", "#F59E0B", "#EF4444", "#6366F1"])),
                    tooltip=["Domain:N", alt.Tooltip("Sites:Q", format=","), alt.Tooltip("Redundancy %:Q", format=".1f"), alt.Tooltip("Health Score:Q", format=".1f")],
                )
                infra_label = alt.Chart(net_infra_assets).mark_text(dy=-10, fontSize=9, color="#1E293B").encode(
                    x="Redundancy %:Q", y="Health Score:Q", text="Domain:N"
                )
                st.altair_chart(style_net_chart(infra_health + infra_label, height=235), use_container_width=True)
                weakest_domain = net_infra_assets.sort_values(["Health Score", "Redundancy %"]).iloc[0]
                render_net_ai_reco(
                    "Infrastructure Quality Focus",
                    f"{weakest_domain['Domain']} is the lowest combined health/redundancy domain.",
                    f"Bundle lifecycle refresh and failover reinforcement in {weakest_domain['Domain']}.",
                    "Improves resilience and lowers restoration pressure during faults.",
                    level="warning",
                )

    with net_tab_map:
        st.markdown('<div class="net-title">Network Map Status</div>', unsafe_allow_html=True)
        st.markdown(dedent(f"""
            <div class="net-kpi-grid">
                <div class="net-kpi-card"><div class="k">Mapped Nodes</div><div class="v">{len(net_map_nodes)}</div><div class="d">Cities with telemetry</div></div>
                <div class="net-kpi-card {'warn' if (net_map_nodes['Status'] == 'Watch').sum() > 2 else ''}"><div class="k">Watch Nodes</div><div class="v">{(net_map_nodes['Status'] == 'Watch').sum()}</div><div class="d">Needs preventive action</div></div>
                <div class="net-kpi-card {'crit' if (net_map_nodes['Status'] == 'At Risk').sum() > 1 else 'warn'}"><div class="k">At-Risk Nodes</div><div class="v">{(net_map_nodes['Status'] == 'At Risk').sum()}</div><div class="d">Immediate mitigation</div></div>
                <div class="net-kpi-card"><div class="k">Incident Hotspots</div><div class="v">{net_incident_points['weight'].gt(3).sum()}</div><div class="d">High-intensity clusters</div></div>
            </div>
        """), unsafe_allow_html=True)

        st.markdown('<div class="net-mini-title">Map Enhancers</div>', unsafe_allow_html=True)
        enh_col1, enh_col2, enh_col3, enh_col4 = st.columns([1.25, 1.25, 1.25, 1.4])
        with enh_col1:
            enh_demand = st.checkbox("Demand Footprint", value=True, key="net_map_enh_demand")
            enh_enterprise = st.checkbox("Enterprise Sites", value=True, key="net_map_enh_enterprise")
        with enh_col2:
            enh_weather = st.checkbox("Weather Risk", value=True, key="net_map_enh_weather")
            enh_build = st.checkbox("Planned Build Corridors", value=True, key="net_map_enh_build")
        with enh_col3:
            enh_labels = st.checkbox("Node Labels", value=True, key="net_map_enh_labels")
            enh_hotspots = st.checkbox("Dense Hotspots", value=True, key="net_map_enh_hotspots")
        with enh_col4:
            lens = st.selectbox(
                "Geography Lens",
                ["National Spain", "Madrid Metro", "Northern Corridor", "Southern Corridor"],
                index=0,
                key="net_map_geo_lens",
            )

        lens_view = {
            "National Spain": {"lat": 40.0, "lon": -3.7, "zoom": 5.35, "pitch": 33},
            "Madrid Metro": {"lat": 40.42, "lon": -3.70, "zoom": 9.2, "pitch": 38},
            "Northern Corridor": {"lat": 43.0, "lon": -2.0, "zoom": 6.25, "pitch": 34},
            "Southern Corridor": {"lat": 37.5, "lon": -3.5, "zoom": 5.95, "pitch": 34},
        }[lens]

        st.markdown(dedent("""
            <div style="display:flex; flex-wrap:wrap; gap:0.4rem; margin:0.2rem 0 0.55rem 0;">
                <span style="background:#FEF3C7; border:1px solid #FCD34D; color:#92400E; border-radius:999px; padding:0.2rem 0.55rem; font-size:0.74rem; font-weight:700;">Watch Pulse (Yellow)</span>
                <span style="background:#FEE2E2; border:1px solid #FCA5A5; color:#991B1B; border-radius:999px; padding:0.2rem 0.55rem; font-size:0.74rem; font-weight:700;">Critical Pulse (Red)</span>
                <span style="background:#DBEAFE; border:1px solid #93C5FD; color:#1E3A8A; border-radius:999px; padding:0.2rem 0.55rem; font-size:0.74rem; font-weight:700;">Enterprise Footprint (Blue)</span>
                <span style="background:#ECFDF5; border:1px solid #6EE7B7; color:#065F46; border-radius:999px; padding:0.2rem 0.55rem; font-size:0.74rem; font-weight:700;">Planned Build Corridors (Blue-Green)</span>
                <span style="background:#FFF7ED; border:1px solid #FDBA74; color:#9A3412; border-radius:999px; padding:0.2rem 0.55rem; font-size:0.74rem; font-weight:700;">Weather Risk (Orange-Red Heat)</span>
            </div>
        """), unsafe_allow_html=True)

        map_col1, map_col2 = st.columns(2)
        with map_col1:
            st.markdown('<div class="net-mini-title">Live Node Health Map</div>', unsafe_allow_html=True)
            with st.container(border=True):
                pulse_factor = 1.0 + (0.25 * (0.5 + 0.5 * math.sin(time.time() * 2.4)))
                pulse_wave = 0.5 + 0.5 * math.sin(time.time() * 3.2)
                node_df = net_map_nodes.copy()
                node_df["radius"] = node_df["Open Incidents"] * 650
                node_df["pulse_radius"] = node_df["radius"] * pulse_factor
                node_df["r"] = node_df["Status"].map({"Healthy": 16, "Watch": 245, "At Risk": 239})
                node_df["g"] = node_df["Status"].map({"Healthy": 185, "Watch": 158, "At Risk": 68})
                node_df["b"] = node_df["Status"].map({"Healthy": 129, "Watch": 11, "At Risk": 68})
                watch_points = net_access_points[net_access_points["Tier"] == "Watch"].copy()
                critical_points = net_access_points[net_access_points["Tier"] == "Critical"].copy()
                watch_points["pulse_radius"] = watch_points["radius"] * (2.6 + 0.7 * pulse_wave)
                critical_points["pulse_radius"] = critical_points["radius"] * (3.0 + 0.9 * pulse_wave)
                watch_alpha = int(32 + 38 * pulse_wave)
                crit_alpha = int(44 + 54 * pulse_wave)

                base_layer = pdk.Layer(
                    "ScatterplotLayer",
                    data=node_df,
                    get_position="[lon, lat]",
                    get_radius="radius",
                    get_fill_color="[r, g, b, 190]",
                    pickable=True,
                )
                pulse_layer = pdk.Layer(
                    "ScatterplotLayer",
                    data=node_df,
                    get_position="[lon, lat]",
                    get_radius="pulse_radius",
                    get_fill_color="[r, g, b, 70]",
                    stroked=True,
                    get_line_color="[r, g, b, 140]",
                    line_width_min_pixels=1,
                    pickable=False,
                )
                density_layer = pdk.Layer(
                    "ScatterplotLayer",
                    data=net_node_density,
                    get_position="[lon, lat]",
                    get_radius="radius",
                    get_fill_color="[r, g, b, 85]",
                    pickable=False,
                )
                access_heat_layer = pdk.Layer(
                    "HeatmapLayer",
                    data=net_access_points,
                    get_position="[lon, lat]",
                    get_weight="Traffic",
                    radiusPixels=45,
                    intensity=1.05,
                    threshold=0.03,
                    pickable=False,
                )
                access_sites_layer = pdk.Layer(
                    "ScatterplotLayer",
                    data=net_access_points,
                    get_position="[lon, lat]",
                    get_radius="radius",
                    get_fill_color="[r, g, b, 80]",
                    pickable=False,
                )
                watch_pulse_layer = pdk.Layer(
                    "ScatterplotLayer",
                    data=watch_points,
                    get_position="[lon, lat]",
                    get_radius="pulse_radius",
                    get_fill_color=[245, 158, 11, watch_alpha],
                    stroked=True,
                    get_line_color=[245, 158, 11, min(180, watch_alpha + 70)],
                    line_width_min_pixels=1,
                    pickable=False,
                )
                critical_pulse_layer = pdk.Layer(
                    "ScatterplotLayer",
                    data=critical_points,
                    get_position="[lon, lat]",
                    get_radius="pulse_radius",
                    get_fill_color=[239, 68, 68, crit_alpha],
                    stroked=True,
                    get_line_color=[239, 68, 68, min(210, crit_alpha + 70)],
                    line_width_min_pixels=1,
                    pickable=False,
                )
                enterprise_layer = pdk.Layer(
                    "ScatterplotLayer",
                    data=net_enterprise_geo,
                    get_position="[lon, lat]",
                    get_radius="radius",
                    get_fill_color=[59, 130, 246, 130],
                    stroked=True,
                    get_line_color=[29, 78, 216, 220],
                    line_width_min_pixels=1,
                    pickable=True,
                )
                weather_heat_layer = pdk.Layer(
                    "HeatmapLayer",
                    data=net_weather_risk_geo,
                    get_position="[lon, lat]",
                    get_weight="Weather Risk",
                    radiusPixels=52,
                    intensity=1.25,
                    threshold=0.06,
                    pickable=False,
                )
                weather_sites_layer = pdk.Layer(
                    "ScatterplotLayer",
                    data=net_weather_risk_geo,
                    get_position="[lon, lat]",
                    get_radius="radius",
                    get_fill_color=[239, 68, 68, 95],
                    stroked=True,
                    get_line_color=[245, 158, 11, 200],
                    line_width_min_pixels=1,
                    pickable=True,
                )
                build_corridor_layer = pdk.Layer(
                    "ArcLayer",
                    data=net_build_corridors,
                    get_source_position="[from_lon, from_lat]",
                    get_target_position="[to_lon, to_lat]",
                    get_source_color=[37, 99, 235, 145],
                    get_target_color=[16, 185, 129, 210],
                    get_width="width",
                    pickable=True,
                )
                node_label_layer = pdk.Layer(
                    "TextLayer",
                    data=net_node_labels,
                    get_position="[lon, lat]",
                    get_text="Label",
                    get_size=12,
                    get_color=[30, 41, 59, 220],
                    get_alignment_baseline="'top'",
                    get_pixel_offset=[0, 10],
                    pickable=False,
                )
                live_layers = []
                if enh_demand:
                    live_layers.extend([access_heat_layer, access_sites_layer])
                if enh_hotspots:
                    live_layers.append(density_layer)
                if enh_weather:
                    live_layers.extend([weather_heat_layer, weather_sites_layer])
                if enh_build:
                    live_layers.append(build_corridor_layer)
                if enh_enterprise:
                    live_layers.append(enterprise_layer)
                live_layers.extend([pulse_layer, base_layer, watch_pulse_layer, critical_pulse_layer])
                if enh_labels:
                    live_layers.append(node_label_layer)
                node_deck = pdk.Deck(
                    layers=live_layers,
                    initial_view_state=pdk.ViewState(latitude=lens_view["lat"], longitude=lens_view["lon"], zoom=lens_view["zoom"], pitch=lens_view["pitch"]),
                    map_style="https://basemaps.cartocdn.com/gl/voyager-gl-style/style.json",
                    tooltip={"html": "<b>{Node}{City}{Zone}</b><br/>Status: {Status}<br/>Availability: {Availability %}%<br/>Utilization: {Utilization %}%<br/>Open Incidents: {Open Incidents}<br/>Accounts: {Accounts}<br/>Weather Risk: {Weather Risk}<br/>Phase: {Phase}<br/>Capex: €{Capex M}M"},
                )
                st.pydeck_chart(node_deck, use_container_width=True)
                st.caption("Watch (yellow) and critical (red) hotspots use pulsing rings, with access-footprint heat and micro-site density layered underneath.")
                weakest_node = net_map_nodes.loc[net_map_nodes["Availability %"].idxmin()]
                render_net_ai_reco(
                    "Geo Reliability Focus",
                    f"{weakest_node['Node']} is the most vulnerable mapped node at {weakest_node['Availability %']:.2f}% availability.",
                    f"Prioritize route hardening and preventive field sweeps in {weakest_node['Node']}.",
                    "Reduce outage concentration in the most exposed geography.",
                    level="warning",
                )

        with map_col2:
            st.markdown('<div class="net-mini-title">Incident Hotspot Heatmap</div>', unsafe_allow_html=True)
            with st.container(border=True):
                heat_layer = pdk.Layer(
                    "HeatmapLayer",
                    data=net_incident_density,
                    get_position="[lon, lat]",
                    get_weight="weight",
                    radiusPixels=70,
                    intensity=1.8,
                    threshold=0.08,
                    pickable=False,
                )
                hex_layer = pdk.Layer(
                    "HexagonLayer",
                    data=net_incident_density,
                    get_position="[lon, lat]",
                    get_weight="weight",
                    radius=14000,
                    elevation_scale=35,
                    elevation_range=[0, 1600],
                    extruded=True,
                    pickable=True,
                    auto_highlight=True,
                )
                scatter_overlay = pdk.Layer(
                    "ScatterplotLayer",
                    data=net_incident_density,
                    get_position="[lon, lat]",
                    get_radius=2800,
                    get_fill_color=[239, 68, 68, 95],
                    pickable=True,
                )
                heat_deck = pdk.Deck(
                    layers=[heat_layer, hex_layer, scatter_overlay],
                    initial_view_state=pdk.ViewState(latitude=lens_view["lat"], longitude=lens_view["lon"], zoom=max(4.8, lens_view["zoom"] - 0.2), pitch=min(40, lens_view["pitch"] + 5)),
                    map_style="https://basemaps.cartocdn.com/gl/voyager-gl-style/style.json",
                    tooltip={"html": "Incident Type: {Type}<br/>Intensity: {weight}"},
                )
                st.pydeck_chart(heat_deck, use_container_width=True)
                top_hotspot_type = net_incident_points.groupby("Type", as_index=False)["weight"].sum().sort_values("weight", ascending=False).iloc[0]
                render_net_ai_reco(
                    "Hotspot Risk Pattern",
                    f"{top_hotspot_type['Type']} is the dominant hotspot pattern on the map by aggregate intensity.",
                    f"Deploy preventive controls for {top_hotspot_type['Type']} clusters before peak utilization windows.",
                    "Lower repeat incidents and improve uptime consistency in hotspot corridors.",
                    level="critical" if top_hotspot_type["weight"] >= 13 else "warning",
                )

        st.markdown('<div class="net-mini-title">Executive Network Command Center (Layer Toggles)</div>', unsafe_allow_html=True)
        st.markdown(dedent("""
            <div style="display:flex; flex-wrap:wrap; gap:0.4rem; margin:0.1rem 0 0.5rem 0;">
                <span style="background:#DBEAFE; border:1px solid #93C5FD; color:#1E3A8A; border-radius:999px; padding:0.18rem 0.52rem; font-size:0.72rem; font-weight:700;">Node Health</span>
                <span style="background:#FFF7ED; border:1px solid #FDBA74; color:#9A3412; border-radius:999px; padding:0.18rem 0.52rem; font-size:0.72rem; font-weight:700;">Incident Hotspots</span>
                <span style="background:#FEF3C7; border:1px solid #FCD34D; color:#92400E; border-radius:999px; padding:0.18rem 0.52rem; font-size:0.72rem; font-weight:700;">Fiber Cut Corridors</span>
                <span style="background:#DCFCE7; border:1px solid #86EFAC; color:#166534; border-radius:999px; padding:0.18rem 0.52rem; font-size:0.72rem; font-weight:700;">Backbone Load Flows</span>
                <span style="background:#E0E7FF; border:1px solid #A5B4FC; color:#3730A3; border-radius:999px; padding:0.18rem 0.52rem; font-size:0.72rem; font-weight:700;">SLA Risk Towers</span>
            </div>
        """), unsafe_allow_html=True)
        ctl_col1, ctl_col2, ctl_col3 = st.columns([1.6, 1.6, 1.2])
        with ctl_col1:
            show_nodes = st.checkbox("Node Health", value=True, key="net_map_toggle_nodes")
            show_hotspots = st.checkbox("Incident Hotspots", value=True, key="net_map_toggle_hotspots")
        with ctl_col2:
            show_fiber_cuts = st.checkbox("Fiber Cut Corridors", value=True, key="net_map_toggle_fiber")
            show_backbone = st.checkbox("Backbone Load Flows", value=True, key="net_map_toggle_backbone")
        with ctl_col3:
            show_sla = st.checkbox("SLA Risk Towers", value=True, key="net_map_toggle_sla")
            basemap_choice = st.selectbox(
                "Basemap",
                ["CARTO Voyager", "CARTO Dark Matter", "CARTO Positron"],
                index=0,
                key="net_map_basemap_choice",
            )

        basemap_url = {
            "CARTO Voyager": "https://basemaps.cartocdn.com/gl/voyager-gl-style/style.json",
            "CARTO Dark Matter": "https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json",
            "CARTO Positron": "https://basemaps.cartocdn.com/gl/positron-gl-style/style.json",
        }[basemap_choice]

        with st.container(border=True):
            big_layers = []
            pulse_factor_big = 1.0 + (0.28 * (0.5 + 0.5 * math.sin(time.time() * 2.8)))

            if show_hotspots:
                big_layers.append(
                    pdk.Layer(
                        "HeatmapLayer",
                        data=net_incident_points,
                        get_position="[lon, lat]",
                        get_weight="weight",
                        radiusPixels=45,
                        intensity=1.2,
                        threshold=0.1,
                    )
                )

            if show_fiber_cuts:
                big_layers.append(
                    pdk.Layer(
                        "LineLayer",
                        data=net_fiber_paths,
                        get_source_position="[from_lon, from_lat]",
                        get_target_position="[to_lon, to_lat]",
                        get_width="Cuts",
                        width_scale=2,
                        get_color=[245, 158, 11, 170],
                        pickable=True,
                    )
                )

            if show_backbone:
                flow_df = net_backbone_flows.copy()
                flow_df["r"] = flow_df["Utilization %"].apply(lambda v: 239 if v >= 80 else 245 if v >= 70 else 16)
                flow_df["g"] = flow_df["Utilization %"].apply(lambda v: 68 if v >= 80 else 158 if v >= 70 else 185)
                flow_df["b"] = flow_df["Utilization %"].apply(lambda v: 68 if v >= 80 else 11 if v >= 70 else 129)
                big_layers.append(
                    pdk.Layer(
                        "ArcLayer",
                        data=flow_df,
                        get_source_position="[source_lon, source_lat]",
                        get_target_position="[target_lon, target_lat]",
                        get_source_color="[r, g, b, 150]",
                        get_target_color="[r, g, b, 200]",
                        get_width=2.8,
                        pickable=True,
                    )
                )

            if show_sla:
                big_layers.append(
                    pdk.Layer(
                        "ColumnLayer",
                        data=net_sla_geo,
                        get_position="[lon, lat]",
                        get_elevation="SLA Risk * 120",
                        elevation_scale=1,
                        radius=9000,
                        get_fill_color=[59, 130, 246, 140],
                        pickable=True,
                        extruded=True,
                    )
                )

            if show_nodes:
                node_big = net_map_nodes.copy()
                node_big["radius"] = node_big["Open Incidents"] * 1200
                node_big["pulse_radius"] = node_big["radius"] * pulse_factor_big
                node_big["r"] = node_big["Status"].map({"Healthy": 16, "Watch": 245, "At Risk": 239})
                node_big["g"] = node_big["Status"].map({"Healthy": 185, "Watch": 158, "At Risk": 68})
                node_big["b"] = node_big["Status"].map({"Healthy": 129, "Watch": 11, "At Risk": 68})
                big_layers.extend([
                    pdk.Layer(
                        "ScatterplotLayer",
                        data=node_big,
                        get_position="[lon, lat]",
                        get_radius="pulse_radius",
                        get_fill_color="[r, g, b, 60]",
                        get_line_color="[r, g, b, 120]",
                        stroked=True,
                        line_width_min_pixels=1,
                        pickable=False,
                    ),
                    pdk.Layer(
                        "ScatterplotLayer",
                        data=node_big,
                        get_position="[lon, lat]",
                        get_radius="radius",
                        get_fill_color="[r, g, b, 195]",
                        pickable=True,
                    ),
                ])

            command_center = pdk.Deck(
                layers=big_layers,
                initial_view_state=pdk.ViewState(latitude=40.0, longitude=-3.7, zoom=4.6, pitch=38),
                map_style=basemap_url,
                tooltip={
                    "html": "<b>{Node}{City}</b><br/>Status: {Status}<br/>Availability: {Availability %}%<br/>Incidents: {Open Incidents}<br/>SLA Risk: {SLA Risk}<br/>Flow Utilization: {Utilization %}%<br/>Cuts: {Cuts}<br/>Type: {Type}"
                },
            )
            st.pydeck_chart(command_center, use_container_width=True)
            st.caption("Use toggles to compose executive narratives: capacity stress, outage concentration, SLA exposure, and geographic risk.")
            highest_sla_city = net_sla_geo.loc[net_sla_geo["SLA Risk"].idxmax()]
            render_net_ai_reco(
                "Command Center Readout",
                f"Highest SLA risk tower is {highest_sla_city['City']} at {highest_sla_city['SLA Risk']:.0f}, while map overlays show concentrated stress corridors.",
                "Lead with corridor hardening and targeted field dispatch in high-risk cities before peak traffic windows.",
                "Improves board-level confidence with visible control of geographic reliability risk.",
                level="critical" if highest_sla_city["SLA Risk"] >= 45 else "warning",
            )

        st.markdown('<div class="net-mini-title">Strategic Expansion Opportunity Atlas</div>', unsafe_allow_html=True)
        st.markdown(dedent("""
            <div style="display:flex; flex-wrap:wrap; gap:0.4rem; margin:0.1rem 0 0.5rem 0;">
                <span style="background:#FEF3C7; border:1px solid #FCD34D; color:#92400E; border-radius:999px; padding:0.18rem 0.52rem; font-size:0.72rem; font-weight:700;">Coverage Gap Grid</span>
                <span style="background:#FEE2E2; border:1px solid #FCA5A5; color:#991B1B; border-radius:999px; padding:0.18rem 0.52rem; font-size:0.72rem; font-weight:700;">Revenue-at-Risk Bubbles</span>
                <span style="background:#FFEDD5; border:1px solid #FDBA74; color:#9A3412; border-radius:999px; padding:0.18rem 0.52rem; font-size:0.72rem; font-weight:700;">Expansion Priority Towers</span>
                <span style="background:#DBEAFE; border:1px solid #93C5FD; color:#1E3A8A; border-radius:999px; padding:0.18rem 0.52rem; font-size:0.72rem; font-weight:700;">Top Expansion Corridors</span>
                <span style="background:#ECFDF5; border:1px solid #6EE7B7; color:#065F46; border-radius:999px; padding:0.18rem 0.52rem; font-size:0.72rem; font-weight:700;">Where to Invest Rings</span>
                <span style="background:#DBEAFE; border:1px solid #60A5FA; color:#1E3A8A; border-radius:999px; padding:0.18rem 0.52rem; font-size:0.72rem; font-weight:700;">Core Hub Cities</span>
                <span style="background:#DCFCE7; border:1px solid #86EFAC; color:#166534; border-radius:999px; padding:0.18rem 0.52rem; font-size:0.72rem; font-weight:700;">Growth Node Cities</span>
                <span style="background:#FEF3C7; border:1px solid #FCD34D; color:#92400E; border-radius:999px; padding:0.18rem 0.52rem; font-size:0.72rem; font-weight:700;">Emerging Node Cities</span>
            </div>
        """), unsafe_allow_html=True)
        exp_col1, exp_col2, exp_col3 = st.columns([1.35, 1.35, 1.3])
        with exp_col1:
            show_cov_gap = st.checkbox("Coverage Gap Grid", value=True, key="net_exp_toggle_gap")
            show_arr_risk = st.checkbox("Revenue-at-Risk Bubbles", value=True, key="net_exp_toggle_arr")
        with exp_col2:
            show_exp_towers = st.checkbox("Expansion Priority Towers", value=True, key="net_exp_toggle_towers")
            show_corridors = st.checkbox("Top Expansion Corridors", value=True, key="net_exp_toggle_corridors")
        with exp_col3:
            show_targets = st.checkbox("Where to Invest (Ranked)", value=True, key="net_exp_toggle_targets")
            horizon = st.selectbox("Planning Horizon", ["6M", "12M", "18M"], index=1, key="net_exp_horizon")

        horizon_profile = {
            "6M": {"priority": 0.93, "gap": 0.88, "arr": 0.78, "capex": 0.82, "tower": 0.86, "corr": 0.84, "target_radius": 0.80, "cell_size": 22000, "payback": 1.08},
            "12M": {"priority": 1.00, "gap": 1.00, "arr": 1.00, "capex": 1.00, "tower": 1.00, "corr": 1.00, "target_radius": 1.00, "cell_size": 28000, "payback": 1.00},
            "18M": {"priority": 1.12, "gap": 1.15, "arr": 1.30, "capex": 1.24, "tower": 1.25, "corr": 1.22, "target_radius": 1.28, "cell_size": 34000, "payback": 0.92},
        }[horizon]
        # Build a denser synthetic opportunity field so national investment coverage
        # looks richer in executive demos.
        opp_seed = net_opportunity_geo.copy()
        synth_rng = random.Random(29)
        synth_offsets = [
            (0.00, 0.00), (0.08, 0.03), (-0.08, 0.03), (0.06, -0.05),
            (-0.06, -0.05), (0.11, 0.00), (-0.11, 0.00), (0.03, 0.08),
        ]
        synth_records = []
        for _, row in opp_seed.iterrows():
            cluster_size = 5 if row["Demand Index"] >= 74 else 4
            for i in range(cluster_size):
                off_lon, off_lat = synth_offsets[i % len(synth_offsets)]
                scale = 0.42 + 0.12 * (i // len(synth_offsets))
                synth_records.append({
                    "Zone": f"{row['Zone']} · Growth Cluster {i + 1}",
                    "lat": row["lat"] + off_lat * scale + synth_rng.uniform(-0.013, 0.013),
                    "lon": row["lon"] + off_lon * scale + synth_rng.uniform(-0.013, 0.013),
                    "Demand Index": min(96, row["Demand Index"] + synth_rng.randint(2, 11)),
                    "Coverage Gap %": min(29, row["Coverage Gap %"] + synth_rng.randint(1, 8)),
                    "ARR Risk M": round(row["ARR Risk M"] * synth_rng.uniform(1.06, 1.36), 2),
                    "Capex M": round(row["Capex M"] * synth_rng.uniform(0.94, 1.14), 2),
                    "Payback Mo": round(max(7.0, row["Payback Mo"] - synth_rng.uniform(0.9, 3.2)), 1),
                    "Priority Score": min(97, row["Priority Score"] + synth_rng.randint(3, 10)),
                })
        opp_df = pd.concat([opp_seed, pd.DataFrame(synth_records)], ignore_index=True)
        opp_df["Priority Adj"] = (opp_df["Priority Score"] * horizon_profile["priority"]).round(1)
        opp_df["Coverage Gap Horizon %"] = (opp_df["Coverage Gap %"] * horizon_profile["gap"]).round(1)
        opp_df["ARR Horizon M"] = (opp_df["ARR Risk M"] * horizon_profile["arr"]).round(2)
        opp_df["Capex Horizon M"] = (opp_df["Capex M"] * horizon_profile["capex"]).round(2)
        opp_df["Payback Horizon Mo"] = (opp_df["Payback Mo"] * horizon_profile["payback"]).round(1)
        opp_df["Gap Elev"] = opp_df["Coverage Gap Horizon %"] * 95
        opp_df["ARR Radius"] = opp_df["ARR Horizon M"] * 42000 * (0.9 + 0.18 * (0.5 + 0.5 * math.sin(time.time() * 2.2)))
        opp_df["Tower Elev"] = opp_df["Priority Adj"] * 135 * horizon_profile["tower"]
        opp_df["r"] = opp_df["Priority Adj"].apply(lambda v: 239 if v >= 84 else 245 if v >= 76 else 16)
        opp_df["g"] = opp_df["Priority Adj"].apply(lambda v: 68 if v >= 84 else 158 if v >= 76 else 185)
        opp_df["b"] = opp_df["Priority Adj"].apply(lambda v: 68 if v >= 84 else 11 if v >= 76 else 129)
        opp_df = opp_df.sort_values("Priority Adj", ascending=False).reset_index(drop=True)
        opp_df["Rank"] = opp_df.index + 1
        opp_df["Invest Label"] = opp_df["Rank"].apply(lambda r: f"{horizon} INVEST #{r}") + " - " + opp_df["Zone"]
        top3 = opp_df.head(3).copy()
        top5 = opp_df.head(5).copy()
        top5["hub_lon"] = -3.7038
        top5["hub_lat"] = 40.4168
        top5["Corridor Width"] = (2.6 + (top5["Priority Adj"] - 70) / 14).clip(lower=2.2, upper=6.0) * horizon_profile["corr"]
        top5["Target Radius"] = (42000 * horizon_profile["target_radius"] * (top5["Priority Adj"] / 90)).round(0)
        city_map_df = net_major_cities_geo.copy()

        st.markdown(dedent(f"""
            <div class="net-kpi-grid" style="margin-bottom: 0.42rem;">
                <div class="net-kpi-card crit"><div class="k">#1 Invest</div><div class="v">{top3.iloc[0]['Zone']}</div><div class="d">Priority {top3.iloc[0]['Priority Adj']:.1f} · Payback {top3.iloc[0]['Payback Horizon Mo']:.1f} mo</div></div>
                <div class="net-kpi-card warn"><div class="k">#2 Invest</div><div class="v">{top3.iloc[1]['Zone']}</div><div class="d">Priority {top3.iloc[1]['Priority Adj']:.1f} · Payback {top3.iloc[1]['Payback Horizon Mo']:.1f} mo</div></div>
                <div class="net-kpi-card"><div class="k">#3 Invest</div><div class="v">{top3.iloc[2]['Zone']}</div><div class="d">Priority {top3.iloc[2]['Priority Adj']:.1f} · Payback {top3.iloc[2]['Payback Horizon Mo']:.1f} mo</div></div>
                <div class="net-kpi-card"><div class="k">Top-3 CAPEX</div><div class="v">€{top3['Capex Horizon M'].sum():.2f}M</div><div class="d">{horizon} targeted build plan</div></div>
            </div>
        """), unsafe_allow_html=True)
        st.caption(f"Horizon profile active: {horizon} - map geometry and investment economics are scaled for this planning window.")

        with st.container(border=True):
            atlas_layers = []
            if show_cov_gap:
                atlas_layers.append(
                    pdk.Layer(
                        "GridCellLayer",
                        data=opp_df,
                        get_position="[lon, lat]",
                        cell_size=horizon_profile["cell_size"],
                        get_elevation="Gap Elev",
                        elevation_scale=1,
                        extruded=True,
                        get_fill_color="[245, 158, 11, 135]",
                        pickable=True,
                    )
                )
            if show_arr_risk:
                atlas_layers.append(
                    pdk.Layer(
                        "ScatterplotLayer",
                        data=opp_df,
                        get_position="[lon, lat]",
                        get_radius="ARR Radius",
                        get_fill_color="[239, 68, 68, 120]",
                        stroked=True,
                        get_line_color="[239, 68, 68, 180]",
                        line_width_min_pixels=1,
                        pickable=True,
                    )
                )
            if show_exp_towers:
                atlas_layers.append(
                    pdk.Layer(
                        "ColumnLayer",
                        data=opp_df,
                        get_position="[lon, lat]",
                        get_elevation="Tower Elev",
                        elevation_scale=1,
                        radius=14000,
                        get_fill_color="[r, g, b, 185]",
                        pickable=True,
                        extruded=True,
                    )
                )
            if show_corridors:
                atlas_layers.append(
                    pdk.Layer(
                        "ArcLayer",
                        data=top5,
                        get_source_position="[hub_lon, hub_lat]",
                        get_target_position="[lon, lat]",
                        get_source_color="[37, 99, 235, 130]",
                        get_target_color="[16, 185, 129, 190]",
                        get_width="Corridor Width",
                        pickable=True,
                    )
                )
            if show_targets:
                atlas_layers.extend([
                    pdk.Layer(
                        "ScatterplotLayer",
                        data=top5,
                        get_position="[lon, lat]",
                        get_radius="Target Radius",
                        get_fill_color=[16, 185, 129, 55],
                        stroked=True,
                        get_line_color=[16, 185, 129, 220],
                        line_width_min_pixels=2,
                        pickable=True,
                    ),
                    pdk.Layer(
                        "TextLayer",
                        data=top5,
                        get_position="[lon, lat]",
                        get_text="Invest Label",
                        get_size=14,
                        get_color=[15, 23, 42, 230],
                        get_alignment_baseline="'top'",
                        get_pixel_offset=[0, 18],
                        pickable=False,
                    ),
                ])
            atlas_layers.extend([
                pdk.Layer(
                    "ScatterplotLayer",
                    data=city_map_df,
                    get_position="[lon, lat]",
                    get_radius="radius",
                    get_fill_color="[r, g, b, 170]",
                    stroked=True,
                    get_line_color="[255, 255, 255, 220]",
                    line_width_min_pixels=1.5,
                    pickable=True,
                ),
                pdk.Layer(
                    "TextLayer",
                    data=city_map_df,
                    get_position="[lon, lat]",
                    get_text="City",
                    get_size=13,
                    get_color=[15, 23, 42, 235],
                    get_alignment_baseline="'bottom'",
                    get_pixel_offset=[0, -10],
                    pickable=False,
                ),
            ])

            atlas_deck = pdk.Deck(
                layers=atlas_layers,
                initial_view_state=pdk.ViewState(latitude=40.0, longitude=-3.7, zoom=5.0, pitch=40),
                map_style="https://basemaps.cartocdn.com/gl/positron-gl-style/style.json",
                tooltip={
                    "html": "<b>{Zone}{City}</b><br/>Tier: {City Tier}<br/>Signal: {Investment Signal}<br/>Invest Rank: #{Rank}<br/>Demand: {Demand Index}<br/>Coverage Gap ({horizon}): {Coverage Gap Horizon %}%<br/>ARR Risk ({horizon}): €{ARR Horizon M}M<br/>Capex ({horizon}): €{Capex Horizon M}M<br/>Payback ({horizon}): {Payback Horizon Mo} mo<br/>Priority: {Priority Adj}"
                },
            )
            st.pydeck_chart(atlas_deck, use_container_width=True)
            st.markdown(dedent("""
                <div style="margin-top:0.45rem; display:flex; flex-wrap:wrap; gap:0.4rem;">
                    <span style="display:inline-flex; align-items:center; gap:0.34rem; background:#F8FAFC; border:1px solid #E2E8F0; border-radius:999px; padding:0.18rem 0.52rem; font-size:0.72rem; color:#334155; font-weight:700;">
                        <span style="width:10px; height:10px; border-radius:50%; background:#2563EB; display:inline-block;"></span> Core Hub Cities
                    </span>
                    <span style="display:inline-flex; align-items:center; gap:0.34rem; background:#F8FAFC; border:1px solid #E2E8F0; border-radius:999px; padding:0.18rem 0.52rem; font-size:0.72rem; color:#334155; font-weight:700;">
                        <span style="width:10px; height:10px; border-radius:50%; background:#10B981; display:inline-block;"></span> Growth Node Cities
                    </span>
                    <span style="display:inline-flex; align-items:center; gap:0.34rem; background:#F8FAFC; border:1px solid #E2E8F0; border-radius:999px; padding:0.18rem 0.52rem; font-size:0.72rem; color:#334155; font-weight:700;">
                        <span style="width:10px; height:10px; border-radius:50%; background:#F59E0B; display:inline-block;"></span> Emerging Node Cities
                    </span>
                    <span style="display:inline-flex; align-items:center; gap:0.34rem; background:#F8FAFC; border:1px solid #E2E8F0; border-radius:999px; padding:0.18rem 0.52rem; font-size:0.72rem; color:#334155; font-weight:700;">
                        <span style="width:10px; height:10px; border-radius:50%; background:#EF4444; display:inline-block;"></span> Revenue-at-Risk Bubbles
                    </span>
                    <span style="display:inline-flex; align-items:center; gap:0.34rem; background:#F8FAFC; border:1px solid #E2E8F0; border-radius:999px; padding:0.18rem 0.52rem; font-size:0.72rem; color:#334155; font-weight:700;">
                        <span style="width:14px; height:3px; border-radius:2px; background:#2563EB; display:inline-block;"></span> Expansion Corridors
                    </span>
                    <span style="display:inline-flex; align-items:center; gap:0.34rem; background:#F8FAFC; border:1px solid #E2E8F0; border-radius:999px; padding:0.18rem 0.52rem; font-size:0.72rem; color:#334155; font-weight:700;">
                        <span style="width:10px; height:10px; border-radius:50%; border:2px solid #10B981; background:transparent; display:inline-block;"></span> Ranked Investment Rings
                    </span>
                </div>
            """), unsafe_allow_html=True)
            st.caption("Executive lens: combine demand, coverage gap, revenue-at-risk, and payback to prioritize expansion corridors.")
            top_zone = opp_df.sort_values("Priority Adj", ascending=False).iloc[0]
            render_net_ai_reco(
                "Expansion Prioritization Signal",
                f"Top zone for {horizon} is {top_zone['Zone']} with priority {top_zone['Priority Adj']:.1f}, coverage gap {top_zone['Coverage Gap Horizon %']:.1f}%, and ARR risk €{top_zone['ARR Horizon M']:.2f}M.",
                f"Prioritize phased build in {top_zone['Zone']} and lock field capacity for first-wave execution.",
                "Improves growth quality by concentrating CAPEX on highest-value, fastest-payback opportunities.",
                level="critical" if top_zone["Priority Adj"] >= 85 else "warning",
            )

    with net_tab_ops:
        st.markdown('<div class="net-title">Network Operations Control Tower</div>', unsafe_allow_html=True)
        st.markdown(dedent(f"""
            <div class="net-kpi-grid">
                <div class="net-kpi-card"><div class="k">Incident Run-Rate</div><div class="v">{net_incident_trend.iloc[-1]['Incidents']:.0f}</div><div class="d">Latest month incidents</div></div>
                <div class="net-kpi-card"><div class="k">MTTR Trend</div><div class="v">{net_incident_trend.iloc[0]['MTTR Min']-mttr_current:.0f} min</div><div class="d">Improvement vs period start</div></div>
                <div class="net-kpi-card {'warn' if breach_rate > 9 else ''}"><div class="k">SLA Breach Rate</div><div class="v">{breach_rate:.1f}%</div><div class="d">Cross-queue average</div></div>
                <div class="net-kpi-card {'warn' if net_queue['Avg Age Hr'].mean() > 10 else ''}"><div class="k">Ticket Aging</div><div class="v">{net_queue['Avg Age Hr'].mean():.1f} h</div><div class="d">Average open ticket age</div></div>
            </div>
        """), unsafe_allow_html=True)

        op_col1, op_col2 = st.columns(2)
        with op_col1:
            st.markdown('<div class="net-mini-title">Incident Volume and MTTR Trend</div>', unsafe_allow_html=True)
            with st.container(border=True):
                inc_bar = alt.Chart(net_incident_trend).mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6, size=36, color="#60A5FA").encode(
                    x=alt.X("Month:N", title=None),
                    y=alt.Y("Incidents:Q", title="Incidents"),
                    tooltip=["Month:N", alt.Tooltip("Incidents:Q", format=".0f"), alt.Tooltip("MTTR Min:Q", format=".0f")],
                )
                mttr_line = alt.Chart(net_incident_trend).mark_line(point=True, strokeWidth=3, color="#F59E0B").encode(
                    x="Month:N",
                    y=alt.Y("MTTR Min:Q", title="MTTR (min)"),
                )
                st.altair_chart(style_net_chart(alt.layer(inc_bar, mttr_line).resolve_scale(y="independent"), height=235), use_container_width=True)
                render_net_ai_reco(
                    "Operational Discipline",
                    f"Incidents dropped from {net_incident_trend.iloc[0]['Incidents']:.0f} to {net_incident_trend.iloc[-1]['Incidents']:.0f}, with MTTR down to {mttr_current:.0f} min.",
                    "Sustain weekly RCA cadence and keep fast-response playbooks active for repeat patterns.",
                    "Continue improving restoration speed while keeping outage volume on a downward track.",
                )

        with op_col2:
            st.markdown('<div class="net-mini-title">Queue Pressure and SLA Risk</div>', unsafe_allow_html=True)
            with st.container(border=True):
                queue_bar = alt.Chart(net_queue).mark_bar(cornerRadiusTopRight=7, cornerRadiusBottomRight=7, size=20).encode(
                    x=alt.X("Open Tickets:Q", title="Open Tickets"),
                    y=alt.Y("Queue:N", sort="-x", title=None),
                    color=alt.Color("SLA Breach %:Q", scale=alt.Scale(scheme="orangered"), legend=alt.Legend(title="SLA Breach %")),
                    tooltip=["Queue:N", alt.Tooltip("Open Tickets:Q", format=".0f"), alt.Tooltip("SLA Breach %:Q", format=".1f"), alt.Tooltip("Avg Age Hr:Q", format=".1f")],
                )
                queue_label = alt.Chart(net_queue).mark_text(align="left", dx=6, fontSize=10, color="#0F172A").encode(
                    x="Open Tickets:Q", y=alt.Y("Queue:N", sort="-x"), text=alt.Text("Avg Age Hr:Q", format=".1f")
                )
                st.altair_chart(style_net_chart(queue_bar + queue_label, height=235), use_container_width=True)
                top_queue = net_queue.loc[net_queue["Open Tickets"].idxmax()]
                render_net_ai_reco(
                    "Workflow Balancing",
                    f"{top_queue['Queue']} queue carries the highest open load with elevated SLA pressure.",
                    f"Reallocate dispatch capacity toward {top_queue['Queue']} and enforce 24-hour breach recovery goals.",
                    "Lower backlog, improve SLA compliance, and stabilize operations workload.",
                    level="warning",
                )

        op_col3, op_col4 = st.columns(2)
        with op_col3:
            st.markdown('<div class="net-mini-title">Queue Aging vs SLA Breach Matrix</div>', unsafe_allow_html=True)
            with st.container(border=True):
                queue_scatter = alt.Chart(net_queue).mark_circle(opacity=0.86, stroke="#FFFFFF", strokeWidth=1.2).encode(
                    x=alt.X("Avg Age Hr:Q", title="Average Ticket Age (hours)"),
                    y=alt.Y("SLA Breach %:Q", title="SLA Breach (%)"),
                    size=alt.Size("Open Tickets:Q", scale=alt.Scale(range=[320, 1400]), legend=None),
                    color=alt.Color("Queue:N", legend=alt.Legend(title=None), scale=alt.Scale(range=["#3B82F6", "#10B981", "#F59E0B", "#EF4444", "#6366F1"])),
                    tooltip=["Queue:N", alt.Tooltip("Open Tickets:Q", format=".0f"), alt.Tooltip("Avg Age Hr:Q", format=".1f"), alt.Tooltip("SLA Breach %:Q", format=".1f")],
                )
                queue_names = alt.Chart(net_queue).mark_text(dy=-10, fontSize=9, color="#1E293B").encode(
                    x="Avg Age Hr:Q", y="SLA Breach %:Q", text="Queue:N"
                )
                st.altair_chart(style_net_chart(queue_scatter + queue_names, height=235), use_container_width=True)
                risk_queue = net_queue.sort_values(["SLA Breach %", "Avg Age Hr"], ascending=False).iloc[0]
                render_net_ai_reco(
                    "Queue Risk Hotspot",
                    f"{risk_queue['Queue']} sits at the highest combined ticket age and SLA breach risk.",
                    f"Deploy surge capacity and stricter triage thresholds for {risk_queue['Queue']} backlog items.",
                    "Shrink breach exposure and accelerate queue normalization.",
                    level="warning",
                )

        with op_col4:
            st.markdown('<div class="net-mini-title">Backlog Mix by Queue</div>', unsafe_allow_html=True)
            with st.container(border=True):
                queue_mix = net_queue.copy()
                queue_mix["Share %"] = (queue_mix["Open Tickets"] / queue_mix["Open Tickets"].sum() * 100).round(1)
                mix_arc = alt.Chart(queue_mix).mark_arc(innerRadius=62, outerRadius=104).encode(
                    theta=alt.Theta("Open Tickets:Q"),
                    color=alt.Color("Queue:N", legend=alt.Legend(title=None), scale=alt.Scale(range=["#3B82F6", "#10B981", "#F59E0B", "#EF4444", "#6366F1"])),
                    tooltip=["Queue:N", alt.Tooltip("Open Tickets:Q", format=".0f"), alt.Tooltip("Share %:Q", format=".1f"), alt.Tooltip("SLA Breach %:Q", format=".1f")],
                )
                mix_text = alt.Chart(pd.DataFrame({"t": [f"{queue_mix['Open Tickets'].sum():.0f}"]})).mark_text(fontSize=22, fontWeight="bold", color="#0F172A").encode(text="t:N")
                mix_sub = alt.Chart(pd.DataFrame({"t": ["Open Tickets"]})).mark_text(fontSize=11, dy=18, color="#64748B").encode(text="t:N")
                st.altair_chart(style_net_chart(mix_arc + mix_text + mix_sub, height=235), use_container_width=True)
                dominant_queue = queue_mix.loc[queue_mix["Open Tickets"].idxmax()]
                render_net_ai_reco(
                    "Workload Composition",
                    f"{dominant_queue['Queue']} represents the largest backlog share at {dominant_queue['Share %']:.1f}%.",
                    "Set queue-specific closure targets and enforce daily burn-down governance.",
                    "Improve throughput predictability and stabilize incident closure cadence.",
                )

        st.markdown('<div class="net-title">Infrastructure Operations Pipeline</div>', unsafe_allow_html=True)
        op_inf_col1, op_inf_col2 = st.columns(2)
        with op_inf_col1:
            st.markdown('<div class="net-mini-title">Maintenance Backlog by Asset Type</div>', unsafe_allow_html=True)
            with st.container(border=True):
                maint_df = net_maintenance.copy()
                maint_df["Critical Workorders"] = (maint_df["Open Workorders"] * maint_df["Critical %"] / 100).round(1)
                maint_bar = alt.Chart(maint_df).mark_bar(cornerRadiusTopRight=7, cornerRadiusBottomRight=7, size=20).encode(
                    x=alt.X("Open Workorders:Q", title="Open Workorders"),
                    y=alt.Y("Asset Type:N", sort="-x", title=None),
                    color=alt.Color("Critical %:Q", scale=alt.Scale(scheme="orangered"), legend=alt.Legend(title="Critical %")),
                    tooltip=["Asset Type:N", alt.Tooltip("Open Workorders:Q", format=".0f"), alt.Tooltip("Critical %:Q", format=".1f"), alt.Tooltip("Avg Delay Hr:Q", format=".1f")],
                )
                maint_label = alt.Chart(maint_df).mark_text(align="left", dx=6, fontSize=10, color="#0F172A").encode(
                    x="Open Workorders:Q", y=alt.Y("Asset Type:N", sort="-x"), text=alt.Text("Critical Workorders:Q", format=".1f")
                )
                st.altair_chart(style_net_chart(maint_bar + maint_label, height=235), use_container_width=True)
                top_maint = maint_df.loc[maint_df["Open Workorders"].idxmax()]
                render_net_ai_reco(
                    "Maintenance Bottleneck",
                    f"{top_maint['Asset Type']} has the highest workorder backlog with elevated critical exposure.",
                    f"Prioritize additional field windows for {top_maint['Asset Type']} and enforce max-age policy.",
                    "Reduces deferred maintenance risk and improves asset reliability trajectory.",
                    level="warning",
                )

        with op_inf_col2:
            st.markdown('<div class="net-mini-title">Upgrade Program Impact vs CAPEX</div>', unsafe_allow_html=True)
            with st.container(border=True):
                upg_scatter = alt.Chart(net_upgrade_program).mark_circle(opacity=0.88, stroke="#FFFFFF", strokeWidth=1.2).encode(
                    x=alt.X("Capex M:Q", title="CAPEX (€ M)"),
                    y=alt.Y("Impact Score:Q", title="Impact Score"),
                    size=alt.Size("Delivery Risk:Q", scale=alt.Scale(range=[260, 1300]), legend=alt.Legend(title="Delivery Risk")),
                    color=alt.Color("Quarter:N", legend=alt.Legend(title="Execution Quarter"), scale=alt.Scale(range=["#3B82F6", "#10B981", "#F59E0B"])),
                    tooltip=["Initiative:N", "Domain:N", alt.Tooltip("Capex M:Q", format=".2f"), alt.Tooltip("Impact Score:Q", format=".0f"), alt.Tooltip("Delivery Risk:Q", format=".1f"), "Quarter:N"],
                )
                upg_labels = alt.Chart(net_upgrade_program).mark_text(dy=-10, fontSize=9, color="#1E293B").encode(
                    x="Capex M:Q", y="Impact Score:Q", text="Initiative:N"
                )
                st.altair_chart(style_net_chart(upg_scatter + upg_labels, height=235), use_container_width=True)
                top_program = net_upgrade_program.sort_values(["Impact Score", "Delivery Risk"], ascending=[False, True]).iloc[0]
                render_net_ai_reco(
                    "Upgrade Sequencing",
                    f"{top_program['Initiative']} offers the best impact-to-risk profile for the current pipeline.",
                    f"Pull forward {top_program['Initiative']} and protect delivery resources in {top_program['Quarter']}.",
                    "Accelerates infrastructure value realization with controlled execution risk.",
                )

    with net_tab_impact:
        st.markdown('<div class="net-title">Service Impact and Customer Exposure</div>', unsafe_allow_html=True)
        service_subs_k = net_service_impact["Subs Impacted K"].sum()
        service_arr_m = net_service_impact["ARR at Risk M"].sum()
        service_enterprise = int(net_service_impact["Enterprise Accounts"].sum())
        sla_target_week = net_sla_command["SLA Target %"].iloc[-1]
        sla_forecast_week = net_sla_command["SLA Forecast %"].iloc[-1]
        sla_gap_pp = sla_target_week - sla_forecast_week

        st.markdown(dedent(f"""
            <div class="net-kpi-grid">
                <div class="net-kpi-card {'crit' if service_subs_k > 8 else 'warn'}"><div class="k">Subscribers Impacted</div><div class="v">{service_subs_k:.1f}K</div><div class="d">Current service exposure</div></div>
                <div class="net-kpi-card {'crit' if service_arr_m > 3.5 else 'warn'}"><div class="k">ARR at Risk</div><div class="v">€{service_arr_m:.2f}M</div><div class="d">Business impact footprint</div></div>
                <div class="net-kpi-card"><div class="k">Enterprise Accounts</div><div class="v">{service_enterprise}</div><div class="d">High-value accounts affected</div></div>
                <div class="net-kpi-card {'crit' if sla_gap_pp > 0.3 else 'warn' if sla_gap_pp > 0.1 else ''}"><div class="k">SLA Forecast Gap</div><div class="v">{sla_gap_pp:+.2f}pp</div><div class="d">vs weekly target</div></div>
            </div>
        """), unsafe_allow_html=True)

        imp_col1, imp_col2 = st.columns(2)
        with imp_col1:
            st.markdown('<div class="net-mini-title">Incident Business Impact by Type</div>', unsafe_allow_html=True)
            with st.container(border=True):
                impact_bar = alt.Chart(net_service_impact).mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6, size=28, color="#60A5FA").encode(
                    x=alt.X("Incident Type:N", title=None),
                    y=alt.Y("Subs Impacted K:Q", title="Impacted Subscribers (K)"),
                    tooltip=["Incident Type:N", alt.Tooltip("Subs Impacted K:Q", format=".0f"), alt.Tooltip("ARR at Risk M:Q", format=".2f"), alt.Tooltip("Avg Restore Hr:Q", format=".1f")],
                )
                impact_line = alt.Chart(net_service_impact).mark_line(point=True, strokeWidth=3, color="#EF4444").encode(
                    x="Incident Type:N",
                    y=alt.Y("ARR at Risk M:Q", title="ARR at Risk (€ M)"),
                )
                st.altair_chart(style_net_chart(alt.layer(impact_bar, impact_line).resolve_scale(y="independent"), height=235), use_container_width=True)
                top_impact = net_service_impact.loc[net_service_impact["ARR at Risk M"].idxmax()]
                render_net_ai_reco(
                    "Business Impact Prioritization",
                    f"{top_impact['Incident Type']} drives the highest ARR exposure at €{top_impact['ARR at Risk M']:.2f}M.",
                    f"Prioritize fast-response and prevention controls for {top_impact['Incident Type']} failure patterns.",
                    "Directly protects revenue continuity and enterprise customer confidence.",
                    level="critical",
                )

        with imp_col2:
            st.markdown('<div class="net-mini-title">Network Quality vs Customer Outcomes</div>', unsafe_allow_html=True)
            with st.container(border=True):
                cust_corr = alt.Chart(net_customer_link).mark_circle(opacity=0.88, stroke="#FFFFFF", strokeWidth=1.2).encode(
                    x=alt.X("Latency ms:Q", title="Latency (ms)"),
                    y=alt.Y("Churn %:Q", title="Churn (%)"),
                    size=alt.Size("Packet Loss %:Q", scale=alt.Scale(range=[300, 1600]), legend=alt.Legend(title="Packet Loss %")),
                    color=alt.Color("NPS:Q", scale=alt.Scale(scheme="orangered"), legend=alt.Legend(title="NPS")),
                    tooltip=["Region:N", alt.Tooltip("Latency ms:Q", format=".1f"), alt.Tooltip("Packet Loss %:Q", format=".2f"), alt.Tooltip("NPS:Q", format=".0f"), alt.Tooltip("Churn %:Q", format=".1f")],
                )
                corr_label = alt.Chart(net_customer_link).mark_text(dy=-10, fontSize=9, color="#1E293B").encode(
                    x="Latency ms:Q", y="Churn %:Q", text="Region:N"
                )
                st.altair_chart(style_net_chart(cust_corr + corr_label, height=235), use_container_width=True)
                worst_exp = net_customer_link.sort_values(["Churn %", "Latency ms"], ascending=False).iloc[0]
                render_net_ai_reco(
                    "Customer Impact Link",
                    f"{worst_exp['Region']} combines high latency/churn pressure and should be treated as a priority quality zone.",
                    f"Pair network remediation with proactive customer retention campaigns in {worst_exp['Region']}.",
                    "Improves technical quality and reduces preventable churn in exposed cohorts.",
                    level="warning",
                )

        imp_col3, imp_col4 = st.columns(2)
        with imp_col3:
            st.markdown('<div class="net-mini-title">SLA Command Widget (Target vs Forecast)</div>', unsafe_allow_html=True)
            with st.container(border=True):
                sla_actual = alt.Chart(net_sla_command).mark_line(point=True, strokeWidth=3, color="#3B82F6").encode(
                    x=alt.X("Day:N", title=None),
                    y=alt.Y("SLA Actual %:Q", title="SLA (%)"),
                    tooltip=["Day:N", alt.Tooltip("SLA Actual %:Q", format=".2f"), alt.Tooltip("SLA Forecast %:Q", format=".2f"), alt.Tooltip("SLA Target %:Q", format=".2f")],
                )
                sla_forecast = alt.Chart(net_sla_command).mark_line(point=True, strokeWidth=2.6, color="#10B981", strokeDash=[6, 3]).encode(
                    x="Day:N", y="SLA Forecast %:Q"
                )
                sla_target = alt.Chart(net_sla_command).mark_line(strokeWidth=2.2, color="#EF4444").encode(
                    x="Day:N", y="SLA Target %:Q"
                )
                st.altair_chart(style_net_chart(alt.layer(sla_actual, sla_forecast, sla_target), height=235), use_container_width=True)
                render_net_ai_reco(
                    "SLA Early Warning",
                    f"Week-end SLA is forecast at {sla_forecast_week:.2f}% vs target {sla_target_week:.2f}% ({sla_gap_pp:+.2f}pp).",
                    "Trigger service stabilization measures before week close and protect high-value circuits first.",
                    "Improves probability of SLA target attainment and lowers penalty exposure.",
                    level="warning" if sla_gap_pp > 0.1 else "info",
                )

        with imp_col4:
            st.markdown('<div class="net-mini-title">Outage Timeline Playback</div>', unsafe_allow_html=True)
            with st.container(border=True):
                selected_hour = st.slider("Playback Hour", 0, 23, 12, key="net_outage_playback_hour")
                timeline_df = net_outage_timeline.copy()
                selected_point = timeline_df[timeline_df["Hour"] == selected_hour]
                timeline_bar = alt.Chart(timeline_df).mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4, color="#93C5FD").encode(
                    x=alt.X("Hour:O", title="Hour of Day"),
                    y=alt.Y("Subs Impacted K:Q", title="Impacted Subs (K)"),
                    tooltip=[alt.Tooltip("Hour:O", title="Hour"), alt.Tooltip("Subs Impacted K:Q", format=".0f"), alt.Tooltip("Incidents:Q", format=".0f")],
                )
                select_rule = alt.Chart(selected_point).mark_rule(color="#EF4444", strokeWidth=2).encode(x=alt.X("Hour:O"))
                inc_line = alt.Chart(timeline_df).mark_line(point=True, strokeWidth=2.4, color="#F59E0B").encode(
                    x=alt.X("Hour:O", title=None), y=alt.Y("Incidents:Q", title="Incidents")
                )
                st.altair_chart(style_net_chart(alt.layer(timeline_bar, inc_line, select_rule).resolve_scale(y="independent"), height=235), use_container_width=True)
                playback = selected_point.iloc[0]
                render_net_ai_reco(
                    "Timeline Snapshot",
                    f"At {int(playback['Hour']):02d}:00, estimated impact is {playback['Subs Impacted K']:.1f}K subscribers across {playback['Incidents']:.0f} incidents.",
                    "Use hourly playback to align dispatch windows and proactive communication timing.",
                    "Improves incident response pacing and stakeholder situational awareness.",
                    level="warning" if playback["Subs Impacted K"] >= 6 else "info",
                )

    with net_tab_exec:
        st.markdown('<div class="net-title">Execution and Playbook Control</div>', unsafe_allow_html=True)
        on_track_pct = (net_mitigation_tracker["Status"] == "On Track").mean() * 100
        total_capex_exec = net_upgrade_program["Capex M"].sum()
        high_critical_sites = int((net_critical_sites["Criticality"] >= 88).sum())
        max_forecast_util = net_capacity_forecast["Projected Util %"].max()

        st.markdown(dedent(f"""
            <div class="net-kpi-grid">
                <div class="net-kpi-card"><div class="k">Program CAPEX</div><div class="v">€{total_capex_exec:.1f}M</div><div class="d">Active infrastructure initiatives</div></div>
                <div class="net-kpi-card {'warn' if max_forecast_util >= 85 else ''}"><div class="k">Peak Forecast Utilization</div><div class="v">{max_forecast_util:.0f}%</div><div class="d">90-day projection ceiling</div></div>
                <div class="net-kpi-card {'warn' if on_track_pct < 70 else ''}"><div class="k">Mitigation On-Track</div><div class="v">{on_track_pct:.0f}%</div><div class="d">Execution confidence</div></div>
                <div class="net-kpi-card {'crit' if high_critical_sites > 3 else 'warn'}"><div class="k">High-Critical Sites</div><div class="v">{high_critical_sites}</div><div class="d">Requires executive oversight</div></div>
            </div>
        """), unsafe_allow_html=True)

        ex_col1, ex_col2 = st.columns(2)
        with ex_col1:
            st.markdown('<div class="net-mini-title">Capacity Forecast by Corridor (30/60/90d)</div>', unsafe_allow_html=True)
            with st.container(border=True):
                cap_fcst = alt.Chart(net_capacity_forecast).mark_line(point=True, strokeWidth=3).encode(
                    x=alt.X("Horizon:N", title=None),
                    y=alt.Y("Projected Util %:Q", title="Projected Utilization (%)"),
                    color=alt.Color("Corridor:N", legend=alt.Legend(title=None), scale=alt.Scale(range=["#3B82F6", "#10B981", "#F59E0B", "#EF4444"])),
                    tooltip=["Corridor:N", "Horizon:N", alt.Tooltip("Projected Util %:Q", format=".0f")],
                )
                threshold = alt.Chart(pd.DataFrame({"y": [80]})).mark_rule(color="#94A3B8", strokeDash=[5, 4]).encode(y="y:Q")
                st.altair_chart(style_net_chart(threshold + cap_fcst, height=235), use_container_width=True)
                top_corridor = net_capacity_forecast.sort_values("Projected Util %", ascending=False).iloc[0]
                render_net_ai_reco(
                    "Capacity Forecast Alert",
                    f"{top_corridor['Corridor']} reaches {top_corridor['Projected Util %']:.0f}% in the {top_corridor['Horizon']} horizon.",
                    "Pre-authorize expansion capacity in this corridor before demand breaches operating thresholds.",
                    "Avoids saturation-driven quality degradation and emergency expansion costs.",
                    level="warning",
                )

        with ex_col2:
            st.markdown('<div class="net-mini-title">Change Risk Monitor</div>', unsafe_allow_html=True)
            with st.container(border=True):
                change_bar = alt.Chart(net_change_monitor).mark_bar(cornerRadiusTopLeft=5, cornerRadiusTopRight=5, size=24, color="#93C5FD").encode(
                    x=alt.X("Week:N", title=None),
                    y=alt.Y("Planned Changes:Q", title="Planned Changes"),
                    tooltip=["Week:N", alt.Tooltip("Planned Changes:Q", format=".0f"), alt.Tooltip("Failed Changes:Q", format=".0f"), alt.Tooltip("Incidents:Q", format=".0f")],
                )
                inc_line = alt.Chart(net_change_monitor).mark_line(point=True, strokeWidth=2.8, color="#EF4444").encode(
                    x="Week:N", y=alt.Y("Incidents:Q", title="Incidents")
                )
                failed_line = alt.Chart(net_change_monitor).mark_line(point=True, strokeWidth=2.2, color="#F59E0B", strokeDash=[5, 3]).encode(
                    x="Week:N", y=alt.Y("Failed Changes:Q", title="Failed Changes")
                )
                st.altair_chart(style_net_chart(alt.layer(change_bar, inc_line, failed_line).resolve_scale(y="independent"), height=235), use_container_width=True)
                riskiest_week = net_change_monitor.sort_values(["Failed Changes", "Incidents"], ascending=False).iloc[0]
                render_net_ai_reco(
                    "Change Governance",
                    f"{riskiest_week['Week']} shows the highest failed-change and incident concentration.",
                    "Apply stricter change windows, rollback readiness, and pre-deployment validation in high-risk periods.",
                    "Reduces change-induced incidents and improves release reliability.",
                    level="warning",
                )

        ex_col3, ex_col4 = st.columns(2)
        with ex_col3:
            st.markdown('<div class="net-mini-title">Mitigation Tracker (Progress vs Risk Reduced)</div>', unsafe_allow_html=True)
            with st.container(border=True):
                mit_bar = alt.Chart(net_mitigation_tracker).mark_bar(cornerRadiusTopLeft=5, cornerRadiusTopRight=5, size=26, color="#3B82F6").encode(
                    x=alt.X("Initiative:N", sort="-y", title=None),
                    y=alt.Y("Progress %:Q", title="Progress (%)"),
                    tooltip=["Initiative:N", "Owner:N", "ETA:N", alt.Tooltip("Progress %:Q", format=".0f"), alt.Tooltip("Risk Reduced %:Q", format=".0f"), "Status:N"],
                )
                risk_line = alt.Chart(net_mitigation_tracker).mark_line(point=True, strokeWidth=2.8, color="#10B981").encode(
                    x=alt.X("Initiative:N", sort="-y"), y=alt.Y("Risk Reduced %:Q", title="Risk Reduced (%)")
                )
                st.altair_chart(style_net_chart(alt.layer(mit_bar, risk_line).resolve_scale(y="independent"), height=235), use_container_width=True)
                lagging = net_mitigation_tracker.sort_values("Progress %").iloc[0]
                render_net_ai_reco(
                    "Execution Tracker",
                    f"{lagging['Initiative']} is the slowest initiative at {lagging['Progress %']:.0f}% completion.",
                    f"Escalate owner support for {lagging['Initiative']} to protect planned risk-reduction outcomes.",
                    "Improves delivery certainty for the resilience roadmap.",
                    level="warning",
                )

        with ex_col4:
            st.markdown('<div class="net-mini-title">Resilience Scorecard Trend</div>', unsafe_allow_html=True)
            with st.container(border=True):
                res_long = net_resilience_score.melt("Month", var_name="Domain", value_name="Score")
                res_line = alt.Chart(res_long).mark_line(point=True, strokeWidth=3).encode(
                    x=alt.X("Month:N", title=None),
                    y=alt.Y("Score:Q", title="Resilience Score"),
                    color=alt.Color("Domain:N", legend=alt.Legend(title=None), scale=alt.Scale(range=["#3B82F6", "#10B981", "#F59E0B"])),
                    tooltip=["Month:N", "Domain:N", alt.Tooltip("Score:Q", format=".0f")],
                )
                st.altair_chart(style_net_chart(res_line, height=235), use_container_width=True)
                latest_core = net_resilience_score.iloc[-1]["Core Score"]
                render_net_ai_reco(
                    "Resilience Trajectory",
                    f"Core resilience reaches {latest_core:.0f} in the latest month with broad upward trend across domains.",
                    "Sustain current program cadence and add targeted support to lagging field domains.",
                    "Builds durable reliability gains and improves crisis absorption capacity.",
                )

        st.markdown('<div class="net-mini-title">Top 10 Critical Sites and Scenario Playbooks</div>', unsafe_allow_html=True)
        ex_col5, ex_col6 = st.columns([1.4, 1.1])
        with ex_col5:
            with st.container(border=True):
                critical_view = net_critical_sites[["Site", "Region", "Criticality", "Subscribers Impact K", "MTTR Min", "Owner"]].sort_values("Criticality", ascending=False)
                st.dataframe(critical_view, use_container_width=True, hide_index=True)
                top_site = critical_view.iloc[0]
                render_net_ai_reco(
                    "Critical Site Governance",
                    f"{top_site['Site']} is currently the highest-criticality site with broad customer impact.",
                    "Assign weekly executive checkpoint on top critical sites with clear owner accountability.",
                    "Reduces probability of severe single-site service disruption.",
                    level="critical",
                )

        with ex_col6:
            with st.container(border=True):
                playbook = st.selectbox(
                    "Scenario Playbook",
                    ["Power Failure Cluster", "Backbone Fiber Cut", "Peak Congestion Event"],
                    index=0,
                    key="net_playbook_selector",
                )
                playbook_data = {
                    "Power Failure Cluster": {
                        "impact": "Availability -0.42pp, 18K subs impacted, ARR risk €0.74M",
                        "actions": "Activate backup chain, dispatch power crews, prioritize enterprise circuits.",
                        "window": "First 90 minutes critical",
                    },
                    "Backbone Fiber Cut": {
                        "impact": "Latency +6.8ms, 24K subs impacted, ARR risk €1.05M",
                        "actions": "Reroute traffic, trigger field splice teams, apply congestion controls.",
                        "window": "First 60 minutes critical",
                    },
                    "Peak Congestion Event": {
                        "impact": "Packet loss +0.14pp, NPS pressure in two regions",
                        "actions": "Traffic shaping, temporary capacity bump, proactive customer comms.",
                        "window": "First 45 minutes critical",
                    },
                }[playbook]
                st.markdown(dedent(f"""
                    <div class="net-ai-card warn" style="margin-top: 0.2rem;">
                        <div class="h">🧭 {playbook}</div>
                        <div class="b"><strong>Expected Impact:</strong> {playbook_data['impact']}</div>
                        <div class="b"><strong>Playbook Actions:</strong> {playbook_data['actions']}</div>
                        <div class="b"><strong>Response Window:</strong> {playbook_data['window']}</div>
                    </div>
                """), unsafe_allow_html=True)

    with net_tab_risk:
        st.markdown('<div class="net-title">Network Risk and Resilience Strategy</div>', unsafe_allow_html=True)
        st.markdown(dedent(f"""
            <div class="net-kpi-grid">
                <div class="net-kpi-card crit"><div class="k">Top Risk Driver</div><div class="v">{highest_risk['Risk Driver']}</div><div class="d">{highest_risk['Exposure Hr']:.0f} exposure hours</div></div>
                <div class="net-kpi-card warn"><div class="k">Risk Exposure</div><div class="v">{net_risk['Exposure Hr'].sum():.0f} h</div><div class="d">Total mapped exposure</div></div>
                <div class="net-kpi-card"><div class="k">Base Availability</div><div class="v">{net_scenario.loc[net_scenario['Scenario']=='Base', 'Availability %'].iloc[0]:.2f}%</div><div class="d">Most probable scenario</div></div>
                <div class="net-kpi-card"><div class="k">Upside Churn Save</div><div class="v">{net_scenario.loc[net_scenario['Scenario']=='Upside', 'Avoided Churn K'].iloc[0]:.1f}K</div><div class="d">Potential retained value</div></div>
            </div>
        """), unsafe_allow_html=True)

        rk_col1, rk_col2 = st.columns(2)
        with rk_col1:
            st.markdown('<div class="net-mini-title">Risk Exposure by Driver</div>', unsafe_allow_html=True)
            with st.container(border=True):
                risk_bar = alt.Chart(net_risk).mark_bar(cornerRadiusTopRight=7, cornerRadiusBottomRight=7, size=20).encode(
                    x=alt.X("Exposure Hr:Q", title="Exposure (hours)"),
                    y=alt.Y("Risk Driver:N", sort="-x", title=None),
                    color=alt.Color("Likelihood:Q", scale=alt.Scale(scheme="orangered"), legend=None),
                    tooltip=["Risk Driver:N", alt.Tooltip("Exposure Hr:Q", format=".0f"), alt.Tooltip("Likelihood:Q", format=".1f")],
                )
                risk_text = alt.Chart(net_risk).mark_text(align="left", dx=6, fontSize=10, color="#0F172A").encode(
                    x="Exposure Hr:Q", y=alt.Y("Risk Driver:N", sort="-x"), text=alt.Text("Exposure Hr:Q", format=".0f")
                )
                st.altair_chart(style_net_chart(risk_bar + risk_text, height=235), use_container_width=True)
                render_net_ai_reco(
                    "Risk Prioritization",
                    f"{highest_risk['Risk Driver']} has the highest exposure at {highest_risk['Exposure Hr']:.0f} hours.",
                    "Launch a focused resilience sprint for this driver with weekly board-level tracking.",
                    "Reduce service disruption probability in the highest-impact failure mode.",
                    level="critical",
                )

        with rk_col2:
            st.markdown('<div class="net-mini-title">Resilience Scenario Outlook</div>', unsafe_allow_html=True)
            with st.container(border=True):
                sc_bar = alt.Chart(net_scenario).mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6, size=56).encode(
                    x=alt.X("Scenario:N", title=None),
                    y=alt.Y("Availability %:Q", title="Availability (%)"),
                    color=alt.Color("Scenario:N", scale=alt.Scale(domain=["Downside", "Base", "Upside"], range=["#EF4444", "#3B82F6", "#10B981"]), legend=None),
                    tooltip=["Scenario:N", alt.Tooltip("Availability %:Q", format=".2f"), alt.Tooltip("Avoided Churn K:Q", format=".1f"), "Probability:N"],
                )
                sc_text = alt.Chart(net_scenario).mark_text(dy=-8, fontSize=11, fontWeight="bold", color="#0F172A").encode(
                    x="Scenario:N", y="Availability %:Q", text=alt.Text("Availability %:Q", format=".2f")
                )
                st.altair_chart(style_net_chart(sc_bar + sc_text, height=235), use_container_width=True)
                base_av = net_scenario.loc[net_scenario["Scenario"] == "Base", "Availability %"].iloc[0]
                render_net_ai_reco(
                    "Scenario Planning",
                    f"Base case targets {base_av:.2f}% availability with clear upside through resilience investments.",
                    "Pre-approve downside playbooks and protect budget for targeted redundancy upgrades.",
                    "Improve forecast confidence and secure customer experience under volatility.",
                )

        rk_col3, rk_col4 = st.columns(2)
        with rk_col3:
            st.markdown('<div class="net-mini-title">Risk Heat Matrix</div>', unsafe_allow_html=True)
            with st.container(border=True):
                risk_heat = alt.Chart(net_risk).mark_circle(opacity=0.86, stroke="#FFFFFF", strokeWidth=1.2).encode(
                    x=alt.X("Likelihood:Q", title="Likelihood"),
                    y=alt.Y("Exposure Hr:Q", title="Exposure (hours)"),
                    size=alt.Size("Exposure Hr:Q", scale=alt.Scale(range=[300, 1900]), legend=None),
                    color=alt.Color("Risk Driver:N", legend=alt.Legend(title=None), scale=alt.Scale(range=["#EF4444", "#F59E0B", "#3B82F6", "#10B981", "#6366F1"])),
                    tooltip=["Risk Driver:N", alt.Tooltip("Likelihood:Q", format=".1f"), alt.Tooltip("Exposure Hr:Q", format=".0f")],
                )
                risk_name = alt.Chart(net_risk).mark_text(dy=-10, fontSize=9, color="#1E293B").encode(
                    x="Likelihood:Q", y="Exposure Hr:Q", text="Risk Driver:N"
                )
                st.altair_chart(style_net_chart(risk_heat + risk_name, height=235), use_container_width=True)
                high_quadrant = net_risk.sort_values(["Likelihood", "Exposure Hr"], ascending=False).iloc[0]
                render_net_ai_reco(
                    "Risk Concentration",
                    f"{high_quadrant['Risk Driver']} is in the highest likelihood-exposure quadrant.",
                    "Escalate this risk into weekly executive review with pre-agreed containment triggers.",
                    "Cuts the probability of high-severity service disruption.",
                    level="critical",
                )

        with rk_col4:
            st.markdown('<div class="net-mini-title">Mitigation Value vs Cost</div>', unsafe_allow_html=True)
            with st.container(border=True):
                mitigation_df = net_risk.copy()
                mitigation_df["Mitigation Cost K"] = (mitigation_df["Exposure Hr"] * 0.85).round(1)
                mitigation_df["Avoided Loss K"] = (mitigation_df["Exposure Hr"] * mitigation_df["Likelihood"] * 0.62).round(1)
                mitigation_df["ROI x"] = (mitigation_df["Avoided Loss K"] / mitigation_df["Mitigation Cost K"]).round(2)
                roi_bar = alt.Chart(mitigation_df).mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6, size=24, color="#10B981").encode(
                    x=alt.X("Risk Driver:N", sort="-y", title=None),
                    y=alt.Y("ROI x:Q", title="Mitigation ROI (x)"),
                    tooltip=["Risk Driver:N", alt.Tooltip("ROI x:Q", format=".2f"), alt.Tooltip("Mitigation Cost K:Q", format=".1f"), alt.Tooltip("Avoided Loss K:Q", format=".1f")],
                )
                roi_target = alt.Chart(pd.DataFrame({"y": [1.3]})).mark_rule(color="#94A3B8", strokeDash=[4, 4]).encode(y="y:Q")
                roi_text = alt.Chart(mitigation_df).mark_text(dy=-8, fontSize=9, color="#0F172A").encode(
                    x=alt.X("Risk Driver:N", sort="-y"),
                    y="ROI x:Q",
                    text=alt.Text("ROI x:Q", format=".2f"),
                )
                st.altair_chart(style_net_chart(roi_target + roi_bar + roi_text, height=235), use_container_width=True)
                top_roi = mitigation_df.loc[mitigation_df["ROI x"].idxmax()]
                render_net_ai_reco(
                    "Mitigation Capital Allocation",
                    f"{top_roi['Risk Driver']} shows the strongest mitigation ROI at {top_roi['ROI x']:.2f}x.",
                    f"Prioritize budget release for {top_roi['Risk Driver']} and phase lower-ROI initiatives.",
                    "Increases resilience returns per unit of mitigation spend.",
                )

        st.markdown('<div class="net-title">Infrastructure Risk Exposure</div>', unsafe_allow_html=True)
        rk_inf_col1, rk_inf_col2 = st.columns(2)
        with rk_inf_col1:
            st.markdown('<div class="net-mini-title">Single Points of Failure by Region</div>', unsafe_allow_html=True)
            with st.container(border=True):
                spof_bar = alt.Chart(net_spof).mark_bar(cornerRadiusTopRight=7, cornerRadiusBottomRight=7, size=20).encode(
                    x=alt.X("SPOF Count:Q", title="Single Points of Failure"),
                    y=alt.Y("Region:N", sort="-x", title=None),
                    color=alt.Color("Criticality:Q", scale=alt.Scale(scheme="orangered"), legend=alt.Legend(title="Criticality")),
                    tooltip=["Region:N", alt.Tooltip("SPOF Count:Q", format=".0f"), alt.Tooltip("Subscribers K:Q", format=".0f"), alt.Tooltip("Criticality:Q", format=".1f")],
                )
                spof_text = alt.Chart(net_spof).mark_text(align="left", dx=6, fontSize=10, color="#0F172A").encode(
                    x="SPOF Count:Q", y=alt.Y("Region:N", sort="-x"), text=alt.Text("Subscribers K:Q", format=".0f")
                )
                st.altair_chart(style_net_chart(spof_bar + spof_text, height=235), use_container_width=True)
                top_spof = net_spof.loc[net_spof["SPOF Count"].idxmax()]
                render_net_ai_reco(
                    "SPOF Exposure",
                    f"{top_spof['Region']} has the highest single-point-of-failure count with high customer impact potential.",
                    f"Deploy redundancy projects in {top_spof['Region']} and sequence high-risk circuits first.",
                    "Lowers catastrophic outage probability and protects subscriber experience.",
                    level="critical",
                )

        with rk_inf_col2:
            st.markdown('<div class="net-mini-title">Backup Autonomy vs Power Instability</div>', unsafe_allow_html=True)
            with st.container(border=True):
                power_scatter = alt.Chart(net_resilience_sites).mark_circle(opacity=0.88, stroke="#FFFFFF", strokeWidth=1.2).encode(
                    x=alt.X("Backup Autonomy Hr:Q", title="Backup Autonomy (hours)"),
                    y=alt.Y("Power Events / Mo:Q", title="Power Events / Month"),
                    size=alt.Size("Critical Sites:Q", scale=alt.Scale(range=[260, 1400]), legend=None),
                    color=alt.Color("Region:N", legend=alt.Legend(title=None), scale=alt.Scale(range=["#3B82F6", "#10B981", "#F59E0B", "#EF4444", "#6366F1", "#14B8A6"])),
                    tooltip=["Region:N", alt.Tooltip("Backup Autonomy Hr:Q", format=".1f"), alt.Tooltip("Power Events / Mo:Q", format=".1f"), alt.Tooltip("Critical Sites:Q", format=".0f")],
                )
                power_label = alt.Chart(net_resilience_sites).mark_text(dy=-10, fontSize=9, color="#1E293B").encode(
                    x="Backup Autonomy Hr:Q", y="Power Events / Mo:Q", text="Region:N"
                )
                st.altair_chart(style_net_chart(power_scatter + power_label, height=235), use_container_width=True)
                weakest_power = net_resilience_sites.sort_values(["Backup Autonomy Hr", "Power Events / Mo"], ascending=[True, False]).iloc[0]
                render_net_ai_reco(
                    "Power Resilience Priority",
                    f"{weakest_power['Region']} has the weakest backup autonomy under high power-event volatility.",
                    f"Increase backup autonomy and power hardening at critical sites in {weakest_power['Region']}.",
                    "Strengthens continuity for infrastructure nodes exposed to utility instability.",
                    level="warning",
                )

        st.markdown(dedent(f"""
            <div style="background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%); border-radius: 10px; padding: 0.82rem 0.95rem; margin-top: 0.55rem; border-left: 4px solid #F59E0B;">
                <div style="display: flex; align-items: center;">
                    <span style="font-size: 1.35rem; margin-right: 0.55rem;">⚠️</span>
                    <div>
                        <strong style="color: #92400E;">Urgent: {highest_risk['Risk Driver']} at {highest_risk['Exposure Hr']:.0f} exposure hours</strong>
                        <div style="color: #B45309; font-size: 0.84rem;">Most vulnerable region: {weakest_region['Region']} ({weakest_region['Availability %']:.2f}% uptime) · execute mitigation in next operating cycle</div>
                    </div>
                </div>
            </div>
        """), unsafe_allow_html=True)

    with net_tab_aiml:
        import numpy as np
        np.random.seed(42)

        anomaly_data = pd.DataFrame({
            "Timestamp": pd.date_range("2025-03-01 00:00", periods=168, freq="h"),
            "Traffic Gbps": [45 + 15*np.sin(i/24*2*np.pi) + np.random.normal(0, 3) + (25 if i in [72, 73, 74, 145] else 0) for i in range(168)],
            "Latency ms": [22 + 4*np.sin(i/24*2*np.pi) + np.random.normal(0, 1.5) + (18 if i in [72, 73, 74] else 0) + (12 if i == 145 else 0) for i in range(168)],
            "Packet Loss %": [0.15 + 0.05*np.sin(i/24*2*np.pi) + np.random.normal(0, 0.02) + (0.8 if i in [72, 73, 74] else 0) + (0.4 if i == 145 else 0) for i in range(168)],
        })
        anomaly_data["Hour"] = anomaly_data["Timestamp"].dt.strftime("%b %d %H:00")
        anomaly_data["Is Anomaly"] = ((anomaly_data["Traffic Gbps"] > 70) | (anomaly_data["Latency ms"] > 35) | (anomaly_data["Packet Loss %"] > 0.5)).astype(int)
        anomaly_data["Anomaly Score"] = np.clip((anomaly_data["Traffic Gbps"] - 60) / 20 + (anomaly_data["Latency ms"] - 30) / 10 + (anomaly_data["Packet Loss %"] - 0.3) / 0.3, 0, 1)

        predictive_assets = pd.DataFrame({
            "Asset ID": ["OLT-MAD-001", "OLT-BCN-003", "TRANS-VAL-007", "OLT-BIL-002", "CORE-MAD-001", "OLT-SEV-004", "TRANS-BCN-012", "OLT-MAL-001"],
            "Asset Type": ["OLT", "OLT", "Transport Node", "OLT", "Core Router", "OLT", "Transport Node", "OLT"],
            "Region": ["Madrid", "Barcelona", "Valencia", "Bilbao", "Madrid", "Sevilla", "Barcelona", "Málaga"],
            "Health Score": [94, 67, 82, 91, 88, 72, 58, 96],
            "Failure Probability %": [3, 28, 12, 5, 8, 22, 38, 2],
            "Days to Failure": [180, 12, 45, 120, 85, 21, 8, 210],
            "Anomalies 30d": [2, 18, 7, 3, 5, 14, 24, 1],
            "Last Maintenance": ["2025-01-15", "2024-09-20", "2024-11-05", "2025-02-01", "2024-12-10", "2024-10-15", "2024-08-22", "2025-02-20"],
            "Subscribers Impacted K": [45, 82, 120, 38, 350, 55, 95, 28],
        })
        predictive_assets["Risk Category"] = pd.cut(predictive_assets["Failure Probability %"], bins=[0, 10, 25, 100], labels=["Low", "Medium", "High"])
        predictive_assets["Urgency"] = pd.cut(predictive_assets["Days to Failure"], bins=[0, 14, 30, 365], labels=["Critical", "Warning", "Normal"])

        ml_model_perf = pd.DataFrame({
            "Model": ["Anomaly Detection", "Failure Prediction", "Capacity Forecast", "Incident Classification"],
            "Accuracy": [94.2, 89.7, 91.3, 96.1],
            "Precision": [92.1, 87.4, 89.8, 94.5],
            "Recall": [96.8, 91.2, 93.1, 97.2],
            "F1Score": [0.94, 0.89, 0.91, 0.96],
            "TrainingDate": ["2025-02-28", "2025-02-25", "2025-02-20", "2025-03-01"],
            "PredictionsToday": [1247, 856, 423, 2891],
        })

        anomaly_by_type = pd.DataFrame({
            "Anomaly Type": ["Traffic Spike", "Latency Surge", "Packet Loss", "CPU Overload", "Memory Pressure", "Link Saturation"],
            "Count 7d": [23, 18, 12, 8, 5, 15],
            "Avg Duration Min": [45, 28, 62, 35, 48, 55],
            "Auto-Resolved %": [78, 85, 45, 92, 88, 62],
            "Severity": [3, 4, 5, 2, 2, 4],
        })

        maintenance_schedule = pd.DataFrame({
            "Asset": ["OLT-BCN-003", "TRANS-BCN-012", "OLT-SEV-004", "TRANS-VAL-007", "OLT-BIL-002"],
            "Scheduled Date": ["2025-03-08", "2025-03-10", "2025-03-15", "2025-03-22", "2025-04-05"],
            "Maintenance Type": ["Preventive", "Emergency", "Preventive", "Preventive", "Routine"],
            "Estimated Duration Hr": [4, 6, 3, 4, 2],
            "Cost €K": [8.5, 15.2, 6.8, 7.2, 3.5],
            "Avoided Outage Hr": [48, 72, 36, 24, 12],
            "ROI x": [5.6, 4.7, 5.3, 3.3, 3.4],
        })

        total_anomalies = anomaly_data["Is Anomaly"].sum()
        critical_assets = len(predictive_assets[predictive_assets["Urgency"] == "Critical"])
        avg_model_accuracy = ml_model_perf["Accuracy"].mean()
        prevented_outages = maintenance_schedule["Avoided Outage Hr"].sum()

        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1E1B4B 0%, #312E81 50%, #4338CA 100%); border-radius: 16px; padding: 1.2rem; margin-bottom: 1rem; box-shadow: 0 8px 32px rgba(67, 56, 202, 0.3);">
            <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                <span style="font-size: 2rem; margin-right: 0.8rem;">🧠</span>
                <div>
                    <div style="color: #E0E7FF; font-size: 1.4rem; font-weight: 700;">AI-Powered Network Intelligence</div>
                    <div style="color: #A5B4FC; font-size: 0.85rem;">Real-time anomaly detection & predictive maintenance powered by ML models</div>
                </div>
            </div>
            <div style="display: grid; grid-template-columns: repeat(5, 1fr); gap: 1rem;">
                <div style="background: rgba(255,255,255,0.1); border-radius: 12px; padding: 0.9rem; text-align: center; backdrop-filter: blur(10px);">
                    <div style="color: #C7D2FE; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.5px;">Anomalies (7d)</div>
                    <div style="color: #FFFFFF; font-size: 1.8rem; font-weight: 800;">{total_anomalies}</div>
                    <div style="color: {'#FCA5A5' if total_anomalies > 5 else '#86EFAC'}; font-size: 0.75rem;">{'↑ Above baseline' if total_anomalies > 5 else '✓ Normal range'}</div>
                </div>
                <div style="background: rgba(255,255,255,0.1); border-radius: 12px; padding: 0.9rem; text-align: center; backdrop-filter: blur(10px);">
                    <div style="color: #C7D2FE; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.5px;">Critical Assets</div>
                    <div style="color: {'#FCA5A5' if critical_assets > 0 else '#FFFFFF'}; font-size: 1.8rem; font-weight: 800;">{critical_assets}</div>
                    <div style="color: #FBBF24; font-size: 0.75rem;">Require immediate action</div>
                </div>
                <div style="background: rgba(255,255,255,0.1); border-radius: 12px; padding: 0.9rem; text-align: center; backdrop-filter: blur(10px);">
                    <div style="color: #C7D2FE; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.5px;">ML Model Accuracy</div>
                    <div style="color: #86EFAC; font-size: 1.8rem; font-weight: 800;">{avg_model_accuracy:.1f}%</div>
                    <div style="color: #86EFAC; font-size: 0.75rem;">↑ +2.3% vs last month</div>
                </div>
                <div style="background: rgba(255,255,255,0.1); border-radius: 12px; padding: 0.9rem; text-align: center; backdrop-filter: blur(10px);">
                    <div style="color: #C7D2FE; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.5px;">Outages Prevented</div>
                    <div style="color: #FFFFFF; font-size: 1.8rem; font-weight: 800;">{prevented_outages}h</div>
                    <div style="color: #86EFAC; font-size: 0.75rem;">€{prevented_outages * 2.5:.0f}K saved</div>
                </div>
                <div style="background: rgba(255,255,255,0.1); border-radius: 12px; padding: 0.9rem; text-align: center; backdrop-filter: blur(10px);">
                    <div style="color: #C7D2FE; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.5px;">Predictions Today</div>
                    <div style="color: #FFFFFF; font-size: 1.8rem; font-weight: 800;">{ml_model_perf['PredictionsToday'].sum():,}</div>
                    <div style="color: #A5B4FC; font-size: 0.75rem;">Active ML inferences</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="net-title">🔍 Real-Time Anomaly Detection</div>', unsafe_allow_html=True)
        anom_col1, anom_col2 = st.columns([2, 1])

        with anom_col1:
            st.markdown('<div class="net-mini-title">Network Metrics with Anomaly Overlay (7-Day View)</div>', unsafe_allow_html=True)
            with st.container(border=True):
                base_traffic = alt.Chart(anomaly_data).mark_area(opacity=0.3, color="#3B82F6").encode(
                    x=alt.X("Hour:N", title=None, axis=alt.Axis(labelAngle=-45, labelFontSize=8)),
                    y=alt.Y("Traffic Gbps:Q", title="Traffic (Gbps)"),
                    tooltip=["Hour:N", alt.Tooltip("Traffic Gbps:Q", format=".1f")],
                )
                traffic_line = alt.Chart(anomaly_data).mark_line(strokeWidth=2, color="#2563EB").encode(
                    x="Hour:N", y="Traffic Gbps:Q",
                )
                anomaly_points = alt.Chart(anomaly_data[anomaly_data["Is Anomaly"] == 1]).mark_circle(size=200, color="#EF4444", opacity=0.9).encode(
                    x="Hour:N", y="Traffic Gbps:Q",
                    tooltip=["Hour:N", alt.Tooltip("Traffic Gbps:Q", format=".1f"), alt.Tooltip("Anomaly Score:Q", format=".2f")],
                )
                threshold_line = alt.Chart(pd.DataFrame({"y": [70]})).mark_rule(strokeDash=[6, 4], color="#F59E0B", strokeWidth=2).encode(y="y:Q")
                st.altair_chart(style_net_chart(base_traffic + traffic_line + anomaly_points + threshold_line, height=200), use_container_width=True)

                latency_area = alt.Chart(anomaly_data).mark_area(opacity=0.3, color="#10B981").encode(
                    x=alt.X("Hour:N", title=None, axis=alt.Axis(labelAngle=-45, labelFontSize=8)),
                    y=alt.Y("Latency ms:Q", title="Latency (ms)"),
                )
                latency_line = alt.Chart(anomaly_data).mark_line(strokeWidth=2, color="#059669").encode(x="Hour:N", y="Latency ms:Q")
                latency_anomaly = alt.Chart(anomaly_data[anomaly_data["Latency ms"] > 35]).mark_circle(size=180, color="#EF4444").encode(
                    x="Hour:N", y="Latency ms:Q",
                    tooltip=["Hour:N", alt.Tooltip("Latency ms:Q", format=".1f")],
                )
                latency_thresh = alt.Chart(pd.DataFrame({"y": [35]})).mark_rule(strokeDash=[6, 4], color="#F59E0B", strokeWidth=2).encode(y="y:Q")
                st.altair_chart(style_net_chart(latency_area + latency_line + latency_anomaly + latency_thresh, height=140), use_container_width=True)

                render_net_ai_reco(
                    "Anomaly Pattern Detected",
                    f"{total_anomalies} anomalies detected in 7 days. Major incident on Mar 4 (72-74h) correlated across traffic, latency, and packet loss.",
                    "ML model flagged root cause as upstream peering congestion. Auto-triggered traffic rerouting.",
                    "Reduced mean-time-to-detect (MTTD) from 15 min to 45 seconds.",
                )

        with anom_col2:
            st.markdown('<div class="net-mini-title">Anomaly Distribution by Type</div>', unsafe_allow_html=True)
            with st.container(border=True):
                anom_bar = alt.Chart(anomaly_by_type).mark_bar(cornerRadiusTopRight=6, cornerRadiusBottomRight=6, size=18).encode(
                    x=alt.X("Count 7d:Q", title="Anomalies (7d)"),
                    y=alt.Y("Anomaly Type:N", sort="-x", title=None),
                    color=alt.Color("Severity:Q", scale=alt.Scale(scheme="orangered"), legend=None),
                    tooltip=["Anomaly Type:N", "Count 7d:Q", alt.Tooltip("Avg Duration Min:Q", format=".0f"), alt.Tooltip("Auto-Resolved %:Q", format=".0f")],
                )
                st.altair_chart(style_net_chart(anom_bar, height=220), use_container_width=True)
                render_net_ai_reco(
                    "Self-Healing Rate",
                    f"Traffic spikes auto-resolved {anomaly_by_type[anomaly_by_type['Anomaly Type']=='Traffic Spike']['Auto-Resolved %'].iloc[0]}% of the time via ML-triggered remediation.",
                    "Expand auto-remediation playbooks to packet loss scenarios (currently 45% auto-resolved).",
                    "Target 80%+ auto-resolution across all anomaly types.",
                    level="warning",
                )

        st.markdown('<div class="net-title">🔮 Predictive Maintenance Intelligence</div>', unsafe_allow_html=True)
        pred_col1, pred_col2 = st.columns(2)

        with pred_col1:
            st.markdown('<div class="net-mini-title">Asset Health vs Failure Probability</div>', unsafe_allow_html=True)
            with st.container(border=True):
                health_scatter = alt.Chart(predictive_assets).mark_circle(opacity=0.85, stroke="#FFFFFF", strokeWidth=1.5).encode(
                    x=alt.X("Health Score:Q", title="Health Score", scale=alt.Scale(domain=[50, 100])),
                    y=alt.Y("Failure Probability %:Q", title="Failure Probability (%)"),
                    size=alt.Size("Subscribers Impacted K:Q", scale=alt.Scale(range=[200, 1200]), legend=alt.Legend(title="Subs (K)")),
                    color=alt.Color("Risk Category:N", scale=alt.Scale(domain=["Low", "Medium", "High"], range=["#10B981", "#F59E0B", "#EF4444"]), legend=alt.Legend(title="Risk")),
                    tooltip=["Asset ID:N", "Asset Type:N", "Region:N", alt.Tooltip("Health Score:Q"), alt.Tooltip("Failure Probability %:Q", format=".0f"), alt.Tooltip("Days to Failure:Q"), alt.Tooltip("Subscribers Impacted K:Q", format=",")],
                )
                health_labels = alt.Chart(predictive_assets[predictive_assets["Failure Probability %"] > 15]).mark_text(dy=-12, fontSize=9, color="#1E293B").encode(
                    x="Health Score:Q", y="Failure Probability %:Q", text="Asset ID:N"
                )
                danger_zone = alt.Chart(pd.DataFrame({"x": [50], "x2": [75], "y": [20], "y2": [50]})).mark_rect(opacity=0.1, color="#EF4444").encode(
                    x="x:Q", x2="x2:Q", y="y:Q", y2="y2:Q"
                )
                st.altair_chart(style_net_chart(danger_zone + health_scatter + health_labels, height=280), use_container_width=True)
                highest_risk = predictive_assets.sort_values("Failure Probability %", ascending=False).iloc[0]
                render_net_ai_reco(
                    "Critical Asset Alert",
                    f"{highest_risk['Asset ID']} has {highest_risk['Failure Probability %']}% failure probability, impacting {highest_risk['Subscribers Impacted K']}K subscribers.",
                    f"Schedule emergency maintenance within {highest_risk['Days to Failure']} days. Pre-position spare parts.",
                    "Prevent unplanned outage affecting {highest_risk['Subscribers Impacted K']}K customers.",
                    level="critical",
                )

        with pred_col2:
            st.markdown('<div class="net-mini-title">Days to Predicted Failure</div>', unsafe_allow_html=True)
            with st.container(border=True):
                sorted_assets = predictive_assets.sort_values("Days to Failure")
                days_bar = alt.Chart(sorted_assets).mark_bar(cornerRadiusTopRight=6, cornerRadiusBottomRight=6, size=22).encode(
                    x=alt.X("Days to Failure:Q", title="Days to Predicted Failure"),
                    y=alt.Y("Asset ID:N", sort=alt.EncodingSortField(field="Days to Failure", order="ascending"), title=None),
                    color=alt.Color("Urgency:N", scale=alt.Scale(domain=["Critical", "Warning", "Normal"], range=["#EF4444", "#F59E0B", "#10B981"]), legend=alt.Legend(title="Urgency")),
                    tooltip=["Asset ID:N", "Asset Type:N", "Region:N", "Days to Failure:Q", alt.Tooltip("Failure Probability %:Q", format=".0f")],
                )
                critical_line = alt.Chart(pd.DataFrame({"x": [14]})).mark_rule(strokeDash=[4, 4], color="#EF4444", strokeWidth=2).encode(x="x:Q")
                warning_line = alt.Chart(pd.DataFrame({"x": [30]})).mark_rule(strokeDash=[4, 4], color="#F59E0B", strokeWidth=2).encode(x="x:Q")
                st.altair_chart(style_net_chart(days_bar + critical_line + warning_line, height=280), use_container_width=True)
                critical_count = len(predictive_assets[predictive_assets["Days to Failure"] <= 14])
                render_net_ai_reco(
                    "Maintenance Urgency",
                    f"{critical_count} assets predicted to fail within 14 days. {len(predictive_assets[predictive_assets['Days to Failure'] <= 30])} within 30 days.",
                    "Accelerate preventive maintenance for TRANS-BCN-012 and OLT-BCN-003 immediately.",
                    "Reduce unplanned outages by 65% through proactive intervention.",
                    level="critical" if critical_count > 1 else "warning",
                )

        st.markdown('<div class="net-title">📅 AI-Optimized Maintenance Schedule</div>', unsafe_allow_html=True)
        maint_col1, maint_col2 = st.columns([1.5, 1])

        with maint_col1:
            st.markdown('<div class="net-mini-title">Scheduled Preventive Maintenance</div>', unsafe_allow_html=True)
            with st.container(border=True):
                st.dataframe(
                    maintenance_schedule.style.format({
                        "Estimated Duration Hr": "{:.0f}h",
                        "Cost €K": "€{:.1f}K",
                        "Avoided Outage Hr": "{:.0f}h",
                        "ROI x": "{:.1f}x",
                    }).background_gradient(subset=["ROI x"], cmap="Greens").map(
                        lambda x: "background-color: #FEE2E2; color: #991B1B;" if x == "Emergency" else "", subset=["Maintenance Type"]
                    ),
                    use_container_width=True,
                    hide_index=True,
                    height=220,
                )
                render_net_ai_reco(
                    "Maintenance ROI",
                    f"Scheduled maintenance will prevent {prevented_outages}h of outages, saving €{prevented_outages * 2.5:.0f}K in SLA penalties.",
                    "AI optimizer recommends consolidating BCN maintenance windows to minimize customer impact.",
                    "Average maintenance ROI of {:.1f}x across scheduled interventions.".format(maintenance_schedule["ROI x"].mean()),
                )

        with maint_col2:
            st.markdown('<div class="net-mini-title">Maintenance Cost vs Avoided Loss</div>', unsafe_allow_html=True)
            with st.container(border=True):
                maint_scatter = alt.Chart(maintenance_schedule).mark_circle(size=300, opacity=0.85, stroke="#FFFFFF", strokeWidth=1.5).encode(
                    x=alt.X("Cost €K:Q", title="Maintenance Cost (€K)"),
                    y=alt.Y("Avoided Outage Hr:Q", title="Avoided Outage (hours)"),
                    color=alt.Color("Maintenance Type:N", scale=alt.Scale(domain=["Emergency", "Preventive", "Routine"], range=["#EF4444", "#F59E0B", "#10B981"]), legend=alt.Legend(title=None)),
                    tooltip=["Asset:N", "Maintenance Type:N", alt.Tooltip("Cost €K:Q", format="€.1f"), alt.Tooltip("Avoided Outage Hr:Q", format=".0f"), alt.Tooltip("ROI x:Q", format=".1f")],
                )
                maint_labels = alt.Chart(maintenance_schedule).mark_text(dy=-12, fontSize=9, color="#1E293B").encode(
                    x="Cost €K:Q", y="Avoided Outage Hr:Q", text="Asset:N"
                )
                st.altair_chart(style_net_chart(maint_scatter + maint_labels, height=200), use_container_width=True)

        st.markdown('<div class="net-title">🧠 ML Model Performance Dashboard</div>', unsafe_allow_html=True)
        ml_col1, ml_col2, ml_col3 = st.columns(3)

        with ml_col1:
            st.markdown('<div class="net-mini-title">Model Accuracy Comparison</div>', unsafe_allow_html=True)
            with st.container(border=True):
                accuracy_bar = alt.Chart(ml_model_perf).mark_bar(cornerRadiusTopRight=8, cornerRadiusBottomRight=8, size=20, color="#6366F1").encode(
                    x=alt.X("Accuracy:Q", title="Accuracy (%)", scale=alt.Scale(domain=[80, 100])),
                    y=alt.Y("Model:N", sort="-x", title=None),
                    tooltip=["Model:N", alt.Tooltip("Accuracy:Q", format=".1f"), alt.Tooltip("F1Score:Q", format=".2f")],
                )
                target_line = alt.Chart(pd.DataFrame({"x": [90]})).mark_rule(strokeDash=[4, 4], color="#10B981", strokeWidth=2).encode(x="x:Q")
                acc_text = alt.Chart(ml_model_perf).mark_text(align="left", dx=4, fontSize=10, color="#1E293B").encode(
                    x="Accuracy:Q", y=alt.Y("Model:N", sort="-x"), text=alt.Text("Accuracy:Q", format=".1f")
                )
                st.altair_chart(style_net_chart(accuracy_bar + target_line + acc_text, height=180), use_container_width=True)

        with ml_col2:
            st.markdown('<div class="net-mini-title">Precision vs Recall</div>', unsafe_allow_html=True)
            with st.container(border=True):
                pr_scatter = alt.Chart(ml_model_perf).mark_circle(size=250, opacity=0.85, stroke="#FFFFFF", strokeWidth=1.5).encode(
                    x=alt.X("Precision:Q", title="Precision (%)", scale=alt.Scale(domain=[85, 100])),
                    y=alt.Y("Recall:Q", title="Recall (%)", scale=alt.Scale(domain=[85, 100])),
                    color=alt.Color("Model:N", legend=None),
                    tooltip=["Model:N", alt.Tooltip("Precision:Q", format=".1f"), alt.Tooltip("Recall:Q", format=".1f"), alt.Tooltip("F1Score:Q", format=".2f")],
                )
                pr_labels = alt.Chart(ml_model_perf).mark_text(dy=-10, fontSize=8, color="#1E293B").encode(
                    x="Precision:Q", y="Recall:Q", text="Model:N"
                )
                st.altair_chart(style_net_chart(pr_scatter + pr_labels, height=180), use_container_width=True)

        with ml_col3:
            st.markdown('<div class="net-mini-title">Daily Predictions Volume</div>', unsafe_allow_html=True)
            with st.container(border=True):
                pred_bar = alt.Chart(ml_model_perf).mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6, size=35).encode(
                    x=alt.X("Model:N", title=None, axis=alt.Axis(labelAngle=-20, labelFontSize=9)),
                    y=alt.Y("PredictionsToday:Q", title="Predictions"),
                    color=alt.Color("Model:N", legend=None, scale=alt.Scale(scheme="category10")),
                    tooltip=["Model:N", alt.Tooltip("PredictionsToday:Q", format=","), "TrainingDate:N"],
                )
                pred_text = alt.Chart(ml_model_perf).mark_text(dy=-8, fontSize=9, color="#1E293B").encode(
                    x="Model:N", y="PredictionsToday:Q", text=alt.Text("PredictionsToday:Q", format=",")
                )
                st.altair_chart(style_net_chart(pred_bar + pred_text, height=180), use_container_width=True)

        render_net_ai_reco(
            "ML Platform Health",
            f"All 4 models exceeding 89% accuracy target. Total {ml_model_perf['PredictionsToday'].sum():,} predictions processed today.",
            "Schedule model retraining for Failure Prediction (oldest training date) to maintain accuracy.",
            "Continuous model monitoring ensures reliable predictive capabilities.",
        )

        st.markdown('<div class="net-title">🌦️ External Data Correlation · Snowflake Marketplace</div>', unsafe_allow_html=True)

        weather_incidents = pd.DataFrame({
            "Date": pd.date_range("2025-02-01", periods=28, freq="D"),
            "Wind Speed kmh": [15, 18, 22, 45, 68, 72, 35, 20, 18, 25, 30, 55, 48, 22, 18, 15, 20, 62, 75, 42, 28, 22, 18, 20, 35, 45, 52, 25],
            "Precipitation mm": [0, 2, 5, 18, 32, 28, 12, 0, 0, 3, 8, 22, 15, 0, 0, 0, 5, 25, 38, 18, 8, 2, 0, 0, 12, 18, 28, 5],
            "Temperature C": [12, 11, 10, 8, 6, 5, 9, 12, 14, 13, 11, 7, 8, 12, 15, 16, 14, 9, 4, 7, 10, 13, 15, 16, 12, 10, 8, 11],
            "Fiber Cuts": [0, 0, 0, 2, 5, 4, 1, 0, 0, 0, 1, 3, 2, 0, 0, 0, 0, 4, 6, 2, 1, 0, 0, 0, 1, 2, 3, 0],
            "Equipment Failures": [1, 0, 1, 1, 3, 2, 1, 0, 1, 0, 1, 2, 1, 0, 0, 1, 0, 2, 4, 1, 1, 0, 0, 0, 1, 1, 2, 0],
            "Power Outages": [0, 0, 0, 1, 2, 3, 1, 0, 0, 0, 0, 2, 1, 0, 0, 0, 0, 2, 3, 1, 0, 0, 0, 0, 1, 1, 2, 0],
        })
        weather_incidents["Day"] = weather_incidents["Date"].dt.strftime("%b %d")
        weather_incidents["Total Incidents"] = weather_incidents["Fiber Cuts"] + weather_incidents["Equipment Failures"]
        weather_incidents["Storm Day"] = (weather_incidents["Wind Speed kmh"] > 50) | (weather_incidents["Precipitation mm"] > 20)

        construction_risk = pd.DataFrame({
            "Region": ["Madrid", "Barcelona", "Valencia", "Bilbao", "Sevilla", "Málaga"],
            "Active Permits": [145, 128, 67, 42, 55, 38],
            "Fiber Route Proximity": [23, 18, 12, 8, 11, 6],
            "Predicted Dig-ups": [8, 6, 3, 2, 4, 2],
            "Risk Score": [85, 72, 45, 38, 52, 28],
        })

        mobility_capacity = pd.DataFrame({
            "Hour": list(range(24)),
            "Population Density Index": [0.3, 0.2, 0.15, 0.12, 0.15, 0.25, 0.55, 0.85, 0.95, 0.88, 0.82, 0.85, 0.9, 0.88, 0.85, 0.82, 0.88, 0.95, 0.92, 0.85, 0.72, 0.58, 0.45, 0.35],
            "Network Utilization": [22, 18, 15, 12, 14, 25, 52, 78, 88, 82, 75, 78, 85, 82, 78, 75, 82, 92, 88, 80, 68, 55, 42, 28],
            "Predicted Demand": [24, 20, 16, 13, 15, 27, 55, 82, 92, 86, 78, 82, 88, 85, 82, 78, 85, 95, 92, 84, 72, 58, 45, 30],
        })

        st.markdown("""
        <div style="background: linear-gradient(135deg, #EEF2FF 0%, #E0E7FF 100%); border-radius: 12px; padding: 1rem; margin-bottom: 1rem; border-left: 4px solid #6366F1;">
            <div style="display: flex; align-items: center;">
                <span style="font-size: 1.3rem; margin-right: 0.6rem;">❄️</span>
                <div>
                    <strong style="color: #3730A3;">Powered by Snowflake Marketplace</strong>
                    <div style="color: #4338CA; font-size: 0.82rem;">Enriching network intelligence with external data: Weather Source, Precisely Geospatial, SafeGraph Mobility, GridStatus Power</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        ext_col1, ext_col2 = st.columns(2)

        with ext_col1:
            st.markdown('<div class="net-mini-title">Weather Impact on Network Incidents</div>', unsafe_allow_html=True)
            with st.container(border=True):
                weather_base = alt.Chart(weather_incidents).mark_area(opacity=0.3, color="#3B82F6").encode(
                    x=alt.X("Day:N", title=None, axis=alt.Axis(labelAngle=-45, labelFontSize=8)),
                    y=alt.Y("Wind Speed kmh:Q", title="Wind Speed (km/h)"),
                )
                weather_line = alt.Chart(weather_incidents).mark_line(strokeWidth=2, color="#2563EB").encode(
                    x="Day:N", y="Wind Speed kmh:Q",
                )
                incident_bars = alt.Chart(weather_incidents).mark_bar(color="#EF4444", opacity=0.7, size=8).encode(
                    x="Day:N",
                    y=alt.Y("Total Incidents:Q", title="Incidents", axis=alt.Axis(titleColor="#EF4444")),
                    tooltip=["Day:N", "Wind Speed kmh:Q", "Precipitation mm:Q", "Fiber Cuts:Q", "Equipment Failures:Q"],
                )
                storm_points = alt.Chart(weather_incidents[weather_incidents["Storm Day"]]).mark_point(size=100, color="#F59E0B", shape="triangle-up", filled=True).encode(
                    x="Day:N", y="Wind Speed kmh:Q",
                    tooltip=["Day:N", alt.Tooltip("Wind Speed kmh:Q"), alt.Tooltip("Precipitation mm:Q"), alt.Tooltip("Fiber Cuts:Q")],
                )
                st.altair_chart(style_net_chart(alt.layer(weather_base, weather_line, storm_points, incident_bars).resolve_scale(y="independent"), height=220), use_container_width=True)

                storm_days = weather_incidents["Storm Day"].sum()
                storm_incidents = weather_incidents[weather_incidents["Storm Day"]]["Total Incidents"].sum()
                correlation = weather_incidents["Wind Speed kmh"].corr(weather_incidents["Total Incidents"])
                render_net_ai_reco(
                    "Weather Correlation",
                    f"{storm_days} storm days caused {storm_incidents} incidents (correlation: {correlation:.2f}). Data from Weather Source via Snowflake Marketplace.",
                    "Pre-position repair crews 24h before predicted storms. ML model triggers alerts at >50 km/h wind forecast.",
                    "Reduce storm-related MTTR by 40% through proactive response.",
                    level="warning",
                )

        with ext_col2:
            st.markdown('<div class="net-mini-title">Construction Activity Risk (Precisely Data)</div>', unsafe_allow_html=True)
            with st.container(border=True):
                const_scatter = alt.Chart(construction_risk).mark_circle(opacity=0.85, stroke="#FFFFFF", strokeWidth=1.5).encode(
                    x=alt.X("Active Permits:Q", title="Active Construction Permits"),
                    y=alt.Y("Fiber Route Proximity:Q", title="Routes in Proximity"),
                    size=alt.Size("Risk Score:Q", scale=alt.Scale(range=[200, 800]), legend=None),
                    color=alt.Color("Risk Score:Q", scale=alt.Scale(scheme="orangered"), legend=alt.Legend(title="Risk")),
                    tooltip=["Region:N", "Active Permits:Q", "Fiber Route Proximity:Q", "Predicted Dig-ups:Q", "Risk Score:Q"],
                )
                const_labels = alt.Chart(construction_risk).mark_text(dy=-12, fontSize=9, color="#1E293B").encode(
                    x="Active Permits:Q", y="Fiber Route Proximity:Q", text="Region:N"
                )
                st.altair_chart(style_net_chart(const_scatter + const_labels, height=220), use_container_width=True)

                high_risk_region = construction_risk.sort_values("Risk Score", ascending=False).iloc[0]
                total_predicted = construction_risk["Predicted Dig-ups"].sum()
                render_net_ai_reco(
                    "Dig-Up Prevention",
                    f"{total_predicted} fiber dig-ups predicted this month. {high_risk_region['Region']} highest risk ({high_risk_region['Predicted Dig-ups']} predicted).",
                    "Cross-reference Precisely construction permits with GIS routes. Auto-notify contractors of fiber presence.",
                    "Prevent €{:.0f}K in dig-up repair costs through proactive outreach.".format(total_predicted * 15),
                )

        ext_col3, ext_col4 = st.columns(2)

        with ext_col3:
            st.markdown('<div class="net-mini-title">Mobility-Driven Capacity Planning (SafeGraph)</div>', unsafe_allow_html=True)
            with st.container(border=True):
                mobility_area = alt.Chart(mobility_capacity).mark_area(opacity=0.4, color="#10B981").encode(
                    x=alt.X("Hour:O", title="Hour of Day"),
                    y=alt.Y("Population Density Index:Q", title="Population Index", scale=alt.Scale(domain=[0, 1])),
                )
                util_line = alt.Chart(mobility_capacity).mark_line(strokeWidth=2.5, color="#6366F1").encode(
                    x="Hour:O",
                    y=alt.Y("Network Utilization:Q", title="Network Util (%)", scale=alt.Scale(domain=[0, 100])),
                )
                demand_line = alt.Chart(mobility_capacity).mark_line(strokeWidth=2, strokeDash=[4, 4], color="#F59E0B").encode(
                    x="Hour:O",
                    y=alt.Y("Predicted Demand:Q", scale=alt.Scale(domain=[0, 100])),
                )
                st.altair_chart(style_net_chart(alt.layer(mobility_area, util_line, demand_line).resolve_scale(y="independent"), height=220), use_container_width=True)

                peak_hour = mobility_capacity.loc[mobility_capacity["Network Utilization"].idxmax(), "Hour"]
                peak_util = mobility_capacity["Network Utilization"].max()
                render_net_ai_reco(
                    "Mobility Intelligence",
                    f"Peak utilization {peak_util}% at {peak_hour}:00 correlates with SafeGraph population density. Demand forecast accuracy: 94%.",
                    "Dynamic bandwidth allocation based on real-time mobility patterns.",
                    "Optimize capacity spend by matching infrastructure to actual population movement.",
                )

        with ext_col4:
            st.markdown('<div class="net-mini-title">Power Grid Correlation (GridStatus)</div>', unsafe_allow_html=True)
            with st.container(border=True):
                power_events = pd.DataFrame({
                    "Region": ["Madrid", "Barcelona", "Valencia", "Bilbao", "Sevilla"],
                    "Grid Outages": [3, 5, 2, 4, 2],
                    "Network Outages": [2, 4, 1, 3, 1],
                    "Correlation": [0.89, 0.92, 0.78, 0.88, 0.82],
                    "Backup Coverage": [95, 88, 92, 85, 90],
                })
                power_bar = alt.Chart(power_events).mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6, size=25).encode(
                    x=alt.X("Region:N", title=None),
                    y=alt.Y("Grid Outages:Q", title="Outages"),
                    color=alt.value("#94A3B8"),
                    tooltip=["Region:N", "Grid Outages:Q", "Network Outages:Q", alt.Tooltip("Correlation:Q", format=".2f")],
                )
                network_bar = alt.Chart(power_events).mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6, size=25, xOffset=15).encode(
                    x=alt.X("Region:N", title=None),
                    y=alt.Y("Network Outages:Q"),
                    color=alt.value("#EF4444"),
                )
                corr_line = alt.Chart(power_events).mark_line(point=True, strokeWidth=2.5, color="#10B981").encode(
                    x="Region:N",
                    y=alt.Y("Correlation:Q", title="Correlation", scale=alt.Scale(domain=[0.7, 1])),
                )
                st.altair_chart(style_net_chart(alt.layer(power_bar, network_bar, corr_line).resolve_scale(y="independent"), height=220), use_container_width=True)

                avg_corr = power_events["Correlation"].mean()
                render_net_ai_reco(
                    "Power-Network Correlation",
                    f"{avg_corr:.0%} average correlation between grid outages and network incidents. GridStatus data enables 15-min advance warning.",
                    "Integrate GridStatus alerts into NOC runbooks. Auto-activate generator pre-start sequence.",
                    "Reduce power-related outages by 60% through predictive UPS management.",
                    level="warning",
                )

        st.markdown('<div class="net-title">🔮 7-Day Predictive Forecast · ML + External Data</div>', unsafe_allow_html=True)

        st.markdown("""
        <div style="background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%); border-radius: 12px; padding: 1rem; margin-bottom: 1rem; border-left: 4px solid #F59E0B;">
            <div style="display: flex; align-items: center;">
                <span style="font-size: 1.3rem; margin-right: 0.6rem;">🧠</span>
                <div>
                    <strong style="color: #92400E;">Snowflake Cortex ML Predictions</strong>
                    <div style="color: #B45309; font-size: 0.82rem;">ML models trained on historical incidents + Weather Source + Precisely + GridStatus data to forecast network events</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        forecast_dates = pd.date_range(pd.Timestamp.today(), periods=7, freq="D")
        weather_forecast = pd.DataFrame({
            "Date": forecast_dates,
            "Day": [d.strftime("%a %d") for d in forecast_dates],
            "Wind Forecast kmh": [25, 35, 62, 78, 55, 30, 22],
            "Rain Forecast mm": [2, 8, 28, 42, 18, 5, 0],
            "Temp Forecast C": [14, 12, 8, 5, 9, 13, 15],
            "Predicted Incidents": [1, 2, 6, 9, 4, 1, 0],
            "Confidence": [0.92, 0.89, 0.94, 0.96, 0.91, 0.88, 0.90],
            "Risk Level": ["Low", "Medium", "High", "Critical", "High", "Low", "Low"],
            "Storm Alert": [False, False, True, True, True, False, False],
            "Predicted Fiber Cuts": [0, 1, 3, 5, 2, 0, 0],
            "Predicted Equipment Failures": [1, 1, 3, 4, 2, 1, 0],
            "Recommended Crews": [2, 3, 8, 12, 6, 2, 2],
        })

        construction_forecast = pd.DataFrame({
            "Date": forecast_dates,
            "Day": [d.strftime("%a %d") for d in forecast_dates],
            "Scheduled Works": [12, 15, 8, 3, 5, 18, 22],
            "High Risk Zones": [3, 4, 2, 1, 1, 5, 6],
            "Predicted Dig-ups": [1, 2, 1, 0, 0, 2, 3],
            "Confidence": [0.87, 0.85, 0.89, 0.92, 0.91, 0.84, 0.82],
            "Proactive Alerts Sent": [8, 12, 5, 2, 3, 14, 18],
        })

        capacity_forecast = pd.DataFrame({
            "Date": forecast_dates,
            "Day": [d.strftime("%a %d") for d in forecast_dates],
            "Expected Events": ["Normal", "Normal", "Storm", "Storm Recovery", "Normal", "Football Match", "Weekend"],
            "Peak Demand Predicted": [82, 85, 45, 78, 88, 96, 72],
            "Capacity Available": [95, 95, 95, 95, 95, 95, 95],
            "Headroom": [13, 10, 50, 17, 7, -1, 23],
            "Action Required": ["None", "None", "None", "Monitor", "Pre-scale", "Scale Up", "None"],
        })

        pred_col1, pred_col2 = st.columns(2)

        with pred_col1:
            st.markdown('<div class="net-mini-title">🌧️ Weather-Based Incident Forecast (Next 7 Days)</div>', unsafe_allow_html=True)
            with st.container(border=True):
                risk_colors = alt.Scale(domain=["Low", "Medium", "High", "Critical"], range=["#10B981", "#F59E0B", "#EF4444", "#7C2D12"])
                forecast_bars = alt.Chart(weather_forecast).mark_bar(cornerRadiusTopLeft=8, cornerRadiusTopRight=8).encode(
                    x=alt.X("Day:N", title=None, sort=list(weather_forecast["Day"])),
                    y=alt.Y("Predicted Incidents:Q", title="Predicted Incidents"),
                    color=alt.Color("Risk Level:N", scale=risk_colors, legend=alt.Legend(title="Risk", orient="bottom", columns=4)),
                    tooltip=["Day:N", "Wind Forecast kmh:Q", "Rain Forecast mm:Q", "Predicted Incidents:Q", "Risk Level:N", alt.Tooltip("Confidence:Q", format=".0%")],
                )
                conf_line = alt.Chart(weather_forecast).mark_line(strokeWidth=2, strokeDash=[4, 4], color="#6366F1", point=alt.OverlayMarkDef(size=50, filled=True)).encode(
                    x=alt.X("Day:N", sort=list(weather_forecast["Day"])),
                    y=alt.Y("Confidence:Q", title="Confidence", scale=alt.Scale(domain=[0.8, 1])),
                )
                storm_markers = alt.Chart(weather_forecast[weather_forecast["Storm Alert"]]).mark_text(dy=-15, fontSize=16).encode(
                    x=alt.X("Day:N", sort=list(weather_forecast["Day"])),
                    y="Predicted Incidents:Q",
                    text=alt.value("⚠️"),
                )
                st.altair_chart(style_net_chart(alt.layer(forecast_bars, storm_markers, conf_line).resolve_scale(y="independent"), height=240), use_container_width=True)

                critical_days = len(weather_forecast[weather_forecast["Risk Level"].isin(["High", "Critical"])])
                total_predicted = weather_forecast["Predicted Incidents"].sum()
                peak_day = weather_forecast.loc[weather_forecast["Predicted Incidents"].idxmax()]

                st.markdown(f"""
                <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.5rem; margin-top: 0.5rem;">
                    <div style="background: #FEF2F2; border-radius: 8px; padding: 0.6rem; text-align: center;">
                        <div style="font-size: 1.4rem; font-weight: 700; color: #DC2626;">{total_predicted}</div>
                        <div style="font-size: 0.7rem; color: #991B1B;">Total Predicted</div>
                    </div>
                    <div style="background: #FEF3C7; border-radius: 8px; padding: 0.6rem; text-align: center;">
                        <div style="font-size: 1.4rem; font-weight: 700; color: #D97706;">{critical_days}</div>
                        <div style="font-size: 0.7rem; color: #92400E;">High Risk Days</div>
                    </div>
                    <div style="background: #DBEAFE; border-radius: 8px; padding: 0.6rem; text-align: center;">
                        <div style="font-size: 1.4rem; font-weight: 700; color: #2563EB;">{peak_day['Day']}</div>
                        <div style="font-size: 0.7rem; color: #1E40AF;">Peak Risk Day</div>
                    </div>
                    <div style="background: #ECFDF5; border-radius: 8px; padding: 0.6rem; text-align: center;">
                        <div style="font-size: 1.4rem; font-weight: 700; color: #059669;">{peak_day['Recommended Crews']}</div>
                        <div style="font-size: 0.7rem; color: #047857;">Crews Needed</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        with pred_col2:
            st.markdown('<div class="net-mini-title">🚧 Construction Dig-Up Risk Forecast</div>', unsafe_allow_html=True)
            with st.container(border=True):
                works_area = alt.Chart(construction_forecast).mark_area(opacity=0.3, color="#6366F1").encode(
                    x=alt.X("Day:N", title=None, sort=list(construction_forecast["Day"])),
                    y=alt.Y("Scheduled Works:Q", title="Scheduled Works"),
                )
                works_line = alt.Chart(construction_forecast).mark_line(strokeWidth=2, color="#4F46E5").encode(
                    x=alt.X("Day:N", sort=list(construction_forecast["Day"])), y="Scheduled Works:Q",
                )
                digup_bars = alt.Chart(construction_forecast).mark_bar(color="#EF4444", opacity=0.8, size=20).encode(
                    x=alt.X("Day:N", sort=list(construction_forecast["Day"])),
                    y=alt.Y("Predicted Dig-ups:Q", title="Predicted Dig-ups"),
                    tooltip=["Day:N", "Scheduled Works:Q", "High Risk Zones:Q", "Predicted Dig-ups:Q", "Proactive Alerts Sent:Q"],
                )
                st.altair_chart(style_net_chart(alt.layer(works_area, works_line, digup_bars).resolve_scale(y="independent"), height=240), use_container_width=True)

                total_digups = construction_forecast["Predicted Dig-ups"].sum()
                total_alerts = construction_forecast["Proactive Alerts Sent"].sum()
                worst_day = construction_forecast.loc[construction_forecast["Predicted Dig-ups"].idxmax()]

                st.markdown(f"""
                <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.5rem; margin-top: 0.5rem;">
                    <div style="background: #FEF2F2; border-radius: 8px; padding: 0.6rem; text-align: center;">
                        <div style="font-size: 1.4rem; font-weight: 700; color: #DC2626;">{total_digups}</div>
                        <div style="font-size: 0.7rem; color: #991B1B;">Predicted Dig-ups</div>
                    </div>
                    <div style="background: #EEF2FF; border-radius: 8px; padding: 0.6rem; text-align: center;">
                        <div style="font-size: 1.4rem; font-weight: 700; color: #4F46E5;">{total_alerts}</div>
                        <div style="font-size: 0.7rem; color: #3730A3;">Alerts to Send</div>
                    </div>
                    <div style="background: #FEF3C7; border-radius: 8px; padding: 0.6rem; text-align: center;">
                        <div style="font-size: 1.4rem; font-weight: 700; color: #D97706;">{worst_day['Day']}</div>
                        <div style="font-size: 0.7rem; color: #92400E;">Highest Risk</div>
                    </div>
                    <div style="background: #ECFDF5; border-radius: 8px; padding: 0.6rem; text-align: center;">
                        <div style="font-size: 1.4rem; font-weight: 700; color: #059669;">€{total_digups * 15}K</div>
                        <div style="font-size: 0.7rem; color: #047857;">At Risk</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown('<div class="net-mini-title">📊 Capacity Demand Forecast vs Available Headroom</div>', unsafe_allow_html=True)
        with st.container(border=True):
            cap_demand = alt.Chart(capacity_forecast).mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6, color="#6366F1").encode(
                x=alt.X("Day:N", title=None, sort=list(capacity_forecast["Day"])),
                y=alt.Y("Peak Demand Predicted:Q", title="Utilization %", scale=alt.Scale(domain=[0, 100])),
                tooltip=["Day:N", "Expected Events:N", "Peak Demand Predicted:Q", "Capacity Available:Q", "Action Required:N"],
            )
            cap_line = alt.Chart(capacity_forecast).mark_line(strokeWidth=3, color="#10B981").encode(
                x=alt.X("Day:N", sort=list(capacity_forecast["Day"])),
                y=alt.Y("Capacity Available:Q"),
            )
            cap_rule = alt.Chart(pd.DataFrame({"y": [90]})).mark_rule(strokeDash=[5, 5], color="#EF4444", strokeWidth=2).encode(y="y:Q")

            headroom_text = alt.Chart(capacity_forecast).mark_text(dy=-10, fontSize=11, fontWeight="bold").encode(
                x=alt.X("Day:N", sort=list(capacity_forecast["Day"])),
                y="Peak Demand Predicted:Q",
                text=alt.Text("Headroom:Q", format="+d"),
                color=alt.condition(alt.datum.Headroom < 5, alt.value("#DC2626"), alt.value("#059669")),
            )
            event_labels = alt.Chart(capacity_forecast).mark_text(dy=15, fontSize=8, color="#64748B").encode(
                x=alt.X("Day:N", sort=list(capacity_forecast["Day"])),
                y=alt.value(5),
                text="Expected Events:N",
            )
            st.altair_chart(style_net_chart(cap_demand + cap_line + cap_rule + headroom_text + event_labels, height=200), use_container_width=True)

            needs_action = capacity_forecast[capacity_forecast["Headroom"] < 10]
            if len(needs_action) > 0:
                action_days = ", ".join(needs_action["Day"].tolist())
                render_net_ai_reco(
                    "Capacity Alert",
                    f"⚠️ {len(needs_action)} days with <10% headroom: {action_days}. SafeGraph mobility data predicts high demand.",
                    f"Pre-scale capacity for {needs_action.iloc[0]['Expected Events']} event. Auto-trigger CDN edge caching.",
                    "Prevent SLA breaches through proactive capacity management.",
                    level="warning",
                )

        st.markdown('<div class="net-mini-title">🎯 Consolidated 7-Day Action Plan</div>', unsafe_allow_html=True)

        action_items = []
        for _, row in weather_forecast.iterrows():
            if row["Risk Level"] in ["High", "Critical"]:
                action_items.append({
                    "Day": row["Day"],
                    "Source": "Weather Source",
                    "Prediction": f"{row['Predicted Incidents']} incidents expected",
                    "Action": f"Deploy {row['Recommended Crews']} crews, pre-stage equipment",
                    "Priority": "🔴 Critical" if row["Risk Level"] == "Critical" else "🟠 High",
                    "Confidence": f"{row['Confidence']:.0%}",
                })
        for _, row in construction_forecast.iterrows():
            if row["Predicted Dig-ups"] >= 2:
                action_items.append({
                    "Day": row["Day"],
                    "Source": "Precisely",
                    "Prediction": f"{row['Predicted Dig-ups']} dig-ups likely",
                    "Action": f"Send {row['Proactive Alerts Sent']} contractor alerts",
                    "Priority": "🟠 High",
                    "Confidence": f"{row['Confidence']:.0%}",
                })
        for _, row in capacity_forecast.iterrows():
            if row["Headroom"] < 10:
                action_items.append({
                    "Day": row["Day"],
                    "Source": "SafeGraph",
                    "Prediction": f"{row['Expected Events']} - {row['Peak Demand Predicted']}% demand",
                    "Action": row["Action Required"],
                    "Priority": "🔴 Critical" if row["Headroom"] < 0 else "🟠 High",
                    "Confidence": "94%",
                })

        if action_items:
            action_df = pd.DataFrame(action_items)
            st.dataframe(
                action_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Day": st.column_config.TextColumn("Day", width="small"),
                    "Source": st.column_config.TextColumn("Data Source", width="medium"),
                    "Prediction": st.column_config.TextColumn("ML Prediction", width="large"),
                    "Action": st.column_config.TextColumn("Recommended Action", width="large"),
                    "Priority": st.column_config.TextColumn("Priority", width="small"),
                    "Confidence": st.column_config.TextColumn("Conf.", width="small"),
                },
            )

        render_net_ai_reco(
            "Predictive Operations Summary",
            f"ML models predict {weather_forecast['Predicted Incidents'].sum()} weather incidents, {construction_forecast['Predicted Dig-ups'].sum()} dig-ups, and {len(needs_action)} capacity constraints in next 7 days.",
            "Execute consolidated action plan above. Estimated prevention value: €{:.0f}K.".format(
                weather_forecast["Predicted Incidents"].sum() * 8 + construction_forecast["Predicted Dig-ups"].sum() * 15
            ),
            "Snowflake Marketplace data transforms reactive NOC into predictive operations center.",
        )

        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #ECFDF5 0%, #D1FAE5 100%); border-radius: 12px; padding: 1rem; margin-top: 1rem; border-left: 4px solid #10B981;">
            <div style="display: flex; align-items: center;">
                <span style="font-size: 1.5rem; margin-right: 0.6rem;">✨</span>
                <div>
                    <strong style="color: #065F46;">AI-Driven Network Operations Summary</strong>
                    <div style="color: #047857; font-size: 0.85rem; margin-top: 0.3rem;">
                        ML models have detected <strong>{total_anomalies} anomalies</strong> this week, with <strong>{critical_assets} critical assets</strong> flagged for immediate maintenance.
                        Predictive maintenance is projected to save <strong>€{prevented_outages * 2.5:.0f}K</strong> in avoided outages.
                        Overall model accuracy: <strong>{avg_model_accuracy:.1f}%</strong>.
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <details style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 0.8rem; margin-top: 1rem;">
        <summary style="cursor: pointer; font-weight: 600; color: #334155; font-size: 0.9rem;">▸ Data Sources & Systems</summary>
        <div style="margin-top: 0.8rem; font-size: 0.85rem; color: #475569;">
            <p><strong>This dashboard aggregates data from the following source systems:</strong></p>
            <table style="width: 100%; border-collapse: collapse; margin: 0.5rem 0;">
                <tr style="border-bottom: 1px solid #E2E8F0;"><th style="text-align: left; padding: 0.4rem;">Data Element</th><th style="text-align: left; padding: 0.4rem;">Source System</th><th style="text-align: left; padding: 0.4rem;">Refresh</th></tr>
                <tr><td style="padding: 0.4rem;">Node status & health</td><td style="padding: 0.4rem;"><strong>NOC</strong> Monitoring</td><td style="padding: 0.4rem;">Real-time</td></tr>
                <tr><td style="padding: 0.4rem;">Traffic utilization</td><td style="padding: 0.4rem;"><strong>NPM</strong> - CA Spectrum</td><td style="padding: 0.4rem;">5 min</td></tr>
                <tr><td style="padding: 0.4rem;">Fiber routes</td><td style="padding: 0.4rem;"><strong>GIS (ESRI ArcGIS)</strong> + OSS</td><td style="padding: 0.4rem;">Daily</td></tr>
                <tr><td style="padding: 0.4rem;">Alarm data</td><td style="padding: 0.4rem;"><strong>Moogsoft</strong> Alarm Correlation</td><td style="padding: 0.4rem;">Real-time</td></tr>
                <tr><td style="padding: 0.4rem;">Weather overlays</td><td style="padding: 0.4rem;"><strong>AEMET API</strong></td><td style="padding: 0.4rem;">Hourly</td></tr>
                <tr><td style="padding: 0.4rem;">Risk exposure</td><td style="padding: 0.4rem;"><strong>Risk Management Platform</strong></td><td style="padding: 0.4rem;">Daily</td></tr>
                <tr><td style="padding: 0.4rem;">Anomaly detection</td><td style="padding: 0.4rem;"><strong>Snowflake ML</strong> + Cortex</td><td style="padding: 0.4rem;">Real-time</td></tr>
                <tr><td style="padding: 0.4rem;">Predictive models</td><td style="padding: 0.4rem;"><strong>Snowflake Model Registry</strong></td><td style="padding: 0.4rem;">Continuous</td></tr>
                <tr><td style="padding: 0.4rem;">Asset health scores</td><td style="padding: 0.4rem;"><strong>CMDB</strong> + ML Pipeline</td><td style="padding: 0.4rem;">Hourly</td></tr>
            </table>
            <p><strong>Key Integrations:</strong></p>
            <ul style="margin: 0.3rem 0; padding-left: 1.2rem;">
                <li>Network elements from <strong>Nokia NSP, Ericsson ENM</strong></li>
                <li>Geographic data from <strong>Catastro</strong></li>
                <li>External threat feeds from <strong>weather/civil protection</strong></li>
                <li>Incident correlation with <strong>tenant NOC systems</strong></li>
                <li>ML inference via <strong>Snowflake Cortex ML</strong></li>
                <li>Model training on <strong>Snowpark Container Services</strong></li>
            </ul>
        </div>
    </details>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Page: Operations & Assets (Service Inventory & Billing Reconciliation)
# ---------------------------------------------------------------------------
elif selected_menu == "Operations & Assets":
    import pandas as pd
    import altair as alt
    from datetime import datetime, timedelta
    import random

    def render_ops_ai_reco(title: str, insight: str, action: str, outcome: str, level: str = "info"):
        color_map = {"info": ("#6366F1", "#EEF2FF", "#3730A3"), "warning": ("#F59E0B", "#FFFBEB", "#92400E"), "critical": ("#EF4444", "#FEF2F2", "#991B1B")}
        accent, bg, text = color_map.get(level, color_map["info"])
        st.markdown(f"""<div style="background: {bg}; border-left: 4px solid {accent}; border-radius: 8px; padding: 0.65rem 0.85rem; margin-top: 0.5rem;">
            <div style="font-weight: 700; color: {text}; font-size: 0.78rem; margin-bottom: 0.2rem;">🤖 {title}</div>
            <div style="color: #334155; font-size: 0.76rem; line-height: 1.4;"><strong>Insight:</strong> {insight}</div>
            <div style="color: #334155; font-size: 0.76rem; line-height: 1.4;"><strong>Action:</strong> {action}</div>
            <div style="color: #059669; font-size: 0.74rem; margin-top: 0.2rem;"><strong>Outcome:</strong> {outcome}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("""<style>
.ops-title { font-size: 1.15rem; font-weight: 800; color: #0F172A; margin: 1.2rem 0 0.6rem; border-bottom: 2px solid #E2E8F0; padding-bottom: 0.4rem; }
.ops-mini-title { font-size: 0.88rem; font-weight: 700; color: #334155; margin-bottom: 0.5rem; }
.ops-pulse { background: linear-gradient(135deg, #0F766E 0%, #14B8A6 100%); border-radius: 14px; padding: 1.1rem 1.3rem; margin-bottom: 1rem; }
.ops-pulse-head { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.8rem; }
.ops-pulse-title { color: #FFFFFF; font-size: 1rem; font-weight: 700; }
.ops-pulse-badge { background: #34D399; color: #065F46; padding: 2px 10px; border-radius: 12px; font-size: 0.68rem; font-weight: 700; }
.ops-pulse-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 0.8rem; }
.ops-pulse-card { background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.15); border-radius: 10px; padding: 0.7rem; text-align: center; }
.ops-pulse-label { color: rgba(255,255,255,0.7); font-size: 0.68rem; text-transform: uppercase; }
.ops-pulse-value { color: #FFFFFF; font-size: 1.3rem; font-weight: 700; }
.ops-pulse-delta { font-size: 0.68rem; }
    </style>""", unsafe_allow_html=True)

    tab_topology, tab_inventory, tab_orders, tab_recon, tab_amort = st.tabs([
        "🌐 Network Topology",
        "📋 Service Inventory",
        "📦 Partner Orders",
        "🔍 Billing Reconciliation",
        "📉 Asset Amortization",
    ])

    # ═══════════════════════════════════════════════════════════════════════
    # TAB 1: Network Topology (OLT to Home)
    # ═══════════════════════════════════════════════════════════════════════
    with tab_topology:

        total_olts = 156
        total_pon_ports = 2496
        total_splitters = 12480
        homes_passed = 1248000
        homes_connected = 892456
        network_utilization = 71.5

        st.markdown(f"""
        <div class="ops-pulse" style="background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);">
            <div class="ops-pulse-head">
                <div class="ops-pulse-title">🌐 Fiber Access Network - OLT to Home</div>
                <div class="ops-pulse-badge">Network Sync · {datetime.now().strftime('%H:%M')}</div>
            </div>
            <div class="ops-pulse-grid">
                <div class="ops-pulse-card"><div class="ops-pulse-label">OLTs</div><div class="ops-pulse-value">{total_olts}</div><div class="ops-pulse-delta" style="color: #A7F3D0;">active chassis</div></div>
                <div class="ops-pulse-card"><div class="ops-pulse-label">PON Ports</div><div class="ops-pulse-value">{total_pon_ports:,}</div><div class="ops-pulse-delta" style="color: #A7F3D0;">16 ports/OLT</div></div>
                <div class="ops-pulse-card"><div class="ops-pulse-label">Splitters</div><div class="ops-pulse-value">{total_splitters:,}</div><div class="ops-pulse-delta" style="color: #A7F3D0;">1:32 ratio</div></div>
                <div class="ops-pulse-card"><div class="ops-pulse-label">Homes Passed</div><div class="ops-pulse-value">{homes_passed/1000:.0f}K</div><div class="ops-pulse-delta" style="color: #A7F3D0;">FTTH coverage</div></div>
                <div class="ops-pulse-card"><div class="ops-pulse-label">Homes Connected</div><div class="ops-pulse-value">{homes_connected/1000:.0f}K</div><div class="ops-pulse-delta" style="color: #A7F3D0;">{network_utilization}% take-rate</div></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="ops-title">🏗️ Network Hierarchy: OLT → PON → Splitter → Home</div>', unsafe_allow_html=True)

        network_elements = pd.DataFrame({
            "Element ID": ["OLT-MAD-001", "OLT-MAD-002", "OLT-BCN-001", "OLT-BCN-002", "OLT-VAL-001", "OLT-SEV-001", "OLT-BIL-001", "OLT-MAL-001"],
            "Location": ["Madrid Central", "Madrid Norte", "Barcelona Hub", "Barcelona 22@", "Valencia DC", "Sevilla POP", "Bilbao POP", "Malaga POP"],
            "Vendor": ["Nokia", "Nokia", "Huawei", "Nokia", "Huawei", "Nokia", "Huawei", "Nokia"],
            "PON Ports Total": [16, 16, 16, 16, 16, 16, 16, 16],
            "PON Ports Used": [14, 12, 15, 11, 13, 10, 9, 8],
            "Splitters": [448, 384, 480, 352, 416, 320, 288, 256],
            "Homes Connected": [14336, 12288, 15360, 11264, 13312, 10240, 9216, 8192],
            "MO Lines": [8320, 7168, 8960, 6554, 7741, 5939, 5356, 4761],
            "VF Lines": [6016, 5120, 6400, 4710, 5571, 4301, 3860, 3431],
            "Utilization Pct": [87.5, 75.0, 93.8, 68.8, 81.3, 62.5, 56.3, 50.0],
        })

        topo_col1, topo_col2 = st.columns([2, 1])

        with topo_col1:
            st.markdown('<div class="ops-mini-title">OLT Capacity & Utilization</div>', unsafe_allow_html=True)
            with st.container(border=True):
                olt_chart = alt.Chart(network_elements).mark_bar().encode(
                    x=alt.X("Element ID:N", title=None, sort="-y"),
                    y=alt.Y("Homes Connected:Q", title="Homes Connected"),
                    color=alt.value("#3B82F6"),
                )
                st.altair_chart(olt_chart, use_container_width=True)

        with topo_col2:
            st.markdown('<div class="ops-mini-title">Partner Split per OLT</div>', unsafe_allow_html=True)
            mo_total = network_elements["MO Lines"].sum()
            vf_total = network_elements["VF Lines"].sum()
            partner_split = pd.DataFrame({
                "Partner": ["MasOrange", "Vodafone"],
                "Lines": [mo_total, vf_total],
                "Color": ["#FF6B00", "#E60000"],
            })
            with st.container(border=True):
                partner_pie = alt.Chart(partner_split).mark_arc(innerRadius=50).encode(
                    theta=alt.Theta("Lines:Q"),
                    color=alt.Color("Partner:N", scale=alt.Scale(domain=["MasOrange", "Vodafone"], range=["#FF6B00", "#E60000"])),
                )
                st.altair_chart(partner_pie, use_container_width=True)

            st.markdown(f"""
            <div style="background: #F8FAFC; border-radius: 8px; padding: 0.8rem; margin-top: 0.5rem;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.4rem;">
                    <span style="color: #FF6B00; font-weight: 600;">MasOrange</span>
                    <span style="font-weight: 700;">{mo_total:,} lines ({mo_total/(mo_total+vf_total)*100:.1f}%)</span>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span style="color: #E60000; font-weight: 600;">Vodafone</span>
                    <span style="font-weight: 700;">{vf_total:,} lines ({vf_total/(mo_total+vf_total)*100:.1f}%)</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<div class="ops-mini-title">OLT Inventory Detail</div>', unsafe_allow_html=True)
        st.dataframe(
            network_elements,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Element ID": st.column_config.TextColumn("OLT ID", width="medium"),
                "Location": st.column_config.TextColumn("Location", width="medium"),
                "Vendor": st.column_config.TextColumn("Vendor", width="small"),
                "PON Ports Total": st.column_config.NumberColumn("Ports", format="%d"),
                "PON Ports Used": st.column_config.NumberColumn("Used", format="%d"),
                "Splitters": st.column_config.NumberColumn("Splitters", format="%d"),
                "Homes Connected": st.column_config.NumberColumn("Homes", format="%,d"),
                "MO Lines": st.column_config.NumberColumn("MasOrange", format="%,d"),
                "VF Lines": st.column_config.NumberColumn("Vodafone", format="%,d"),
                "Utilization Pct": st.column_config.ProgressColumn("Utilization", min_value=0, max_value=100, format="%.0f%%"),
            },
        )

        high_util_olts = network_elements[network_elements["Utilization Pct"] > 85]
        if len(high_util_olts) > 0:
            render_ops_ai_reco(
                "Capacity Planning Alert",
                f"{len(high_util_olts)} OLTs above 85% utilization. {high_util_olts.iloc[0]['Element ID']} at {high_util_olts.iloc[0]['Utilization Pct']}% - risk of service rejection.",
                "Initiate PON port expansion for high-utilization OLTs. Pre-provision additional splitters in growth areas.",
                "Prevent service rejection and maintain SLA commitments to Vodafone and MasOrange.",
                level="warning",
            )

        st.markdown('<div class="ops-title">📊 Network Topology Flow</div>', unsafe_allow_html=True)
        st.markdown("""
        <div style="background: #F8FAFC; border-radius: 12px; padding: 1.2rem; border: 1px solid #E2E8F0;">
            <div style="display: flex; justify-content: space-between; align-items: center; text-align: center;">
                <div style="flex: 1;">
                    <div style="background: #1E3A8A; color: white; padding: 1rem; border-radius: 8px; font-weight: 700;">OLT</div>
                    <div style="color: #64748B; font-size: 0.75rem; margin-top: 0.3rem;">156 chassis</div>
                </div>
                <div style="color: #94A3B8; font-size: 1.5rem;">→</div>
                <div style="flex: 1;">
                    <div style="background: #3B82F6; color: white; padding: 1rem; border-radius: 8px; font-weight: 700;">PON Port</div>
                    <div style="color: #64748B; font-size: 0.75rem; margin-top: 0.3rem;">2,496 ports</div>
                </div>
                <div style="color: #94A3B8; font-size: 1.5rem;">→</div>
                <div style="flex: 1;">
                    <div style="background: #60A5FA; color: white; padding: 1rem; border-radius: 8px; font-weight: 700;">Splitter 1:32</div>
                    <div style="color: #64748B; font-size: 0.75rem; margin-top: 0.3rem;">12,480 units</div>
                </div>
                <div style="color: #94A3B8; font-size: 1.5rem;">→</div>
                <div style="flex: 1;">
                    <div style="background: #93C5FD; color: #1E3A8A; padding: 1rem; border-radius: 8px; font-weight: 700;">Distribution</div>
                    <div style="color: #64748B; font-size: 0.75rem; margin-top: 0.3rem;">Feeder/Drop fiber</div>
                </div>
                <div style="color: #94A3B8; font-size: 1.5rem;">→</div>
                <div style="flex: 1;">
                    <div style="background: #10B981; color: white; padding: 1rem; border-radius: 8px; font-weight: 700;">Home</div>
                    <div style="color: #64748B; font-size: 0.75rem; margin-top: 0.3rem;">892,456 connected</div>
                </div>
            </div>
            <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid #E2E8F0;">
                <div style="display: flex; justify-content: center; gap: 2rem;">
                    <div style="display: flex; align-items: center; gap: 0.5rem;">
                        <div style="width: 12px; height: 12px; background: #FF6B00; border-radius: 2px;"></div>
                        <span style="font-size: 0.8rem; color: #334155;"><strong>MasOrange:</strong> 54,799 lines (58%)</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 0.5rem;">
                        <div style="width: 12px; height: 12px; background: #E60000; border-radius: 2px;"></div>
                        <span style="font-size: 0.8rem; color: #334155;"><strong>Vodafone:</strong> 39,409 lines (42%)</span>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════════════════
    # TAB 2: Service Inventory (Core - Billable Lines)
    # ═══════════════════════════════════════════════════════════════════════
    with tab_inventory:

        total_active_lines = 892456
        mo_lines = 517625
        vf_lines = 374831
        total_mrc = 13386840
        avg_bandwidth = "612 Mbps"
        pending_activations = 1247
        pending_disconnects = 423

        st.markdown(f"""
        <div class="ops-pulse" style="background: linear-gradient(135deg, #7C2D12 0%, #EA580C 100%);">
            <div class="ops-pulse-head">
                <div class="ops-pulse-title">📋 Service Inventory - Billable Lines</div>
                <div class="ops-pulse-badge">Golden Record · {datetime.now().strftime('%H:%M')}</div>
            </div>
            <div class="ops-pulse-grid">
                <div class="ops-pulse-card"><div class="ops-pulse-label">Active Lines</div><div class="ops-pulse-value">{total_active_lines:,}</div><div class="ops-pulse-delta" style="color: #A7F3D0;">billable services</div></div>
                <div class="ops-pulse-card"><div class="ops-pulse-label">MasOrange</div><div class="ops-pulse-value">{mo_lines:,}</div><div class="ops-pulse-delta" style="color: #FFEDD5;">{mo_lines/total_active_lines*100:.1f}% share</div></div>
                <div class="ops-pulse-card"><div class="ops-pulse-label">Vodafone</div><div class="ops-pulse-value">{vf_lines:,}</div><div class="ops-pulse-delta" style="color: #FECACA;">{vf_lines/total_active_lines*100:.1f}% share</div></div>
                <div class="ops-pulse-card"><div class="ops-pulse-label">Monthly MRC</div><div class="ops-pulse-value">€{total_mrc/1000000:.1f}M</div><div class="ops-pulse-delta" style="color: #A7F3D0;">recurring revenue</div></div>
                <div class="ops-pulse-card"><div class="ops-pulse-label">Pending Orders</div><div class="ops-pulse-value">{pending_activations + pending_disconnects}</div><div class="ops-pulse-delta" style="color: #FDE68A;">{pending_activations} new / {pending_disconnects} cease</div></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="ops-title">📊 Service Inventory by Partner & Bandwidth</div>', unsafe_allow_html=True)

        service_inventory_sample = pd.DataFrame({
            "Service ID": [f"SVC-2024-{str(i).zfill(6)}" for i in range(1, 21)],
            "Partner": ["MasOrange", "Vodafone", "MasOrange", "MasOrange", "Vodafone", "MasOrange", "Vodafone", "MasOrange", "Vodafone", "MasOrange",
                       "Vodafone", "MasOrange", "MasOrange", "Vodafone", "MasOrange", "Vodafone", "MasOrange", "Vodafone", "MasOrange", "Vodafone"],
            "Address": ["Calle Gran Via 42, 3A, Madrid", "Passeig de Gracia 78, 2B, Barcelona", "Av. del Puerto 156, Valencia", "Calle Serrano 89, 4C, Madrid",
                       "Rambla Catalunya 112, Barcelona", "Plaza Mayor 23, Salamanca", "Calle Larios 15, Malaga", "Gran Via 67, Bilbao", "Calle Colon 45, Valencia",
                       "Paseo Castellana 200, Madrid", "Diagonal 456, Barcelona", "Calle Alcala 78, Madrid", "Av. Diagonal 234, Barcelona", "Calle Preciados 12, Madrid",
                       "Ramblas 89, Barcelona", "Gran Via 34, Madrid", "Passeig Joan de Borbo 56, Barcelona", "Calle Mayor 90, Madrid", "Via Laietana 78, Barcelona", "Calle Fuencarral 123, Madrid"],
            "OLT": ["OLT-MAD-001", "OLT-BCN-001", "OLT-VAL-001", "OLT-MAD-001", "OLT-BCN-002", "OLT-MAD-002", "OLT-MAL-001", "OLT-BIL-001", "OLT-VAL-001", "OLT-MAD-001",
                   "OLT-BCN-001", "OLT-MAD-002", "OLT-BCN-001", "OLT-MAD-001", "OLT-BCN-002", "OLT-MAD-001", "OLT-BCN-001", "OLT-MAD-002", "OLT-BCN-002", "OLT-MAD-001"],
            "PON Port": ["PON-001-01", "PON-001-03", "PON-001-02", "PON-001-05", "PON-002-01", "PON-002-04", "PON-001-02", "PON-001-01", "PON-001-06", "PON-001-08",
                        "PON-001-05", "PON-002-02", "PON-001-07", "PON-001-09", "PON-002-03", "PON-001-10", "PON-001-04", "PON-002-06", "PON-002-05", "PON-001-11"],
            "Bandwidth": ["1 Gbps", "600 Mbps", "300 Mbps", "1 Gbps", "600 Mbps", "300 Mbps", "1 Gbps", "600 Mbps", "300 Mbps", "1 Gbps",
                         "600 Mbps", "1 Gbps", "300 Mbps", "600 Mbps", "1 Gbps", "300 Mbps", "600 Mbps", "1 Gbps", "300 Mbps", "600 Mbps"],
            "Status": ["Active", "Active", "Active", "Active", "Active", "Active", "Active", "Active", "Active", "Active",
                      "Active", "Active", "Pending Disconnect", "Active", "Active", "Active", "Pending Activation", "Active", "Active", "Active"],
            "Activation Date": ["2023-06-15", "2023-08-22", "2024-01-10", "2022-11-05", "2023-09-18", "2024-02-28", "2023-07-14", "2024-03-01", "2023-12-20", "2022-05-30",
                               "2023-10-12", "2024-01-25", "2023-04-08", "2023-11-15", "2024-02-14", "2022-08-19", "2025-03-10", "2023-06-28", "2024-01-05", "2023-09-22"],
            "MRC EUR": [15.50, 12.00, 9.50, 15.50, 12.00, 9.50, 15.50, 12.00, 9.50, 15.50, 12.00, 15.50, 9.50, 12.00, 15.50, 9.50, 12.00, 15.50, 9.50, 12.00],
        })

        inv_filter_col1, inv_filter_col2, inv_filter_col3 = st.columns([1, 1, 1])
        with inv_filter_col1:
            partner_filter = st.selectbox("Partner", ["All", "MasOrange", "Vodafone"])
        with inv_filter_col2:
            status_filter = st.selectbox("Status", ["All", "Active", "Pending Activation", "Pending Disconnect"])
        with inv_filter_col3:
            bandwidth_filter = st.selectbox("Bandwidth", ["All", "1 Gbps", "600 Mbps", "300 Mbps"])

        filtered_inventory = service_inventory_sample.copy()
        if partner_filter != "All":
            filtered_inventory = filtered_inventory[filtered_inventory["Partner"] == partner_filter]
        if status_filter != "All":
            filtered_inventory = filtered_inventory[filtered_inventory["Status"] == status_filter]
        if bandwidth_filter != "All":
            filtered_inventory = filtered_inventory[filtered_inventory["Bandwidth"] == bandwidth_filter]

        inv_col1, inv_col2 = st.columns([2, 1])

        with inv_col1:
            st.markdown('<div class="ops-mini-title">Lines by Bandwidth Tier</div>', unsafe_allow_html=True)
            bandwidth_dist = pd.DataFrame({
                "Bandwidth": ["1 Gbps", "600 Mbps", "300 Mbps"],
                "Lines": [312456, 356789, 223211],
                "MRC EUR": [4843068, 4281468, 2120505],
            })
            with st.container(border=True):
                bw_chart = alt.Chart(bandwidth_dist).mark_bar().encode(
                    x=alt.X("Bandwidth:N", title=None, sort=["1 Gbps", "600 Mbps", "300 Mbps"]),
                    y=alt.Y("Lines:Q", title="Active Lines"),
                    color=alt.value("#EA580C"),
                )
                st.altair_chart(bw_chart, use_container_width=True)

        with inv_col2:
            st.markdown('<div class="ops-mini-title">MRC by Partner</div>', unsafe_allow_html=True)
            partner_mrc = pd.DataFrame({
                "Partner": ["MasOrange", "Vodafone"],
                "MRC": [7764427, 5622413],
            })
            with st.container(border=True):
                mrc_pie = alt.Chart(partner_mrc).mark_arc(innerRadius=50).encode(
                    theta=alt.Theta("MRC:Q"),
                    color=alt.Color("Partner:N", scale=alt.Scale(domain=["MasOrange", "Vodafone"], range=["#FF6B00", "#E60000"])),
                )
                st.altair_chart(mrc_pie, use_container_width=True)

        st.markdown('<div class="ops-mini-title">Service Inventory Detail (Sample)</div>', unsafe_allow_html=True)
        st.dataframe(
            filtered_inventory,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Service ID": st.column_config.TextColumn("Service ID", width="medium"),
                "Partner": st.column_config.TextColumn("Partner", width="small"),
                "Address": st.column_config.TextColumn("Address", width="large"),
                "OLT": st.column_config.TextColumn("OLT", width="small"),
                "PON Port": st.column_config.TextColumn("PON", width="small"),
                "Bandwidth": st.column_config.TextColumn("BW", width="small"),
                "Status": st.column_config.TextColumn("Status", width="medium"),
                "Activation Date": st.column_config.DateColumn("Activated", format="YYYY-MM-DD"),
                "MRC EUR": st.column_config.NumberColumn("MRC €", format="€%.2f"),
            },
        )
        st.markdown('<div style="background: #F3E8FF; border-left: 3px solid #9333EA; border-radius: 4px; padding: 0.6rem; margin-top: 0.5rem; font-size: 0.78rem;"><strong style="color: #6B21A8;">🎯 Anomaly Insight:</strong> <span style="color: #581C87;">SPL-MAD-BATCH-045 shows 66% faster depreciation than expected - likely environmental factors. FBR-VAL-TRUNK-003 over-allocated by 50% - risk of service degradation.</span></div>', unsafe_allow_html=True)

        render_ops_ai_reco(
            "Service Inventory Health",
            f"892,456 active lines generating €13.4M MRC. {pending_activations} pending activations, {pending_disconnects} pending disconnects. Inventory sync rate: 99.2%.",
            "Process pending orders within SLA. Flag any services without OLT assignment for investigation.",
            "Maintain accurate inventory as the 'golden record' for billing reconciliation with partners.",
        )

    # ═══════════════════════════════════════════════════════════════════════
    # TAB 3: Partner Orders (Connect/Modify/Cease)
    # ═══════════════════════════════════════════════════════════════════════
    with tab_orders:

        total_orders_mtd = 4567
        orders_completed = 3892
        orders_in_progress = 548
        orders_pending = 127
        sla_compliance = 94.2
        avg_fulfillment_days = 4.8

        st.markdown(f"""
        <div class="ops-pulse" style="background: linear-gradient(135deg, #0F766E 0%, #14B8A6 100%);">
            <div class="ops-pulse-head">
                <div class="ops-pulse-title">📦 Partner Orders - Vodafone & MasOrange</div>
                <div class="ops-pulse-badge">MTD · {datetime.now().strftime('%H:%M')}</div>
            </div>
            <div class="ops-pulse-grid">
                <div class="ops-pulse-card"><div class="ops-pulse-label">Orders MTD</div><div class="ops-pulse-value">{total_orders_mtd:,}</div><div class="ops-pulse-delta" style="color: #A7F3D0;">total received</div></div>
                <div class="ops-pulse-card"><div class="ops-pulse-label">Completed</div><div class="ops-pulse-value">{orders_completed:,}</div><div class="ops-pulse-delta" style="color: #A7F3D0;">{orders_completed/total_orders_mtd*100:.1f}%</div></div>
                <div class="ops-pulse-card"><div class="ops-pulse-label">In Progress</div><div class="ops-pulse-value">{orders_in_progress}</div><div class="ops-pulse-delta" style="color: #FDE68A;">active</div></div>
                <div class="ops-pulse-card"><div class="ops-pulse-label">SLA Compliance</div><div class="ops-pulse-value">{sla_compliance}%</div><div class="ops-pulse-delta" style="color: #A7F3D0;">on target</div></div>
                <div class="ops-pulse-card"><div class="ops-pulse-label">Avg Fulfillment</div><div class="ops-pulse-value">{avg_fulfillment_days}</div><div class="ops-pulse-delta" style="color: #A7F3D0;">days</div></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1rem;">
            <div style="background: linear-gradient(135deg, #FFF7ED 0%, #FFEDD5 100%); border: 2px solid #FF6B00; border-radius: 12px; padding: 1rem;">
                <div style="display: flex; align-items: center; margin-bottom: 0.6rem;">
                    <div style="width: 40px; height: 40px; background: #FF6B00; border-radius: 8px; display: flex; align-items: center; justify-content: center; margin-right: 0.8rem;">
                        <span style="color: white; font-weight: 700; font-size: 0.7rem;">MO</span>
                    </div>
                    <div>
                        <div style="font-weight: 700; color: #9A3412; font-size: 1rem;">MasOrange Orders</div>
                        <div style="font-size: 0.72rem; color: #C2410C;">58% JV Share</div>
                    </div>
                </div>
                <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.5rem;">
                    <div style="background: white; border-radius: 8px; padding: 0.5rem; text-align: center;">
                        <div style="font-size: 1.1rem; font-weight: 700; color: #EA580C;">2,648</div>
                        <div style="font-size: 0.65rem; color: #9A3412;">Total</div>
                    </div>
                    <div style="background: white; border-radius: 8px; padding: 0.5rem; text-align: center;">
                        <div style="font-size: 1.1rem; font-weight: 700; color: #059669;">2,156</div>
                        <div style="font-size: 0.65rem; color: #047857;">Connect</div>
                    </div>
                    <div style="background: white; border-radius: 8px; padding: 0.5rem; text-align: center;">
                        <div style="font-size: 1.1rem; font-weight: 700; color: #3B82F6;">312</div>
                        <div style="font-size: 0.65rem; color: #1D4ED8;">Modify</div>
                    </div>
                    <div style="background: white; border-radius: 8px; padding: 0.5rem; text-align: center;">
                        <div style="font-size: 1.1rem; font-weight: 700; color: #DC2626;">180</div>
                        <div style="font-size: 0.65rem; color: #B91C1C;">Cease</div>
                    </div>
                </div>
            </div>
            <div style="background: linear-gradient(135deg, #FEF2F2 0%, #FECACA 100%); border: 2px solid #E60000; border-radius: 12px; padding: 1rem;">
                <div style="display: flex; align-items: center; margin-bottom: 0.6rem;">
                    <div style="width: 40px; height: 40px; background: #E60000; border-radius: 8px; display: flex; align-items: center; justify-content: center; margin-right: 0.8rem;">
                        <span style="color: white; font-weight: 700; font-size: 0.7rem;">VF</span>
                    </div>
                    <div>
                        <div style="font-weight: 700; color: #991B1B; font-size: 1rem;">Vodafone Orders</div>
                        <div style="font-size: 0.72rem; color: #B91C1C;">42% JV Share</div>
                    </div>
                </div>
                <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.5rem;">
                    <div style="background: white; border-radius: 8px; padding: 0.5rem; text-align: center;">
                        <div style="font-size: 1.1rem; font-weight: 700; color: #DC2626;">1,919</div>
                        <div style="font-size: 0.65rem; color: #991B1B;">Total</div>
                    </div>
                    <div style="background: white; border-radius: 8px; padding: 0.5rem; text-align: center;">
                        <div style="font-size: 1.1rem; font-weight: 700; color: #059669;">1,523</div>
                        <div style="font-size: 0.65rem; color: #047857;">Connect</div>
                    </div>
                    <div style="background: white; border-radius: 8px; padding: 0.5rem; text-align: center;">
                        <div style="font-size: 1.1rem; font-weight: 700; color: #3B82F6;">254</div>
                        <div style="font-size: 0.65rem; color: #1D4ED8;">Modify</div>
                    </div>
                    <div style="background: white; border-radius: 8px; padding: 0.5rem; text-align: center;">
                        <div style="font-size: 1.1rem; font-weight: 700; color: #DC2626;">142</div>
                        <div style="font-size: 0.65rem; color: #B91C1C;">Cease</div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="ops-title">📋 Order Pipeline & Billing Impact</div>', unsafe_allow_html=True)

        partner_orders = pd.DataFrame({
            "Order ID": ["ORD-MO-2025-004521", "ORD-VF-2025-003892", "ORD-MO-2025-004520", "ORD-VF-2025-003891", "ORD-MO-2025-004519",
                        "ORD-VF-2025-003890", "ORD-MO-2025-004518", "ORD-VF-2025-003889", "ORD-MO-2025-004517", "ORD-VF-2025-003888"],
            "Partner": ["MasOrange", "Vodafone", "MasOrange", "Vodafone", "MasOrange", "Vodafone", "MasOrange", "Vodafone", "MasOrange", "Vodafone"],
            "Order Type": ["Connect", "Connect", "Modify", "Cease", "Connect", "Modify", "Cease", "Connect", "Connect", "Connect"],
            "Service ID": ["SVC-2024-892457", "SVC-2024-892458", "SVC-2024-000156", "SVC-2024-000089", "SVC-2024-892459",
                          "SVC-2024-000234", "SVC-2024-000312", "SVC-2024-892460", "SVC-2024-892461", "SVC-2024-892462"],
            "Address": ["Calle Alcala 156, Madrid", "Via Augusta 234, Barcelona", "Gran Via 89, Madrid", "Diagonal 567, Barcelona",
                       "Paseo Castellana 45, Madrid", "Rambla Catalunya 78, Barcelona", "Calle Serrano 123, Madrid",
                       "Passeig de Gracia 90, Barcelona", "Calle Goya 67, Madrid", "Av. Meridiana 345, Barcelona"],
            "Bandwidth": ["1 Gbps", "600 Mbps", "600 Mbps → 1 Gbps", "-", "300 Mbps", "300 Mbps → 600 Mbps", "-", "1 Gbps", "600 Mbps", "300 Mbps"],
            "Order Date": ["2025-03-06", "2025-03-06", "2025-03-05", "2025-03-05", "2025-03-05", "2025-03-04", "2025-03-04", "2025-03-04", "2025-03-03", "2025-03-03"],
            "SLA Deadline": ["2025-03-13", "2025-03-13", "2025-03-12", "2025-03-12", "2025-03-12", "2025-03-11", "2025-03-11", "2025-03-11", "2025-03-10", "2025-03-10"],
            "Status": ["In Progress", "In Progress", "Completed", "Completed", "In Progress", "In Progress", "Completed", "Completed", "Completed", "Completed"],
            "Billing Impact": ["+€15.50/mo", "+€12.00/mo", "+€3.50/mo", "-€12.00/mo", "+€9.50/mo", "+€2.50/mo", "-€15.50/mo", "+€15.50/mo", "+€12.00/mo", "+€9.50/mo"],
            "Inventory Updated": ["Pending", "Pending", "Yes", "Yes", "Pending", "Pending", "Yes", "Yes", "Yes", "Yes"],
        })

        order_col1, order_col2 = st.columns([2, 1])

        with order_col1:
            st.markdown('<div class="ops-mini-title">Orders by Type</div>', unsafe_allow_html=True)
            order_type_dist = pd.DataFrame({
                "Type": ["Connect", "Modify", "Cease"],
                "MasOrange": [2156, 312, 180],
                "Vodafone": [1523, 254, 142],
            })
            order_melted = order_type_dist.melt(id_vars=["Type"], value_vars=["MasOrange", "Vodafone"], var_name="Partner", value_name="Orders")
            with st.container(border=True):
                order_chart = alt.Chart(order_melted).mark_bar().encode(
                    x=alt.X("Type:N", title=None, sort=["Connect", "Modify", "Cease"]),
                    y=alt.Y("Orders:Q", title="Order Count"),
                    color=alt.Color("Partner:N", scale=alt.Scale(domain=["MasOrange", "Vodafone"], range=["#FF6B00", "#E60000"])),
                    xOffset="Partner:N",
                )
                st.altair_chart(order_chart, use_container_width=True)

        with order_col2:
            st.markdown('<div class="ops-mini-title">Billing Impact MTD</div>', unsafe_allow_html=True)
            new_mrc = (2156 + 1523) * 12.50
            upgrade_mrc = (312 + 254) * 3.00
            lost_mrc = (180 + 142) * 12.50
            net_mrc = new_mrc + upgrade_mrc - lost_mrc

            st.markdown(f"""
            <div style="background: #F8FAFC; border-radius: 10px; padding: 1rem; border: 1px solid #E2E8F0;">
                <div style="font-weight: 700; color: #0F172A; margin-bottom: 0.8rem; font-size: 0.9rem;">MRC Impact Summary</div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                    <span style="color: #64748B; font-size: 0.8rem;">New Connects</span>
                    <span style="color: #059669; font-weight: 600; font-size: 0.85rem;">+€{new_mrc:,.0f}/mo</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                    <span style="color: #64748B; font-size: 0.8rem;">Upgrades</span>
                    <span style="color: #3B82F6; font-weight: 600; font-size: 0.85rem;">+€{upgrade_mrc:,.0f}/mo</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                    <span style="color: #64748B; font-size: 0.8rem;">Ceases</span>
                    <span style="color: #DC2626; font-weight: 600; font-size: 0.85rem;">-€{lost_mrc:,.0f}/mo</span>
                </div>
                <div style="border-top: 1px solid #E2E8F0; padding-top: 0.5rem; display: flex; justify-content: space-between;">
                    <span style="color: #0F172A; font-weight: 600; font-size: 0.85rem;">Net MRC Change</span>
                    <span style="color: #059669; font-weight: 700; font-size: 0.95rem;">+€{net_mrc:,.0f}/mo</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<div class="ops-mini-title">Recent Orders</div>', unsafe_allow_html=True)
        st.dataframe(
            partner_orders,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Order ID": st.column_config.TextColumn("Order ID", width="medium"),
                "Partner": st.column_config.TextColumn("Partner", width="small"),
                "Order Type": st.column_config.TextColumn("Type", width="small"),
                "Service ID": st.column_config.TextColumn("Service ID", width="medium"),
                "Address": st.column_config.TextColumn("Address", width="large"),
                "Bandwidth": st.column_config.TextColumn("Bandwidth", width="medium"),
                "Order Date": st.column_config.DateColumn("Ordered", format="YYYY-MM-DD"),
                "SLA Deadline": st.column_config.DateColumn("SLA Due", format="YYYY-MM-DD"),
                "Status": st.column_config.TextColumn("Status", width="small"),
                "Billing Impact": st.column_config.TextColumn("Billing", width="small"),
                "Inventory Updated": st.column_config.TextColumn("Inventory", width="small"),
            },
        )

        pending_inventory = partner_orders[partner_orders["Inventory Updated"] == "Pending"]
        if len(pending_inventory) > 0:
            render_ops_ai_reco(
                "Inventory Sync Alert",
                f"{len(pending_inventory)} orders not yet reflected in Service Inventory. Billing reconciliation will show discrepancies until inventory is updated.",
                "Complete order processing and update Service Inventory within 24 hours of SLA completion.",
                "Ensure accurate billing and prevent disputes in weekly committee meetings.",
                level="warning",
            )

    # ═══════════════════════════════════════════════════════════════════════
    # TAB 4: Billing Reconciliation (Orphan/Ghost Detection)
    # ═══════════════════════════════════════════════════════════════════════
    with tab_recon:

        total_lines_pf = 892456
        total_lines_mo_view = 518234
        total_lines_vf_view = 374012
        matched_lines = 886234
        orphan_lines = 3456
        ghost_lines = 1892
        lifecycle_mismatches = 874

        st.markdown(f"""
        <div class="ops-pulse" style="background: linear-gradient(135deg, #7C3AED 0%, #A855F7 100%);">
            <div class="ops-pulse-head">
                <div class="ops-pulse-title">🔍 Billing Reconciliation - PremiumFiber vs Partners</div>
                <div class="ops-pulse-badge">Weekly Committee · {datetime.now().strftime('%H:%M')}</div>
            </div>
            <div class="ops-pulse-grid">
                <div class="ops-pulse-card"><div class="ops-pulse-label">PF Inventory</div><div class="ops-pulse-value">{total_lines_pf:,}</div><div class="ops-pulse-delta" style="color: #A7F3D0;">golden record</div></div>
                <div class="ops-pulse-card"><div class="ops-pulse-label">Matched</div><div class="ops-pulse-value">{matched_lines:,}</div><div class="ops-pulse-delta" style="color: #A7F3D0;">{matched_lines/total_lines_pf*100:.1f}% aligned</div></div>
                <div class="ops-pulse-card"><div class="ops-pulse-label">Orphan Lines</div><div class="ops-pulse-value" style="color: #FCA5A5;">{orphan_lines:,}</div><div class="ops-pulse-delta" style="color: #FCA5A5;">in PF, not partner</div></div>
                <div class="ops-pulse-card"><div class="ops-pulse-label">Ghost Lines</div><div class="ops-pulse-value" style="color: #FDE68A;">{ghost_lines:,}</div><div class="ops-pulse-delta" style="color: #FDE68A;">in partner, not PF</div></div>
                <div class="ops-pulse-card"><div class="ops-pulse-label">Lifecycle Drift</div><div class="ops-pulse-value" style="color: #93C5FD;">{lifecycle_mismatches}</div><div class="ops-pulse-delta" style="color: #93C5FD;">date mismatches</div></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="ops-title">📊 Reconciliation Overview</div>', unsafe_allow_html=True)

        recon_col1, recon_col2 = st.columns([1.5, 1])

        with recon_col1:
            st.markdown("""
            <div style="background: #F8FAFC; border-radius: 12px; padding: 1.2rem; border: 1px solid #E2E8F0;">
                <div style="font-weight: 700; color: #0F172A; font-size: 1rem; margin-bottom: 1rem;">Inventory Comparison: PremiumFiber vs Partners</div>
                <div style="display: flex; justify-content: space-around; align-items: center;">
                    <div style="text-align: center;">
                        <div style="width: 120px; height: 120px; background: linear-gradient(135deg, #0F766E, #14B8A6); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto;">
                            <div>
                                <div style="color: white; font-size: 1.2rem; font-weight: 700;">892,456</div>
                                <div style="color: rgba(255,255,255,0.8); font-size: 0.65rem;">PF Lines</div>
                            </div>
                        </div>
                        <div style="margin-top: 0.5rem; font-weight: 600; color: #0F766E;">PremiumFiber</div>
                    </div>
                    <div style="text-align: center; padding: 0 1rem;">
                        <div style="font-size: 2rem; color: #10B981;">∩</div>
                        <div style="background: #ECFDF5; border: 2px solid #10B981; border-radius: 8px; padding: 0.5rem 1rem;">
                            <div style="font-size: 1.3rem; font-weight: 700; color: #059669;">886,234</div>
                            <div style="font-size: 0.7rem; color: #047857;">Matched (99.3%)</div>
                        </div>
                    </div>
                    <div style="text-align: center;">
                        <div style="display: flex; gap: 0.5rem;">
                            <div style="width: 80px; height: 80px; background: #FF6B00; border-radius: 50%; display: flex; align-items: center; justify-content: center;">
                                <div>
                                    <div style="color: white; font-size: 0.9rem; font-weight: 700;">518K</div>
                                    <div style="color: rgba(255,255,255,0.8); font-size: 0.55rem;">MO</div>
                                </div>
                            </div>
                            <div style="width: 80px; height: 80px; background: #E60000; border-radius: 50%; display: flex; align-items: center; justify-content: center;">
                                <div>
                                    <div style="color: white; font-size: 0.9rem; font-weight: 700;">374K</div>
                                    <div style="color: rgba(255,255,255,0.8); font-size: 0.55rem;">VF</div>
                                </div>
                            </div>
                        </div>
                        <div style="margin-top: 0.5rem; font-weight: 600; color: #64748B;">Partner Views</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with recon_col2:
            st.markdown('<div class="ops-mini-title">Discrepancy Summary</div>', unsafe_allow_html=True)
            orphan_mrc = orphan_lines * 12.50
            ghost_mrc = ghost_lines * 12.50
            lifecycle_mrc = lifecycle_mismatches * 2.50

            st.markdown(f"""
            <div style="background: #FEF2F2; border: 2px solid #EF4444; border-radius: 10px; padding: 0.8rem; margin-bottom: 0.5rem;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div style="font-weight: 700; color: #991B1B; font-size: 0.9rem;">Orphan Lines</div>
                        <div style="font-size: 0.72rem; color: #B91C1C;">In PF inventory, not in partner view</div>
                    </div>
                    <div style="text-align: right;">
                        <div style="font-size: 1.3rem; font-weight: 700; color: #DC2626;">{orphan_lines:,}</div>
                        <div style="font-size: 0.7rem; color: #991B1B;">€{orphan_mrc:,.0f}/mo at risk</div>
                    </div>
                </div>
            </div>
            <div style="background: #FFFBEB; border: 2px solid #F59E0B; border-radius: 10px; padding: 0.8rem; margin-bottom: 0.5rem;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div style="font-weight: 700; color: #92400E; font-size: 0.9rem;">Ghost Lines</div>
                        <div style="font-size: 0.72rem; color: #B45309;">In partner view, not in PF inventory</div>
                    </div>
                    <div style="text-align: right;">
                        <div style="font-size: 1.3rem; font-weight: 700; color: #D97706;">{ghost_lines:,}</div>
                        <div style="font-size: 0.7rem; color: #92400E;">€{ghost_mrc:,.0f}/mo unbilled</div>
                    </div>
                </div>
            </div>
            <div style="background: #EFF6FF; border: 2px solid #3B82F6; border-radius: 10px; padding: 0.8rem;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div style="font-weight: 700; color: #1E40AF; font-size: 0.9rem;">Lifecycle Drift</div>
                        <div style="font-size: 0.72rem; color: #1D4ED8;">Mismatched activation/deactivation dates</div>
                    </div>
                    <div style="text-align: right;">
                        <div style="font-size: 1.3rem; font-weight: 700; color: #2563EB;">{lifecycle_mismatches}</div>
                        <div style="font-size: 0.7rem; color: #1E40AF;">€{lifecycle_mrc:,.0f}/mo variance</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<div class="ops-title">🔎 Discrepancy Details</div>', unsafe_allow_html=True)

        discrepancy_details = pd.DataFrame({
            "Service ID": ["SVC-2024-234567", "SVC-2024-345678", "SVC-2024-456789", "SVC-2024-567890", "SVC-2024-678901",
                          "SVC-2024-789012", "SVC-2024-890123", "SVC-2024-901234", "SVC-2024-012345", "SVC-2024-123456"],
            "Partner": ["MasOrange", "Vodafone", "MasOrange", "Vodafone", "MasOrange", "Vodafone", "MasOrange", "Vodafone", "MasOrange", "Vodafone"],
            "Discrepancy Type": ["Orphan", "Ghost", "Lifecycle Mismatch", "Orphan", "Ghost", "Lifecycle Mismatch", "Orphan", "Ghost", "Lifecycle Mismatch", "Orphan"],
            "PF Status": ["Active", "-", "Active", "Active", "-", "Active", "Active", "-", "Inactive", "Active"],
            "Partner Status": ["-", "Active", "Active", "-", "Active", "Active", "-", "Active", "Active", "-"],
            "PF Activation": ["2023-06-15", "-", "2023-08-22", "2024-01-10", "-", "2023-09-18", "2023-07-14", "-", "2024-02-28", "2023-12-20"],
            "Partner Activation": ["-", "2023-06-15", "2023-09-01", "-", "2024-01-10", "2023-09-01", "-", "2023-07-14", "2024-02-28", "-"],
            "PF Deactivation": ["-", "-", "-", "-", "-", "-", "-", "-", "2025-02-15", "-"],
            "Partner Deactivation": ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
            "MRC Impact EUR": [15.50, -12.00, 1.50, 9.50, -15.50, 0.75, 12.00, -9.50, 15.50, 15.50],
            "Root Cause": ["Disconnect not synced to MO", "Missing in PF OSS", "Activation date drift", "Cease not processed by VF", "Order not created in PF",
                         "Activation date drift", "Partner system lag", "Missing ONT record", "Deactivation not synced", "Disconnect pending"],
            "Days Outstanding": [45, 12, 8, 23, 5, 15, 34, 7, 3, 18],
        })

        disc_filter = st.selectbox("Filter by Discrepancy Type", ["All", "Orphan", "Ghost", "Lifecycle Mismatch"])
        filtered_disc = discrepancy_details if disc_filter == "All" else discrepancy_details[discrepancy_details["Discrepancy Type"] == disc_filter]

        st.dataframe(
            filtered_disc,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Service ID": st.column_config.TextColumn("Service ID", width="medium"),
                "Partner": st.column_config.TextColumn("Partner", width="small"),
                "Discrepancy Type": st.column_config.TextColumn("Type", width="medium"),
                "PF Status": st.column_config.TextColumn("PF Status", width="small"),
                "Partner Status": st.column_config.TextColumn("Partner Status", width="small"),
                "PF Activation": st.column_config.TextColumn("PF Activated", width="small"),
                "Partner Activation": st.column_config.TextColumn("Partner Activated", width="small"),
                "MRC Impact EUR": st.column_config.NumberColumn("MRC Impact €", format="€%.2f"),
                "Root Cause": st.column_config.TextColumn("Root Cause", width="large"),
                "Days Outstanding": st.column_config.NumberColumn("Days Open", format="%d"),
            },
        )

        st.markdown('<div class="ops-title">📈 Reconciliation by Partner</div>', unsafe_allow_html=True)

        partner_recon = pd.DataFrame({
            "Partner": ["MasOrange", "MasOrange", "MasOrange", "Vodafone", "Vodafone", "Vodafone"],
            "Discrepancy": ["Orphan", "Ghost", "Lifecycle", "Orphan", "Ghost", "Lifecycle"],
            "Count": [2134, 987, 512, 1322, 905, 362],
            "MRC Impact": [26675, -12337, 1280, 16525, -11312, 905],
        })

        partner_col1, partner_col2 = st.columns(2)

        with partner_col1:
            st.markdown('<div class="ops-mini-title">MasOrange Discrepancies</div>', unsafe_allow_html=True)
            mo_disc = partner_recon[partner_recon["Partner"] == "MasOrange"]
            with st.container(border=True):
                mo_chart = alt.Chart(mo_disc).mark_bar().encode(
                    x=alt.X("Discrepancy:N", title=None),
                    y=alt.Y("Count:Q", title="Lines"),
                    color=alt.value("#FF6B00"),
                )
                st.altair_chart(mo_chart, use_container_width=True)

        with partner_col2:
            st.markdown('<div class="ops-mini-title">Vodafone Discrepancies</div>', unsafe_allow_html=True)
            vf_disc = partner_recon[partner_recon["Partner"] == "Vodafone"]
            with st.container(border=True):
                vf_chart = alt.Chart(vf_disc).mark_bar().encode(
                    x=alt.X("Discrepancy:N", title=None),
                    y=alt.Y("Count:Q", title="Lines"),
                    color=alt.value("#E60000"),
                )
                st.altair_chart(vf_chart, use_container_width=True)

        total_at_risk = orphan_mrc + lifecycle_mrc
        total_unbilled = ghost_mrc
        render_ops_ai_reco(
            "Weekly Billing Committee Preparation",
            f"€{total_at_risk:,.0f}/mo at risk from orphan lines and lifecycle drift. €{total_unbilled:,.0f}/mo potentially unbilled from ghost lines. Total discrepancy impact: €{total_at_risk + total_unbilled:,.0f}/mo.",
            "Prioritize orphan resolution with MasOrange (2,134 lines). Initiate ghost line investigation with Vodafone (905 lines). Schedule joint audit for lifecycle mismatches.",
            "Resolve 80% of discrepancies before next weekly committee to reduce billing disputes.",
            level="critical",
        )

        st.markdown('<div class="ops-title">🤖 AI-Powered Reconciliation Intelligence</div>', unsafe_allow_html=True)

        ai_col1, ai_col2 = st.columns(2)

        with ai_col1:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #1E1B4B 0%, #4338CA 100%); border-radius: 12px; padding: 1.2rem; margin-bottom: 1rem;">
                <div style="display: flex; align-items: center; margin-bottom: 0.8rem;">
                    <div style="background: #A5B4FC; border-radius: 8px; padding: 0.5rem; margin-right: 0.8rem;">
                        <span style="font-size: 1.2rem;">🔮</span>
                    </div>
                    <div>
                        <div style="color: #E0E7FF; font-size: 0.7rem; text-transform: uppercase;">Cortex ML</div>
                        <div style="color: white; font-weight: 700; font-size: 1rem;">Anomaly Detection</div>
                    </div>
                </div>
                <div style="color: #C7D2FE; font-size: 0.82rem; line-height: 1.5;">
                    ML model analyzing 892K service records to detect unusual discrepancy patterns that deviate from normal reconciliation behavior.
                </div>
            </div>
            """, unsafe_allow_html=True)

            anomaly_results = pd.DataFrame({
                "Anomaly ID": ["ANM-001", "ANM-002", "ANM-003", "ANM-004", "ANM-005"],
                "Pattern": ["Spike in MO orphans", "VF ghost cluster", "Date drift surge", "OLT-BCN bulk mismatch", "Weekend disconnect lag"],
                "Affected Lines": [156, 89, 234, 312, 67],
                "Confidence": [94.2, 87.5, 91.8, 96.3, 82.1],
                "MRC Impact EUR": [2418, 1068, 585, 4836, 1005],
                "Detection Date": ["2025-03-06", "2025-03-05", "2025-03-05", "2025-03-04", "2025-03-03"],
                "Status": ["Investigating", "Confirmed", "Resolved", "Investigating", "New"],
            })

            st.markdown('<div class="ops-mini-title">Detected Anomalies (Last 7 Days)</div>', unsafe_allow_html=True)
            st.dataframe(
                anomaly_results,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Anomaly ID": st.column_config.TextColumn("ID", width="small"),
                    "Pattern": st.column_config.TextColumn("Pattern Detected", width="medium"),
                    "Affected Lines": st.column_config.NumberColumn("Lines", format="%d"),
                    "Confidence": st.column_config.ProgressColumn("Confidence", min_value=0, max_value=100, format="%.1f%%"),
                    "MRC Impact EUR": st.column_config.NumberColumn("MRC €", format="€%,.0f"),
                    "Detection Date": st.column_config.DateColumn("Detected", format="YYYY-MM-DD"),
                    "Status": st.column_config.TextColumn("Status", width="small"),
                },
            )
            st.markdown('<div style="background: #FEF3C7; border-left: 3px solid #D97706; border-radius: 4px; padding: 0.6rem; margin-top: 0.5rem; font-size: 0.78rem;"><strong style="color: #92400E;">🔍 Insight:</strong> <span style="color: #78350F;">5 anomalies detected with 87%+ confidence. ANO-005 (312 lines, OLT-BCN cluster) requires immediate attention - VF migration without B2B notification.</span></div>', unsafe_allow_html=True)

        with ai_col2:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #14532D 0%, #22C55E 100%); border-radius: 12px; padding: 1.2rem; margin-bottom: 1rem;">
                <div style="display: flex; align-items: center; margin-bottom: 0.8rem;">
                    <div style="background: #BBF7D0; border-radius: 8px; padding: 0.5rem; margin-right: 0.8rem;">
                        <span style="font-size: 1.2rem;">🎯</span>
                    </div>
                    <div>
                        <div style="color: #DCFCE7; font-size: 0.7rem; text-transform: uppercase;">ML Classification</div>
                        <div style="color: white; font-weight: 700; font-size: 1rem;">Root Cause Predictor</div>
                    </div>
                </div>
                <div style="color: #D1FAE5; font-size: 0.82rem; line-height: 1.5;">
                    Classification model trained on 2.4M historical discrepancies to auto-predict root cause with 91% accuracy.
                </div>
            </div>
            """, unsafe_allow_html=True)

            root_cause_predictions = pd.DataFrame({
                "Root Cause": ["OSS Sync Delay", "Partner API Timeout", "Manual Entry Error", "Batch Processing Gap", "Order Workflow Stuck", "System Migration"],
                "Predicted Count": [1456, 892, 567, 423, 312, 156],
                "Confidence Avg": [93.2, 89.4, 86.7, 91.2, 84.5, 78.9],
                "Resolution Time Hrs": [4.2, 8.6, 24.0, 2.1, 12.4, 48.0],
                "Auto-Resolvable": ["Yes", "Yes", "No", "Yes", "Partial", "No"],
            })

            st.markdown('<div class="ops-mini-title">Predicted Root Causes</div>', unsafe_allow_html=True)
            with st.container(border=True):
                rc_chart = alt.Chart(root_cause_predictions).mark_bar().encode(
                    y=alt.Y("Root Cause:N", title=None, sort="-x"),
                    x=alt.X("Predicted Count:Q", title="Discrepancies"),
                    color=alt.value("#22C55E"),
                )
                st.altair_chart(rc_chart, use_container_width=True)
            st.markdown('<div style="background: #DCFCE7; border-left: 3px solid #16A34A; border-radius: 4px; padding: 0.6rem; margin-top: 0.5rem; font-size: 0.78rem;"><strong style="color: #166534;">💡 AI Insight:</strong> <span style="color: #14532D;">OSS Sync Delay (1,456 cases) is 93% auto-resolvable with 4.2hr avg resolution. Recommend enabling auto-fix to reduce manual effort by 38%.</span></div>', unsafe_allow_html=True)

        st.markdown("""
        <div style="background: linear-gradient(135deg, #7C2D12 0%, #F97316 100%); border-radius: 12px; padding: 1.2rem; margin: 1rem 0;">
            <div style="display: flex; align-items: center; margin-bottom: 0.8rem;">
                <div style="background: #FED7AA; border-radius: 8px; padding: 0.5rem; margin-right: 0.8rem;">
                    <span style="font-size: 1.2rem;">📊</span>
                </div>
                <div>
                    <div style="color: #FFEDD5; font-size: 0.7rem; text-transform: uppercase;">Cortex FORECAST</div>
                    <div style="color: white; font-weight: 700; font-size: 1rem;">Discrepancy Prediction - Next 30 Days</div>
                </div>
            </div>
            <div style="color: #FED7AA; font-size: 0.82rem; line-height: 1.5;">
                Time-series forecasting predicts discrepancy volumes to enable proactive resource allocation for reconciliation teams.
            </div>
        </div>
        """, unsafe_allow_html=True)

        forecast_data = pd.DataFrame({
            "Week": ["Week 11", "Week 12", "Week 13", "Week 14", "Week 15"],
            "Predicted Orphans": [3234, 3456, 3123, 2987, 2845],
            "Predicted Ghosts": [1756, 1892, 1678, 1534, 1423],
            "Predicted Lifecycle": [812, 874, 756, 689, 623],
            "Confidence Band": ["±12%", "±15%", "±18%", "±22%", "±25%"],
        })

        forecast_col1, forecast_col2 = st.columns([2, 1])

        with forecast_col1:
            forecast_melted = forecast_data.melt(id_vars=["Week"], value_vars=["Predicted Orphans", "Predicted Ghosts", "Predicted Lifecycle"], var_name="Type", value_name="Count")
            with st.container(border=True):
                forecast_chart = alt.Chart(forecast_melted).mark_line(point=True, strokeWidth=2).encode(
                    x=alt.X("Week:N", title=None),
                    y=alt.Y("Count:Q", title="Predicted Discrepancies"),
                    color=alt.Color("Type:N", scale=alt.Scale(domain=["Predicted Orphans", "Predicted Ghosts", "Predicted Lifecycle"], range=["#EF4444", "#F59E0B", "#3B82F6"])),
                )
                st.altair_chart(forecast_chart, use_container_width=True)
            st.markdown('<div style="background: #FFEDD5; border-left: 3px solid #EA580C; border-radius: 4px; padding: 0.6rem; margin-top: 0.5rem; font-size: 0.78rem;"><strong style="color: #9A3412;">📈 Forecast Insight:</strong> <span style="color: #7C2D12;">Week 12 spike (+18% predicted) aligns with MasOrange maintenance. Pre-assign 2 additional reconciliation resources to maintain SLA.</span></div>', unsafe_allow_html=True)

        with forecast_col2:
            st.markdown(f"""
            <div style="background: #FFF7ED; border: 2px solid #F97316; border-radius: 10px; padding: 1rem;">
                <div style="font-weight: 700; color: #9A3412; font-size: 0.9rem; margin-bottom: 0.6rem;">30-Day Forecast Summary</div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.4rem;">
                    <span style="color: #64748B; font-size: 0.8rem;">Total Predicted</span>
                    <span style="font-weight: 700; color: #EA580C;">{forecast_data['Predicted Orphans'].sum() + forecast_data['Predicted Ghosts'].sum() + forecast_data['Predicted Lifecycle'].sum():,}</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.4rem;">
                    <span style="color: #64748B; font-size: 0.8rem;">Trend</span>
                    <span style="font-weight: 600; color: #059669;">↓ Declining 12%</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.4rem;">
                    <span style="color: #64748B; font-size: 0.8rem;">Model Accuracy</span>
                    <span style="font-weight: 600; color: #7C3AED;">94.2%</span>
                </div>
                <div style="margin-top: 0.6rem; padding-top: 0.6rem; border-top: 1px solid #FDBA74;">
                    <div style="font-size: 0.75rem; color: #9A3412;"><strong>Peak Week:</strong> Week 12 - Staff accordingly</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        <div style="background: linear-gradient(135deg, #581C87 0%, #A855F7 100%); border-radius: 12px; padding: 1.2rem; margin: 1rem 0;">
            <div style="display: flex; align-items: center; margin-bottom: 0.8rem;">
                <div style="background: #E9D5FF; border-radius: 8px; padding: 0.5rem; margin-right: 0.8rem;">
                    <span style="font-size: 1.2rem;">✨</span>
                </div>
                <div>
                    <div style="color: #F3E8FF; font-size: 0.7rem; text-transform: uppercase;">Cortex LLM · Complete</div>
                    <div style="color: white; font-weight: 700; font-size: 1rem;">AI-Generated Weekly Committee Report</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        with st.container(border=True):
            report_html = """<div style="background: #FAFAFA; border-radius: 8px; padding: 1rem; font-family: 'Georgia', serif;">
<div style="color: #6B21A8; font-weight: 700; font-size: 1rem; margin-bottom: 0.8rem; border-bottom: 2px solid #E9D5FF; padding-bottom: 0.5rem;">
📋 PremiumFiber Billing Reconciliation Report
<span style="float: right; font-size: 0.75rem; color: #9CA3AF; font-weight: 400;">Week 10, 2025</span>
</div>
<div style="color: #1F2937; font-size: 0.88rem; line-height: 1.7;">
<p><strong>Executive Summary:</strong> This week's reconciliation identified <span style="color: #DC2626; font-weight: 600;">6,222 total discrepancies</span> across both partners, representing a combined MRC impact of <span style="color: #DC2626; font-weight: 600;">€89,285/month</span>. This is a 7.2% improvement from last week.</p>
<p><strong>MasOrange (58% JV share):</strong> 3,633 discrepancies identified. The primary issue is <span style="color: #F59E0B;">orphan lines (2,134)</span> caused by disconnect orders not syncing to the MO portal. Root cause analysis indicates 78% stem from the OSS batch processing delay introduced in the Feb 15 maintenance window. <em>Recommended action: Expedite OSS patch deployment scheduled for March 12.</em></p>
<p><strong>Vodafone (42% JV share):</strong> 2,589 discrepancies identified. Notable spike in <span style="color: #F59E0B;">ghost lines (905)</span> traced to VF's API timeout issues during peak hours. ML anomaly detection flagged OLT-BCN-001 cluster with 312 mismatches - investigation reveals VF migrated 400 lines without proper B2B notification. <em>Recommended action: Escalate to VF wholesale operations for data reconciliation.</em></p>
<p><strong>Forecast:</strong> Cortex ML predicts discrepancy volume will decline 12% over the next 30 days as OSS fixes take effect. Week 12 shows a temporary spike due to planned MasOrange system maintenance - recommend pre-positioning reconciliation resources.</p>
</div>
<div style="margin-top: 1rem; padding-top: 0.8rem; border-top: 1px solid #E5E7EB; display: flex; justify-content: space-between; align-items: center;">
<span style="font-size: 0.72rem; color: #9CA3AF;">Generated by Snowflake Cortex LLM · Model: llama3.1-70b</span>
<span style="font-size: 0.72rem; color: #7C3AED;">Confidence: 96.4%</span>
</div>
</div>"""
            st.markdown(report_html, unsafe_allow_html=True)

        render_ops_ai_reco(
            "AI Reconciliation Insights",
            "Cortex ML detected 5 anomaly patterns this week. Root cause classifier achieving 91% accuracy. LLM report generation reducing manual effort by 4 hours/week.",
            "Deploy auto-resolution for 'OSS Sync Delay' root cause (1,456 lines, 93% confidence). Review OLT-BCN cluster anomaly with network ops.",
            "Reduce manual reconciliation effort by 60% while improving accuracy to 98%+.",
        )

    # ═══════════════════════════════════════════════════════════════════════
    # TAB 5: Asset Amortization (Linked to Services)
    # ═══════════════════════════════════════════════════════════════════════
    with tab_amort:

        total_gross_value = 892.4
        total_net_book_value = 524.8
        accumulated_depreciation = 367.6
        monthly_depreciation = 4.8
        ytd_depreciation = 38.4

        st.markdown(f"""
        <div class="ops-pulse" style="background: linear-gradient(135deg, #1E40AF 0%, #3B82F6 100%);">
            <div class="ops-pulse-head">
                <div class="ops-pulse-title">📉 Asset Amortization - Linked to Billable Services</div>
                <div class="ops-pulse-badge">FY 2025 · Q1</div>
            </div>
            <div class="ops-pulse-grid">
                <div class="ops-pulse-card"><div class="ops-pulse-label">Gross Value</div><div class="ops-pulse-value">€{total_gross_value}M</div><div class="ops-pulse-delta" style="color: #A7F3D0;">original cost</div></div>
                <div class="ops-pulse-card"><div class="ops-pulse-label">Net Book Value</div><div class="ops-pulse-value">€{total_net_book_value}M</div><div class="ops-pulse-delta" style="color: #FDE68A;">{total_net_book_value/total_gross_value*100:.1f}% remaining</div></div>
                <div class="ops-pulse-card"><div class="ops-pulse-label">Accum. Depreciation</div><div class="ops-pulse-value">€{accumulated_depreciation}M</div><div class="ops-pulse-delta" style="color: #FCA5A5;">{accumulated_depreciation/total_gross_value*100:.1f}% depreciated</div></div>
                <div class="ops-pulse-card"><div class="ops-pulse-label">Monthly Expense</div><div class="ops-pulse-value">€{monthly_depreciation}M</div><div class="ops-pulse-delta" style="color: #A7F3D0;">per month</div></div>
                <div class="ops-pulse-card"><div class="ops-pulse-label">YTD Depreciation</div><div class="ops-pulse-value">€{ytd_depreciation}M</div><div class="ops-pulse-delta" style="color: #A7F3D0;">8 months</div></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="ops-title">🔗 Asset-to-Service Linkage</div>', unsafe_allow_html=True)

        asset_service_link = pd.DataFrame({
            "Asset ID": ["OLT-MAD-001", "OLT-MAD-002", "OLT-BCN-001", "OLT-BCN-002", "OLT-VAL-001", "SPL-MAD-001-BATCH", "SPL-BCN-001-BATCH", "FBR-MAD-TRUNK-001"],
            "Asset Type": ["OLT Chassis", "OLT Chassis", "OLT Chassis", "OLT Chassis", "OLT Chassis", "Splitter 1:32", "Splitter 1:32", "Fiber Trunk"],
            "Location": ["Madrid Central", "Madrid Norte", "Barcelona Hub", "Barcelona 22@", "Valencia DC", "Madrid Region", "Barcelona Region", "Madrid Backbone"],
            "Gross Value EUR": [125000, 125000, 145000, 125000, 145000, 224000, 192000, 890000],
            "Net Book Value EUR": [78125, 93750, 72500, 109375, 126875, 140000, 144000, 623000],
            "Depreciation Pct": [37.5, 25.0, 50.0, 12.5, 12.5, 37.5, 25.0, 30.0],
            "Status": ["In Service", "In Service", "In Service", "In Service", "In Service", "In Service", "In Service", "In Service"],
            "Services Supported": [14336, 12288, 15360, 11264, 13312, 14336, 15360, 41984],
            "Monthly MRC EUR": [222208, 190464, 238080, 174592, 206336, 222208, 238080, 650752],
            "MRC per EUR NBV": [2.84, 2.03, 3.28, 1.60, 1.63, 1.59, 1.65, 1.04],
        })

        link_col1, link_col2 = st.columns([2, 1])

        with link_col1:
            st.markdown('<div class="ops-mini-title">Asset Depreciation vs Services Supported</div>', unsafe_allow_html=True)
            with st.container(border=True):
                asset_chart = alt.Chart(asset_service_link).mark_bar().encode(
                    x=alt.X("Asset ID:N", title=None, sort="-y"),
                    y=alt.Y("Services Supported:Q", title="Lines Supported"),
                    color=alt.value("#3B82F6"),
                )
                st.altair_chart(asset_chart, use_container_width=True)
            st.markdown('<div style="background: #DBEAFE; border-left: 3px solid #2563EB; border-radius: 4px; padding: 0.6rem; margin-top: 0.5rem; font-size: 0.78rem;"><strong style="color: #1E40AF;">📊 Insight:</strong> <span style="color: #1E3A8A;">FBR-MAD-TRUNK-001 supports 42K services but has lowest efficiency (€1.04/NBV). OLT-BCN-001 leads with €3.28/NBV - consider rebalancing loads.</span></div>', unsafe_allow_html=True)

        with link_col2:
            st.markdown('<div class="ops-mini-title">Revenue Efficiency</div>', unsafe_allow_html=True)
            avg_mrc_per_nbv = asset_service_link["MRC per EUR NBV"].mean()
            best_asset = asset_service_link.loc[asset_service_link["MRC per EUR NBV"].idxmax()]
            worst_asset = asset_service_link.loc[asset_service_link["MRC per EUR NBV"].idxmin()]

            st.markdown(f"""
            <div style="background: #F8FAFC; border-radius: 10px; padding: 1rem; border: 1px solid #E2E8F0;">
                <div style="font-weight: 700; color: #0F172A; margin-bottom: 0.8rem; font-size: 0.9rem;">MRC per € Net Book Value</div>
                <div style="text-align: center; margin-bottom: 0.8rem;">
                    <div style="font-size: 2rem; font-weight: 700; color: #3B82F6;">€{avg_mrc_per_nbv:.2f}</div>
                    <div style="font-size: 0.75rem; color: #64748B;">Average across assets</div>
                </div>
                <div style="border-top: 1px solid #E2E8F0; padding-top: 0.6rem;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 0.3rem;">
                        <span style="color: #059669; font-size: 0.8rem;">Best: {best_asset['Asset ID']}</span>
                        <span style="font-weight: 600; color: #059669;">€{best_asset['MRC per EUR NBV']:.2f}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between;">
                        <span style="color: #DC2626; font-size: 0.8rem;">Lowest: {worst_asset['Asset ID']}</span>
                        <span style="font-weight: 600; color: #DC2626;">€{worst_asset['MRC per EUR NBV']:.2f}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<div class="ops-mini-title">Asset-Service Detail</div>', unsafe_allow_html=True)
        st.dataframe(
            asset_service_link,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Asset ID": st.column_config.TextColumn("Asset ID", width="medium"),
                "Asset Type": st.column_config.TextColumn("Type", width="medium"),
                "Location": st.column_config.TextColumn("Location", width="medium"),
                "Gross Value EUR": st.column_config.NumberColumn("Gross €", format="€%,.0f"),
                "Net Book Value EUR": st.column_config.NumberColumn("NBV €", format="€%,.0f"),
                "Depreciation Pct": st.column_config.ProgressColumn("Depreciated", min_value=0, max_value=100, format="%.0f%%"),
                "Status": st.column_config.TextColumn("Status", width="small"),
                "Services Supported": st.column_config.NumberColumn("Lines", format="%,d"),
                "Monthly MRC EUR": st.column_config.NumberColumn("MRC €/mo", format="€%,.0f"),
                "MRC per EUR NBV": st.column_config.NumberColumn("Efficiency", format="€%.2f"),
            },
        )

        st.markdown('<div class="ops-title">⚠️ Asset-Billing Anomalies</div>', unsafe_allow_html=True)

        anomalies = pd.DataFrame({
            "Asset ID": ["SPL-MAD-045", "SPL-BCN-023", "OLT-SEV-002", "SPL-VAL-012", "FBR-BIL-DROP-078"],
            "Asset Type": ["Splitter 1:32", "Splitter 1:32", "OLT Line Card", "Splitter 1:32", "Drop Fiber"],
            "Status": ["Decommissioned", "Decommissioned", "Decommissioned", "Failed", "Decommissioned"],
            "Decommission Date": ["2024-11-15", "2024-12-01", "2025-01-10", "2025-02-20", "2024-10-05"],
            "Services Still Linked": [24, 18, 156, 12, 8],
            "MRC Still Billed EUR": [372, 279, 2418, 186, 124],
            "Net Book Value EUR": [0, 0, 15000, 280, 0],
            "Anomaly Type": ["Ghost billing", "Ghost billing", "Ghost billing", "Failed asset billing", "Ghost billing"],
            "Action Required": ["Remove from billing", "Remove from billing", "Migrate services", "Replace asset", "Remove from billing"],
        })

        st.dataframe(
            anomalies,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Asset ID": st.column_config.TextColumn("Asset", width="medium"),
                "Asset Type": st.column_config.TextColumn("Type", width="medium"),
                "Status": st.column_config.TextColumn("Status", width="small"),
                "Decommission Date": st.column_config.DateColumn("Decommissioned", format="YYYY-MM-DD"),
                "Services Still Linked": st.column_config.NumberColumn("Lines Linked", format="%d"),
                "MRC Still Billed EUR": st.column_config.NumberColumn("MRC Billed €", format="€%,.0f"),
                "Net Book Value EUR": st.column_config.NumberColumn("NBV €", format="€%,.0f"),
                "Anomaly Type": st.column_config.TextColumn("Anomaly", width="medium"),
                "Action Required": st.column_config.TextColumn("Action", width="medium"),
            },
        )

        total_ghost_billing = anomalies["MRC Still Billed EUR"].sum()
        render_ops_ai_reco(
            "Asset-Billing Integrity Alert",
            f"5 decommissioned/failed assets still linked to {anomalies['Services Still Linked'].sum()} active services, generating €{total_ghost_billing:,.0f}/mo in potentially invalid billing.",
            "Migrate services from OLT-SEV-002 to active line card. Update billing system to remove decommissioned splitters. Process asset write-offs for fully depreciated items.",
            "Clean up ghost billing and ensure accurate capex recovery from partners.",
            level="critical",
        )

        st.markdown('<div class="ops-title">📊 Depreciation by Asset Class</div>', unsafe_allow_html=True)

        depreciation_schedule = pd.DataFrame({
            "Asset Class": ["OLT Equipment", "Splitters", "Fiber Cable", "Distribution Points", "Civil Works"],
            "Gross Value M": [156.8, 18.4, 234.2, 45.6, 89.4],
            "Net Book Value M": [98.2, 12.8, 168.5, 28.4, 62.1],
            "Accum Depreciation M": [58.6, 5.6, 65.7, 17.2, 27.3],
            "Useful Life Years": [10, 10, 20, 15, 25],
            "Avg Age Years": [3.7, 3.0, 5.6, 5.7, 7.6],
            "Monthly Depreciation M": [1.31, 0.15, 0.98, 0.25, 0.30],
            "Services Supported": [892456, 892456, 892456, 892456, 892456],
        })

        dep_col1, dep_col2 = st.columns(2)

        with dep_col1:
            st.markdown('<div class="ops-mini-title">Gross vs Net Book Value</div>', unsafe_allow_html=True)
            dep_melted = depreciation_schedule.melt(id_vars=["Asset Class"], value_vars=["Gross Value M", "Net Book Value M"], var_name="Type", value_name="Value")
            with st.container(border=True):
                dep_chart = alt.Chart(dep_melted).mark_bar().encode(
                    x=alt.X("Asset Class:N", title=None),
                    y=alt.Y("Value:Q", title="Value (€M)"),
                    color=alt.Color("Type:N", scale=alt.Scale(domain=["Gross Value M", "Net Book Value M"], range=["#94A3B8", "#3B82F6"])),
                    xOffset="Type:N",
                )
                st.altair_chart(dep_chart, use_container_width=True)
            st.markdown('<div style="background: #F1F5F9; border-left: 3px solid #475569; border-radius: 4px; padding: 0.6rem; margin-top: 0.5rem; font-size: 0.78rem;"><strong style="color: #334155;">📉 Insight:</strong> <span style="color: #1E293B;">OLT Equipment (62.6% remaining) is youngest asset class. Fiber Cable has €65.7M accumulated depreciation - largest contributor to monthly expense.</span></div>', unsafe_allow_html=True)

        with dep_col2:
            st.markdown('<div class="ops-mini-title">Monthly Depreciation Expense</div>', unsafe_allow_html=True)
            with st.container(border=True):
                monthly_chart = alt.Chart(depreciation_schedule).mark_bar().encode(
                    y=alt.Y("Asset Class:N", title=None, sort="-x"),
                    x=alt.X("Monthly Depreciation M:Q", title="€M/month"),
                    color=alt.value("#6366F1"),
                )
                st.altair_chart(monthly_chart, use_container_width=True)
            st.markdown('<div style="background: #EEF2FF; border-left: 3px solid #6366F1; border-radius: 4px; padding: 0.6rem; margin-top: 0.5rem; font-size: 0.78rem;"><strong style="color: #4338CA;">💰 Insight:</strong> <span style="color: #312E81;">OLT Equipment drives 44% of monthly depreciation (€1.31M). Consider accelerating splitter depreciation schedule given 3-year avg age vs 10-year useful life.</span></div>', unsafe_allow_html=True)

        st.markdown('<div class="ops-title">🤖 AI-Powered Asset Intelligence</div>', unsafe_allow_html=True)

        ai_asset_col1, ai_asset_col2 = st.columns(2)

        with ai_asset_col1:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #7F1D1D 0%, #EF4444 100%); border-radius: 12px; padding: 1.2rem; margin-bottom: 1rem;">
                <div style="display: flex; align-items: center; margin-bottom: 0.8rem;">
                    <div style="background: #FECACA; border-radius: 8px; padding: 0.5rem; margin-right: 0.8rem;">
                        <span style="font-size: 1.2rem;">⚠️</span>
                    </div>
                    <div>
                        <div style="color: #FEE2E2; font-size: 0.7rem; text-transform: uppercase;">Cortex ML · Predictive Maintenance</div>
                        <div style="color: white; font-weight: 700; font-size: 1rem;">Asset Failure Prediction</div>
                    </div>
                </div>
                <div style="color: #FECACA; font-size: 0.82rem; line-height: 1.5;">
                    ML model analyzing telemetry, age, utilization, and environmental data to predict asset failures 30-90 days in advance.
                </div>
            </div>
            """, unsafe_allow_html=True)

            failure_predictions = pd.DataFrame({
                "Asset ID": ["OLT-MAD-001-LC4", "SPL-VAL-089", "OLT-BCN-002-PS1", "SPL-SEV-034", "OLT-BIL-001-LC2", "FBR-MAD-DROP-234"],
                "Asset Type": ["OLT Line Card", "Splitter 1:32", "OLT Power Supply", "Splitter 1:32", "OLT Line Card", "Drop Fiber"],
                "Failure Probability": [89.2, 76.4, 72.1, 68.9, 64.3, 58.7],
                "Predicted Window": ["7-14 days", "15-30 days", "30-45 days", "30-45 days", "45-60 days", "60-90 days"],
                "Services at Risk": [512, 28, 1024, 24, 384, 12],
                "MRC at Risk EUR": [7936, 434, 15872, 372, 5952, 186],
                "Replacement Cost EUR": [8500, 450, 3200, 450, 8500, 280],
            })

            st.markdown('<div class="ops-mini-title">High-Risk Assets (Next 90 Days)</div>', unsafe_allow_html=True)
            st.dataframe(
                failure_predictions,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Asset ID": st.column_config.TextColumn("Asset ID", width="medium"),
                    "Asset Type": st.column_config.TextColumn("Type", width="medium"),
                    "Failure Probability": st.column_config.ProgressColumn("Failure Risk", min_value=0, max_value=100, format="%.1f%%"),
                    "Predicted Window": st.column_config.TextColumn("Window", width="small"),
                    "Services at Risk": st.column_config.NumberColumn("Lines", format="%d"),
                    "MRC at Risk EUR": st.column_config.NumberColumn("MRC €", format="€%,.0f"),
                    "Replacement Cost EUR": st.column_config.NumberColumn("Replace €", format="€%,.0f"),
                },
            )
            st.markdown('<div style="background: #FEE2E2; border-left: 3px solid #DC2626; border-radius: 4px; padding: 0.6rem; margin-top: 0.5rem; font-size: 0.78rem;"><strong style="color: #991B1B;">⚠️ Alert:</strong> <span style="color: #7F1D1D;">OLT-MAD-001-LC4 at 89% failure risk with 512 services (€7.9K MRC) at risk. Replacement cost €8.5K has 24-month payback - recommend immediate action.</span></div>', unsafe_allow_html=True)

        with ai_asset_col2:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%); border-radius: 12px; padding: 1.2rem; margin-bottom: 1rem;">
                <div style="display: flex; align-items: center; margin-bottom: 0.8rem;">
                    <div style="background: #BFDBFE; border-radius: 8px; padding: 0.5rem; margin-right: 0.8rem;">
                        <span style="font-size: 1.2rem;">💰</span>
                    </div>
                    <div>
                        <div style="color: #DBEAFE; font-size: 0.7rem; text-transform: uppercase;">ML Optimization</div>
                        <div style="color: white; font-weight: 700; font-size: 1rem;">Replacement Optimizer</div>
                    </div>
                </div>
                <div style="color: #BFDBFE; font-size: 0.82rem; line-height: 1.5;">
                    Optimization model balancing NBV, maintenance costs, failure risk, and service impact to recommend optimal replacement timing.
                </div>
            </div>
            """, unsafe_allow_html=True)

            replacement_reco = pd.DataFrame({
                "Asset ID": ["OLT-MAD-001-LC4", "OLT-BCN-002-PS1", "OLT-BIL-001-LC2", "SPL-VAL-089", "SPL-SEV-034"],
                "Current NBV EUR": [2125, 800, 4250, 112, 168],
                "Maint Cost YTD EUR": [3400, 1200, 890, 45, 0],
                "Failure Risk": [89.2, 72.1, 64.3, 76.4, 68.9],
                "Optimal Action": ["Replace Now", "Replace Now", "Schedule Q2", "Replace Now", "Monitor"],
                "ROI if Replaced": ["+€4,200/yr", "+€2,800/yr", "+€1,900/yr", "+€890/yr", "+€340/yr"],
                "Payback Months": [24, 14, 54, 6, 16],
            })

            st.markdown('<div class="ops-mini-title">Optimal Replacement Recommendations</div>', unsafe_allow_html=True)
            for _, row in replacement_reco.iterrows():
                if row["Optimal Action"] == "Replace Now":
                    action_color = "#EF4444"
                    action_bg = "#FEF2F2"
                elif row["Optimal Action"] == "Schedule Q2":
                    action_color = "#F59E0B"
                    action_bg = "#FFFBEB"
                else:
                    action_color = "#10B981"
                    action_bg = "#ECFDF5"

                st.markdown(f"""
                <div style="background: {action_bg}; border-left: 4px solid {action_color}; border-radius: 6px; padding: 0.6rem; margin-bottom: 0.4rem;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <span style="font-weight: 600; color: #0F172A; font-size: 0.85rem;">{row['Asset ID']}</span>
                            <span style="color: #64748B; font-size: 0.75rem; margin-left: 0.5rem;">NBV €{row['Current NBV EUR']:,}</span>
                        </div>
                        <div style="background: {action_color}; color: white; padding: 2px 8px; border-radius: 4px; font-size: 0.7rem; font-weight: 600;">
                            {row['Optimal Action']}
                        </div>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-top: 0.3rem; font-size: 0.75rem;">
                        <span style="color: #059669;">{row['ROI if Replaced']}</span>
                        <span style="color: #64748B;">Payback: {row['Payback Months']} mo</span>
                        <span style="color: #DC2626;">Risk: {row['Failure Risk']}%</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown('<div style="background: #DBEAFE; border-left: 3px solid #3B82F6; border-radius: 4px; padding: 0.6rem; margin-top: 0.5rem; font-size: 0.78rem;"><strong style="color: #1E40AF;">🎯 Optimizer Insight:</strong> <span style="color: #1E3A8A;">3 assets flagged for immediate replacement with combined ROI of €7.9K/yr. Total payback across recommendations: 23 months avg. Delaying increases failure risk by 12%/month.</span></div>', unsafe_allow_html=True)

        st.markdown("""
        <div style="background: linear-gradient(135deg, #14532D 0%, #22C55E 100%); border-radius: 12px; padding: 1.2rem; margin: 1rem 0;">
            <div style="display: flex; align-items: center; margin-bottom: 0.8rem;">
                <div style="background: #BBF7D0; border-radius: 8px; padding: 0.5rem; margin-right: 0.8rem;">
                    <span style="font-size: 1.2rem;">📈</span>
                </div>
                <div>
                    <div style="color: #DCFCE7; font-size: 0.7rem; text-transform: uppercase;">Cortex FORECAST</div>
                    <div style="color: white; font-weight: 700; font-size: 1rem;">12-Month Capex Forecast & Optimization</div>
                </div>
            </div>
            <div style="color: #D1FAE5; font-size: 0.82rem; line-height: 1.5;">
                Time-series model forecasting depreciation expense, maintenance costs, and replacement needs to optimize capex planning.
            </div>
        </div>
        """, unsafe_allow_html=True)

        capex_forecast = pd.DataFrame({
            "Month": ["Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec", "Jan", "Feb", "Mar"],
            "Depreciation M": [4.8, 4.8, 4.9, 4.9, 5.0, 5.0, 5.1, 5.1, 5.2, 5.2, 5.3, 5.3],
            "Predicted Failures": [3, 5, 4, 6, 4, 3, 5, 7, 4, 3, 4, 5],
            "Replacement Capex M": [0.12, 0.18, 0.15, 0.22, 0.14, 0.11, 0.19, 0.28, 0.16, 0.12, 0.15, 0.18],
            "Maintenance M": [0.08, 0.09, 0.07, 0.11, 0.08, 0.06, 0.10, 0.12, 0.09, 0.07, 0.08, 0.09],
            "ML Savings M": [0.04, 0.05, 0.04, 0.06, 0.04, 0.03, 0.05, 0.07, 0.05, 0.04, 0.04, 0.05],
        })

        capex_col1, capex_col2 = st.columns([2, 1])

        with capex_col1:
            capex_melted = capex_forecast.melt(id_vars=["Month"], value_vars=["Replacement Capex M", "Maintenance M", "ML Savings M"], var_name="Category", value_name="Value")
            with st.container(border=True):
                capex_chart = alt.Chart(capex_melted).mark_bar().encode(
                    x=alt.X("Month:N", title=None, sort=list(capex_forecast["Month"])),
                    y=alt.Y("Value:Q", title="€M", stack="zero"),
                    color=alt.Color("Category:N", scale=alt.Scale(domain=["Replacement Capex M", "Maintenance M", "ML Savings M"], range=["#3B82F6", "#F59E0B", "#10B981"])),
                )
                st.altair_chart(capex_chart, use_container_width=True)
            st.markdown('<div style="background: #DCFCE7; border-left: 3px solid #16A34A; border-radius: 4px; padding: 0.6rem; margin-top: 0.5rem; font-size: 0.78rem;"><strong style="color: #166534;">📈 Forecast Insight:</strong> <span style="color: #14532D;">November spike (7 failures, €0.28M capex) driven by OLT equipment lifecycle. ML savings of €0.56M/yr justify predictive maintenance investment.</span></div>', unsafe_allow_html=True)

        with capex_col2:
            total_replacement = capex_forecast["Replacement Capex M"].sum()
            total_maintenance = capex_forecast["Maintenance M"].sum()
            total_savings = capex_forecast["ML Savings M"].sum()
            total_failures = capex_forecast["Predicted Failures"].sum()

            st.markdown(f"""
            <div style="background: #F8FAFC; border: 2px solid #22C55E; border-radius: 10px; padding: 1rem;">
                <div style="font-weight: 700; color: #0F172A; font-size: 0.9rem; margin-bottom: 0.8rem;">12-Month Forecast Summary</div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.4rem;">
                    <span style="color: #64748B; font-size: 0.8rem;">Predicted Failures</span>
                    <span style="font-weight: 700; color: #DC2626;">{total_failures}</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.4rem;">
                    <span style="color: #64748B; font-size: 0.8rem;">Replacement Capex</span>
                    <span style="font-weight: 700; color: #3B82F6;">€{total_replacement:.2f}M</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.4rem;">
                    <span style="color: #64748B; font-size: 0.8rem;">Maintenance Cost</span>
                    <span style="font-weight: 700; color: #F59E0B;">€{total_maintenance:.2f}M</span>
                </div>
                <div style="border-top: 1px solid #E2E8F0; margin-top: 0.6rem; padding-top: 0.6rem;">
                    <div style="display: flex; justify-content: space-between;">
                        <span style="color: #059669; font-weight: 600; font-size: 0.85rem;">ML-Driven Savings</span>
                        <span style="font-weight: 700; color: #059669;">€{total_savings:.2f}M</span>
                    </div>
                    <div style="font-size: 0.72rem; color: #64748B; margin-top: 0.2rem;">
                        Predictive maintenance avoiding unplanned failures
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        <div style="background: linear-gradient(135deg, #581C87 0%, #A855F7 100%); border-radius: 12px; padding: 1.2rem; margin: 1rem 0;">
            <div style="display: flex; align-items: center; margin-bottom: 0.8rem;">
                <div style="background: #E9D5FF; border-radius: 8px; padding: 0.5rem; margin-right: 0.8rem;">
                    <span style="font-size: 1.2rem;">🎯</span>
                </div>
                <div>
                    <div style="color: #F3E8FF; font-size: 0.7rem; text-transform: uppercase;">Cortex ML · Anomaly Detection</div>
                    <div style="color: white; font-weight: 700; font-size: 1rem;">Asset Performance Anomalies</div>
                </div>
            </div>
            <div style="color: #E9D5FF; font-size: 0.82rem; line-height: 1.5;">
                Detecting assets with abnormal MRC efficiency, unexpected depreciation patterns, or billing misalignments.
            </div>
        </div>
        """, unsafe_allow_html=True)

        perf_anomalies = pd.DataFrame({
            "Asset ID": ["OLT-BCN-001", "SPL-MAD-BATCH-045", "FBR-VAL-TRUNK-003", "OLT-SEV-001"],
            "Anomaly Type": ["Low MRC Efficiency", "Unexpected Depreciation", "Over-allocated Services", "Underutilized Capacity"],
            "Expected Value": ["€2.50/NBV", "37.5% depreciated", "32 services/splitter", "85% utilization"],
            "Actual Value": ["€1.04/NBV", "62.1% depreciated", "48 services/splitter", "42% utilization"],
            "Deviation": ["-58%", "+66%", "+50%", "-51%"],
            "Recommended Action": ["Review pricing", "Investigate accelerated wear", "Rebalance load", "Consolidate or decommission"],
            "Priority": ["Medium", "High", "High", "Low"],
        })

        st.dataframe(
            perf_anomalies,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Asset ID": st.column_config.TextColumn("Asset", width="medium"),
                "Anomaly Type": st.column_config.TextColumn("Anomaly", width="medium"),
                "Expected Value": st.column_config.TextColumn("Expected", width="medium"),
                "Actual Value": st.column_config.TextColumn("Actual", width="medium"),
                "Deviation": st.column_config.TextColumn("Deviation", width="small"),
                "Recommended Action": st.column_config.TextColumn("Action", width="large"),
                "Priority": st.column_config.TextColumn("Priority", width="small"),
            },
        )

        render_ops_ai_reco(
            "AI Asset Management Summary",
            f"Predictive maintenance model identified 6 high-risk assets with 89% confidence. Replacement optimizer recommends immediate action on 3 assets to prevent €30,752/mo MRC disruption.",
            f"Execute proactive replacement of OLT-MAD-001-LC4 and OLT-BCN-002-PS1 this week. Schedule Q2 capex review for remaining recommendations. Investigate OLT-SEV-001 underutilization.",
            f"Reduce unplanned failures by 70% and save €{total_savings:.2f}M annually through predictive maintenance.",
        )

    st.markdown("""
    <details style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 0.8rem; margin-top: 1rem;">
        <summary style="cursor: pointer; font-weight: 600; color: #334155; font-size: 0.9rem;">Data Sources & Reconciliation Flow</summary>
        <div style="margin-top: 0.8rem; font-size: 0.85rem; color: #475569;">
            <p><strong>This dashboard aggregates data for billing reconciliation:</strong></p>
            <table style="width: 100%; border-collapse: collapse; margin: 0.5rem 0;">
                <tr style="border-bottom: 1px solid #E2E8F0;"><th style="text-align: left; padding: 0.4rem;">Data Entity</th><th style="text-align: left; padding: 0.4rem;">Source System</th><th style="text-align: left; padding: 0.4rem;">Reconciliation Role</th></tr>
                <tr><td style="padding: 0.4rem;">Network Elements</td><td style="padding: 0.4rem;"><strong>OSS/NMS</strong></td><td style="padding: 0.4rem;">Physical capacity for services</td></tr>
                <tr><td style="padding: 0.4rem;">Service Inventory</td><td style="padding: 0.4rem;"><strong>OSS/BSS</strong></td><td style="padding: 0.4rem;">Golden record for billing</td></tr>
                <tr><td style="padding: 0.4rem;">Partner Orders</td><td style="padding: 0.4rem;"><strong>Salesforce CPQ</strong></td><td style="padding: 0.4rem;">Creates/modifies inventory</td></tr>
                <tr><td style="padding: 0.4rem;">MasOrange Inventory</td><td style="padding: 0.4rem;"><strong>MO B2B Portal</strong></td><td style="padding: 0.4rem;">Partner view for reconciliation</td></tr>
                <tr><td style="padding: 0.4rem;">Vodafone Inventory</td><td style="padding: 0.4rem;"><strong>VF Wholesale API</strong></td><td style="padding: 0.4rem;">Partner view for reconciliation</td></tr>
                <tr><td style="padding: 0.4rem;">Asset Register</td><td style="padding: 0.4rem;"><strong>SAP S/4HANA AA</strong></td><td style="padding: 0.4rem;">Capex recovery tracking</td></tr>
            </table>
            <p style="margin-top: 0.5rem;"><strong>Snowflake Data Flow:</strong></p>
            <ul style="margin: 0.3rem 0; padding-left: 1.2rem;">
                <li><strong>OSS → Snowflake:</strong> Kafka streaming for service inventory changes</li>
                <li><strong>Partner Files → Snowflake:</strong> Daily SFTP ingestion of MO/VF inventory views</li>
                <li><strong>SAP → Snowflake:</strong> Real-time CDC via SAP SLT for asset data</li>
                <li><strong>Reconciliation Engine:</strong> SQL/dbt transforms compare PF vs partner views</li>
            </ul>
            <p style="margin-top: 0.5rem;"><strong>Reconciliation Logic:</strong></p>
            <ul style="margin: 0.3rem 0; padding-left: 1.2rem;">
                <li><strong>Orphan:</strong> SERVICE_INVENTORY.service_id NOT IN PARTNER_INVENTORY</li>
                <li><strong>Ghost:</strong> PARTNER_INVENTORY.line_id NOT IN SERVICE_INVENTORY</li>
                <li><strong>Lifecycle Drift:</strong> Activation/deactivation date mismatches</li>
            </ul>
        </div>
    </details>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Page: Data Sharing (Tenant Data Exchange & Governance)
# ---------------------------------------------------------------------------
elif selected_menu == "Data Sharing":
    import pandas as pd
    import altair as alt
    from datetime import datetime, timedelta

    def style_ds_chart(chart: alt.Chart, height: int = 220) -> alt.Chart:
        return (
            chart.properties(height=height, padding={"left": 6, "top": 10, "right": 8, "bottom": 6})
            .configure(background="#FFFFFF")
            .configure_view(stroke=None)
            .configure_axis(labelFontSize=10, titleFontSize=11, gridColor="#E2E8F0", domainColor="#E2E8F0")
            .configure_legend(labelFontSize=10)
        )

    def render_ds_ai_reco(title: str, insight: str, action: str, outcome: str, level: str = "info"):
        color_map = {"info": ("#6366F1", "#EEF2FF", "#3730A3"), "warning": ("#F59E0B", "#FFFBEB", "#92400E"), "critical": ("#EF4444", "#FEF2F2", "#991B1B")}
        accent, bg, text = color_map.get(level, color_map["info"])
        st.markdown(f"""<div style="background: {bg}; border-left: 4px solid {accent}; border-radius: 8px; padding: 0.65rem 0.85rem; margin-top: 0.5rem;">
            <div style="font-weight: 700; color: {text}; font-size: 0.78rem; margin-bottom: 0.2rem;">🔗 {title}</div>
            <div style="color: #334155; font-size: 0.76rem; line-height: 1.4;"><strong>Insight:</strong> {insight}</div>
            <div style="color: #334155; font-size: 0.76rem; line-height: 1.4;"><strong>Action:</strong> {action}</div>
            <div style="color: #059669; font-size: 0.74rem; margin-top: 0.2rem;"><strong>Outcome:</strong> {outcome}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("""<style>
.ds-title { font-size: 1.15rem; font-weight: 800; color: #0F172A; margin: 1.2rem 0 0.6rem; border-bottom: 2px solid #E2E8F0; padding-bottom: 0.4rem; }
.ds-mini-title { font-size: 0.88rem; font-weight: 700; color: #334155; margin-bottom: 0.5rem; }
.ds-pulse { background: linear-gradient(135deg, #4338CA 0%, #6366F1 100%); border-radius: 14px; padding: 1.1rem 1.3rem; margin-bottom: 1rem; }
.ds-pulse-head { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.8rem; }
.ds-pulse-title { color: #FFFFFF; font-size: 1rem; font-weight: 700; }
.ds-pulse-badge { background: #34D399; color: #065F46; padding: 2px 10px; border-radius: 12px; font-size: 0.68rem; font-weight: 700; }
.ds-pulse-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 0.8rem; }
.ds-pulse-card { background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.15); border-radius: 10px; padding: 0.7rem; text-align: center; }
.ds-pulse-label { color: rgba(255,255,255,0.7); font-size: 0.68rem; text-transform: uppercase; }
.ds-pulse-value { color: #FFFFFF; font-size: 1.4rem; font-weight: 800; margin-top: 0.15rem; }
.ds-pulse-delta { color: #34D399; font-size: 0.72rem; font-weight: 600; margin-top: 0.1rem; }
.ds-feed-card { background: white; border: 1px solid #E2E8F0; border-radius: 10px; padding: 0.8rem; margin-bottom: 0.5rem; }
.ds-feed-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem; }
.ds-feed-name { font-weight: 700; color: #1E293B; font-size: 0.85rem; }
.ds-feed-badge { padding: 2px 8px; border-radius: 8px; font-size: 0.68rem; font-weight: 700; }
.ds-feed-badge.masorange { background: #FFF7ED; color: #C2410C; }
.ds-feed-badge.vodafone { background: #FEF2F2; color: #B91C1C; }
.ds-feed-badge.both { background: #EEF2FF; color: #4338CA; }
.ds-feed-meta { display: flex; gap: 1rem; font-size: 0.75rem; color: #64748B; }
.ds-status-dot { width: 8px; height: 8px; border-radius: 50%; display: inline-block; margin-right: 4px; }
.ds-status-dot.active { background: #10B981; }
.ds-status-dot.warning { background: #F59E0B; }
.ds-status-dot.error { background: #EF4444; }
</style>""", unsafe_allow_html=True)

    ds_data_feeds = pd.DataFrame({
        "Feed Name": [
            "Network Availability Real-time",
            "SLA Performance Daily",
            "Incident Tickets",
            "Provisioning Orders",
            "Billing & Usage",
            "CPE Inventory",
            "Planned Maintenance",
            "Capacity Utilization",
            "Quality of Service (QoS)",
            "Fiber Route Status",
        ],
        "Category": ["Network", "SLA", "Operations", "Provisioning", "Billing", "Inventory", "Operations", "Network", "Network", "Infrastructure"],
        "Tenant": ["Both", "Both", "Both", "Both", "Both", "Both", "Both", "MasOrange", "Vodafone", "Both"],
        "Frequency": ["Real-time", "Daily", "Real-time", "Real-time", "Daily", "Weekly", "As needed", "Hourly", "Hourly", "Daily"],
        "Records/Day": [86400, 1, 245, 1820, 12000000, 50, 12, 8640, 8640, 1],
        "Latency Sec": [2, 3600, 5, 3, 7200, 86400, 300, 60, 60, 3600],
        "Status": ["Active", "Active", "Active", "Active", "Active", "Active", "Active", "Warning", "Active", "Active"],
        "SLA Target Sec": [5, 7200, 30, 10, 14400, 172800, 600, 120, 120, 7200],
        "Uptime %": [99.98, 99.95, 99.92, 99.88, 99.96, 99.90, 100.0, 98.45, 99.87, 99.94],
    })
    ds_data_feeds["SLA Met"] = ds_data_feeds["Latency Sec"] <= ds_data_feeds["SLA Target Sec"]

    ds_volume_trend = pd.DataFrame({
        "Month": ["2025-09", "2025-10", "2025-11", "2025-12", "2026-01", "2026-02"],
        "MasOrange Records M": [312, 328, 345, 362, 378, 392],
        "Vodafone Records M": [224, 235, 248, 260, 271, 281],
        "API Calls M": [48, 52, 58, 64, 68, 72],
    })

    ds_api_health = pd.DataFrame({
        "API Endpoint": ["Network Status API", "SLA Reporting API", "Order Management API", "Billing Data API", "Inventory API", "Incident API"],
        "Tenant": ["Both", "Both", "Both", "Both", "Both", "Both"],
        "Avg Response ms": [45, 120, 85, 210, 95, 38],
        "P99 Response ms": [180, 450, 320, 780, 380, 150],
        "Error Rate %": [0.02, 0.05, 0.08, 0.12, 0.04, 0.03],
        "Calls/Day K": [125, 48, 86, 24, 12, 156],
    })

    ds_data_quality = pd.DataFrame({
        "Data Domain": ["Customer Records", "Network Topology", "Billing Events", "Service Orders", "Incident Data", "Inventory"],
        "Completeness %": [99.4, 98.8, 99.7, 99.1, 98.9, 97.5],
        "Accuracy %": [99.2, 99.5, 99.8, 98.7, 99.1, 98.2],
        "Timeliness %": [99.6, 99.2, 99.4, 98.5, 99.3, 96.8],
        "DQ Score": [99.4, 99.2, 99.6, 98.8, 99.1, 97.5],
    })

    ds_compliance = pd.DataFrame({
        "Requirement": ["GDPR Data Access Logs", "Tenant Data Isolation", "Encryption at Rest", "Encryption in Transit", "Access Control Audit", "Data Retention Policy"],
        "Status": ["Compliant", "Compliant", "Compliant", "Compliant", "Compliant", "Review Needed"],
        "Last Audit": ["2026-02-15", "2026-02-15", "2026-01-20", "2026-01-20", "2026-02-01", "2025-11-30"],
        "Next Audit": ["2026-05-15", "2026-05-15", "2026-04-20", "2026-04-20", "2026-05-01", "2026-02-28"],
    })

    ds_sharing_by_category = pd.DataFrame({
        "Category": ["Network", "Billing", "Operations", "Provisioning", "SLA", "Inventory", "Infrastructure"],
        "MasOrange Feeds": [4, 2, 3, 2, 2, 1, 1],
        "Vodafone Feeds": [4, 2, 3, 2, 2, 1, 1],
        "Daily Volume GB": [45, 128, 12, 8, 2, 0.5, 0.3],
    })

    total_feeds = len(ds_data_feeds)
    active_feeds = len(ds_data_feeds[ds_data_feeds["Status"] == "Active"])
    total_daily_records = ds_data_feeds["Records/Day"].sum()
    avg_uptime = ds_data_feeds["Uptime %"].mean()
    sla_compliance = len(ds_data_feeds[ds_data_feeds["SLA Met"]]) / total_feeds * 100

    st.markdown(f"""
    <div class="ds-pulse">
        <div class="ds-pulse-head">
            <span class="ds-pulse-title">🔗 Tenant Data Sharing · Exchange & Governance</span>
            <span class="ds-pulse-badge">Live Monitoring</span>
        </div>
        <div class="ds-pulse-grid">
            <div class="ds-pulse-card">
                <div class="ds-pulse-label">Active Data Feeds</div>
                <div class="ds-pulse-value">{active_feeds}/{total_feeds}</div>
                <div class="ds-pulse-delta">All operational</div>
            </div>
            <div class="ds-pulse-card">
                <div class="ds-pulse-label">Daily Records</div>
                <div class="ds-pulse-value">{total_daily_records/1_000_000:.1f}M</div>
                <div class="ds-pulse-delta">Shared with tenants</div>
            </div>
            <div class="ds-pulse-card">
                <div class="ds-pulse-label">Avg Feed Uptime</div>
                <div class="ds-pulse-value">{avg_uptime:.2f}%</div>
                <div class="ds-pulse-delta">Above 99.5% SLA</div>
            </div>
            <div class="ds-pulse-card">
                <div class="ds-pulse-label">SLA Compliance</div>
                <div class="ds-pulse-value">{sla_compliance:.0f}%</div>
                <div class="ds-pulse-delta">Latency targets met</div>
            </div>
            <div class="ds-pulse-card">
                <div class="ds-pulse-label">Data Quality</div>
                <div class="ds-pulse-value">{ds_data_quality['DQ Score'].mean():.1f}%</div>
                <div class="ds-pulse-delta">Across all domains</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    ds_tab_feeds, ds_tab_volume, ds_tab_quality, ds_tab_compliance = st.tabs(["📡 Data Feeds", "📊 Volume & APIs", "✅ Data Quality", "🔒 Compliance"])

    with ds_tab_feeds:
        st.markdown('<div class="ds-title">Active Data Feeds by Tenant</div>', unsafe_allow_html=True)

        for _, feed in ds_data_feeds.iterrows():
            tenant_class = "both" if feed["Tenant"] == "Both" else feed["Tenant"].lower()
            status_class = "active" if feed["Status"] == "Active" else "warning" if feed["Status"] == "Warning" else "error"
            sla_status = "✓ SLA Met" if feed["SLA Met"] else "⚠ SLA Breach"
            sla_color = "#10B981" if feed["SLA Met"] else "#F59E0B"
            
            st.markdown(f"""
            <div class="ds-feed-card">
                <div class="ds-feed-header">
                    <span class="ds-feed-name"><span class="ds-status-dot {status_class}"></span>{feed['Feed Name']}</span>
                    <span class="ds-feed-badge {tenant_class}">{feed['Tenant']}</span>
                </div>
                <div class="ds-feed-meta">
                    <span>📁 {feed['Category']}</span>
                    <span>⏱️ {feed['Frequency']}</span>
                    <span>📈 {feed['Records/Day']:,} records/day</span>
                    <span>⚡ {feed['Latency Sec']}s latency</span>
                    <span style="color: {sla_color}; font-weight: 600;">{sla_status}</span>
                    <span>📊 {feed['Uptime %']:.2f}% uptime</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        warning_feeds = ds_data_feeds[ds_data_feeds["Status"] == "Warning"]
        if len(warning_feeds) > 0:
            warn_feed = warning_feeds.iloc[0]
            render_ds_ai_reco(
                "Feed Health Alert",
                f"{warn_feed['Feed Name']} showing degraded performance ({warn_feed['Uptime %']:.2f}% uptime).",
                "Investigate capacity utilization feed latency and scale infrastructure if needed.",
                "Restore full SLA compliance for MasOrange data feeds.",
                level="warning",
            )

        st.markdown('<div class="ds-title">Data Sharing by Category</div>', unsafe_allow_html=True)
        with st.container(border=True):
            cat_bar = alt.Chart(ds_sharing_by_category).mark_bar(cornerRadiusTopRight=5, cornerRadiusBottomRight=5, size=20).encode(
                x=alt.X("Daily Volume GB:Q", title="Daily Volume (GB)"),
                y=alt.Y("Category:N", title=None, sort="-x"),
                color=alt.Color("Category:N", scale=alt.Scale(scheme="tableau10"), legend=None),
                tooltip=["Category:N", alt.Tooltip("Daily Volume GB:Q", format=".1f"), "MasOrange Feeds:Q", "Vodafone Feeds:Q"],
            )
            st.altair_chart(style_ds_chart(cat_bar, height=220), use_container_width=True)
            top_category = ds_sharing_by_category.sort_values("Daily Volume GB", ascending=False).iloc[0]
            render_ds_ai_reco(
                "Data Category Distribution",
                f"Billing data dominates at {top_category['Daily Volume GB']:.0f} GB/day ({top_category['Daily Volume GB']/ds_sharing_by_category['Daily Volume GB'].sum()*100:.0f}% of total volume).",
                "Optimize billing data compression and consider incremental sync for large datasets.",
                "Reduce bandwidth costs while maintaining data freshness for tenant billing reconciliation.",
            )

    with ds_tab_volume:
        st.markdown('<div class="ds-title">Data Exchange Volume Trends</div>', unsafe_allow_html=True)
        vol_col1, vol_col2 = st.columns(2)

        with vol_col1:
            st.markdown('<div class="ds-mini-title">Records Shared by Tenant</div>', unsafe_allow_html=True)
            with st.container(border=True):
                vol_long = ds_volume_trend.melt(id_vars=["Month"], value_vars=["MasOrange Records M", "Vodafone Records M"], var_name="Tenant", value_name="Records M")
                vol_long["Tenant"] = vol_long["Tenant"].str.replace(" Records M", "")
                vol_area = alt.Chart(vol_long).mark_area(opacity=0.7).encode(
                    x=alt.X("Month:N", title=None),
                    y=alt.Y("Records M:Q", title="Records (Millions)", stack=True),
                    color=alt.Color("Tenant:N", scale=alt.Scale(domain=["MasOrange", "Vodafone"], range=["#FF6B00", "#E60000"]), legend=alt.Legend(title=None)),
                    tooltip=["Month:N", "Tenant:N", alt.Tooltip("Records M:Q", format=",")],
                )
                st.altair_chart(style_ds_chart(vol_area, height=240), use_container_width=True)
                total_mo = ds_volume_trend["MasOrange Records M"].iloc[-1]
                total_vf = ds_volume_trend["Vodafone Records M"].iloc[-1]
                render_ds_ai_reco(
                    "Data Volume Growth",
                    f"Monthly data sharing: {total_mo}M records to MasOrange, {total_vf}M to Vodafone.",
                    "Monitor storage and bandwidth capacity as volumes grow ~5% monthly.",
                    "Ensure scalable data infrastructure for tenant growth.",
                )

        with vol_col2:
            st.markdown('<div class="ds-mini-title">API Call Volume</div>', unsafe_allow_html=True)
            with st.container(border=True):
                api_line = alt.Chart(ds_volume_trend).mark_line(point=True, strokeWidth=3, color="#6366F1").encode(
                    x=alt.X("Month:N", title=None),
                    y=alt.Y("API Calls M:Q", title="API Calls (Millions)"),
                    tooltip=["Month:N", alt.Tooltip("API Calls M:Q", format=",")],
                )
                api_area = alt.Chart(ds_volume_trend).mark_area(opacity=0.3, color="#6366F1").encode(
                    x=alt.X("Month:N", title=None),
                    y=alt.Y("API Calls M:Q"),
                )
                st.altair_chart(style_ds_chart(api_area + api_line, height=240), use_container_width=True)
                api_growth = (ds_volume_trend["API Calls M"].iloc[-1] - ds_volume_trend["API Calls M"].iloc[0]) / ds_volume_trend["API Calls M"].iloc[0] * 100
                render_ds_ai_reco(
                    "API Integration Trend",
                    f"API calls grew {api_growth:.0f}% over 6 months ({ds_volume_trend['API Calls M'].iloc[0]}M → {ds_volume_trend['API Calls M'].iloc[-1]}M/month).",
                    "Evaluate API gateway capacity and consider rate limiting policies for peak loads.",
                    "Maintain sub-100ms response times during tenant integration growth.",
                )

        st.markdown('<div class="ds-title">API Endpoint Health</div>', unsafe_allow_html=True)
        with st.container(border=True):
            api_scatter = alt.Chart(ds_api_health).mark_circle(opacity=0.85, stroke="#FFFFFF", strokeWidth=1.2).encode(
                x=alt.X("Avg Response ms:Q", title="Avg Response Time (ms)"),
                y=alt.Y("Error Rate %:Q", title="Error Rate (%)"),
                size=alt.Size("Calls/Day K:Q", scale=alt.Scale(range=[200, 1000]), legend=alt.Legend(title="Calls/Day (K)")),
                color=alt.Color("API Endpoint:N", legend=None),
                tooltip=["API Endpoint:N", alt.Tooltip("Avg Response ms:Q"), alt.Tooltip("P99 Response ms:Q"), alt.Tooltip("Error Rate %:Q", format=".2f"), alt.Tooltip("Calls/Day K:Q", format=",")],
            )
            api_labels = alt.Chart(ds_api_health).mark_text(dy=-12, fontSize=9, color="#1E293B").encode(
                x="Avg Response ms:Q", y="Error Rate %:Q", text="API Endpoint:N"
            )
            st.altair_chart(style_ds_chart(api_scatter + api_labels, height=260), use_container_width=True)
            slowest_api = ds_api_health.sort_values("Avg Response ms", ascending=False).iloc[0]
            render_ds_ai_reco(
                "API Performance",
                f"{slowest_api['API Endpoint']} has highest latency ({slowest_api['Avg Response ms']}ms avg, {slowest_api['P99 Response ms']}ms P99).",
                "Optimize billing data queries and consider caching for frequently accessed data.",
                "Improve tenant API experience and reduce integration complaints.",
                level="warning",
            )

    with ds_tab_quality:
        st.markdown('<div class="ds-title">Data Quality Scorecard</div>', unsafe_allow_html=True)
        dq_col1, dq_col2 = st.columns(2)

        with dq_col1:
            st.markdown('<div class="ds-mini-title">DQ Score by Domain</div>', unsafe_allow_html=True)
            with st.container(border=True):
                dq_bar = alt.Chart(ds_data_quality).mark_bar(cornerRadiusTopRight=5, cornerRadiusBottomRight=5, size=22).encode(
                    x=alt.X("DQ Score:Q", title="DQ Score (%)", scale=alt.Scale(domain=[95, 100])),
                    y=alt.Y("Data Domain:N", title=None, sort="-x"),
                    color=alt.Color("DQ Score:Q", scale=alt.Scale(domain=[96, 100], range=["#FCD34D", "#10B981"]), legend=None),
                    tooltip=["Data Domain:N", alt.Tooltip("DQ Score:Q", format=".1f"), alt.Tooltip("Completeness %:Q", format=".1f"), alt.Tooltip("Accuracy %:Q", format=".1f"), alt.Tooltip("Timeliness %:Q", format=".1f")],
                )
                target_line = alt.Chart(pd.DataFrame({"x": [98]})).mark_rule(strokeDash=[4, 4], color="#6366F1", strokeWidth=2).encode(x="x:Q")
                st.altair_chart(style_ds_chart(dq_bar + target_line, height=220), use_container_width=True)
                lowest_dq = ds_data_quality.sort_values("DQ Score").iloc[0]
                render_ds_ai_reco(
                    "Data Quality Focus",
                    f"{lowest_dq['Data Domain']} has lowest DQ score ({lowest_dq['DQ Score']:.1f}%), mainly due to timeliness.",
                    "Implement automated inventory reconciliation to improve data freshness.",
                    "Meet 98% DQ target across all data domains.",
                    level="warning",
                )

        with dq_col2:
            st.markdown('<div class="ds-mini-title">Quality Dimensions</div>', unsafe_allow_html=True)
            with st.container(border=True):
                dq_long = ds_data_quality.melt(id_vars=["Data Domain"], value_vars=["Completeness %", "Accuracy %", "Timeliness %"], var_name="Dimension", value_name="Score")
                dq_heat = alt.Chart(dq_long).mark_rect(cornerRadius=4).encode(
                    x=alt.X("Dimension:N", title=None),
                    y=alt.Y("Data Domain:N", title=None),
                    color=alt.Color("Score:Q", scale=alt.Scale(domain=[96, 100], range=["#FEF3C7", "#10B981"]), legend=alt.Legend(title="Score %")),
                    tooltip=["Data Domain:N", "Dimension:N", alt.Tooltip("Score:Q", format=".1f")],
                )
                dq_text = alt.Chart(dq_long).mark_text(fontSize=10, fontWeight="bold").encode(
                    x="Dimension:N", y="Data Domain:N", text=alt.Text("Score:Q", format=".1f"),
                    color=alt.condition(alt.datum.Score < 98, alt.value("#B45309"), alt.value("#065F46"))
                )
                st.altair_chart(style_ds_chart(dq_heat + dq_text, height=220), use_container_width=True)
                timeliness_issues = dq_long[dq_long["Dimension"] == "Timeliness %"].sort_values("Score").iloc[0]
                render_ds_ai_reco(
                    "Quality Dimensions Analysis",
                    f"Timeliness is the weakest dimension across domains ({timeliness_issues['Data Domain']}: {timeliness_issues['Score']:.1f}%).",
                    "Implement real-time data pipelines for inventory and order data to reduce latency.",
                    "Achieve 99%+ timeliness across all data domains shared with tenants.",
                )

    with ds_tab_compliance:
        st.markdown('<div class="ds-title">Data Governance & Compliance</div>', unsafe_allow_html=True)

        comp_col1, comp_col2 = st.columns([2, 1])
        with comp_col1:
            for _, req in ds_compliance.iterrows():
                status_color = "#10B981" if req["Status"] == "Compliant" else "#F59E0B"
                status_icon = "✅" if req["Status"] == "Compliant" else "⚠️"
                st.markdown(f"""
                <div style="background: white; border: 1px solid #E2E8F0; border-radius: 10px; padding: 0.8rem; margin-bottom: 0.5rem; border-left: 4px solid {status_color};">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-weight: 700; color: #1E293B;">{status_icon} {req['Requirement']}</span>
                        <span style="background: {'#ECFDF5' if req['Status'] == 'Compliant' else '#FFFBEB'}; color: {'#065F46' if req['Status'] == 'Compliant' else '#92400E'}; padding: 2px 10px; border-radius: 8px; font-size: 0.72rem; font-weight: 700;">{req['Status']}</span>
                    </div>
                    <div style="font-size: 0.75rem; color: #64748B; margin-top: 0.3rem;">
                        Last Audit: {req['Last Audit']} · Next Audit: {req['Next Audit']}
                    </div>
                </div>
                """, unsafe_allow_html=True)

        with comp_col2:
            compliant_count = len(ds_compliance[ds_compliance["Status"] == "Compliant"])
            total_reqs = len(ds_compliance)
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #ECFDF5 0%, #D1FAE5 100%); border-radius: 12px; padding: 1.2rem; text-align: center;">
                <div style="font-size: 2.5rem; font-weight: 800; color: #065F46;">{compliant_count}/{total_reqs}</div>
                <div style="font-size: 0.85rem; color: #047857; font-weight: 600;">Requirements Compliant</div>
                <div style="font-size: 0.75rem; color: #059669; margin-top: 0.5rem;">1 item needs review</div>
            </div>
            """, unsafe_allow_html=True)

        review_needed = ds_compliance[ds_compliance["Status"] == "Review Needed"]
        if len(review_needed) > 0:
            render_ds_ai_reco(
                "Compliance Action Required",
                f"'{review_needed.iloc[0]['Requirement']}' requires review before {review_needed.iloc[0]['Next Audit']}.",
                "Schedule compliance review meeting with legal and data governance teams.",
                "Maintain full regulatory compliance and avoid audit findings.",
                level="warning",
            )

        st.markdown('<div class="ds-title">Data Access Summary by Tenant</div>', unsafe_allow_html=True)
        with st.container(border=True):
            access_summary = pd.DataFrame({
                "Tenant": ["MasOrange", "Vodafone"],
                "Data Feeds": [10, 10],
                "API Endpoints": [6, 6],
                "Daily Volume GB": [142, 98],
                "Active Users": [45, 32],
                "Last Access": ["2 min ago", "5 min ago"],
            })
            st.dataframe(
                access_summary.style.format({
                    "Daily Volume GB": "{:.0f} GB",
                    "Active Users": "{:.0f}",
                }),
                use_container_width=True,
                hide_index=True,
            )
            render_ds_ai_reco(
                "Tenant Access Patterns",
                "MasOrange consumes 45% more data volume than Vodafone (142 GB vs 98 GB daily).",
                "Review MasOrange data needs and optimize delivery pipelines for high-volume feeds.",
                "Ensure equitable data access and SLA performance across both tenants.",
            )

    st.markdown("""
    <details style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 0.8rem; margin-top: 1rem;">
        <summary style="cursor: pointer; font-weight: 600; color: #334155; font-size: 0.9rem;">▸ Data Sources & Systems</summary>
        <div style="margin-top: 0.8rem; font-size: 0.85rem; color: #475569;">
            <p><strong>This dashboard aggregates data from the following source systems:</strong></p>
            <table style="width: 100%; border-collapse: collapse; margin: 0.5rem 0;">
                <tr style="border-bottom: 1px solid #E2E8F0;"><th style="text-align: left; padding: 0.4rem;">Data Element</th><th style="text-align: left; padding: 0.4rem;">Source System</th><th style="text-align: left; padding: 0.4rem;">Refresh</th></tr>
                <tr><td style="padding: 0.4rem;">Data feed status</td><td style="padding: 0.4rem;"><strong>Kong/Apigee</strong> + Airflow</td><td style="padding: 0.4rem;">Real-time</td></tr>
                <tr><td style="padding: 0.4rem;">Records/volume metrics</td><td style="padding: 0.4rem;"><strong>Snowflake</strong> Data Warehouse</td><td style="padding: 0.4rem;">Hourly</td></tr>
                <tr><td style="padding: 0.4rem;">API call metrics</td><td style="padding: 0.4rem;"><strong>API Gateway Analytics</strong></td><td style="padding: 0.4rem;">Real-time</td></tr>
                <tr><td style="padding: 0.4rem;">API response times</td><td style="padding: 0.4rem;"><strong>Datadog/New Relic</strong> APM</td><td style="padding: 0.4rem;">Real-time</td></tr>
                <tr><td style="padding: 0.4rem;">Data quality scores</td><td style="padding: 0.4rem;"><strong>Great Expectations</strong></td><td style="padding: 0.4rem;">Daily</td></tr>
                <tr><td style="padding: 0.4rem;">Compliance status</td><td style="padding: 0.4rem;"><strong>ServiceNow GRC</strong></td><td style="padding: 0.4rem;">On audit</td></tr>
            </table>
            <p><strong>Key Integrations:</strong></p>
            <ul style="margin: 0.3rem 0; padding-left: 1.2rem;">
                <li>Tenant feeds via <strong>Snowflake Data Sharing</strong></li>
                <li>API auth via <strong>OAuth 2.0</strong></li>
                <li>Lineage in <strong>Alation/Collibra</strong> Data Catalog</li>
                <li>GDPR logs synced with <strong>Legal & Privacy</strong></li>
                <li>Audit trails in <strong>immutable storage</strong> (7 years)</li>
            </ul>
        </div>
    </details>
    """, unsafe_allow_html=True)

elif selected_menu == "Marketing":
    import pandas as pd
    import altair as alt

    MKT_CHART_THEME = {
        "bg": "#F8FAFF",
        "title": "#1E3A8A",
        "axis": "#334155",
        "grid": "#E2E8F0",
        "font": "Inter",
    }

    def style_mkt_chart(chart: alt.Chart, height: int = 220) -> alt.Chart:
        return (
            chart.properties(height=height, padding={"left": 10, "right": 10, "top": 8, "bottom": 4})
            .configure(background=MKT_CHART_THEME["bg"])
            .configure_view(stroke=None, cornerRadius=10)
            .configure_title(color=MKT_CHART_THEME["title"], fontSize=13, font=MKT_CHART_THEME["font"], anchor="start")
            .configure_axis(
                labelColor=MKT_CHART_THEME["axis"],
                titleColor=MKT_CHART_THEME["axis"],
                gridColor=MKT_CHART_THEME["grid"],
                labelFont=MKT_CHART_THEME["font"],
                titleFont=MKT_CHART_THEME["font"],
            )
            .configure_legend(
                labelColor=MKT_CHART_THEME["axis"],
                titleColor=MKT_CHART_THEME["axis"],
                labelFont=MKT_CHART_THEME["font"],
                titleFont=MKT_CHART_THEME["font"],
            )
        )

    def render_mkt_ai_reco(headline: str, insight: str, action: str, impact: str, level: str = "info") -> None:
        level_class = "crit" if level == "critical" else "warn" if level == "warning" else ""
        icon = "🚨" if level == "critical" else "⚠️" if level == "warning" else "🤖"
        st.markdown(dedent(f"""
            <div class="mkt-ai-card {level_class}">
                <div class="h">{icon} {headline}</div>
                <div class="b"><strong>Insight:</strong> {insight}</div>
                <div class="b"><strong>Action:</strong> {action}</div>
                <div class="b"><strong>Expected Impact:</strong> {impact}</div>
            </div>
        """), unsafe_allow_html=True)

    st.markdown(dedent("""
        <style>
            @keyframes mkt-fade-up {
                from { opacity: 0; transform: translateY(8px); }
                to { opacity: 1; transform: translateY(0); }
            }
            @keyframes mkt-pulse-glow {
                0%, 100% { box-shadow: 0 0 0 0 rgba(37, 99, 235, 0.1); }
                50% { box-shadow: 0 0 0 8px rgba(37, 99, 235, 0.03); }
            }
            .mkt-title {
                font-size: 1.08rem;
                font-weight: 800;
                color: #1E3A8A;
                letter-spacing: 0.01em;
                margin: 0.3rem 0 0.6rem 0;
                animation: mkt-fade-up 0.45s ease-out both;
            }
            .mkt-mini-title {
                font-size: 0.92rem;
                font-weight: 700;
                color: #334155;
                margin: 0.12rem 0 0.5rem 0;
                animation: mkt-fade-up 0.45s ease-out both;
            }
            .mkt-pulse {
                border-radius: 12px;
                border: 1px solid #DBEAFE;
                background: linear-gradient(135deg, #EFF6FF 0%, #E0F2FE 100%);
                padding: 0.8rem 0.95rem;
                margin-bottom: 0.65rem;
                animation: mkt-fade-up 0.45s ease-out both, mkt-pulse-glow 2.8s ease-in-out infinite;
            }
            .mkt-pulse-grid, .mkt-kpi-grid {
                display: grid;
                grid-template-columns: repeat(4, minmax(0, 1fr));
                gap: 0.48rem;
            }
            .mkt-pulse-card, .mkt-kpi-card {
                border-radius: 10px;
                background: rgba(255, 255, 255, 0.88);
                border: 1px solid #E2E8F0;
                padding: 0.52rem 0.62rem;
            }
            .mkt-pulse-card .k, .mkt-kpi-card .k {
                font-size: 0.69rem;
                color: #64748B;
                text-transform: uppercase;
                letter-spacing: 0.03em;
                font-weight: 700;
            }
            .mkt-pulse-card .v, .mkt-kpi-card .v {
                font-size: 1.04rem;
                color: #0F172A;
                font-weight: 800;
                line-height: 1.1;
                margin-top: 0.08rem;
            }
            .mkt-pulse-card .d, .mkt-kpi-card .d {
                font-size: 0.74rem;
                color: #475569;
                margin-top: 0.12rem;
            }
            .mkt-kpi-card.warn { border-left: 4px solid #F59E0B; }
            .mkt-kpi-card.crit { border-left: 4px solid #EF4444; }
            .mkt-ai-card {
                border-radius: 10px;
                border-left: 4px solid #3B82F6;
                background: #EFF6FF;
                padding: 0.62rem 0.72rem;
                margin-top: 0.46rem;
                animation: mkt-fade-up 0.42s ease-out both;
            }
            .mkt-ai-card.warn { border-left-color: #F59E0B; background: #FFFBEB; }
            .mkt-ai-card.crit { border-left-color: #EF4444; background: #FEF2F2; }
            .mkt-ai-card .h {
                font-size: 0.83rem;
                font-weight: 800;
                color: #1E293B;
                margin-bottom: 0.28rem;
            }
            .mkt-ai-card .b {
                font-size: 0.78rem;
                color: #334155;
                line-height: 1.42;
            }
            @media (max-width: 1200px) {
                .mkt-pulse-grid, .mkt-kpi-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
            }
        </style>
    """), unsafe_allow_html=True)

    mkt_monthly = pd.DataFrame({
        "Month": ["2025-09", "2025-10", "2025-11", "2025-12", "2026-01", "2026-02"],
        "Spend M": [0.38, 0.40, 0.43, 0.45, 0.47, 0.49],
        "Leads K": [3.8, 4.0, 4.2, 4.5, 4.7, 5.0],
        "MQL K": [1.9, 2.0, 2.2, 2.4, 2.5, 2.7],
        "SQL K": [0.82, 0.88, 0.95, 1.03, 1.10, 1.18],
        "New Subs K": [0.28, 0.31, 0.34, 0.37, 0.40, 0.43],
        "Pipeline M": [1.6, 1.7, 1.9, 2.1, 2.3, 2.5],
        "Revenue M": [0.58, 0.63, 0.69, 0.76, 0.84, 0.92],
    })
    mkt_channels = pd.DataFrame({
        "Channel": ["PF Search", "PF Social", "PF SEO", "PF Afiliados", "PF Partners", "PF CRM"],
        "Spend M": [0.62, 0.44, 0.39, 0.33, 0.47, 0.37],
        "Leads K": [8.2, 6.9, 4.5, 3.8, 4.1, 2.7],
        "New Subs K": [0.52, 0.41, 0.33, 0.29, 0.35, 0.23],
        "Revenue M": [1.36, 0.91, 0.78, 0.65, 1.01, 0.62],
    })
    mkt_channels["CAC"] = (mkt_channels["Spend M"] * 1_000_000 / (mkt_channels["New Subs K"] * 1_000)).round(0)
    mkt_channels["CVR %"] = (mkt_channels["New Subs K"] / mkt_channels["Leads K"] * 100).round(1)
    mkt_channels["ROAS"] = (mkt_channels["Revenue M"] / mkt_channels["Spend M"]).round(2)

    mkt_campaigns = pd.DataFrame({
        "Campaign": ["PF Hogar Upgrade 600", "PF Vuelta a Clases", "PF Empresas Fast Lane", "PF Referidos Plus", "PF Winback Sprint", "PF Retention Upgrade"],
        "Stage": ["Acquisition", "Acquisition", "Acquisition", "Referral", "Retention", "Retention"],
        "Spend M": [0.36, 0.34, 0.39, 0.28, 0.23, 0.21],
        "Clicks K": [82, 76, 69, 54, 47, 42],
        "Leads K": [5.2, 4.8, 4.4, 3.8, 3.0, 2.6],
        "Revenue M": [0.92, 0.84, 0.98, 0.71, 0.55, 0.49],
    })
    mkt_campaigns["CTR %"] = (mkt_campaigns["Clicks K"] / 4_600 * 100).round(2)
    mkt_campaigns["CVR %"] = (mkt_campaigns["Leads K"] / mkt_campaigns["Clicks K"] * 100).round(2)
    mkt_campaigns["CPA"] = (mkt_campaigns["Spend M"] * 1_000_000 / (mkt_campaigns["Leads K"] * 1_000)).round(0)
    mkt_campaigns["ROI %"] = ((mkt_campaigns["Revenue M"] - mkt_campaigns["Spend M"]) / mkt_campaigns["Spend M"] * 100).round(1)

    mkt_funnel = pd.DataFrame({
        "Stage": ["Visits", "Leads", "MQL", "SQL", "Wins"],
        "Volume K": [310, mkt_monthly.iloc[-1]["Leads K"], mkt_monthly.iloc[-1]["MQL K"], mkt_monthly.iloc[-1]["SQL K"], mkt_monthly.iloc[-1]["New Subs K"]],
    })
    mkt_funnel["Conversion %"] = (mkt_funnel["Volume K"] / mkt_funnel["Volume K"].shift(1) * 100).round(1)
    mkt_funnel.loc[0, "Conversion %"] = 100.0

    mkt_risk = pd.DataFrame({
        "Risk Driver": ["Channel CAC Inflation", "Attribution Blind Spots", "Partner Lead Volatility", "Creative Fatigue", "Compliance Delay"],
        "Exposure M": [1.42, 1.15, 0.96, 0.82, 0.58],
        "Likelihood": [3.9, 3.4, 3.2, 3.1, 2.6],
    })
    mkt_scenario = pd.DataFrame({
        "Scenario": ["Downside", "Base", "Upside"],
        "Quarter Revenue M": [2.2, 2.5, 2.9],
        "New Subs K": [1.9, 2.2, 2.5],
        "Probability": ["25%", "50%", "25%"],
    })

    total_spend_m = mkt_monthly["Spend M"].sum()
    total_revenue_m = mkt_monthly["Revenue M"].sum()
    blended_roas = total_revenue_m / total_spend_m
    total_new_subs_k = mkt_monthly["New Subs K"].sum()
    blended_cac = total_spend_m * 1_000_000 / (total_new_subs_k * 1_000)
    lead_to_mql = mkt_monthly["MQL K"].sum() / mkt_monthly["Leads K"].sum()
    sql_to_win = mkt_monthly["New Subs K"].sum() / mkt_monthly["SQL K"].sum()
    pipeline_latest = mkt_monthly.iloc[-1]["Pipeline M"]
    revenue_growth = (mkt_monthly.iloc[-1]["Revenue M"] / mkt_monthly.iloc[0]["Revenue M"] - 1) * 100
    top_risk_mkt = mkt_risk.loc[mkt_risk["Exposure M"].idxmax()]

    st.markdown('<div class="mkt-title">Marketing Pulse</div>', unsafe_allow_html=True)
    st.markdown(dedent(f"""
        <div class="mkt-pulse">
            <div class="mkt-pulse-grid">
                <div class="mkt-pulse-card"><div class="k">Revenue Influenced</div><div class="v">€{total_revenue_m:.2f}M</div><div class="d">Six-month attributable revenue</div></div>
                <div class="mkt-pulse-card"><div class="k">Pipeline</div><div class="v">€{pipeline_latest:.2f}M</div><div class="d">Latest month pipeline</div></div>
                <div class="mkt-pulse-card"><div class="k">Blended ROAS</div><div class="v">{blended_roas:.2f}x</div><div class="d">Revenue per € invested</div></div>
                <div class="mkt-pulse-card"><div class="k">Blended CAC</div><div class="v">€{blended_cac:,.0f}</div><div class="d">Acquisition efficiency</div></div>
                <div class="mkt-pulse-card"><div class="k">Lead → MQL</div><div class="v">{lead_to_mql:.1%}</div><div class="d">Qualification quality</div></div>
                <div class="mkt-pulse-card"><div class="k">Revenue Growth</div><div class="v">{revenue_growth:+.1f}%</div><div class="d">Six-month trajectory</div></div>
            </div>
        </div>
    """), unsafe_allow_html=True)

    mkt_tab_overview, mkt_tab_ops, mkt_tab_risk = st.tabs([
        "📈 Marketing Overview",
        "🧭 Marketing Operations",
        "⚠️ Risk & Strategy",
    ])

    with mkt_tab_overview:
        st.markdown('<div class="mkt-title">Marketing Performance Overview</div>', unsafe_allow_html=True)
        st.markdown(dedent(f"""
            <div class="mkt-kpi-grid">
                <div class="mkt-kpi-card"><div class="k">Total Spend</div><div class="v">€{total_spend_m:.2f}M</div><div class="d">Six-month investment</div></div>
                <div class="mkt-kpi-card"><div class="k">New Subscribers</div><div class="v">{total_new_subs_k:.1f}K</div><div class="d">Marketing-driven wins</div></div>
                <div class="mkt-kpi-card {'warn' if blended_cac > 140 else ''}"><div class="k">Blended CAC</div><div class="v">€{blended_cac:,.0f}</div><div class="d">Efficiency benchmark</div></div>
                <div class="mkt-kpi-card"><div class="k">SQL to Win</div><div class="v">{sql_to_win:.1%}</div><div class="d">Sales conversion quality</div></div>
            </div>
        """), unsafe_allow_html=True)

        ov_col1, ov_col2 = st.columns(2)
        with ov_col1:
            st.markdown('<div class="mkt-mini-title">Spend and Revenue Trend</div>', unsafe_allow_html=True)
            with st.container(border=True):
                spend_bar = alt.Chart(mkt_monthly).mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6, size=34, color="#93C5FD").encode(
                    x=alt.X("Month:N", title=None),
                    y=alt.Y("Spend M:Q", title="Spend (€ M)"),
                    tooltip=["Month:N", alt.Tooltip("Spend M:Q", format=".2f"), alt.Tooltip("Revenue M:Q", format=".2f"), alt.Tooltip("New Subs K:Q", format=".1f")],
                )
                rev_line = alt.Chart(mkt_monthly).mark_line(point=True, strokeWidth=3, color="#10B981").encode(
                    x="Month:N",
                    y=alt.Y("Revenue M:Q", title="Revenue (€ M)"),
                )
                st.altair_chart(style_mkt_chart(alt.layer(spend_bar, rev_line).resolve_scale(y="independent"), height=235), use_container_width=True)
                render_mkt_ai_reco(
                    "Investment Efficiency",
                    f"Revenue trend outpaces spend growth, delivering blended ROAS of {blended_roas:.2f}x.",
                    "Sustain high-performing campaign mix and shift budget away from low-ROI cohorts.",
                    "Improves marginal returns while preserving volume growth.",
                )

        with ov_col2:
            st.markdown('<div class="mkt-mini-title">Channel Efficiency Matrix</div>', unsafe_allow_html=True)
            with st.container(border=True):
                ch_scatter = alt.Chart(mkt_channels).mark_circle(opacity=0.88, stroke="#FFFFFF", strokeWidth=1.2).encode(
                    x=alt.X("CAC:Q", title="CAC (€)"),
                    y=alt.Y("CVR %:Q", title="Conversion (%)"),
                    size=alt.Size("Spend M:Q", scale=alt.Scale(range=[260, 1500]), legend=None),
                    color=alt.Color("ROAS:Q", scale=alt.Scale(scheme="blues"), legend=alt.Legend(title="ROAS")),
                    tooltip=["Channel:N", alt.Tooltip("CAC:Q", format=".0f"), alt.Tooltip("CVR %:Q", format=".1f"), alt.Tooltip("ROAS:Q", format=".2f"), alt.Tooltip("Spend M:Q", format=".2f")],
                )
                ch_label = alt.Chart(mkt_channels).mark_text(dy=-10, fontSize=9, color="#1E293B").encode(
                    x="CAC:Q", y="CVR %:Q", text="Channel:N"
                )
                st.altair_chart(style_mkt_chart(ch_scatter + ch_label, height=235), use_container_width=True)
                best_channel = mkt_channels.sort_values(["ROAS", "CVR %"], ascending=False).iloc[0]
                render_mkt_ai_reco(
                    "Channel Prioritization",
                    f"{best_channel['Channel']} is currently the strongest efficiency channel with ROAS {best_channel['ROAS']:.2f}x.",
                    f"Increase budget elasticity for {best_channel['Channel']} while capping high-CAC channels.",
                    "Raises qualified volume with controlled acquisition cost inflation.",
                )

        ov_col3, ov_col4 = st.columns(2)
        with ov_col3:
            st.markdown('<div class="mkt-mini-title">Lead and Pipeline Momentum</div>', unsafe_allow_html=True)
            with st.container(border=True):
                lead_line = alt.Chart(mkt_monthly).mark_line(point=True, strokeWidth=3, color="#3B82F6").encode(
                    x=alt.X("Month:N", title=None),
                    y=alt.Y("Leads K:Q", title="Leads (K)"),
                    tooltip=["Month:N", alt.Tooltip("Leads K:Q", format=".1f"), alt.Tooltip("MQL K:Q", format=".1f"), alt.Tooltip("Pipeline M:Q", format=".2f")],
                )
                pipe_line = alt.Chart(mkt_monthly).mark_line(point=True, strokeWidth=2.8, color="#10B981").encode(
                    x="Month:N",
                    y=alt.Y("Pipeline M:Q", title="Pipeline (€ M)"),
                )
                st.altair_chart(style_mkt_chart(alt.layer(lead_line, pipe_line).resolve_scale(y="independent"), height=235), use_container_width=True)
                pipeline_growth = (mkt_monthly.iloc[-1]["Pipeline M"] / mkt_monthly.iloc[0]["Pipeline M"] - 1) * 100
                render_mkt_ai_reco(
                    "Demand Momentum",
                    f"Pipeline expanded {pipeline_growth:.1f}% across the period with steady lead growth.",
                    "Reinforce high-intent nurture flows to protect lead quality while scaling volume.",
                    "Supports durable top-funnel growth and stronger quarter-close confidence.",
                )

        with ov_col4:
            st.markdown('<div class="mkt-mini-title">ROAS by Channel</div>', unsafe_allow_html=True)
            with st.container(border=True):
                roas_bar = alt.Chart(mkt_channels).mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6, size=26).encode(
                    x=alt.X("Channel:N", sort="-y", title=None),
                    y=alt.Y("ROAS:Q", title="ROAS (x)"),
                    color=alt.Color("ROAS:Q", scale=alt.Scale(scheme="blues"), legend=None),
                    tooltip=["Channel:N", alt.Tooltip("ROAS:Q", format=".2f"), alt.Tooltip("Spend M:Q", format=".2f"), alt.Tooltip("Revenue M:Q", format=".2f"), alt.Tooltip("CAC:Q", format=".0f")],
                )
                roas_target = alt.Chart(pd.DataFrame({"y": [3.0]})).mark_rule(color="#94A3B8", strokeDash=[4, 4]).encode(y="y:Q")
                roas_text = alt.Chart(mkt_channels).mark_text(dy=-8, fontSize=9, color="#0F172A").encode(
                    x=alt.X("Channel:N", sort="-y"),
                    y="ROAS:Q",
                    text=alt.Text("ROAS:Q", format=".2f"),
                )
                st.altair_chart(style_mkt_chart(roas_target + roas_bar + roas_text, height=235), use_container_width=True)
                low_roas = mkt_channels.loc[mkt_channels["ROAS"].idxmin()]
                render_mkt_ai_reco(
                    "Channel Return Mix",
                    f"{low_roas['Channel']} is the lowest-return channel at {low_roas['ROAS']:.2f}x.",
                    f"Refine targeting and creative on {low_roas['Channel']} before additional spend increases.",
                    "Lifts blended ROAS and protects marketing efficiency under scale.",
                    level="warning",
                )

    with mkt_tab_ops:
        st.markdown('<div class="mkt-title">Marketing Operations and Journey</div>', unsafe_allow_html=True)
        st.markdown(dedent(f"""
            <div class="mkt-kpi-grid">
                <div class="mkt-kpi-card"><div class="k">Current Funnel Lead Base</div><div class="v">{mkt_funnel.loc[mkt_funnel['Stage']=='Leads', 'Volume K'].iloc[0]:.0f}K</div><div class="d">Latest month demand</div></div>
                <div class="mkt-kpi-card {'warn' if mkt_funnel.loc[mkt_funnel['Stage']=='SQL', 'Conversion %'].iloc[0] < 55 else ''}"><div class="k">MQL → SQL</div><div class="v">{mkt_funnel.loc[mkt_funnel['Stage']=='SQL', 'Conversion %'].iloc[0]:.1f}%</div><div class="d">Mid-funnel conversion</div></div>
                <div class="mkt-kpi-card"><div class="k">Best Campaign ROI</div><div class="v">{mkt_campaigns['ROI %'].max():.0f}%</div><div class="d">Top portfolio performer</div></div>
                <div class="mkt-kpi-card"><div class="k">Campaign Mix</div><div class="v">{mkt_campaigns['Campaign'].nunique()}</div><div class="d">Active initiatives</div></div>
            </div>
        """), unsafe_allow_html=True)

        op_col1, op_col2 = st.columns(2)
        with op_col1:
            st.markdown('<div class="mkt-mini-title">Funnel Conversion by Stage</div>', unsafe_allow_html=True)
            with st.container(border=True):
                funnel_bar = alt.Chart(mkt_funnel).mark_bar(cornerRadiusTopRight=7, cornerRadiusBottomRight=7, size=24).encode(
                    x=alt.X("Volume K:Q", title="Volume (K)"),
                    y=alt.Y("Stage:N", sort=["Visits", "Leads", "MQL", "SQL", "Wins"], title=None),
                    color=alt.Color("Conversion %:Q", scale=alt.Scale(scheme="blues"), legend=None),
                    tooltip=["Stage:N", alt.Tooltip("Volume K:Q", format=".1f"), alt.Tooltip("Conversion %:Q", format=".1f")],
                )
                funnel_label = alt.Chart(mkt_funnel).mark_text(align="left", dx=6, fontSize=10, color="#0F172A").encode(
                    x="Volume K:Q", y=alt.Y("Stage:N", sort=["Visits", "Leads", "MQL", "SQL", "Wins"]), text=alt.Text("Conversion %:Q", format=".1f")
                )
                st.altair_chart(style_mkt_chart(funnel_bar + funnel_label, height=235), use_container_width=True)
                render_mkt_ai_reco(
                    "Funnel Health",
                    f"Lead-to-win conversion currently lands at {mkt_funnel.loc[mkt_funnel['Stage']=='Wins', 'Conversion %'].iloc[0]:.1f}% from SQL stage.",
                    "Tighten scoring model and sales handoff SLAs at MQL and SQL transition points.",
                    "Improves yield from acquired demand without proportional spend increase.",
                    level="warning",
                )

        with op_col2:
            st.markdown('<div class="mkt-mini-title">Campaign ROI Portfolio</div>', unsafe_allow_html=True)
            with st.container(border=True):
                camp_bar = alt.Chart(mkt_campaigns).mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6, size=24, color="#60A5FA").encode(
                    x=alt.X("Campaign:N", sort="-y", title=None),
                    y=alt.Y("ROI %:Q", title="ROI (%)"),
                    tooltip=["Campaign:N", "Stage:N", alt.Tooltip("ROI %:Q", format=".1f"), alt.Tooltip("Spend M:Q", format=".2f"), alt.Tooltip("Revenue M:Q", format=".2f"), alt.Tooltip("CPA:Q", format=".0f")],
                )
                roi_target = alt.Chart(pd.DataFrame({"y": [180]})).mark_rule(color="#94A3B8", strokeDash=[4, 4]).encode(y="y:Q")
                st.altair_chart(style_mkt_chart(roi_target + camp_bar, height=235), use_container_width=True)
                top_campaign = mkt_campaigns.loc[mkt_campaigns["ROI %"].idxmax()]
                render_mkt_ai_reco(
                    "Campaign Optimization",
                    f"{top_campaign['Campaign']} leads portfolio ROI at {top_campaign['ROI %']:.1f}%.",
                    f"Scale creative and audience variants from {top_campaign['Campaign']} into adjacent segments.",
                    "Improves campaign-level return while keeping execution risk low.",
                )

        st.markdown('<div class="mkt-mini-title">Attribution Mix by Channel Revenue</div>', unsafe_allow_html=True)
        with st.container(border=True):
            mix_df = mkt_channels.copy()
            mix_df["Revenue Share %"] = (mix_df["Revenue M"] / mix_df["Revenue M"].sum() * 100).round(1)
            mix_arc = alt.Chart(mix_df).mark_arc(innerRadius=64, outerRadius=102).encode(
                theta=alt.Theta("Revenue M:Q"),
                color=alt.Color("Channel:N", legend=alt.Legend(title=None), scale=alt.Scale(range=["#3B82F6", "#10B981", "#F59E0B", "#EF4444", "#6366F1", "#14B8A6"])),
                tooltip=["Channel:N", alt.Tooltip("Revenue M:Q", format=".2f"), alt.Tooltip("Revenue Share %:Q", format=".1f"), alt.Tooltip("ROAS:Q", format=".2f")],
            )
            center_txt = alt.Chart(pd.DataFrame({"t": [f"{mix_df['Revenue Share %'].max():.1f}%"]})).mark_text(fontSize=22, fontWeight="bold", color="#0F172A").encode(text="t:N")
            center_sub = alt.Chart(pd.DataFrame({"t": ["Top Share"]})).mark_text(fontSize=11, dy=18, color="#64748B").encode(text="t:N")
            st.altair_chart(style_mkt_chart(mix_arc + center_txt + center_sub, height=235), use_container_width=True)
            dominant_channel = mix_df.loc[mix_df["Revenue Share %"].idxmax()]
            render_mkt_ai_reco(
                "Attribution Concentration",
                f"{dominant_channel['Channel']} contributes the largest revenue share at {dominant_channel['Revenue Share %']:.1f}%.",
                "Maintain diversification guardrails to avoid dependency on a single channel.",
                "Protects growth resilience under channel volatility.",
                level="warning",
            )

        st.markdown('<div class="mkt-mini-title">Campaign Quality Matrix (CTR vs CVR)</div>', unsafe_allow_html=True)
        with st.container(border=True):
            camp_matrix = alt.Chart(mkt_campaigns).mark_circle(opacity=0.88, stroke="#FFFFFF", strokeWidth=1.2).encode(
                x=alt.X("CTR %:Q", title="CTR (%)"),
                y=alt.Y("CVR %:Q", title="CVR (%)"),
                size=alt.Size("Spend M:Q", scale=alt.Scale(range=[260, 1600]), legend=None),
                color=alt.Color("ROI %:Q", scale=alt.Scale(scheme="blues"), legend=alt.Legend(title="ROI %")),
                tooltip=["Campaign:N", "Stage:N", alt.Tooltip("CTR %:Q", format=".2f"), alt.Tooltip("CVR %:Q", format=".2f"), alt.Tooltip("CPA:Q", format=".0f"), alt.Tooltip("ROI %:Q", format=".1f")],
            )
            camp_label = alt.Chart(mkt_campaigns).mark_text(dy=-10, fontSize=9, color="#1E293B").encode(
                x="CTR %:Q", y="CVR %:Q", text="Campaign:N"
            )
            st.altair_chart(style_mkt_chart(camp_matrix + camp_label, height=235), use_container_width=True)
            weak_creative = mkt_campaigns.sort_values(["CTR %", "ROI %"]).iloc[0]
            render_mkt_ai_reco(
                "Creative and Targeting Quality",
                f"{weak_creative['Campaign']} shows the weakest CTR/ROI combination in the active mix.",
                f"Refresh creative and audience segmentation strategy for {weak_creative['Campaign']}.",
                "Improves campaign quality and reduces inefficient spend pockets.",
                level="warning",
            )

    with mkt_tab_risk:
        st.markdown('<div class="mkt-title">Marketing Risk and Strategy</div>', unsafe_allow_html=True)
        st.markdown(dedent(f"""
            <div class="mkt-kpi-grid">
                <div class="mkt-kpi-card crit"><div class="k">Top Risk Driver</div><div class="v">{top_risk_mkt['Risk Driver']}</div><div class="d">Highest exposure line</div></div>
                <div class="mkt-kpi-card warn"><div class="k">Total Exposure</div><div class="v">€{mkt_risk['Exposure M'].sum():.2f}M</div><div class="d">Mapped downside</div></div>
                <div class="mkt-kpi-card"><div class="k">Base Quarter Revenue</div><div class="v">€{mkt_scenario.loc[mkt_scenario['Scenario']=='Base', 'Quarter Revenue M'].iloc[0]:.1f}M</div><div class="d">Most probable scenario</div></div>
                <div class="mkt-kpi-card {'warn' if (mkt_scenario.loc[mkt_scenario['Scenario']=='Base', 'Quarter Revenue M'].iloc[0] - mkt_scenario.loc[mkt_scenario['Scenario']=='Downside', 'Quarter Revenue M'].iloc[0]) > 0.6 else ''}"><div class="k">Downside Gap</div><div class="v">€{(mkt_scenario.loc[mkt_scenario['Scenario']=='Base', 'Quarter Revenue M'].iloc[0] - mkt_scenario.loc[mkt_scenario['Scenario']=='Downside', 'Quarter Revenue M'].iloc[0]):.1f}M</div><div class="d">vs base case</div></div>
            </div>
        """), unsafe_allow_html=True)

        rk_col1, rk_col2 = st.columns(2)
        with rk_col1:
            st.markdown('<div class="mkt-mini-title">Marketing Risk Exposure by Driver</div>', unsafe_allow_html=True)
            with st.container(border=True):
                risk_bar = alt.Chart(mkt_risk).mark_bar(cornerRadiusTopRight=7, cornerRadiusBottomRight=7, size=20).encode(
                    x=alt.X("Exposure M:Q", title="Exposure (€ M)"),
                    y=alt.Y("Risk Driver:N", sort="-x", title=None),
                    color=alt.Color("Likelihood:Q", scale=alt.Scale(scheme="orangered"), legend=None),
                    tooltip=["Risk Driver:N", alt.Tooltip("Exposure M:Q", format=".2f"), alt.Tooltip("Likelihood:Q", format=".1f")],
                )
                risk_txt = alt.Chart(mkt_risk).mark_text(align="left", dx=6, fontSize=10, color="#0F172A").encode(
                    x="Exposure M:Q", y=alt.Y("Risk Driver:N", sort="-x"), text=alt.Text("Exposure M:Q", format=".2f")
                )
                st.altair_chart(style_mkt_chart(risk_bar + risk_txt, height=235), use_container_width=True)
                render_mkt_ai_reco(
                    "Risk Prioritization",
                    f"{top_risk_mkt['Risk Driver']} has the highest exposure at €{top_risk_mkt['Exposure M']:.2f}M.",
                    f"Launch mitigation sprint against {top_risk_mkt['Risk Driver']} with weekly executive tracking.",
                    "Improves forecast reliability and reduces downside variance.",
                    level="critical",
                )

        with rk_col2:
            st.markdown('<div class="mkt-mini-title">Quarter Marketing Scenarios</div>', unsafe_allow_html=True)
            with st.container(border=True):
                sc_bar = alt.Chart(mkt_scenario).mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6, size=56).encode(
                    x=alt.X("Scenario:N", title=None),
                    y=alt.Y("Quarter Revenue M:Q", title="Revenue (€ M)"),
                    color=alt.Color("Scenario:N", scale=alt.Scale(domain=["Downside", "Base", "Upside"], range=["#EF4444", "#3B82F6", "#10B981"]), legend=None),
                    tooltip=["Scenario:N", alt.Tooltip("Quarter Revenue M:Q", format=".1f"), alt.Tooltip("New Subs K:Q", format=".1f"), "Probability:N"],
                )
                sc_label = alt.Chart(mkt_scenario).mark_text(dy=-8, fontSize=11, fontWeight="bold", color="#0F172A").encode(
                    x="Scenario:N", y="Quarter Revenue M:Q", text=alt.Text("Quarter Revenue M:Q", format=".1f")
                )
                st.altair_chart(style_mkt_chart(sc_bar + sc_label, height=235), use_container_width=True)
                base_rev = mkt_scenario.loc[mkt_scenario["Scenario"] == "Base", "Quarter Revenue M"].iloc[0]
                render_mkt_ai_reco(
                    "Scenario Planning",
                    f"Base case is €{base_rev:.1f}M with balanced probability and controlled upside/downside ranges.",
                    "Pre-approve tactical budget shifts for downside protection and upside acceleration.",
                    "Shortens reaction cycles and stabilizes quarter outcomes.",
                )

        rk_col3, rk_col4 = st.columns(2)
        with rk_col3:
            st.markdown('<div class="mkt-mini-title">Risk Heat Matrix</div>', unsafe_allow_html=True)
            with st.container(border=True):
                risk_matrix = alt.Chart(mkt_risk).mark_circle(opacity=0.88, stroke="#FFFFFF", strokeWidth=1.2).encode(
                    x=alt.X("Likelihood:Q", title="Likelihood"),
                    y=alt.Y("Exposure M:Q", title="Exposure (€ M)"),
                    size=alt.Size("Exposure M:Q", scale=alt.Scale(range=[300, 1800]), legend=None),
                    color=alt.Color("Risk Driver:N", legend=alt.Legend(title=None), scale=alt.Scale(range=["#EF4444", "#F59E0B", "#3B82F6", "#10B981", "#6366F1"])),
                    tooltip=["Risk Driver:N", alt.Tooltip("Likelihood:Q", format=".1f"), alt.Tooltip("Exposure M:Q", format=".2f")],
                )
                risk_lbl = alt.Chart(mkt_risk).mark_text(dy=-10, fontSize=9, color="#1E293B").encode(
                    x="Likelihood:Q", y="Exposure M:Q", text="Risk Driver:N"
                )
                st.altair_chart(style_mkt_chart(risk_matrix + risk_lbl, height=235), use_container_width=True)
                max_quad = mkt_risk.sort_values(["Likelihood", "Exposure M"], ascending=False).iloc[0]
                render_mkt_ai_reco(
                    "Risk Concentration",
                    f"{max_quad['Risk Driver']} sits in the highest likelihood-exposure quadrant.",
                    "Elevate this driver to executive watchlist with pre-defined trigger actions.",
                    "Reduces probability of abrupt quarter underperformance.",
                    level="critical",
                )

        with rk_col4:
            st.markdown('<div class="mkt-mini-title">Risk-Adjusted Channel Return</div>', unsafe_allow_html=True)
            with st.container(border=True):
                risk_adj = mkt_channels.copy()
                risk_adj["Risk Factor"] = (risk_adj["CAC"] / risk_adj["CAC"].max() * 0.7 + (1 - risk_adj["CVR %"] / risk_adj["CVR %"].max()) * 0.3)
                risk_adj["Risk-Adjusted ROAS"] = (risk_adj["ROAS"] * (1 - 0.35 * risk_adj["Risk Factor"])).round(2)
                ra_bar = alt.Chart(risk_adj).mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6, size=24, color="#10B981").encode(
                    x=alt.X("Channel:N", sort="-y", title=None),
                    y=alt.Y("Risk-Adjusted ROAS:Q", title="Risk-Adjusted ROAS (x)"),
                    tooltip=["Channel:N", alt.Tooltip("ROAS:Q", format=".2f"), alt.Tooltip("Risk-Adjusted ROAS:Q", format=".2f"), alt.Tooltip("CAC:Q", format=".0f"), alt.Tooltip("CVR %:Q", format=".1f")],
                )
                ra_target = alt.Chart(pd.DataFrame({"y": [2.6]})).mark_rule(color="#94A3B8", strokeDash=[4, 4]).encode(y="y:Q")
                ra_text = alt.Chart(risk_adj).mark_text(dy=-8, fontSize=9, color="#0F172A").encode(
                    x=alt.X("Channel:N", sort="-y"),
                    y="Risk-Adjusted ROAS:Q",
                    text=alt.Text("Risk-Adjusted ROAS:Q", format=".2f"),
                )
                st.altair_chart(style_mkt_chart(ra_target + ra_bar + ra_text, height=235), use_container_width=True)
                weakest_ra = risk_adj.loc[risk_adj["Risk-Adjusted ROAS"].idxmin()]
                render_mkt_ai_reco(
                    "Defensive Budget Allocation",
                    f"{weakest_ra['Channel']} has the weakest risk-adjusted return at {weakest_ra['Risk-Adjusted ROAS']:.2f}x.",
                    f"Apply stricter guardrails and optimization sprints on {weakest_ra['Channel']} before scaling budget.",
                    "Improves downside protection while preserving growth trajectory.",
                    level="warning",
                )

        st.markdown(dedent(f"""
            <div style="background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%); border-radius: 10px; padding: 0.82rem 0.95rem; margin-top: 0.55rem; border-left: 4px solid #F59E0B;">
                <div style="display: flex; align-items: center;">
                    <span style="font-size: 1.35rem; margin-right: 0.55rem;">⚠️</span>
                    <div>
                        <strong style="color: #92400E;">Urgent: {top_risk_mkt['Risk Driver']} exposure at €{top_risk_mkt['Exposure M']:.2f}M</strong>
                        <div style="color: #B45309; font-size: 0.84rem;">Highest likelihood-impact concentration in current marketing risk portfolio · trigger mitigation in next planning cycle</div>
                    </div>
                </div>
            </div>
        """), unsafe_allow_html=True)

elif selected_menu == "HR & Workforce":
    import pandas as pd
    import altair as alt

    HR_CHART_THEME = {
        "bg": "#F8FAFF",
        "title": "#1E3A8A",
        "axis": "#334155",
        "grid": "#E2E8F0",
        "font": "Inter",
    }

    def style_hr_chart(chart: alt.Chart, height: int = 220) -> alt.Chart:
        return (
            chart.properties(height=height, padding={"left": 10, "right": 10, "top": 8, "bottom": 4})
            .configure(background=HR_CHART_THEME["bg"])
            .configure_view(stroke=None, cornerRadius=10)
            .configure_title(color=HR_CHART_THEME["title"], fontSize=13, font=HR_CHART_THEME["font"], anchor="start")
            .configure_axis(
                labelColor=HR_CHART_THEME["axis"],
                titleColor=HR_CHART_THEME["axis"],
                gridColor=HR_CHART_THEME["grid"],
                labelFont=HR_CHART_THEME["font"],
                titleFont=HR_CHART_THEME["font"],
            )
            .configure_legend(
                labelColor=HR_CHART_THEME["axis"],
                titleColor=HR_CHART_THEME["axis"],
                labelFont=HR_CHART_THEME["font"],
                titleFont=HR_CHART_THEME["font"],
            )
        )

    def render_hr_ai_reco(headline: str, insight: str, action: str, impact: str, level: str = "info") -> None:
        level_class = "crit" if level == "critical" else "warn" if level == "warning" else ""
        icon = "🚨" if level == "critical" else "⚠️" if level == "warning" else "🤖"
        st.markdown(dedent(f"""
            <div class="hr-ai-card {level_class}">
                <div class="h">{icon} {headline}</div>
                <div class="b"><strong>Insight:</strong> {insight}</div>
                <div class="b"><strong>Action:</strong> {action}</div>
                <div class="b"><strong>Expected Impact:</strong> {impact}</div>
            </div>
        """), unsafe_allow_html=True)

    st.markdown(dedent("""
        <style>
            @keyframes hr-fade-up {
                from { opacity: 0; transform: translateY(8px); }
                to { opacity: 1; transform: translateY(0); }
            }
            @keyframes hr-pulse-glow {
                0%, 100% { box-shadow: 0 0 0 0 rgba(37, 99, 235, 0.1); }
                50% { box-shadow: 0 0 0 8px rgba(37, 99, 235, 0.03); }
            }
            .hr-title {
                font-size: 1.08rem;
                font-weight: 800;
                color: #1E3A8A;
                letter-spacing: 0.01em;
                margin: 0.3rem 0 0.6rem 0;
                animation: hr-fade-up 0.45s ease-out both;
            }
            .hr-mini-title {
                font-size: 0.92rem;
                font-weight: 700;
                color: #334155;
                margin: 0.12rem 0 0.5rem 0;
                animation: hr-fade-up 0.45s ease-out both;
            }
            .hr-pulse {
                border-radius: 12px;
                border: 1px solid #DBEAFE;
                background: linear-gradient(135deg, #EFF6FF 0%, #E0F2FE 100%);
                padding: 0.8rem 0.95rem;
                margin-bottom: 0.65rem;
                animation: hr-fade-up 0.45s ease-out both, hr-pulse-glow 2.8s ease-in-out infinite;
            }
            .hr-pulse-grid, .hr-kpi-grid {
                display: grid;
                grid-template-columns: repeat(4, minmax(0, 1fr));
                gap: 0.48rem;
            }
            .hr-pulse-card, .hr-kpi-card {
                border-radius: 10px;
                background: rgba(255, 255, 255, 0.88);
                border: 1px solid #E2E8F0;
                padding: 0.52rem 0.62rem;
            }
            .hr-pulse-card .k, .hr-kpi-card .k {
                font-size: 0.69rem;
                color: #64748B;
                text-transform: uppercase;
                letter-spacing: 0.03em;
                font-weight: 700;
            }
            .hr-pulse-card .v, .hr-kpi-card .v {
                font-size: 1.04rem;
                color: #0F172A;
                font-weight: 800;
                line-height: 1.1;
                margin-top: 0.08rem;
            }
            .hr-pulse-card .d, .hr-kpi-card .d {
                font-size: 0.74rem;
                color: #475569;
                margin-top: 0.12rem;
            }
            .hr-kpi-card.warn { border-left: 4px solid #F59E0B; }
            .hr-kpi-card.crit { border-left: 4px solid #EF4444; }
            .hr-ai-card {
                border-radius: 10px;
                border-left: 4px solid #3B82F6;
                background: #EFF6FF;
                padding: 0.62rem 0.72rem;
                margin-top: 0.46rem;
                animation: hr-fade-up 0.42s ease-out both;
            }
            .hr-ai-card.warn { border-left-color: #F59E0B; background: #FFFBEB; }
            .hr-ai-card.crit { border-left-color: #EF4444; background: #FEF2F2; }
            .hr-ai-card .h {
                font-size: 0.83rem;
                font-weight: 800;
                color: #1E293B;
                margin-bottom: 0.28rem;
            }
            .hr-ai-card .b {
                font-size: 0.78rem;
                color: #334155;
                line-height: 1.42;
            }
            @media (max-width: 1200px) {
                .hr-pulse-grid, .hr-kpi-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
            }
        </style>
    """), unsafe_allow_html=True)

    hr_monthly = pd.DataFrame({
        "Month": ["2025-09", "2025-10", "2025-11", "2025-12", "2026-01", "2026-02"],
        "Headcount": [612, 619, 624, 632, 638, 645],
        "Hiring": [18, 16, 17, 19, 20, 18],
        "Attrition": [11, 10, 12, 11, 13, 12],
        "Absenteeism %": [3.2, 3.1, 3.4, 3.3, 3.6, 3.5],
        "Engagement": [74, 75, 76, 76, 77, 78],
        "Productivity Index": [100, 101, 102, 104, 105, 106],
    })
    hr_dept = pd.DataFrame({
        "Department": ["Network Ops", "Customer Care", "Sales", "Marketing", "Tech & Data", "Corporate"],
        "Headcount": [154, 132, 116, 58, 101, 84],
        "Turnover %": [8.9, 11.6, 10.8, 9.1, 7.6, 6.8],
        "eNPS": [35, 24, 28, 33, 39, 36],
        "Time to Fill": [47, 39, 35, 32, 54, 41],
        "Training Hrs": [18, 14, 12, 11, 22, 15],
        "Quality of Hire": [78, 72, 75, 77, 81, 79],
    })
    hr_recruit = pd.DataFrame({
        "Stage": ["Applicants", "Screened", "Interviewed", "Offers", "Hired"],
        "Volume": [1420, 486, 214, 91, 31],
    })
    hr_recruit["Conversion %"] = (hr_recruit["Volume"] / hr_recruit["Volume"].shift(1) * 100).round(1)
    hr_recruit.loc[0, "Conversion %"] = 100.0

    hr_training = pd.DataFrame({
        "Program": ["Leadership", "Tech Certification", "Sales Enablement", "Customer Excellence", "Data Literacy"],
        "Participants": [46, 64, 71, 83, 58],
        "Hours": [18, 24, 14, 12, 16],
        "Post Performance Lift %": [8.2, 11.4, 9.1, 7.6, 10.3],
    })
    hr_risk = pd.DataFrame({
        "Risk Driver": ["Critical Skill Attrition", "Hiring Delay", "Low Engagement Cohorts", "Absenteeism Spike", "Leadership Gap"],
        "Exposure Score": [88, 77, 71, 66, 58],
        "Likelihood": [3.9, 3.5, 3.3, 3.1, 2.8],
    })
    hr_scenario = pd.DataFrame({
        "Scenario": ["Downside", "Base", "Upside"],
        "Headcount EoQ": [638, 652, 666],
        "Productivity Index": [102, 107, 112],
        "Voluntary Attrition %": [11.8, 10.3, 8.9],
        "Probability": ["25%", "50%", "25%"],
    })

    current_headcount = hr_monthly.iloc[-1]["Headcount"]
    attrition_rate = hr_monthly["Attrition"].sum() / ((hr_monthly["Headcount"].iloc[0] + current_headcount) / 2) * 100
    net_hiring = hr_monthly["Hiring"].sum() - hr_monthly["Attrition"].sum()
    avg_engagement = hr_monthly["Engagement"].mean()
    avg_absent = hr_monthly["Absenteeism %"].mean()
    productivity_gain = hr_monthly.iloc[-1]["Productivity Index"] - hr_monthly.iloc[0]["Productivity Index"]
    top_hr_risk = hr_risk.loc[hr_risk["Exposure Score"].idxmax()]

    st.markdown('<div class="hr-title">Workforce Pulse</div>', unsafe_allow_html=True)
    st.markdown(dedent(f"""
        <div class="hr-pulse">
            <div class="hr-pulse-grid">
                <div class="hr-pulse-card"><div class="k">Current Headcount</div><div class="v">{current_headcount:.0f}</div><div class="d">Total active workforce</div></div>
                <div class="hr-pulse-card"><div class="k">Net Hiring</div><div class="v">{net_hiring:+.0f}</div><div class="d">Six-month net movement</div></div>
                <div class="hr-pulse-card"><div class="k">Attrition Rate</div><div class="v">{attrition_rate:.1f}%</div><div class="d">Period attrition pressure</div></div>
                <div class="hr-pulse-card"><div class="k">Engagement</div><div class="v">{avg_engagement:.1f}</div><div class="d">Average monthly score</div></div>
                <div class="hr-pulse-card"><div class="k">Absenteeism</div><div class="v">{avg_absent:.2f}%</div><div class="d">Attendance reliability</div></div>
                <div class="hr-pulse-card"><div class="k">Productivity Lift</div><div class="v">{productivity_gain:+.0f}</div><div class="d">Index points vs period start</div></div>
            </div>
        </div>
    """), unsafe_allow_html=True)

    hr_tab_overview, hr_tab_ops, hr_tab_risk = st.tabs([
        "📈 Workforce Overview",
        "🧭 Workforce Operations",
        "⚠️ Risk & Strategy",
    ])

    with hr_tab_overview:
        st.markdown('<div class="hr-title">Workforce Performance Overview</div>', unsafe_allow_html=True)
        st.markdown(dedent(f"""
            <div class="hr-kpi-grid">
                <div class="hr-kpi-card"><div class="k">Headcount</div><div class="v">{current_headcount:.0f}</div><div class="d">Current period close</div></div>
                <div class="hr-kpi-card {'warn' if attrition_rate > 10.5 else ''}"><div class="k">Attrition</div><div class="v">{attrition_rate:.1f}%</div><div class="d">Rolling period rate</div></div>
                <div class="hr-kpi-card"><div class="k">Engagement Score</div><div class="v">{avg_engagement:.1f}</div><div class="d">Employee sentiment</div></div>
                <div class="hr-kpi-card {'warn' if avg_absent > 3.4 else ''}"><div class="k">Absenteeism</div><div class="v">{avg_absent:.2f}%</div><div class="d">Attendance trend</div></div>
            </div>
        """), unsafe_allow_html=True)

        ov_col1, ov_col2 = st.columns(2)
        with ov_col1:
            st.markdown('<div class="hr-mini-title">Headcount vs Hiring and Attrition</div>', unsafe_allow_html=True)
            with st.container(border=True):
                hc_line = alt.Chart(hr_monthly).mark_line(point=True, strokeWidth=3, color="#3B82F6").encode(
                    x=alt.X("Month:N", title=None),
                    y=alt.Y("Headcount:Q", title="Headcount"),
                    tooltip=["Month:N", alt.Tooltip("Headcount:Q", format=".0f"), alt.Tooltip("Hiring:Q", format=".0f"), alt.Tooltip("Attrition:Q", format=".0f")],
                )
                hiring_bar = alt.Chart(hr_monthly).mark_bar(cornerRadiusTopLeft=5, cornerRadiusTopRight=5, size=20, color="#10B981", opacity=0.55).encode(
                    x=alt.X("Month:N", title=None), y=alt.Y("Hiring:Q", title="Hiring")
                )
                attr_line = alt.Chart(hr_monthly).mark_line(point=True, strokeWidth=2.5, color="#EF4444").encode(
                    x="Month:N", y=alt.Y("Attrition:Q", title="Attrition")
                )
                st.altair_chart(style_hr_chart(alt.layer(hiring_bar, hc_line, attr_line).resolve_scale(y="independent"), height=235), use_container_width=True)
                render_hr_ai_reco(
                    "Workforce Balance",
                    f"Headcount closed at {current_headcount:.0f} with net hiring {net_hiring:+.0f} across the period.",
                    "Maintain selective hiring in high-productivity teams while reducing avoidable attrition.",
                    "Stabilizes capacity and improves labor productivity trajectory.",
                )

        with ov_col2:
            st.markdown('<div class="hr-mini-title">Department Health Matrix</div>', unsafe_allow_html=True)
            with st.container(border=True):
                dep_scatter = alt.Chart(hr_dept).mark_circle(opacity=0.88, stroke="#FFFFFF", strokeWidth=1.2).encode(
                    x=alt.X("Turnover %:Q", title="Turnover (%)"),
                    y=alt.Y("eNPS:Q", title="eNPS"),
                    size=alt.Size("Headcount:Q", scale=alt.Scale(range=[280, 1700]), legend=None),
                    color=alt.Color("Quality of Hire:Q", scale=alt.Scale(scheme="blues"), legend=alt.Legend(title="Quality of Hire")),
                    tooltip=["Department:N", alt.Tooltip("Headcount:Q", format=".0f"), alt.Tooltip("Turnover %:Q", format=".1f"), alt.Tooltip("eNPS:Q", format=".0f"), alt.Tooltip("Quality of Hire:Q", format=".0f")],
                )
                dep_lbl = alt.Chart(hr_dept).mark_text(dy=-10, fontSize=9, color="#1E293B").encode(x="Turnover %:Q", y="eNPS:Q", text="Department:N")
                st.altair_chart(style_hr_chart(dep_scatter + dep_lbl, height=235), use_container_width=True)
                weak_dep = hr_dept.sort_values(["Turnover %", "eNPS"], ascending=[False, True]).iloc[0]
                render_hr_ai_reco(
                    "Department Retention Focus",
                    f"{weak_dep['Department']} shows the highest retention pressure with weaker sentiment profile.",
                    f"Prioritize manager coaching, career-pathing, and engagement actions in {weak_dep['Department']}.",
                    "Reduces avoidable exits in high-impact teams.",
                    level="warning",
                )

        ov_col3, ov_col4 = st.columns(2)
        with ov_col3:
            st.markdown('<div class="hr-mini-title">Engagement and Absenteeism Trend</div>', unsafe_allow_html=True)
            with st.container(border=True):
                eng_line = alt.Chart(hr_monthly).mark_line(point=True, strokeWidth=3, color="#3B82F6").encode(
                    x=alt.X("Month:N", title=None),
                    y=alt.Y("Engagement:Q", title="Engagement Score"),
                    tooltip=["Month:N", alt.Tooltip("Engagement:Q", format=".0f"), alt.Tooltip("Absenteeism %:Q", format=".2f"), alt.Tooltip("Productivity Index:Q", format=".0f")],
                )
                abs_line = alt.Chart(hr_monthly).mark_line(point=True, strokeWidth=2.6, color="#F59E0B").encode(
                    x="Month:N",
                    y=alt.Y("Absenteeism %:Q", title="Absenteeism (%)"),
                )
                st.altair_chart(style_hr_chart(alt.layer(eng_line, abs_line).resolve_scale(y="independent"), height=235), use_container_width=True)
                render_hr_ai_reco(
                    "People Experience Signal",
                    f"Engagement improved to {hr_monthly.iloc[-1]['Engagement']:.0f} while absenteeism remains elevated at {hr_monthly.iloc[-1]['Absenteeism %']:.2f}%.",
                    "Pair engagement initiatives with attendance coaching in teams above absenteeism threshold.",
                    "Supports stronger morale while protecting operational continuity.",
                    level="warning" if hr_monthly.iloc[-1]["Absenteeism %"] > 3.4 else "info",
                )

        with ov_col4:
            st.markdown('<div class="hr-mini-title">Department Capability Index</div>', unsafe_allow_html=True)
            with st.container(border=True):
                capability_df = hr_dept.copy()
                capability_df["Capability Index"] = (
                    capability_df["Quality of Hire"] * 0.45
                    + capability_df["eNPS"] * 0.35
                    + capability_df["Training Hrs"] * 0.9
                    - capability_df["Turnover %"] * 1.2
                ).round(1)
                cap_bar = alt.Chart(capability_df).mark_bar(cornerRadiusTopRight=7, cornerRadiusBottomRight=7, size=20).encode(
                    x=alt.X("Capability Index:Q", title="Capability Index"),
                    y=alt.Y("Department:N", sort="-x", title=None),
                    color=alt.Color("Capability Index:Q", scale=alt.Scale(scheme="blues"), legend=None),
                    tooltip=["Department:N", alt.Tooltip("Capability Index:Q", format=".1f"), alt.Tooltip("Quality of Hire:Q", format=".0f"), alt.Tooltip("eNPS:Q", format=".0f"), alt.Tooltip("Training Hrs:Q", format=".0f"), alt.Tooltip("Turnover %:Q", format=".1f")],
                )
                cap_text = alt.Chart(capability_df).mark_text(align="left", dx=6, fontSize=10, color="#0F172A").encode(
                    x="Capability Index:Q", y=alt.Y("Department:N", sort="-x"), text=alt.Text("Capability Index:Q", format=".1f")
                )
                st.altair_chart(style_hr_chart(cap_bar + cap_text, height=235), use_container_width=True)
                low_cap = capability_df.loc[capability_df["Capability Index"].idxmin()]
                render_hr_ai_reco(
                    "Capability Development Focus",
                    f"{low_cap['Department']} has the weakest capability index and needs accelerated support.",
                    f"Increase targeted upskilling and retention interventions in {low_cap['Department']}.",
                    "Improves bench strength in teams with higher delivery risk.",
                    level="warning",
                )

    with hr_tab_ops:
        st.markdown('<div class="hr-title">Workforce Operations and Journey</div>', unsafe_allow_html=True)
        st.markdown(dedent(f"""
            <div class="hr-kpi-grid">
                <div class="hr-kpi-card"><div class="k">Applicants</div><div class="v">{hr_recruit.loc[hr_recruit['Stage']=='Applicants', 'Volume'].iloc[0]:,.0f}</div><div class="d">Current hiring funnel volume</div></div>
                <div class="hr-kpi-card"><div class="k">Offers</div><div class="v">{hr_recruit.loc[hr_recruit['Stage']=='Offers', 'Volume'].iloc[0]:.0f}</div><div class="d">Offer-stage candidates</div></div>
                <div class="hr-kpi-card {'warn' if hr_dept['Time to Fill'].mean() > 42 else ''}"><div class="k">Avg Time to Fill</div><div class="v">{hr_dept['Time to Fill'].mean():.1f} d</div><div class="d">Hiring cycle efficiency</div></div>
                <div class="hr-kpi-card"><div class="k">Training Lift</div><div class="v">{hr_training['Post Performance Lift %'].mean():.1f}%</div><div class="d">Post-training performance impact</div></div>
            </div>
        """), unsafe_allow_html=True)

        op_col1, op_col2 = st.columns(2)
        with op_col1:
            st.markdown('<div class="hr-mini-title">Recruitment Funnel Conversion</div>', unsafe_allow_html=True)
            with st.container(border=True):
                rec_bar = alt.Chart(hr_recruit).mark_bar(cornerRadiusTopRight=7, cornerRadiusBottomRight=7, size=24).encode(
                    x=alt.X("Volume:Q", title="Candidates"),
                    y=alt.Y("Stage:N", sort=["Applicants", "Screened", "Interviewed", "Offers", "Hired"], title=None),
                    color=alt.Color("Conversion %:Q", scale=alt.Scale(scheme="blues"), legend=None),
                    tooltip=["Stage:N", alt.Tooltip("Volume:Q", format=".0f"), alt.Tooltip("Conversion %:Q", format=".1f")],
                )
                rec_txt = alt.Chart(hr_recruit).mark_text(align="left", dx=6, fontSize=10, color="#0F172A").encode(
                    x="Volume:Q", y=alt.Y("Stage:N", sort=["Applicants", "Screened", "Interviewed", "Offers", "Hired"]), text=alt.Text("Conversion %:Q", format=".1f")
                )
                st.altair_chart(style_hr_chart(rec_bar + rec_txt, height=235), use_container_width=True)
                render_hr_ai_reco(
                    "Talent Funnel Quality",
                    f"Interview-to-offer conversion is {hr_recruit.loc[hr_recruit['Stage']=='Offers', 'Conversion %'].iloc[0]:.1f}%, indicating mid-funnel selectivity.",
                    "Improve sourcing fit and screening quality to increase interview efficiency.",
                    "Shortens hiring cycle and lowers hiring cost per role.",
                )

        with op_col2:
            st.markdown('<div class="hr-mini-title">Time to Fill vs Quality of Hire</div>', unsafe_allow_html=True)
            with st.container(border=True):
                fill_scatter = alt.Chart(hr_dept).mark_circle(opacity=0.88, stroke="#FFFFFF", strokeWidth=1.2).encode(
                    x=alt.X("Time to Fill:Q", title="Time to Fill (days)"),
                    y=alt.Y("Quality of Hire:Q", title="Quality of Hire"),
                    size=alt.Size("Headcount:Q", scale=alt.Scale(range=[280, 1500]), legend=None),
                    color=alt.Color("Department:N", legend=alt.Legend(title=None), scale=alt.Scale(range=["#3B82F6", "#10B981", "#F59E0B", "#EF4444", "#6366F1", "#14B8A6"])),
                    tooltip=["Department:N", alt.Tooltip("Time to Fill:Q", format=".0f"), alt.Tooltip("Quality of Hire:Q", format=".0f"), alt.Tooltip("Headcount:Q", format=".0f")],
                )
                fill_lbl = alt.Chart(hr_dept).mark_text(dy=-10, fontSize=9, color="#1E293B").encode(x="Time to Fill:Q", y="Quality of Hire:Q", text="Department:N")
                st.altair_chart(style_hr_chart(fill_scatter + fill_lbl, height=235), use_container_width=True)
                slow_dep = hr_dept.loc[hr_dept["Time to Fill"].idxmax()]
                render_hr_ai_reco(
                    "Hiring Cycle Optimization",
                    f"{slow_dep['Department']} has the slowest time-to-fill at {slow_dep['Time to Fill']:.0f} days.",
                    f"Activate specialized talent pools and faster panel scheduling for {slow_dep['Department']}.",
                    "Improves capacity fill-rate in constrained skill areas.",
                    level="warning",
                )

        st.markdown('<div class="hr-mini-title">Training Programs vs Performance Lift</div>', unsafe_allow_html=True)
        with st.container(border=True):
            train_bar = alt.Chart(hr_training).mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6, size=24, color="#60A5FA").encode(
                x=alt.X("Program:N", title=None),
                y=alt.Y("Participants:Q", title="Participants"),
                tooltip=["Program:N", alt.Tooltip("Participants:Q", format=".0f"), alt.Tooltip("Hours:Q", format=".0f"), alt.Tooltip("Post Performance Lift %:Q", format=".1f")],
            )
            lift_line = alt.Chart(hr_training).mark_line(point=True, strokeWidth=2.8, color="#10B981").encode(
                x="Program:N", y=alt.Y("Post Performance Lift %:Q", title="Performance Lift (%)")
            )
            st.altair_chart(style_hr_chart(alt.layer(train_bar, lift_line).resolve_scale(y="independent"), height=235), use_container_width=True)
            top_prog = hr_training.loc[hr_training["Post Performance Lift %"].idxmax()]
            render_hr_ai_reco(
                "Capability Building",
                f"{top_prog['Program']} shows the strongest post-training lift at {top_prog['Post Performance Lift %']:.1f}%.",
                f"Scale enrollment for {top_prog['Program']} and replicate its learning model in adjacent tracks.",
                "Raises workforce capability and measurable productivity outcomes.",
            )

        op_col3, op_col4 = st.columns(2)
        with op_col3:
            st.markdown('<div class="hr-mini-title">Recruitment Stage Drop-Off</div>', unsafe_allow_html=True)
            with st.container(border=True):
                drop_df = hr_recruit.copy()
                drop_df["Drop-Off"] = (drop_df["Volume"].shift(1) - drop_df["Volume"]).fillna(0)
                drop_chart = alt.Chart(drop_df[drop_df["Stage"] != "Applicants"]).mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6, size=30, color="#EF4444").encode(
                    x=alt.X("Stage:N", title=None),
                    y=alt.Y("Drop-Off:Q", title="Drop-Off Volume"),
                    tooltip=["Stage:N", alt.Tooltip("Drop-Off:Q", format=".0f"), alt.Tooltip("Conversion %:Q", format=".1f")],
                )
                drop_text = alt.Chart(drop_df[drop_df["Stage"] != "Applicants"]).mark_text(dy=-8, fontSize=9, color="#0F172A").encode(
                    x="Stage:N", y="Drop-Off:Q", text=alt.Text("Drop-Off:Q", format=".0f")
                )
                st.altair_chart(style_hr_chart(drop_chart + drop_text, height=235), use_container_width=True)
                top_drop = drop_df[drop_df["Stage"] != "Applicants"].sort_values("Drop-Off", ascending=False).iloc[0]
                render_hr_ai_reco(
                    "Funnel Leakage",
                    f"Largest drop-off occurs at {top_drop['Stage']} stage ({top_drop['Drop-Off']:.0f} candidates).",
                    "Audit stage criteria and interviewer calibration to reduce avoidable candidate loss.",
                    "Improves hire yield without expanding sourcing spend.",
                    level="warning",
                )

        with op_col4:
            st.markdown('<div class="hr-mini-title">Training Hours vs Quality of Hire</div>', unsafe_allow_html=True)
            with st.container(border=True):
                train_scatter = alt.Chart(hr_dept).mark_circle(opacity=0.88, stroke="#FFFFFF", strokeWidth=1.2).encode(
                    x=alt.X("Training Hrs:Q", title="Training Hours"),
                    y=alt.Y("Quality of Hire:Q", title="Quality of Hire"),
                    size=alt.Size("Headcount:Q", scale=alt.Scale(range=[260, 1500]), legend=None),
                    color=alt.Color("Turnover %:Q", scale=alt.Scale(scheme="orangered"), legend=alt.Legend(title="Turnover %")),
                    tooltip=["Department:N", alt.Tooltip("Training Hrs:Q", format=".0f"), alt.Tooltip("Quality of Hire:Q", format=".0f"), alt.Tooltip("Turnover %:Q", format=".1f"), alt.Tooltip("Headcount:Q", format=".0f")],
                )
                train_lbl = alt.Chart(hr_dept).mark_text(dy=-10, fontSize=9, color="#1E293B").encode(
                    x="Training Hrs:Q", y="Quality of Hire:Q", text="Department:N"
                )
                st.altair_chart(style_hr_chart(train_scatter + train_lbl, height=235), use_container_width=True)
                undertrained = hr_dept.sort_values(["Training Hrs", "Quality of Hire"]).iloc[0]
                render_hr_ai_reco(
                    "Upskilling Priority",
                    f"{undertrained['Department']} combines lower training hours with weaker quality-of-hire outcomes.",
                    f"Increase structured development hours and mentorship in {undertrained['Department']}.",
                    "Strengthens role readiness and reduces early-performance variability.",
                    level="warning",
                )

    with hr_tab_risk:
        st.markdown('<div class="hr-title">Workforce Risk and Strategy</div>', unsafe_allow_html=True)
        st.markdown(dedent(f"""
            <div class="hr-kpi-grid">
                <div class="hr-kpi-card crit"><div class="k">Top Risk Driver</div><div class="v">{top_hr_risk['Risk Driver']}</div><div class="d">Highest exposure risk</div></div>
                <div class="hr-kpi-card warn"><div class="k">Risk Exposure</div><div class="v">{hr_risk['Exposure Score'].sum():.0f}</div><div class="d">Portfolio risk index</div></div>
                <div class="hr-kpi-card"><div class="k">Base Headcount EoQ</div><div class="v">{hr_scenario.loc[hr_scenario['Scenario']=='Base', 'Headcount EoQ'].iloc[0]:.0f}</div><div class="d">Most probable scenario</div></div>
                <div class="hr-kpi-card {'warn' if hr_scenario.loc[hr_scenario['Scenario']=='Downside', 'Voluntary Attrition %'].iloc[0] > 11 else ''}"><div class="k">Downside Attrition</div><div class="v">{hr_scenario.loc[hr_scenario['Scenario']=='Downside', 'Voluntary Attrition %'].iloc[0]:.1f}%</div><div class="d">Stress case signal</div></div>
            </div>
        """), unsafe_allow_html=True)

        rk_col1, rk_col2 = st.columns(2)
        with rk_col1:
            st.markdown('<div class="hr-mini-title">Risk Exposure by Driver</div>', unsafe_allow_html=True)
            with st.container(border=True):
                hr_risk_bar = alt.Chart(hr_risk).mark_bar(cornerRadiusTopRight=7, cornerRadiusBottomRight=7, size=20).encode(
                    x=alt.X("Exposure Score:Q", title="Exposure Score"),
                    y=alt.Y("Risk Driver:N", sort="-x", title=None),
                    color=alt.Color("Likelihood:Q", scale=alt.Scale(scheme="orangered"), legend=None),
                    tooltip=["Risk Driver:N", alt.Tooltip("Exposure Score:Q", format=".0f"), alt.Tooltip("Likelihood:Q", format=".1f")],
                )
                hr_risk_txt = alt.Chart(hr_risk).mark_text(align="left", dx=6, fontSize=10, color="#0F172A").encode(
                    x="Exposure Score:Q", y=alt.Y("Risk Driver:N", sort="-x"), text=alt.Text("Exposure Score:Q", format=".0f")
                )
                st.altair_chart(style_hr_chart(hr_risk_bar + hr_risk_txt, height=235), use_container_width=True)
                render_hr_ai_reco(
                    "Risk Prioritization",
                    f"{top_hr_risk['Risk Driver']} has the highest workforce risk exposure score ({top_hr_risk['Exposure Score']:.0f}).",
                    f"Create mitigation sprint with retention and capability interventions focused on {top_hr_risk['Risk Driver']}.",
                    "Reduces execution risk in critical workforce capabilities.",
                    level="critical",
                )

        with rk_col2:
            st.markdown('<div class="hr-mini-title">Workforce Scenario Outlook</div>', unsafe_allow_html=True)
            with st.container(border=True):
                hr_sc_bar = alt.Chart(hr_scenario).mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6, size=56).encode(
                    x=alt.X("Scenario:N", title=None),
                    y=alt.Y("Headcount EoQ:Q", title="Headcount EoQ"),
                    color=alt.Color("Scenario:N", scale=alt.Scale(domain=["Downside", "Base", "Upside"], range=["#EF4444", "#3B82F6", "#10B981"]), legend=None),
                    tooltip=["Scenario:N", alt.Tooltip("Headcount EoQ:Q", format=".0f"), alt.Tooltip("Productivity Index:Q", format=".0f"), alt.Tooltip("Voluntary Attrition %:Q", format=".1f"), "Probability:N"],
                )
                hr_sc_txt = alt.Chart(hr_scenario).mark_text(dy=-8, fontSize=11, fontWeight="bold", color="#0F172A").encode(
                    x="Scenario:N", y="Headcount EoQ:Q", text=alt.Text("Headcount EoQ:Q", format=".0f")
                )
                st.altair_chart(style_hr_chart(hr_sc_bar + hr_sc_txt, height=235), use_container_width=True)
                base_head = hr_scenario.loc[hr_scenario["Scenario"] == "Base", "Headcount EoQ"].iloc[0]
                render_hr_ai_reco(
                    "Scenario Planning",
                    f"Base scenario closes at {base_head:.0f} headcount with balanced productivity trajectory.",
                    "Pre-approve contingency levers for downside attrition and upside hiring acceleration.",
                    "Improves workforce planning agility and delivery predictability.",
                )

        rk_col3, rk_col4 = st.columns(2)
        with rk_col3:
            st.markdown('<div class="hr-mini-title">Risk Heat Matrix</div>', unsafe_allow_html=True)
            with st.container(border=True):
                risk_heat = alt.Chart(hr_risk).mark_circle(opacity=0.88, stroke="#FFFFFF", strokeWidth=1.2).encode(
                    x=alt.X("Likelihood:Q", title="Likelihood"),
                    y=alt.Y("Exposure Score:Q", title="Exposure Score"),
                    size=alt.Size("Exposure Score:Q", scale=alt.Scale(range=[300, 1800]), legend=None),
                    color=alt.Color("Risk Driver:N", legend=alt.Legend(title=None), scale=alt.Scale(range=["#EF4444", "#F59E0B", "#3B82F6", "#10B981", "#6366F1"])),
                    tooltip=["Risk Driver:N", alt.Tooltip("Likelihood:Q", format=".1f"), alt.Tooltip("Exposure Score:Q", format=".0f")],
                )
                risk_lbl = alt.Chart(hr_risk).mark_text(dy=-10, fontSize=9, color="#1E293B").encode(
                    x="Likelihood:Q", y="Exposure Score:Q", text="Risk Driver:N"
                )
                st.altair_chart(style_hr_chart(risk_heat + risk_lbl, height=235), use_container_width=True)
                max_risk = hr_risk.sort_values(["Likelihood", "Exposure Score"], ascending=False).iloc[0]
                render_hr_ai_reco(
                    "Risk Concentration",
                    f"{max_risk['Risk Driver']} is the highest-likelihood, highest-exposure risk in the matrix.",
                    "Escalate this risk to monthly executive governance with clear trigger thresholds.",
                    "Improves proactive control of people-related delivery risk.",
                    level="critical",
                )

        with rk_col4:
            st.markdown('<div class="hr-mini-title">Scenario Attrition vs Productivity Trade-off</div>', unsafe_allow_html=True)
            with st.container(border=True):
                trade_scatter = alt.Chart(hr_scenario).mark_circle(opacity=0.9, stroke="#FFFFFF", strokeWidth=1.3).encode(
                    x=alt.X("Voluntary Attrition %:Q", title="Voluntary Attrition (%)"),
                    y=alt.Y("Productivity Index:Q", title="Productivity Index"),
                    size=alt.Size("Headcount EoQ:Q", scale=alt.Scale(range=[420, 1700]), legend=None),
                    color=alt.Color("Scenario:N", scale=alt.Scale(domain=["Downside", "Base", "Upside"], range=["#EF4444", "#3B82F6", "#10B981"]), legend=None),
                    tooltip=["Scenario:N", alt.Tooltip("Headcount EoQ:Q", format=".0f"), alt.Tooltip("Productivity Index:Q", format=".0f"), alt.Tooltip("Voluntary Attrition %:Q", format=".1f"), "Probability:N"],
                )
                trade_lbl = alt.Chart(hr_scenario).mark_text(dy=-10, fontSize=10, color="#1E293B").encode(
                    x="Voluntary Attrition %:Q", y="Productivity Index:Q", text="Scenario:N"
                )
                st.altair_chart(style_hr_chart(trade_scatter + trade_lbl, height=235), use_container_width=True)
                render_hr_ai_reco(
                    "Strategic Workforce Trade-off",
                    "Lower attrition scenarios align with materially higher productivity outcomes.",
                    "Concentrate retention investments in critical roles where productivity elasticity is strongest.",
                    "Improves both service capacity and workforce efficiency in parallel.",
                    level="warning",
                )

        st.markdown(dedent(f"""
            <div style="background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%); border-radius: 10px; padding: 0.82rem 0.95rem; margin-top: 0.55rem; border-left: 4px solid #F59E0B;">
                <div style="display: flex; align-items: center;">
                    <span style="font-size: 1.35rem; margin-right: 0.55rem;">⚠️</span>
                    <div>
                        <strong style="color: #92400E;">Urgent: {top_hr_risk['Risk Driver']} is the top workforce risk</strong>
                        <div style="color: #B45309; font-size: 0.84rem;">Exposure score {top_hr_risk['Exposure Score']:.0f} with high likelihood ({top_hr_risk['Likelihood']:.1f}) · prioritize mitigation in next HR operating cycle</div>
                    </div>
                </div>
            </div>
        """), unsafe_allow_html=True)

elif selected_menu == "Conclusion":
    st.image(
        "https://raw.githubusercontent.com/pmjose/PremiumFiber/main/image/gemini.png",
        use_container_width=True,
    )

# ---------------------------------------------------------------------------
# Footer (PremiumFiber footer)
# ---------------------------------------------------------------------------
st.markdown(dedent(f"""
    <div class="mf-footer">
        <div class="mf-footer-brand">Premium<span>Fiber</span></div>
        <div style="max-width:760px; margin:16px auto 0; padding:14px 16px; border-radius:12px; background:rgba(255,255,255,0.07); border:1px solid rgba(255,255,255,0.18); color:#E2E8F0;">
            <div style="font-size:0.9rem; font-weight:800; letter-spacing:0.2px;">PremiumFiber + Snowflake: partnership for scalable telecom growth</div>
            <div style="font-size:0.82rem; line-height:1.45; margin-top:6px; color:rgba(255,255,255,0.82);">
                Unified data, AI-driven decisions, and faster execution from network operations to subscriber retention.
            </div>
            <div style="display:flex; justify-content:center; gap:12px; flex-wrap:wrap; margin-top:9px; font-size:0.74rem; color:rgba(255,255,255,0.78);">
                <span>Real-time analytics</span>
                <span>Predictive churn prevention</span>
                <span>CAPEX prioritization intelligence</span>
            </div>
        </div>
        <hr class="mf-footer-divider">
        <div class="mf-footer-copy" style="display:flex; flex-direction:column; align-items:center; gap:0.32rem;">
            <div style="display:inline-flex; align-items:center; gap:0.46rem; background:rgba(255,255,255,0.08); border:1px solid rgba(255,255,255,0.22); border-radius:999px; padding:0.24rem 0.68rem; color:#E2E8F0; font-weight:700;">Build with &#10084;&#65039; by Snowflake for PremiumFiber</div>
        </div>
    </div>
"""), unsafe_allow_html=True)
