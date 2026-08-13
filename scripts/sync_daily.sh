#!/bin/zsh
# Daily Finsa sync — run manually, ideally every trading day:
#     scripts/sync_daily.sh
# Steps: sync (all instruments incl. futures) -> status -> validate ->
#        rebuild clean store -> verify. Logs to logs/sync/YYYY-MM-DD.log.
# Rationale: the minute feed has a ~30-day rolling retention floor —
# unsynced 1M data is permanently lost. See DATA.md.
set -uo pipefail
cd "$(dirname "$0")/.."
export PYTHONUNBUFFERED=1   # stream python output live through the tee pipe

LOGDIR=logs/sync
mkdir -p "$LOGDIR"
LOG="$LOGDIR/$(date +%F).log"

echo "sync starting — full run takes several minutes; streaming to terminal"
echo "and appending to $LOG"

{
  echo "=== sync start $(date -u +%FT%TZ) ==="

  # 1. pull new bars into data/ (all instruments — incl. uk100fut/uk100sep26 —
  #    all feeds, all sides)
  venv/bin/python scripts/collect.py sync --instr all
  SYNC_RC=$?

  # 2. check what landed (validate exits 1 on NEW issues beyond the
  #    accepted baseline in data/_known_issues.json)
  venv/bin/python scripts/collect.py status
  venv/bin/python scripts/collect.py validate
  VALIDATE_RC=$?

  # 3. rebuild the clean store from raw
  venv/bin/python scripts/store.py build --instr all
  BUILD_RC=$?
  venv/bin/python scripts/store.py verify --instr all
  VERIFY_RC=$?

  echo "=== done $(date -u +%FT%TZ) sync=$SYNC_RC validate=$VALIDATE_RC build=$BUILD_RC verify=$VERIFY_RC ==="
  if [ $SYNC_RC -ne 0 ] || [ $VALIDATE_RC -ne 0 ] || [ $BUILD_RC -ne 0 ] || [ $VERIFY_RC -ne 0 ]; then
    echo "!!! FAILURE — see above"
  fi
} 2>&1 | tee -a "$LOG"

# keep 60 days of logs
find "$LOGDIR" -name '*.log' -mtime +60 -delete
