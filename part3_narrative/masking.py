def alias_for(reseller_id: str) -> str:
  """Derives a privacy alias from a reseller ID.

  Acceptance criterion: alias_for('RS019') == 'ALIAS-19'.
  """
  clean_id = reseller_id.strip()
  if not clean_id.startswith("RS") or len(clean_id) < 5:
    raise ValueError(f"Invalid reseller_id format: {reseller_id}")
  # RS019 -> ALIAS-19; RS006 -> ALIAS-06
  suffix = clean_id[3:]
  return f"ALIAS-{suffix}"


def assert_no_raw_names_leak(text: str, reseller_names: list[str]) -> bool:
  """Returns False if any raw reseller name appears verbatim in text, else True."""
  for name in reseller_names:
    if name.strip() and name in text:
      return False
  return True