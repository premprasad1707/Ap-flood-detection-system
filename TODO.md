## Completed
- [x] 1. Fix data ✓ (81 unique locations, rainfall 0-300mm varied)
- [x] 2. Upgrade model ✓ (RF acc 0.824, integrated to model.py)
- [x] 3. requirements.txt ✓ (+joblib)
- [x] 4. Test app.py running (shapefile permission error - fix geo_utils)
- [x] 5. Load locations to UI + Canals fix
- [x] 6. Commit/push 
- [x] 7. Demo: streamlit run app.py (http://localhost:8501)
- [x] Partial screenshots added (live_ml_dashboard.png committed/pushed)

## Completed (Updated)
- [x] 1. Fix data ✓ (81 unique locations, rainfall 0-300mm varied)
- [x] 2. Upgrade model ✓ (RF acc 0.824, integrated to model.py)
- [x] 3. requirements.txt ✓ (+joblib)
- [x] 4. Test app.py running (shapefile permission error - fix geo_utils)
- [x] 5. Load locations to UI + Canals fix
- [x] 6. Commit/push 
- [x] 7. Demo: streamlit run app.py (http://localhost:8501)
- [x] venv/ created & deps installed (all satisfied)
- [x] Partial screenshots added/committed/pushed (live_ml_dashboard.png + README merge to main)

## Remaining (User Manual)
- Capture remaining 6 screenshots per table (TODO step 3).
- git add/commit/push screenshots/.

**Repo updated: https://github.com/premprasad1707/Ap-flood-detection-system**


2. **Run App**:
   ```
   streamlit run app.py
   ```
   Opens http://localhost:8501. Keep running.

3. **Capture Screenshots** (Browser full-page, ~1200x800px):
   | File | State |
   |------|-------|
   | `screenshots/dashboard.png` | Default Vijayawada load |
   | `screenshots/map_view.png` | Map with circles/canals |
   | `screenshots/ml_risk_low.png` | Low risk predict (rain=20, prev=10) |
   | `screenshots/ml_risk_high.png` | High risk (rain=250, prev=100) |
   | `screenshots/live_ml_dashboard.png` | Sliders + live predict |
   | `screenshots/ml_dashboard.png` | ML outputs (score/bar/alert) |
   | `screenshots/risk_report.png` | Chips + location/date |

   Save overwriting blanks. Use Chrome DevTools: F12 → Ctrl+Shift+P → "Capture full size screenshot".

4. **Test Model** (if needed):
   ```
   python utils/train_model.py
   ```

5. **Commit**:
   ```
   git add screenshots/ && git commit -m "Replace blanks with live screenshots" && git push
   ```

**Next**: Run steps 1-2 above. Take screenshots while app runs. Report back when done for verification/commit help.

