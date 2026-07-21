# 🎮 Augmented Wordle

A recreated and enhanced version of the popular [The New York Times Wordle](https://www.nytimes.com/games/wordle/index.html) game, built using the Pygame library. This project features multiple game modes, user account management, leaderboards, and game state saving.

This is the final project for the **Fundamentals of Programming for Artificial Intelligence** course for first-year Artificial Intelligence students at the University of Science, VNU-HCM (HCMUS), done from January to February 13, 2026.

---
## ⚠️ Warning

Source code is badly written and could cause you health problems from reading it. This is because I haven't learnt Object-Oriented Programming and source code is mostly self-written, with insignificant parts generated/suggested by LLM models.
---

## 🚀 Getting Started

The project requires the `pygame` library to render the graphical user interface.

**1. Install Pygame:**
Open your Terminal or Command Prompt (CMD) and run the following command:
`pip install pygame`

**2. Run the Game:**
Ensure you have all the provided files in the correct directory structure, then execute `main.py`:
`python Resources/main.py`

---

## ✨ Key Features

- 🔐 **Account System:** Register and log in to a personal account to track and save progress.
- 🌍 **Multiple Game Modes:** Play in English, Vietnamese, or solve Math equations.
- 💾 **Save & Resume:** Save your current game state and resume the latest unfinished round at any time.
- 🔄 **Undo & Redo:** Cancel the most recent input action (clearing the current row) or reapply it.
- ⏱️ **Timer & Leaderboard:** Tracks the time taken to complete a round. The Leaderboard ranks the top 10 players based on their average time per correct round across different modes.
- 📜 **Match History:** Review your 10 most recently completed games (win/loss status, time taken, date played, and all entered words).

---

## 🖥️ Game Scenes

- **Login Scene:** The initial screen where players register or log in using a Username and Password. Includes error handling for invalid credentials or unregistered accounts.
- **Start Scene:** The main hub containing navigation buttons: New Game, Resume, Leaderboard, History, and Log Out.
- **Game Scene:** The core gameplay area featuring a 6-row grid, a virtual keyboard, a timer, and a mode selection bar. 
- **Leaderboard Scene:** Displays top-ranking players for a selected game mode.
- **History Scene:** Shows a table of recent matches. Clicking on a specific match reveals the exact words guessed during that round.

---

## 📂 Project Structure

    ├── Videos/                  # Gameplay demonstration videos
    ├── README.md                # Project documentation
    └── Resources/               # Main source code and assets
        ├── font/                # Contains font files (Montserrat-Bold.ttf)
        ├── scenes/              # Scene management and individual screen modules
        │   ├── manager.py       # Manages and coordinates game scenes
        │   ├── login_scene.py   # Login UI and logic
        │   ├── start_scene.py   # Main menu UI
        │   ├── game_scene.py    # Core gameplay logic
        │   ├── history_scene.py # Match history UI
        │   └── leaderboard_scene.py # Leaderboard UI
        ├── words/               # Answer banks (eng.txt, vie.txt, math.txt)
        ├── background.jpg       # Game background image
        ├── components.py        # Core Wordle structures (Grid, WordleLine)
        ├── config.py            # Color codes and dimension constants
        ├── main.py              # Main execution script
        ├── ui.py                # UI components (Box, TextBox, Buttons)
        └── utils.py             # Global variables and utility functions

---

## 🎯 Future Roadmap

- **Vietnamese Mode Enhancements:** Expand the dictionary and implement support for displaying Vietnamese diacritics.
- **Daily Challenge:** Introduce a mechanic where players can only play one specific round per day.
- **Customization:** Allow players to adjust the required word length across all modes.
- **Time Attack Mode:** Players must guess words within a strict time limit, gaining bonus time for correct characters.
- **Hint System:** Provide clues regarding which characters are in the answer and their positions.
- **Action Limits:** Restrict the number of Undo/Redo actions allowed per round.
- **Advanced Saving:** Support multiple save slots and encrypt local save data (account info, match history, dictionaries) in binary format.
- **Web Deployment:** Host the game online for browser access.

---

## 📚 References & Resources

- **Libraries & Tools:** [Pygame Documentation](https://www.pygame.org/news).
- **Tutorials:** [Clear Code Pygame Tutorial](https://youtu.be/AY9MnQ4x3zk?si=MXFQRarlBa5sU2R7), [Pygame Text Input Box Guide (StackOverflow)](https://stackoverflow.com/questions/46390231/how-can-i-create-a-text-input-box-with-pygame/46390412#46390412).
- **UI/UX Design:** Start, Leaderboard, and History scene layouts were inspired by the menu design of *Grand Theft Auto: San Andreas*.
- **Data & Logic Inspirations:** 
  - Valid English words list: [dracos/dd0668f281e685bad51479e5acaadb93](https://gist.github.com/dracos/dd0668f281e685bad51479e5acaadb93).
  - Vietnamese dictionary: [winstonleedev/tudien](https://github.com/winstonleedev/tudien), [minhqnd/wordle](https://minhqnd.com/wordle).
  - Math mode logic: [Numberle](https://numberle.org/).
- **AI Assistance:** Various Gemini AI chats were utilized for generating the math answer bank, structuring save/resume logic, synchronizing the virtual keyboard, time tracking, and organizing the codebase.

---

## 🎓 Credits & Acknowledgments

This project would not have been possible without the guidance and support of many individuals. 

I would like to express my deepest gratitude to **Dr. Bùi Duy Đăng** and **Teaching Assistant MSc. Huỳnh Lâm Hải Đăng** for their dedicated teaching, timely assistance, and for providing specific instructions that helped shape this project throughout the semester. 

A special thanks to my classmates in the Artificial Intelligence major (Class 25TNT2) for sharing their ideas and serving as a great source of inspiration. Finally, thank you to all the open-source authors and developers whose tools and libraries made this project achievable.

**Author:** Trương Tiến Dương ([DepthSociety](https://github.com/DepthSociety)).