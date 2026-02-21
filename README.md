# 🏎️ F1 ELO & ML Prediction Project (2025-2026)

This repository contains a specialized Machine Learning and ELO-based pipeline to predict Formula 1 race outcomes. Unlike standard models, this project uses a custom logic that isolates raw driver speed from mechanical race variables.

## 🚀 Key Features

* **ML Model (`prediction1.py` / `prediction2.py`):** Uses Gradient Boosting to forecast lap times based on 2024/2025 FastF1 data.
* **ELO Engine (`Predictor-2026-ELO.py`):** A custom-coded ranking system designed for the 2026 season.

---

## 📊 Custom ELO Logic

The model ranks drivers using a "Fair Speed" approach. It follows a strict 3-phase calculation:

### 1. The "Pure Speed" Phase (Practice & Sorting)
In this phase, ELO is calculated strictly from **Practice** and **Qualifying (Sorting)** sessions. This represents the driver's raw capability without pit crew influence.
$$Speed\_ELO = \frac{Avg\_Practice\_Pos + Avg\_Quali\_Pos}{2}$$

### 2. The "Real Race" Phase (Pit Isolation)
Pit stop data is **isolated**. It is only added to the final race potential, ensuring a slow pit stop doesn't "pollute" the driver's qualifying rank.
$$Race\_Score = Avg\_Race\_Pos + (Pit\_Reaction\_Factor)$$

### 3. Experience Multiplier
The model rewards career longevity. Drivers receive a bonus based on the year they started playing in F1:
* **Veteran Bonus:** +10 points per year of experience (e.g., Alonso 2001 vs. Rookies 2026).

---

## 🔧 Installation & Usage

1. **Clone the repo:**
   ```bash
   git clone [https://github.com/yishaksisay/f1-ml-project.git](https://github.com/yishaksisay/f1-ml-project.git)
