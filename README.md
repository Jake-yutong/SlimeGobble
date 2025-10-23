# SlimeGobble 🎮

SlimeGobble is a Pac-Man-like game with three independent levels. Players need to control the cute slime "Mumu" to get higher scores. Please be careful of the evil "chaser"!

## 🌐 Play Online

**🎮 [Play in Browser](https://jake-yutong.github.io/SlimeGobble/)** *(Coming soon)*

Or run locally on your computer (see below).

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Virtual environment (venv)

### Installation & Run

```bash
# 1. Activate virtual environment
source venv/bin/activate

# 2. Install dependencies (if not already installed)
pip install pygame numpy

# 3. Run the game
python main.py

# Or use the quick start script
./run.sh
```

### 🌐 Deploy to Web

Want to share your game online? See:
- **[Quick Deploy Guide](QUICK_DEPLOY.md)** - 5 minute setup
- **[Full Deployment Guide](WEB_DEPLOYMENT.md)** - Detailed instructions

## 🎯 Controls

| Key | Action |
|-----|--------|
| W | Move Up |
| A | Move Left |
| S | Move Down |
| D | Move Right |
| P | Pause/Resume |
| ESC | Return to Main Menu |

## 🎮 Gameplay

- **Objective**: Collect coins to reach 500 points per level
- **Small Coin**: 10 points
- **Big Coin**: 50 points
- **Levels**: 3 levels with increasing difficulty
- **Lives**: 3 lives (to be implemented in Phase 2)

## 📁 Project Structure

```
SlimeGobble/
├── main.py              # Game entry point
├── game.py              # Game class - main logic
├── player.py            # Player class - character control
├── config.py            # Configuration and level maps
├── test_phase1.py       # Automated tests
├── run.sh               # Quick start script
├── PHASE1_SUMMARY.md    # Phase 1 delivery summary
├── DEVELOPMENT.md       # Development documentation
└── venv/                # Virtual environment
```

## 🧪 Testing

Run automated tests to verify the implementation:

```bash
python test_phase1.py
```

## 📋 Development Status

**Phase 1** ✅ Complete
- Game framework with main loop
- Player class with movement and animation
- Level 1 fully playable
- Coin collection system
- HUD display
- Main menu

**Phase 2** 🚧 Coming Next
- Enemy class with AI
- Life system
- Complete 3-level progression
- Sound effects and music
- Game over and victory screens

## 📚 Documentation

- [Phase 1 Summary](PHASE1_SUMMARY.md) - Detailed delivery report
- [Development Guide](DEVELOPMENT.md) - Technical documentation

## 🎨 Assets

The game uses placeholder graphics currently. To use custom assets, place them in an `assets/` folder and update `ASSETS_PATH` in `config.py`.

## 📝 License

This is a demo project for educational purposes.
