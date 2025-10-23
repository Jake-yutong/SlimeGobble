"""
SlimeGobble - 游戏入口文件
启动并运行游戏
"""

import asyncio
from game import Game


async def main():
    """主函数 - 异步版本用于Web部署"""
    print("=" * 50)
    print("欢迎来到 SlimeGobble!")
    print("=" * 50)
    print("\n控制说明:")
    print("  W - 向上移动")
    print("  A - 向左移动")
    print("  S - 向下移动")
    print("  D - 向右移动")
    print("  P - 暂停/继续")
    print("  ESC - 返回主菜单")
    print("\n游戏目标:")
    print("  收集金币达到500分即可进入下一关卡！")
    print("=" * 50)
    print()
    
    # 创建游戏实例
    game = Game()
    
    # 异步运行游戏循环
    await game.run_async()
    
    print("\n感谢游玩 SlimeGobble!")


# Pygbag 需要在顶层调用
asyncio.run(main())
