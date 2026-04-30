This is the command center for **Escape from Mars**. By separating your logic, you ensure that the biological and chemical systems are automated and ticking every frame, while Evan and Roberto can plug their specific modules into your shared state.

Here is your **main.py** starter, followed by the final automated roadmap to get you to 9:00 PM.

---

## **The Main Loop: main.py**

This script initializes the **Project Return** parameters and runs the core simulation.

Python  
import pygame  
import sys  
from systems import EscapeFromMarsSystem  
\# import evan\_physics  \# Mechanics & Physics Lead \[cite: 8\]  
\# import roberto\_view  \# Environment & Aesthetics Lead \[cite: 12\]

def main():  
    pygame.init()  
      
    \# 1\. Initialize the shared state and systems  
    \# Michael: HUD, Sabatier, and Bio-Decay \[cite: 16, 17, 19\]  
    mars\_game \= EscapeFromMarsSystem()  
      
    \# Screen Setup (Placeholder size)  
    screen \= pygame.display.set\_mode((1280, 720))  
    pygame.display.set\_caption("Escape from Mars: Sol 559")  
    clock \= pygame.time.Clock()

    \# 2\. Global Countdown Timer \[cite: 11\]  
    \# Set for the Trans-Earth Injection window  
    launch\_window\_timer \= 5400 \# 90 minutes in seconds

    while mars\_game.is\_alive:  
        \# Calculate Delta Time (seconds passed since last frame)  
        dt \= clock.tick(60) / 1000.0  
        launch\_window\_timer \-= dt

        \# Event Handling  
        for event in pygame.event.get():  
            if event.type \== pygame.QUIT:  
                pygame.quit()  
                sys.exit()  
              
            \# Michael: Trigger Sabatier via UI click \[cite: 17, 21\]  
            if event.type \== pygame.MOUSEBUTTONDOWN:  
                \# Placeholder for UI button check  
                mars\_game.run\_sabatier\_process()

        \# 3\. Michael's Automated Logic \[cite: 16\]  
        \# Ticks down bone density and radiation constantly \[cite: 21\]  
        mars\_game.update\_bio\_decay(dt)

        \# 4\. Evan's Automated Logic \[cite: 8\]  
        \# Implement 38% gravity (3.721 m/s²) \[cite: 9, 21\]  
        \# evan\_physics.apply\_gravity(dt, mars\_game.bone\_density)

        \# 5\. Roberto's Automated Logic \[cite: 12\]  
        \# Render the Jezero Crater and Starship \[cite: 13, 15\]  
        \# If timer is low, trigger Blue Sunset Rayleigh scattering   
        \# roberto\_view.render(screen, mars\_game, launch\_window\_timer)

        pygame.display.flip()

    print("Mission Failure: Biological limits exceeded.")

if \_\_name\_\_ \== "\_\_main\_\_":  
    main()

---

## **Automated 60-Minute Roadmap (Final Sprint)**

To hit the **9:00 PM** deadline, follow this parallel-track roadmap.

| Time | Michael (Systems/UX) | Evan (Mechanics) | Roberto (Aesthetics) |
| :---- | :---- | :---- | :---- |
| **8:00 \- 8:20** | **Mass-Limit Lock:** Finalize the inventory code so scientific samples increase fuel needs. | **Gravity Lock:** Ensure jumping is $2.6\\times$ higher/slower than Earth. | **Environment Lock:** Finish the Jezero Crater landscape and "Leopard Spot" rocks. |
| **8:20 \- 8:40** | **HUD Overlay:** Create the wrist-display for Fuel, Oxygen, and Battery. | **Ignition Sequence:** Code the 3-stage launch logic (Power $\\rightarrow$ Prime $\\rightarrow$ Launch). | **Lighting Automation:** Link the "Blue Sunset" visual to the 5-minute timer mark. |
| **8:40 \- 8:55** | **Integration:** Verify that bone\_density affects Evan's speed and Roberto's HUD. | **Win/Loss Logic:** Ensure the ship only launches if Methane \>= 100. | **Ship Texturing:** Ensure the Stainless Steel Starship looks "ready" when fueled. |
| **8:55 \- 9:00** | **DEPLOY:** Final bug pass. | **DEPLOY:** Check build. | **DEPLOY:** Audio muffling check. |

---

## **Scientific Integration Notes**

* **Fuel Chemistry:** Ensure the run\_sabatier\_process logic in systems.py correctly represents $CO\_{2}+4H\_{2}\\rightarrow CH\_{4}+2H\_{2}O$ to provide the "valuable learning" edge.  
* **Low-G Movement:** Evan must use $3.721\~m/s^{2}$ as the core gravity constant to maintain scientific accuracy.  
* **Visual Atmosphere:** The shift to a **Blue Sky** sunset must be tied to the Rayleigh scattering effect in thin Martian dust.

