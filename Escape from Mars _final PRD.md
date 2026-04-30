This is a high-octane sprint. With a **9:00 PM** hard deadline and a 75-minute window remaining, we need to strip away any non-essential complexity and focus on a "vertical slice" that is playable, visually striking, and scientifically grounded.

Here is the final, unified blueprint for **Escape from Mars**.

---

## **1\. Core Mission Objective**

Launch the Starship from the Jezero Crater before the **Trans-Earth Injection** window closes. You must manage your body's physical decay and the ship's fuel production through automated systems before you reach a lethal dose of radiation or become too weak to fly.

---

## **2\. Rapid-Fire Team Assignments**

### **Michael |**

Systems & UX Lead

* **The Sabatier Console:** Create the UI for the reactor to convert $CO\_2 \+ 4H\_2 \\rightarrow CH\_4 \+ 2H\_2O$.  
* **Mass-Management Inventory:** Implement the trade-off system where carrying scientific samples increases the fuel requirement for launch.  
* **The Biological Clock:** Code the ticking "Death Clock" for **Bone Density** and **Radiation Exposure**.  
  * *Learning Hook:* Bone density drops \~1% per month in low-G environments.

### **Evan |**

Mechanics & Physics Lead

* **38% Gravity Controller:** Set the gravity constant to $3.721 \\text{ m/s}^2$. Jumps should feel floaty and slow (2.6x higher than Earth).  
* **The Window Timer:** A global countdown to the launch window. If the timer hits zero before the fuel bar is full, the mission fails.  
* **Launch Logic:** Build the 3-stage ignition sequence: **Power $\\rightarrow$ Prime $\\rightarrow$ Launch**.

### **Roberto |**

Environment & Aesthetics Lead

* **The Martian Landscape:** Build the Jezero Crater using "Leopard Spot" rock textures and a Stainless Steel Starship model.  
* **Atmospheric Cues:** Implement the **Blue Sunset** (Rayleigh scattering) as the visual indicator that the window is closing.  
* **Audio:** Apply a "muffling" filter to all sounds to simulate the thin Martian atmosphere.

---

## **3\.**

Core Gameplay Loop (The "Must-Haves")

| Feature | Physics/Chemistry Basis | Gameplay Impact |
| :---- | :---- | :---- |
| **Sabatier Fueling** | In-Situ Resource Utilization (ISRU). | Player clicks "Process" to convert $H\_2$ and $CO\_2$ into Methane. |
| **Dust Maintenance** | Electrostatic dust buildup. | Solar power drops over time; player must "brush" panels to keep the factory powered. |
| **Low-G Movement** | $3.721 \\text{ m/s}^2$ gravity. | High jumps are possible, but fall damage triggers at greater heights. |
| **Payload Stress** | Tsiolkovsky Rocket Equation. | Every 1kg of "Science Samples" added to inventory increases the Methane requirement. |

---

## **4\. The 75-Minute "Crunch" Schedule**

| Time Window | Phase | Task |
| :---- | :---- | :---- |
| **7:45 \- 8:00** | **Foundation** | Michael sets up the GameState (Health, Fuel, Power). Evan implements the Gravity jump. Roberto places the ship model. |
| **8:00 \- 8:30** | **Integration** | Michael connects the Sabatier UI to the Fuel bar. Evan links the "Launch" button to the fuel requirement. Roberto adds the Blue Sunset. |
| **8:30 \- 8:50** | **The Merge** | Combine all scripts. Test the "Game Over" states (Radiation death vs. Missing the window). |
| **8:50 \- 9:00** | **Deployment** | Final build export. No new code. Check the HUD text for clarity. |

---

## **5\. Technical Constants**

* **Gravity:** $3.721 \\text{ m/s}^2$.  
* **Fuel Chemistry:** $CO\_2 \+ 4H\_2 \\rightarrow CH\_4 \+ 2H\_2O$.  
* **Delta-v Goal:** $\\Delta v \= v\_e \\ln \\frac{m\_0}{m\_f}$.

**Let’s get to work. Michael, do you want me to generate the logic for the Sabatier UI conversion or the Bio-Decay timer first to get your code block started?**

