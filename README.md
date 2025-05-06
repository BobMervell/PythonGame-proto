# 🧩 PythonGame-proto

This is an old prototype of a simple **1v1 turn-based strategy game** developed in Python. Two players face off on a **7x11 grid**, each controlling a team of six unique characters. The objective is to **bring at least one of your units into the opponent’s end zone** while preventing your opponent from doing the same.

A tactical duel of movement, positioning, and resource management – lightweight in visuals, but rich in strategic depth.

![image](https://github.com/user-attachments/assets/586d362a-4447-4b10-a106-502e44b64fea)

---

If you want to try the game, be wary everything is in french.
To try, run the script "LeJeuV2",  very good name i know. 

---

## 🎮 Gameplay Overview

- **Grid-based battlefield**: 7 rows by 11 columns, resembling an extended chessboard.
- **Two players**, local only, compete with **teams of six characters**.
- **Minimalistic visuals**: Sprite-based display with a focus on core mechanics.
- Each unit type offers **distinct abilities**, encouraging team synergy and thoughtful planning.

---

## 🧙‍♂️ Character Abilities

Each team is composed of six units with **complementary capabilities**. Character types may include:

- Fast movement
- Healing allies
- Large HP pool
- Wall construction
- Wall destruction
- Long-range attacks
- Teleportation across obstacles

---

## 🔁 Turn Mechanics

- At the start of each turn, both players gain **1 action point** (referred to as a "move").
- Players may:
  - Spend their available action points to move, attack, heal, etc.
  - **Save** action points to use in later turns (they accumulate).
- Once both players have marked themselves as **ready**, the turn is executed **simultaneously**.

