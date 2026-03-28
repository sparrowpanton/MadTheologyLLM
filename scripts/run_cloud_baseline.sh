#!/bin/bash
# Run cloud baseline testing — Llama 3.1 8B on Thunder Compute
# 59 prompts × 1 model = 59 responses
#
# NOTE: GPT-OSS 20B skipped due to Ollama GPU loading issue on Thunder Compute
# (model loads to CPU instead of GPU, exceeds system RAM)
# Will retry GPT-OSS on Lambda Labs hardware when grant comes through

echo "========================================"
echo "  DISABILITY JUSTICE LLM — CLOUD BASELINE"
echo "  Llama 3.1 8B (Meta, USA)"
echo "  59 prompts = 59 responses"
echo "  Starting at $(date)"
echo "========================================"

mkdir -p data/baseline

OUTFILE="data/baseline/cloud_baseline_$(date +%Y%m%d_%H%M%S).jsonl"
PROMPTS_FILE="data/prompts_all.jsonl"

if [ ! -f "$PROMPTS_FILE" ]; then
    echo "ERROR: $PROMPTS_FILE not found!"
    exit 1
fi

echo "Output: $OUTFILE"
echo ""

MODELS=(
    "llama3.1:8b|3|8B|Meta|USA"
)

NUM_PROMPTS=$(wc -l < "$PROMPTS_FILE")
TOTAL=$(( ${#MODELS[@]} * NUM_PROMPTS ))
CURRENT=0
ERRORS=0
START_RUN=$(date +%s)

for MODEL_STR in "${MODELS[@]}"; do
    IFS='|' read -r MODEL TIER PARAMS ORIGIN COUNTRY <<< "$MODEL_STR"

    echo ""
    echo "════════════════════════════════════════"
    echo "  Model: $MODEL (Tier $TIER, $PARAMS, $ORIGIN, $COUNTRY)"
    echo "════════════════════════════════════════"

    MODEL_START=$(date +%s)

    while IFS= read -r PROMPT_LINE; do
        PID=$(echo "$PROMPT_LINE" | python3 -c "import sys,json; print(json.loads(sys.stdin.read())['prompt_id'])")
        CATEGORY=$(echo "$PROMPT_LINE" | python3 -c "import sys,json; print(json.loads(sys.stdin.read())['prompt_category'])")
        PROMPT_TEXT=$(echo "$PROMPT_LINE" | python3 -c "import sys,json; print(json.loads(sys.stdin.read())['prompt_text'])")

        CURRENT=$((CURRENT + 1))
        echo ""
        echo "  [$CURRENT/$TOTAL] $PID ($CATEGORY) — $MODEL"
        echo "  Running..."

        START_TIME=$(date +%s)
        RESPONSE=$(echo "$PROMPT_TEXT" | ollama run "$MODEL" 2>/dev/null)
        EXIT_CODE=$?
        END_TIME=$(date +%s)
        ELAPSED=$((END_TIME - START_TIME))

        if [ $EXIT_CODE -ne 0 ] || [ -z "$RESPONSE" ]; then
            echo "  ⚠ ERROR: Failed or empty response (exit code: $EXIT_CODE)"
            ERRORS=$((ERRORS + 1))
            ERROR_VAL="\"exit_code_${EXIT_CODE}_or_empty\""
        else
            ERROR_VAL="null"
        fi

        CLEAN_RESPONSE=$(echo "$RESPONSE" | python3 -c "import sys,json; print(json.dumps(sys.stdin.read().strip()))")
        CLEAN_PROMPT=$(echo "$PROMPT_TEXT" | python3 -c "import sys,json; print(json.dumps(sys.stdin.read().strip()))")

        echo "{\"timestamp\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"phase\":\"baseline\",\"model\":\"$MODEL\",\"model_tier\":$TIER,\"model_params\":\"$PARAMS\",\"model_origin\":\"$ORIGIN\",\"model_country\":\"$COUNTRY\",\"prompt_id\":\"$PID\",\"prompt_category\":\"$CATEGORY\",\"prompt_case\":\"\",\"prompt_text\":$CLEAN_PROMPT,\"response_text\":$CLEAN_RESPONSE,\"response_time_seconds\":$ELAPSED,\"error\":$ERROR_VAL}" >> "$OUTFILE"

        echo "  Done (${ELAPSED}s)"
        echo "  Preview: ${RESPONSE:0:120}..."

    done < "$PROMPTS_FILE"

    MODEL_END=$(date +%s)
    MODEL_ELAPSED=$(( MODEL_END - MODEL_START ))
    echo ""
    echo "  → $MODEL complete in ${MODEL_ELAPSED}s ($(( MODEL_ELAPSED / 60 ))m $(( MODEL_ELAPSED % 60 ))s)"

done

END_RUN=$(date +%s)
TOTAL_ELAPSED=$(( END_RUN - START_RUN ))

echo ""
echo "========================================"
echo "  CLOUD BASELINE COMPLETE"
echo "  Results: $OUTFILE"
echo "  Total responses: $CURRENT"
echo "  Errors: $ERRORS"
echo "  Total time: $(( TOTAL_ELAPSED / 60 ))m $(( TOTAL_ELAPSED % 60 ))s"
echo "  Finished at $(date)"
echo "========================================"
echo ""
echo "REMEMBER: STOP YOUR THUNDER COMPUTE INSTANCE!"
