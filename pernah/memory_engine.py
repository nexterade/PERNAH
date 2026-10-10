from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta, timezone

IDR_WORDS = {'jt': 1_000_000, 'juta': 1_000_000, 'rb': 1_000, 'ribu': 1_000}

@dataclass
class MemoryDraft:
    original_text: str
    normalized_text: str
    detected_language: str
    intent: str
    entities: list[dict] = field(default_factory=list)
    transaction: dict | None = None
    event: dict | None = None
    relationships: list[dict] = field(default_factory=list)
    temporal_expression: str | None = None
    occurred_at: str | None = None
    query: dict | None = None
    confidence: float = 1.0
    source_type: str = 'manual'


def detect_language(text: str) -> str:
    s = text.lower()
    words = set(re.findall(r"\b[\w']+\b", s))
    su_markers = ('urang','teu','can','nya','meli','geus','ieu','eta','mah')
    id_markers = ('gue','aku','saya','pernah','beli','nggak','gak','tidak','sama')
    su = sum(w in words for w in su_markers)
    idn = sum(w in words for w in id_markers)
    # Some natural Sundanese/Indonesian sentences code-switch common verbs such as
    # "beli" or "pernah". Distinctive Sundanese markers should win an otherwise
    # tied score instead of collapsing the sentence to Indonesian.
    strong_su = any(w in words for w in ('urang','teu','can','meli','geus','ieu','eta'))
    if su > idn or (su == idn and strong_su): return 'su'
    if idn: return 'id'
    if re.search(r'\b(the|bought|buy|yesterday|today|where|when)\b', s): return 'en'
    return 'id'


def _amount(text: str):
    m = re.search(r'(?:harga(?:nya|na)?|rp\.?)\s*([0-9][0-9.,]*)\s*(jt|juta|rb|ribu)?', text.lower())
    if not m: return None
    raw = m.group(1).replace('.', '').replace(',', '')
    value = int(raw)
    mult = IDR_WORDS.get(m.group(2) or '', 1)
    return value * mult


def _utc(reference_time: datetime) -> datetime:
    return reference_time.astimezone(timezone.utc)


def _day_window(reference_time: datetime, offset_days: int = 0):
    day = (_utc(reference_time) + timedelta(days=offset_days)).date()
    return (
        f'{day.isoformat()}T00:00:00Z',
        f'{day.isoformat()}T23:59:59Z',
    )


def _week_window(reference_time: datetime, offset_weeks: int = 0):
    day = _utc(reference_time).date() + timedelta(weeks=offset_weeks)
    monday = day - timedelta(days=day.weekday())
    sunday = monday + timedelta(days=6)
    return (
        f'{monday.isoformat()}T00:00:00Z',
        f'{sunday.isoformat()}T23:59:59Z',
    )


def _month_window(reference_time: datetime, offset_months: int = 0):
    current = _utc(reference_time).date()
    month_index = current.year * 12 + (current.month - 1) + offset_months
    year, month_zero = divmod(month_index, 12)
    month = month_zero + 1
    first = date(year, month, 1)
    if month == 12:
        next_first = date(year + 1, 1, 1)
    else:
        next_first = date(year, month + 1, 1)
    last = next_first - timedelta(days=1)
    return (
        f'{first.isoformat()}T00:00:00Z',
        f'{last.isoformat()}T23:59:59Z',
    )


def _relative_time(text: str, reference_time: datetime):
    s = text.lower()
    ref = _utc(reference_time)
    if 'tadi isuk' in s or 'tadi pagi' in s:
        return (ref.replace(hour=7, minute=0, second=0, microsecond=0), 'tadi isuk' if 'tadi isuk' in s else 'tadi pagi')
    patterns = (
        (r'\b(?:kemarin|yesterday)\b', -1, 'kemarin' if 'kemarin' in s else 'yesterday'),
        (r'\b(?:hari ini|today)\b', 0, 'hari ini' if 'hari ini' in s else 'today'),
        (r'\b(?:besok|tomorrow)\b', 1, 'besok' if 'besok' in s else 'tomorrow'),
    )
    for pattern, offset, label in patterns:
        if re.search(pattern, s):
            return (ref + timedelta(days=offset), label)
    m = re.search(r'\b(\d+)\s*(?:hari\s*(?:yang\s*)?lalu|days?\s+ago)\b', s)
    if m:
        n = int(m.group(1))
        return (ref - timedelta(days=n), m.group(0))
    return None, None


def _temporal_window(text: str, reference_time: datetime):
    s = text.lower()
    if re.search(r'\b(?:kemarin|yesterday)\b', s):
        return (*_day_window(reference_time, -1), 'kemarin' if 'kemarin' in s else 'yesterday')
    if re.search(r'\b(?:hari ini|today)\b', s):
        return (*_day_window(reference_time, 0), 'hari ini' if 'hari ini' in s else 'today')
    m = re.search(r'\b(\d+)\s*(?:hari\s*(?:yang\s*)?lalu|days?\s+ago)\b', s)
    if m:
        n = int(m.group(1))
        return (*_day_window(reference_time, -n), m.group(0))
    if re.search(r'\b(?:minggu lalu|last week)\b', s):
        return (*_week_window(reference_time, -1), 'minggu lalu' if 'minggu lalu' in s else 'last week')
    if re.search(r'\b(?:minggu ini|this week)\b', s):
        return (*_week_window(reference_time, 0), 'minggu ini' if 'minggu ini' in s else 'this week')
    if re.search(r'\b(?:bulan lalu|last month)\b', s):
        return (*_month_window(reference_time, -1), 'bulan lalu' if 'bulan lalu' in s else 'last month')
    if re.search(r'\b(?:bulan ini|this month)\b', s):
        return (*_month_window(reference_time, 0), 'bulan ini' if 'bulan ini' in s else 'this month')
    return None, None, None


def _entities(text: str):
    found = []
    low = text.lower()
    for word in ('laptop','handphone','hp','passport','paspor'):
        if re.search(rf'\b{re.escape(word)}\b', low):
            name = {'hp':'handphone','paspor':'passport'}.get(word, word)
            if not any(e['name'] == name for e in found): found.append({'type':'object','name':name})
    # Capitalized person/place candidates after supported relationship/event verbs.
    relationship_prefixes = (
        'sama', 'with', 'ketemu', 'meet', 'bertemu', 'bersama',
        'ngobrol sama', 'ngobrol dengan', 'chat sama', 'chat dengan',
        'telepon', 'telefon', 'call', 'kerja bareng', 'kerja dengan',
        'work with', 'worked with',
    )
    prefix_pattern = '|'.join(sorted((re.escape(x) for x in relationship_prefixes), key=len, reverse=True))
    for m in re.finditer(rf'\b(?:{prefix_pattern})\s+([A-Z][\w-]*(?:\s+[A-Z][\w-]*)*)', text):
        name = m.group(1).strip().rstrip('?.!,')
        if not any(e['name'] == name for e in found):
            found.append({'type':'person','name':name})
    return found


def normalize(text: str, reference_time: datetime | None = None, source_type: str = 'manual') -> MemoryDraft:
    ref = reference_time or datetime.now(timezone.utc)
    lang = detect_language(text)
    low = text.lower()
    query = None
    intent = 'capture_memory'
    transaction = None
    event = None
    relationships = []
    temporal, temporal_expr = _relative_time(text, ref)
    entities = _entities(text)

    relationship_patterns = (
        ('meeting', 'participant', ('ketemu ', 'meet ', 'bertemu ')),
        ('conversation', 'participant', ('ngobrol ', 'ngobrol sama ', 'ngobrol dengan ', 'chat ', 'chat dengan ')),
        ('call', 'participant', ('telepon ', 'telefon ', 'call ')),
        ('collaboration', 'participant', ('kerja bareng ', 'kerja dengan ', 'work with ', 'worked with ')),
    )

    def relationship_pattern():
        for event_type, relation_type, markers in relationship_patterns:
            if any(marker in low for marker in markers):
                return event_type, relation_type
        return None

    rel_pattern = relationship_pattern()
    is_relationship_query = ('?' in text and (rel_pattern or any(x in low for x in ('hubungan dengan', 'relationship with'))))
    is_purchase_query = any(x in low for x in ('pernah meli','pernah beli','pernah membeli','did you buy','pernah beli')) and '?' in text
    is_purchase_capture = any(x in low for x in ('meli','beli','membeli','bought','buy')) and not is_purchase_query
    is_semantic_query = '?' in text and not is_relationship_query and not is_purchase_query
    if is_relationship_query and entities:
        intent = 'entity_relationship_retrieval'
        query = {
            'action': 'entity_relationship',
            'entity': entities[0]['name'],
            'relation_type': rel_pattern[1] if rel_pattern else 'participant',
            'event_type': rel_pattern[0] if rel_pattern else None,
            'temporal': 'past',
        }
        after, before, _ = _temporal_window(text, ref)
        if after and before:
            query['occurred_after'] = after
            query['occurred_before'] = before
    elif is_purchase_query:
        intent = 'temporal_retrieval'
        query = {'action':'purchase','temporal':'past','text': text}
        if entities: query['entity'] = entities[0]['name']
        after, before, _ = _temporal_window(text, ref)
        if after and before:
            query['occurred_after'] = after
            query['occurred_before'] = before
    elif is_semantic_query:
        intent = 'semantic_retrieval'
        query = {'action': 'semantic_search', 'text': text}
    elif is_purchase_capture:
        intent = 'record_purchase'
        amount = _amount(text)
        if amount is not None:
            transaction = {'amount': amount, 'currency':'IDR', 'direction':'expense', 'category':'purchase'}
        event = {'type':'purchase', 'occurred_at': temporal.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z') if temporal else None}
        for e in entities:
            relationships.append({'relation_type':'involves','entity':e})
    else:
        # Deterministic relationship capture across the supported richer event patterns.
        if rel_pattern and entities:
            event_type, relation_type = rel_pattern
            intent = 'record_event'
            event = {'type': event_type, 'occurred_at': temporal.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z') if temporal else None}
            relationships.append({'relation_type': relation_type, 'entity': entities[0]})

    occurred = event['occurred_at'] if event else (temporal.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z') if temporal else None)
    return MemoryDraft(text, ' '.join(text.split()), lang, intent, entities, transaction, event, relationships, temporal_expr, occurred, query, 1.0, source_type)
