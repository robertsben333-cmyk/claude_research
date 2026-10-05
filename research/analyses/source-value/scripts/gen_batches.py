#!/usr/bin/env python3
"""Generate the systematic question batches (Phase 3) from the frozen codebook, its merges and
the LABEL counts only (how many voting items a code has in stratum A). No outcome is read.

  python3 scripts/gen_batches.py <batch id> [...]    # writes ledger/batches/<id>.json

Batches b01-b12 are the systematic families of PROMPT.md Phase 3; later batches (b13+) are
written by hand from leads and must be tested on a different stratum or on forward days.
"""
import json, os, sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
SV = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import core  # noqa: E402

GROUPS = ['company_own', 'other_company', 'official_record', 'market_data', 'media', 'alt_data', 'researcher_own', 'search_note']
BANDS = ['micro', 'small', 'mid', 'large']


def label_counts():
    """codes -> voting items / all items in stratum A (labels only; no move is touched)."""
    cb = core.codebook()
    grp = {s['id']: s['group'] for s in cb['subtypes']}
    mm = core.merge_map()
    L = core.load_labels()
    I = json.load(open(f'{SV}/data/items.json'))
    E = {e['id']: e for e in json.load(open(f'{SV}/data/events.json'))}
    vote, allc = Counter(), Counter()
    for it in I:
        if it['stratum'] != 'A' or E[it['event']]['duplicate_hunt']:
            continue
        runs = [r[it['i']] for r in L.get(it['pack_id'], []) if it['i'] in r]
        if not runs:
            continue
        lab = core.merged_label(runs, mm, grp)
        for c, w in lab['subtype_w'].items():
            allc[c] += w
            if lab['vote']:
                vote[c] += w
    return vote, allc, grp, mm


def codes(min_vote):
    vote, allc, grp, mm = label_counts()
    return [c for c, n in vote.most_common() if n >= min_vote], vote, allc


def Q(qid, question, metric, cut=None, hyp='any', unit='item', why='', **kw):
    d = {'id': qid, 'question': question, 'hypothesis': hyp, 'unit': unit, 'metric': metric, 'cut': cut or {}, 'why': why}
    d.update(kw)
    return d


def b01():
    """Seed questions of PROMPT.md and group main effects."""
    qs = [
        Q('b01-01', "Do the company's own quantified disclosures dated inside the window carry the sign in large caps?", 'DVstar',
          {'group': 'company_own', 'quantified': True, 'dated_in_window': True, 'cap_band': 'large'}, '+', why='seed 1'),
        Q('b01-02', "Same, mid and large caps together (more prints).", 'DVstar',
          {'group': 'company_own', 'quantified': True, 'dated_in_window': True, 'cap_band': ['mid', 'large']}, '+', why='seed 1, power'),
        Q('b01-03', "In large caps, do option-market items (implied move, skew, flow) carry the sign?", 'DVstar',
          {'subtype': 'mkt_options', 'cap_band': 'large'}, 'any', why='seed 2'),
        Q('b01-04', "In large caps, do short-interest items carry the sign?", 'DVstar', {'subtype': 'mkt_short_interest', 'cap_band': 'large'}, 'any', why='seed 2'),
        Q('b01-05', "In large caps, do consensus and estimate-revision items carry the sign?", 'DVstar', {'subtype': 'mkt_consensus', 'cap_band': 'large'}, 'any', why='seed 2'),
        Q('b01-06', "In large caps, does the market-data group as a whole carry the sign?", 'DVstar', {'group': 'market_data', 'cap_band': 'large'}, 'any', why='seed 2'),
        Q('b01-07', "Do peer earnings results carry the sign better in micro and small caps than in mid and large?", 'contrast_DVstar',
          {'subtype': 'oth_peer_results', 'cap_band': ['micro', 'small']}, '+', cut_b={'subtype': 'oth_peer_results', 'cap_band': ['mid', 'large']}, why='seed 3'),
        Q('b01-08', "Do peer earnings results carry the sign in micro and small caps?", 'DVstar', {'subtype': 'oth_peer_results', 'cap_band': ['micro', 'small']}, '+', why='seed 3'),
        Q('b01-09', "Are retail-finance portal articles worse than noise?", 'DVstar', {'subtype': 'med_retail_portal'}, '-', why='seed 4'),
        Q('b01-10', "Are retail-finance-domain items (any subtype) worse than noise?", 'DVstar', {'domain_class': 'retail_finance', 'not_subtype': [c for c in ['G:search_note'] ] , 'kind': ['filed_by_first_hunter', 'put_outside_window_by_first_hunter', 'rejected_by_first_hunter']}, '-', why='seed 4, by domain'),
        Q('b01-11', "Among retail-finance-domain items, do those already widely reported do worse than the rest?", 'contrast_DVstar',
          {'domain_class': 'retail_finance', 'already_widely_reported': True}, '-', cut_b={'domain_class': 'retail_finance', 'already_widely_reported': False}, why='seed 4, mechanism'),
        Q('b01-12', "Does alternative data carry the sign anywhere (all bands)?", 'DVstar', {'group': 'alt_data'}, 'any', why='seed 5'),
        Q('b01-13', "Does alternative data with 2+ independent sources do better than uncorroborated alt data?", 'contrast_DVstar',
          {'group': 'alt_data', 'corroborated': True}, '+', cut_b={'group': 'alt_data', 'corroborated': False}, why='seed 5'),
        Q('b01-14', "Do micro caps holding a financing item (ATM, S-3, 424B, convertible) fall more than other micro caps, beyond drift?", 'presence_res',
          {'subtype': 'own_financing'}, '-', unit='name', base_events={'cap_band': 'micro'}, why='seed 6'),
        Q('b01-15', "Do financing items' votes carry the sign in micro caps?", 'DVstar', {'subtype': 'own_financing', 'cap_band': 'micro'}, '+', why='seed 6'),
        Q('b01-16', "Do absence items (an expected disclosure missing, or a search note with a direction) carry the sign?", 'DVstar',
          {'group': ['researcher_own', 'search_note'], 'subtype': ['res_absence_of_disclosure'] + ['srch_preannouncement_guidance', 'srch_filing_stream_quiet', 'srch_insider_ownership', 'srch_litigation_regulatory', 'srch_balance_sheet_capital', 'srch_management_governance', 'srch_business_events', 'srch_consensus_analyst', 'srch_unexplained_move', 'srch_positioning', 'srch_alt_data', 'srch_external_readthrough', 'srch_earnings_item', 'srch_source_unusable', 'srch_general', 'srch_other', 'G:search_note']}, 'any', why='seed 7'),
        Q('b01-17', "Do prints whose hunter found no pre-announcement or guidance change move differently (residual) from the rest?", 'presence_res',
          {'subtype': ['srch_preannouncement_guidance']}, 'any', unit='name', why='seed 7, name level'),
        Q('b01-18', "Does the hunter oversize market-data (positioning, options, prices) findings relative to the realised move?", 'oversize',
          {'group': 'market_data'}, '+', why='seed 8'),
        Q('b01-19', "Does the hunter oversize macro and commodity findings (official statistics, commodity/FX prices, trade policy)?", 'oversize',
          {'subtype': ['off_official_statistics', 'mkt_commodity_fx', 'off_trade_policy']}, '+', why='seed 8'),
        Q('b01-20', "Reference: does the hunter oversize the company's own disclosures?", 'oversize', {'group': 'company_own'}, 'any', why='seed 8 reference'),
        Q('b01-21', "Do the items the hunter FILED carry the sign (labeller vote)?", 'DVstar', {'kind': 'filed_by_first_hunter'}, '+', why='seed 9'),
        Q('b01-22', "Do the items the hunter put OUTSIDE the window carry the sign?", 'DVstar', {'kind': 'put_outside_window_by_first_hunter'}, 'any', why='seed 9'),
        Q('b01-23', "Filed against put-outside-window items: is the value concentrated in filed items?", 'contrast_DVstar',
          {'kind': 'filed_by_first_hunter'}, '+', cut_b={'kind': 'put_outside_window_by_first_hunter'}, why='seed 9'),
        Q('b01-24', "Do items claiming a LARGE move (relative to priced) come in names that move more than priced?", 'MV',
          {'magnitude_claim': 'large'}, '+', unit='name', why='seed 10'),
    ]
    for g in GROUPS:
        qs.append(Q(f'b01-g-{g}', f"Main effect: does the {g} group carry the sign (DV*) in US hunts?", 'DVstar', {'group': g},
                    '+' if g == 'company_own' else 'any', why='main effect, group'))
    return qs


def b02():
    cs, vote, allc = codes(8)
    return [Q(f'b02-{c}', f"Main effect: does subtype {c} carry the sign (DV*) in US hunts, all bands?", 'DVstar', {'subtype': c}, 'any',
              why=f'main effect, subtype ({vote[c]:.0f} voting items)') for c in cs if not c.startswith('srch_')]


def band_batches():
    cs, vote, allc = codes(8)
    cs = [c for c in cs if not c.startswith('srch_')]
    qs = [Q(f'bx-{c}-{b}', f"Registry cell: does {c} carry the sign (DV*) in {b} caps?", 'DVstar', {'subtype': c, 'cap_band': b}, 'any',
            why='subtype x size band (registry cell)') for c in cs for b in BANDS]
    qs += [Q(f'bx-G-{g}-{b}', f"Registry cell: does the {g} group carry the sign (DV*) in {b} caps?", 'DVstar', {'group': g, 'cap_band': b}, 'any',
             why='group x size band') for g in GROUPS for b in BANDS]
    return qs


def b07():
    """Item qualities."""
    D = 'filed_by_first_hunter'
    pairs = [('quantified', True, False), ('primary_document', True, False), ('dated_in_window', True, False), ('corroborated', True, False),
             ('already_widely_reported', False, True), ('contradicted_in_pack', False, True), ('about_focal_company', True, False), ('non_english', True, False)]
    qs = []
    for f, a, b in pairs:
        qs.append(Q(f'b07-{f}', f"Item quality: do items with {f}={a} carry the sign better than {f}={b}?", 'contrast_DVstar', {f: a}, '+', cut_b={f: b},
                    why='item quality contrast'))
        qs.append(Q(f'b07-{f}-own', f"Item quality within the company's own disclosures: {f}={a} against {f}={b}.", 'contrast_DVstar',
                    {f: a, 'group': 'company_own'}, '+', cut_b={f: b, 'group': 'company_own'}, why='item quality, own group'))
    for ab in ['<=7', '8-30', '31-90', '>90']:
        qs.append(Q(f'b07-age-{ab}', f"Do items whose source is {ab} days old at entry carry the sign?", 'DVstar', {'age_bucket': ab}, 'any', why='age of source'))
    qs.append(Q('b07-age-fresh-vs-old', "Fresh sources (<=30 days) against older ones (>30).", 'contrast_DVstar', {'age_bucket': ['<=7', '8-30']}, '+',
                cut_b={'age_bucket': ['31-90', '>90']}, why='age of source'))
    for f in ('quantified', 'primary_document', 'corroborated', 'dated_in_window'):
        qs.append(Q(f'b07-{f}-main', f"Do items with {f}=True carry the sign (DV*)?", 'DVstar', {f: True}, 'any', why='flag main effect'))
    qs.append(Q('b07-mag-large-dv', "Do items claiming a large move carry the sign?", 'DVstar', {'magnitude_claim': 'large'}, 'any', why='magnitude flag'))
    qs.append(Q('b07-8k202', "Do items citing a results 8-K (Item 2.02) carry the sign?", 'DVstar', {'is_8k_202': True}, 'any', why='mechanical: 8-K 2.02'))
    qs.append(Q('b07-secform-ownership', "Do items citing ownership filings (Form 4, 144, 13D/G) carry the sign?", 'DVstar', {'sec_family': 'ownership'}, 'any', why='mechanical form'))
    qs.append(Q('b07-newswire-own', "Do the company's own newswire releases carry the sign?", 'DVstar', {'newswire_own': True}, '+', why='prior study: press releases 65%'))
    return qs


def b08():
    """Context."""
    ctx = [('option_anchor', True, False), ('session', 'amc', 'bmo'), ('runup_dir', 'up', 'down'), ('vol_high', True, False),
           ('retail_high', True, False), ('search_spike_high', True, False), ('bar', True, False), ('hunter_era', 'opus5', 'opus55'),
           ('implied_big', True, False)]
    qs = []
    for g in ['company_own', 'other_company', 'market_data', 'media']:
        for f, a, b in ctx:
            qs.append(Q(f'b08-{g}-{f}', f"Does the {g} group carry the sign better where {f}={a} than where {f}={b}?", 'contrast_DVstar',
                        {'group': g, f: a}, 'any', cut_b={'group': g, f: b}, why='group x context'))
    qs.append(Q('b08-lean-agree', "Do item votes that agree with the sealed price lean carry the sign better than those against it?", 'contrast_DVstar',
                {'lean_agree': True}, 'any', cut_b={'lean_agree': False}, why='context: priced lean (dashboard H: hunt earns where it follows the lean)'))
    qs.append(Q('b08-own-anchorless', "Company's own disclosures in names without an option chain (prior study: 63%).", 'DVstar',
                {'group': 'company_own', 'option_anchor': False}, '+', why='prior study replication on new labels'))
    qs.append(Q('b08-own-anchored', "Company's own disclosures in option-priced names.", 'DVstar', {'group': 'company_own', 'option_anchor': True}, 'any', why='prior study'))
    qs.append(Q('b08-mkt-anchorless', "Market-data items in names without an option chain (prior study: positioning wrong way).", 'DVstar',
                {'group': 'market_data', 'option_anchor': False}, '-', why='prior study replication'))
    qs.append(Q('b08-oth-anchorless', "Other-company read-across in names without an option chain (prior study: wrong way).", 'DVstar',
                {'group': 'other_company', 'option_anchor': False}, '-', why='prior study replication'))
    return qs


def b09():
    """Magnitude: does presence of a group / code predict a move larger than priced?"""
    cs, vote, allc = codes(8)
    qs = [Q(f'b09-G-{g}', f"Magnitude: are prints holding a {g} item more likely to move more than priced?", 'MV', {'group': g}, 'any', unit='name',
            why='magnitude, group') for g in GROUPS]
    allcs = [c for c, n in allc.most_common() if n >= 15][:26]
    qs += [Q(f'b09-{c}', f"Magnitude: are prints holding a {c} item more likely to move more than priced?", 'MV', {'subtype': c}, 'any', unit='name',
             why='magnitude, subtype') for c in allcs]
    return qs


def b10():
    """Horizons: open against close, groups."""
    qs = []
    for g in GROUPS[:6]:
        for h in ('open', 'close'):
            qs.append(Q(f'b10-{g}-{h}', f"Does the {g} group carry the sign to the {h}?", 'DVstar', {'group': g}, 'any', outcome_horizon=h, why='horizon'))
    cs, vote, allc = codes(15)
    for c in [c for c in cs if not c.startswith('srch_')][:12]:
        for h in ('open', 'close'):
            qs.append(Q(f'b10-{c}-{h}', f"Does {c} carry the sign to the {h}?", 'DVstar', {'subtype': c}, 'any', outcome_horizon=h, why='horizon, subtype'))
    return qs


def b11():
    """The hunter's own judgement, and marginal value against the judges."""
    qs = [
        Q('b11-hunter-sign', "Does the hunter's own sign on its filed findings carry the sign (DV*)?", 'DVstar', {'kind': 'filed_by_first_hunter'}, '+',
          vote_field='hunter_vote', why='hunter judgement'),
        Q('b11-agree', "Filed findings where hunter and labeller agree on the sign, against those where they disagree (labeller vote).", 'contrast_DVstar',
          {'hunter_agrees_labeller': True}, '+', cut_b={'hunter_agrees_labeller': False}, why='hunter judgement'),
        Q('b11-disagree-labeller', "Where hunter and labeller disagree, is the labeller's sign right more often than chance?", 'DVstar',
          {'hunter_agrees_labeller': False}, 'any', why='hunter judgement'),
    ]
    for g in GROUPS[:7]:
        qs.append(Q(f'b11-hsign-{g}', f"Does the hunter's sign on its {g} findings carry the sign?", 'DVstar', {'group': g, 'kind': 'filed_by_first_hunter'}, 'any',
                    vote_field='hunter_vote', why='hunter judgement by group'))
        qs.append(Q(f'b11-over-{g}', f"Does the hunter oversize its {g} findings?", 'oversize', {'group': g}, 'any', why='hunter sizing by group'))
    for g in GROUPS[:6]:
        qs.append(Q(f'b11-mgv-{g}', f"Marginal value: are the four judges right more often where the {g} net vote agrees with them?", 'MgV_obs',
                    {'group': g}, '+', unit='name', why='MgV observational'))
    return qs


def b12():
    """Replication strata: B (US dossiers) and C (ex-US hunts)."""
    qs = []
    cs, vote, allc = codes(8)
    top = [c for c in cs if not c.startswith('srch_')][:14]
    for s in ('B', 'C'):
        for g in GROUPS[:7]:
            qs.append(Q(f'b12-{s}-G-{g}', f"Stratum {s}: does the {g} group carry the sign (DV*)?", 'DVstar', {'group': g}, 'any', stratum=s, why='replication stratum'))
        for c in top:
            qs.append(Q(f'b12-{s}-{c}', f"Stratum {s}: does {c} carry the sign (DV*)?", 'DVstar', {'subtype': c}, 'any', stratum=s, why='replication stratum'))
    return qs


GEN = {'b01': b01, 'b02': b02, 'b07': b07, 'b08': b08, 'b09': b09, 'b10': b10, 'b11': b11, 'b12': b12}


def main():
    os.makedirs(f'{SV}/ledger/batches', exist_ok=True)
    for bid in sys.argv[1:]:
        if bid == 'bx':
            qs = band_batches()
            for k in range(0, len(qs), 40):
                n = f'b{3 + k // 40:02d}' if 3 + k // 40 <= 6 else f'bx{k // 40}'
                json.dump({'batch': n, 'questions': [dict(q, id=q['id'].replace('bx-', n + '-')) for q in qs[k:k + 40]]},
                          open(f'{SV}/ledger/batches/{n}.json', 'w'), indent=1)
                print(n, len(qs[k:k + 40]))
            continue
        qs = GEN[bid]()
        json.dump({'batch': bid, 'questions': qs}, open(f'{SV}/ledger/batches/{bid}.json', 'w'), indent=1)
        print(bid, len(qs))


if __name__ == '__main__':
    main()
