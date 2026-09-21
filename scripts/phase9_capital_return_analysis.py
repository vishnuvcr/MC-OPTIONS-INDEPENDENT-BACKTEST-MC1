from __future__ import annotations

import argparse
import json
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

LEGS_QTY = {'P35_PE': 1, 'P20_PE': -2, 'P65_CE': 1, 'P80_CE': -2}

def load_primary(zippath: Path, underlying: str) -> pd.DataFrame:
    lower = underlying.lower()
    member = f'data/processed/phase8/{lower}/scenarios/{lower}_w756_p5000.csv'
    with zipfile.ZipFile(zippath) as z:
        with z.open(member) as f:
            df = pd.read_csv(f)
    if df.empty:
        raise ValueError(f'empty primary trade file: {member}')
    df['expiry'] = pd.to_datetime(df['expiry'])
    df['signal_date'] = pd.to_datetime(df['signal_date'])
    df['net_realized_rupees'] = pd.to_numeric(df['net_realized_rupees'], errors='coerce')
    df['net_realized_rupees_enhanced_friction'] = pd.to_numeric(df['net_realized_rupees_enhanced_friction'], errors='coerce')
    df['lot_size'] = pd.to_numeric(df['lot_size'], errors='coerce')
    return df.sort_values(['expiry', 'signal_date']).reset_index(drop=True)

def premium_cashflows(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for rec in df.to_dict('records'):
        prices = json.loads(rec['execution_prices_slipped'])
        lot = float(rec['lot_size'])
        long_cash = sum(max(q, 0) * float(prices[k]) for k, q in LEGS_QTY.items()) * lot
        short_credit = sum(max(-q, 0) * float(prices[k]) for k, q in LEGS_QTY.items()) * lot
        net_cash = long_cash - short_credit
        rows.append((long_cash, short_credit, net_cash))
    out = pd.DataFrame(rows, columns=['long_premium_cash', 'short_premium_credit', 'net_premium_cash'])
    return pd.concat([df.reset_index(drop=True), out], axis=1)

def drawdown_stats(df: pd.DataFrame) -> float:
    equity = df['net_realized_rupees'].cumsum()
    drawdown = equity - equity.cummax()
    return float(drawdown.min())

def overlap_stats(df: pd.DataFrame) -> tuple[int, float | None, list[dict]]:
    records = df[['signal_date', 'expiry', 'net_realized_rupees']].to_dict('records')
    max_concurrent = 0
    worst_combined = None
    worst_dates = []
    dates = pd.date_range(df['signal_date'].min(), df['expiry'].max(), freq='D')
    for d in dates:
        active = [i for i, r in enumerate(records) if r['signal_date'] <= d <= r['expiry']]
        max_concurrent = max(max_concurrent, len(active))
        if len(active) >= 2:
            p = float(sum(records[i]['net_realized_rupees'] for i in active))
            if worst_combined is None or p < worst_combined:
                worst_combined = p
                worst_dates = [{'date': str(d.date()), 'active_positions': active, 'combined_net_pnl': p}]
            elif p == worst_combined:
                worst_dates.append({'date': str(d.date()), 'active_positions': active, 'combined_net_pnl': p})
    return max_concurrent, worst_combined, worst_dates

def analyze(df: pd.DataFrame, underlying: str):
    d = premium_cashflows(df)
    pnl = d['net_realized_rupees'].astype(float)
    loss = -pnl
    q95 = float(np.quantile(loss, 0.95))
    q99 = float(np.quantile(loss, 0.99))
    es95 = float(loss[loss >= q95].mean())
    es99 = float(loss[loss >= q99].mean())
    dd = drawdown_stats(d)
    max_concurrent, worst_overlap_pnl, worst_overlap_dates = overlap_stats(d)
    elapsed_years = float((d['expiry'].max() - d['expiry'].min()).days) / 365.25
    trades_per_year = float(len(d) / elapsed_years) if elapsed_years > 0 else np.nan
    mean_net = float(pnl.mean())
    mean_enh = float(d['net_realized_rupees_enhanced_friction'].mean())
    conservative_capital = max(abs(es95) * max_concurrent, abs(dd))
    metrics = {
        'underlying': underlying,
        'executed_trades': int(len(d)),
        'sample_first_expiry': str(d['expiry'].min().date()),
        'sample_last_expiry': str(d['expiry'].max().date()),
        'elapsed_years': elapsed_years,
        'mean_net_pnl_rupees': mean_net,
        'median_net_pnl_rupees': float(pnl.median()),
        'mean_enhanced_net_pnl_rupees': mean_enh,
        'max_single_trade_loss_rupees': float(loss.max()),
        'pnl_q05_rupees': float(pnl.quantile(0.05)),
        'pnl_q01_rupees': float(pnl.quantile(0.01)),
        'var95_loss_rupees': q95,
        'var99_loss_rupees': q99,
        'es95_loss_rupees': es95,
        'es99_loss_rupees': es99,
        'max_drawdown_rupees': float(dd),
        'mean_long_premium_cash_rupees': float(d['long_premium_cash'].mean()),
        'max_long_premium_cash_rupees': float(d['long_premium_cash'].max()),
        'mean_short_premium_credit_rupees': float(d['short_premium_credit'].mean()),
        'max_short_premium_credit_rupees': float(d['short_premium_credit'].max()),
        'mean_net_premium_cash_rupees': float(d['net_premium_cash'].mean()),
        'min_net_premium_cash_rupees': float(d['net_premium_cash'].min()),
        'max_net_premium_cash_rupees': float(d['net_premium_cash'].max()),
        'max_concurrent_positions': int(max_concurrent),
        'worst_overlapping_combined_pnl_rupees': float(worst_overlap_pnl),
        'es95_capital_proxy_per_position_rupees': es95,
        'observed_drawdown_reserve_rupees': abs(float(dd)),
        'conservative_research_capital_proxy_rupees': conservative_capital,
        'mean_pnl_over_es95': mean_net / es95 if es95 else np.nan,
        'mean_enhanced_pnl_over_es95': mean_enh / es95 if es95 else np.nan,
        'mean_pnl_over_conservative_capital_proxy': mean_net / conservative_capital if conservative_capital else np.nan,
        'mean_enhanced_pnl_over_conservative_capital_proxy': mean_enh / conservative_capital if conservative_capital else np.nan,
        'trades_per_observed_year': trades_per_year,
        'simple_linear_annual_pnl_rupees': mean_net * trades_per_year if np.isfinite(trades_per_year) else np.nan,
        'simple_linear_annual_enhanced_pnl_rupees': mean_enh * trades_per_year if np.isfinite(trades_per_year) else np.nan,
        'simple_linear_annual_return_on_conservative_capital_proxy': (mean_net * trades_per_year) / conservative_capital if np.isfinite(trades_per_year) and conservative_capital else np.nan,
        'simple_linear_annual_enhanced_return_on_conservative_capital_proxy': (mean_enh * trades_per_year) / conservative_capital if np.isfinite(trades_per_year) and conservative_capital else np.nan,
        'worst_overlap_dates': worst_overlap_dates,
    }
    cols = ['expiry','signal_date','lot_size','long_premium_cash','short_premium_credit','net_premium_cash','net_realized_rupees','net_realized_rupees_enhanced_friction']
    return metrics, d[cols]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--artifact', required=True)
    ap.add_argument('--outdir', required=True)
    args = ap.parse_args()
    zippath = Path(args.artifact)
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    all_metrics = []
    for underlying in ('NIFTY','SENSEX'):
        df = load_primary(zippath, underlying)
        metrics, premium = analyze(df, underlying)
        all_metrics.append(metrics)
        premium.to_csv(outdir / f'{underlying.lower()}_capital_trade_table.csv', index=False)
    summary = pd.DataFrame(all_metrics)
    summary.to_csv(outdir / 'phase9_capital_return_summary.csv', index=False)
    (outdir / 'phase9_capital_return_summary.json').write_text(json.dumps(all_metrics, indent=2, default=float), encoding='utf-8')

if __name__ == '__main__':
    main()