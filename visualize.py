"""
SlimeGobble - 游戏元素可视化演示
快速展示游戏的所有核心元素和状态
"""

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame
from config import *


def visualize_level_map(level_index):
    """可视化展示关卡地图"""
    print(f"\n{'='*50}")
    print(f"关卡 {level_index + 1} 地图")
    print(f"{'='*50}")
    
    level_map = LEVELS[level_index]
    
    # 统计信息
    stats = {
        'W': 0, '.': 0, 'O': 0, 'P': 0, 'E': 0, ' ': 0
    }
    
    for row in level_map:
        for cell in row:
            stats[cell] = stats.get(cell, 0) + 1
    
    print(f"\n地图尺寸: {len(level_map[0])}x{len(level_map)}")
    print(f"\n元素统计:")
    print(f"  墙壁 (W):      {stats['W']}")
    print(f"  金币 (.):      {stats['.']}")
    print(f"  大金币 (O):    {stats['O']}")
    print(f"  玩家出生点 (P): {stats['P']}")
    print(f"  敌人出生点 (E): {stats['E']}")
    print(f"  空地 ( ):      {stats[' ']}")
    
    max_score = stats['.'] * COIN_SCORE + stats['O'] * BIG_COIN_SCORE
    print(f"\n最大可能得分: {max_score}")
    print(f"升级所需分数: {LEVEL_UP_SCORE}")
    print(f"得分余量: {max_score - LEVEL_UP_SCORE}")
    
    # ASCII可视化
    print(f"\nASCII地图预览:")
    print("┌" + "─" * len(level_map[0]) + "┐")
    for row in level_map:
        print("│" + "".join(row) + "│")
    print("└" + "─" * len(level_map[0]) + "┘")


def visualize_game_states():
    """展示游戏状态"""
    print(f"\n{'='*50}")
    print("游戏状态系统")
    print(f"{'='*50}")
    
    states = [
        (MAIN_MENU, "主菜单", "显示标题和开始按钮"),
        (PLAYING, "游戏中", "玩家控制角色收集金币"),
        (PAUSED, "暂停", "游戏暂停，按P继续"),
        (LEVEL_COMPLETE, "关卡完成", "达到500分，准备进入下一关"),
        (GAME_OVER, "游戏结束", "生命耗尽（Phase 2）"),
        (VICTORY, "最终胜利", "完成所有关卡（Phase 2）")
    ]
    
    print("\n状态列表:")
    for state, name, desc in states:
        status = "✅" if state in [MAIN_MENU, PLAYING, PAUSED, LEVEL_COMPLETE] else "🚧"
        print(f"  {status} {state:20s} - {name:10s} : {desc}")


def visualize_controls():
    """展示控制方案"""
    print(f"\n{'='*50}")
    print("控制系统")
    print(f"{'='*50}")
    
    controls = [
        ("W", "向上移动", "✅"),
        ("A", "向左移动", "✅"),
        ("S", "向下移动", "✅"),
        ("D", "向右移动", "✅"),
        ("P", "暂停/继续", "✅"),
        ("ESC", "返回主菜单", "✅"),
        ("鼠标", "点击按钮", "✅")
    ]
    
    print("\n按键映射:")
    for key, action, status in controls:
        print(f"  {status} {key:6s} → {action}")


def visualize_scoring():
    """展示得分系统"""
    print(f"\n{'='*50}")
    print("得分系统")
    print(f"{'='*50}")
    
    print(f"\n得分规则:")
    print(f"  小金币 (.): +{COIN_SCORE:3d} 分")
    print(f"  大金币 (O): +{BIG_COIN_SCORE:3d} 分")
    print(f"\n升级要求:")
    print(f"  所需分数: {LEVEL_UP_SCORE} 分")
    
    print(f"\n示例得分计算:")
    examples = [
        (10, 1, "10×10 + 1×50 = 150分"),
        (25, 2, "25×10 + 2×50 = 350分"),
        (40, 3, "40×10 + 3×50 = 550分 → 升级！")
    ]
    for coins, big_coins, calc in examples:
        print(f"  {coins}金币 + {big_coins}大金币 = {calc}")


def visualize_player_speed():
    """展示速度系统"""
    print(f"\n{'='*50}")
    print("速度系统")
    print(f"{'='*50}")
    
    print(f"\n移动速度（像素/帧 @ 60 FPS）:")
    print(f"  玩家:          {PLAYER_SPEED:.1f} px/frame")
    print(f"  敌人 (关卡1): {ENEMY_SPEED_LEVEL1:.1f} px/frame (随机AI)")
    print(f"  敌人 (关卡2): {ENEMY_SPEED_LEVEL2:.1f} px/frame (追踪AI)")
    print(f"  敌人 (关卡3): {ENEMY_SPEED_LEVEL3:.1f} px/frame (快速追踪)")
    
    print(f"\n速度对比:")
    print(f"  玩家 vs 关卡1敌人: {PLAYER_SPEED / ENEMY_SPEED_LEVEL1:.1f}x 更快")
    print(f"  玩家 vs 关卡2敌人: {PLAYER_SPEED / ENEMY_SPEED_LEVEL2:.1f}x 更快")
    print(f"  玩家 vs 关卡3敌人: {PLAYER_SPEED / ENEMY_SPEED_LEVEL3:.1f}x 更快")


def visualize_project_structure():
    """展示项目结构"""
    print(f"\n{'='*50}")
    print("项目结构")
    print(f"{'='*50}")
    
    structure = """
SlimeGobble/
├── 📄 main.py              - 游戏入口
├── 🎮 game.py              - Game类（主逻辑）
├── 👾 player.py            - Player类（角色控制）
├── ⚙️  config.py            - 配置和地图
├── 🧪 test_phase1.py       - 自动化测试
├── 🚀 run.sh               - 快速启动脚本
├── 📚 README.md            - 项目说明
├── 📋 DEVELOPMENT.md       - 开发文档
├── 📊 PHASE1_SUMMARY.md    - 第一阶段总结
├── 📖 QUICKREF.md          - 快速参考
└── 🐍 venv/                - Python虚拟环境
    """
    print(structure)


def main():
    """主函数"""
    print("╔" + "═" * 50 + "╗")
    print("║" + " " * 10 + "SlimeGobble - 游戏元素演示" + " " * 10 + "║")
    print("╚" + "═" * 50 + "╝")
    
    # 展示各个系统
    visualize_game_states()
    visualize_controls()
    visualize_scoring()
    visualize_player_speed()
    
    # 展示所有关卡
    for i in range(len(LEVELS)):
        visualize_level_map(i)
    
    # 展示项目结构
    visualize_project_structure()
    
    # 总结
    print(f"\n{'='*50}")
    print("第一阶段实现总结")
    print(f"{'='*50}")
    print("\n✅ 已完成:")
    print("  • 游戏框架（主循环、事件处理）")
    print("  • Player类（移动、动画、碰撞）")
    print("  • 3个关卡地图设计")
    print("  • 金币收集系统")
    print("  • 得分和HUD显示")
    print("  • 主菜单和状态管理")
    print("\n🚧 下一阶段:")
    print("  • Enemy类和AI系统")
    print("  • 生命系统和碰撞")
    print("  • 完整游戏流程")
    print("  • 音效和BGM")
    
    print(f"\n{'='*50}")
    print("运行 'python main.py' 开始游戏！")
    print(f"{'='*50}\n")


if __name__ == "__main__":
    main()
