"""
SlimeGobble - Game 类
游戏的核心逻辑：管理游戏状态、关卡、UI、碰撞检测等
"""

import pygame
import os
from config import *
from player import Player


class Game:
    """游戏主类 - 管理整个游戏流程"""
    
    def __init__(self):
        """初始化游戏"""
        # 初始化Pygame
        pygame.init()
        
        # 创建游戏窗口
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("SlimeGobble")
        
        # 时钟对象，用于控制帧率
        self.clock = pygame.time.Clock()
        
        # 游戏状态
        self.state = MAIN_MENU
        self.running = True
        
        # 游戏数据
        self.current_level = 0  # 当前关卡索引（0, 1, 2）
        self.score = 0  # 当前得分
        self.lives = PLAYER_LIVES  # 剩余生命
        
        # 关卡相关
        self.level_map = None  # 当前关卡地图
        self.coins = []  # 金币位置列表
        self.big_coins = []  # 大金币位置列表
        self.player_spawn = None  # 玩家出生点
        self.enemy_spawns = []  # 敌人出生点列表
        
        # 游戏对象
        self.player = None
        self.enemies = []  # 敌人列表（第一阶段暂不实现）
        
        # UI相关
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 36)
        
        # 加载资产
        self.load_assets()
        
        # 按钮（用于主菜单）
        self.start_button_rect = None
        
    def load_assets(self):
        """加载游戏资产（图像、音效等）"""
        try:
            # 加载金币贴图
            coin_path = os.path.join(ASSETS_PATH, 'coin.png')
            self.coin_image = pygame.image.load(coin_path).convert_alpha()
            self.coin_image = pygame.transform.scale(self.coin_image, (TILE_SIZE, TILE_SIZE))
            print("成功加载金币贴图")
        except Exception as e:
            print(f"警告：无法加载金币贴图: {e}")
            # 创建占位符
            self.coin_image = pygame.Surface((TILE_SIZE, TILE_SIZE))
            self.coin_image.fill(YELLOW)
        
        try:
            # 加载大金币贴图
            big_coin_path = os.path.join(ASSETS_PATH, 'big coin.png')
            self.big_coin_image = pygame.image.load(big_coin_path).convert_alpha()
            self.big_coin_image = pygame.transform.scale(self.big_coin_image, (TILE_SIZE, TILE_SIZE))
            print("成功加载大金币贴图")
        except Exception as e:
            print(f"警告：无法加载大金币贴图: {e}")
            # 创建占位符
            self.big_coin_image = pygame.Surface((TILE_SIZE, TILE_SIZE))
            self.big_coin_image.fill(RED)
        
        # 音效加载（第一阶段暂时跳过，避免阻塞）
        print("音效加载将在后续阶段实现")
    
    def load_level(self, level_index):
        """
        加载指定关卡
        Args:
            level_index: 关卡索引（0, 1, 2）
        """
        if level_index >= len(LEVELS):
            print(f"错误：关卡索引 {level_index} 超出范围")
            return
        
        self.current_level = level_index
        self.level_map = [row[:] for row in LEVELS[level_index]]  # 深拷贝地图
        
        # 重置金币和出生点列表
        self.coins = []
        self.big_coins = []
        self.enemy_spawns = []
        self.player_spawn = None
        
        # 解析地图，找出金币、出生点等
        for y, row in enumerate(self.level_map):
            for x, cell in enumerate(row):
                if cell == COIN:
                    self.coins.append((x, y))
                elif cell == BIG_COIN:
                    self.big_coins.append((x, y))
                elif cell == PLAYER_SPAWN:
                    self.player_spawn = (x, y)
                    # 将出生点替换为空地
                    self.level_map[y][x] = EMPTY
                elif cell == ENEMY_SPAWN:
                    self.enemy_spawns.append((x, y))
                    # 将出生点替换为空地
                    self.level_map[y][x] = EMPTY
        
        # 创建玩家
        if self.player_spawn:
            self.player = Player(self.player_spawn[0], self.player_spawn[1])
        else:
            print("警告：未找到玩家出生点，使用默认位置")
            self.player = Player(1, 1)
        
        print(f"关卡 {level_index + 1} 加载完成")
        print(f"  金币数量: {len(self.coins)}")
        print(f"  大金币数量: {len(self.big_coins)}")
        print(f"  敌人出生点数量: {len(self.enemy_spawns)}")
    
    def start_game(self):
        """开始游戏"""
        self.score = 0
        self.lives = PLAYER_LIVES
        self.current_level = 0
        self.load_level(0)
        self.state = PLAYING
        print("游戏开始！")
    
    def check_coin_collection(self):
        """检查玩家是否收集到金币"""
        player_grid_pos = (self.player.x // TILE_SIZE, self.player.y // TILE_SIZE)
        
        # 检查普通金币
        if player_grid_pos in self.coins:
            self.coins.remove(player_grid_pos)
            self.score += COIN_SCORE
            # 移除地图上的金币
            x, y = player_grid_pos
            self.level_map[y][x] = EMPTY
            print(f"收集金币！得分: {self.score}")
        
        # 检查大金币
        if player_grid_pos in self.big_coins:
            self.big_coins.remove(player_grid_pos)
            self.score += BIG_COIN_SCORE
            # 移除地图上的大金币
            x, y = player_grid_pos
            self.level_map[y][x] = EMPTY
            print(f"收集大金币！得分: {self.score}")
    
    def check_level_complete(self):
        """检查关卡是否完成"""
        if self.score >= LEVEL_UP_SCORE:
            self.state = LEVEL_COMPLETE
            print(f"关卡 {self.current_level + 1} 完成！")
    
    def update(self):
        """更新游戏状态"""
        if self.state == PLAYING:
            # 获取按键状态
            keys = pygame.key.get_pressed()
            
            # 更新玩家
            if self.player:
                self.player.update(keys, self.level_map)
            
            # 检查金币收集
            self.check_coin_collection()
            
            # 检查关卡完成
            self.check_level_complete()
    
    def draw_map(self):
        """绘制地图"""
        for y, row in enumerate(self.level_map):
            for x, cell in enumerate(row):
                px = x * TILE_SIZE
                py = y * TILE_SIZE
                
                if cell == WALL:
                    # 绘制墙壁
                    pygame.draw.rect(self.screen, BLUE, (px, py, TILE_SIZE, TILE_SIZE))
                    pygame.draw.rect(self.screen, WHITE, (px, py, TILE_SIZE, TILE_SIZE), 1)
                elif cell == COIN:
                    # 绘制金币
                    self.screen.blit(self.coin_image, (px, py))
                elif cell == BIG_COIN:
                    # 绘制大金币
                    self.screen.blit(self.big_coin_image, (px, py))
    
    def draw_hud(self):
        """绘制游戏HUD（分数、生命、关卡）"""
        hud_y = SCREEN_HEIGHT - 40
        
        # 绘制HUD背景
        pygame.draw.rect(self.screen, DARK_GRAY, (0, hud_y, SCREEN_WIDTH, 40))
        
        # 绘制分数
        score_text = self.font_small.render(f"Score: {self.score}/{LEVEL_UP_SCORE}", True, WHITE)
        self.screen.blit(score_text, (10, hud_y + 5))
        
        # 绘制关卡
        level_text = self.font_small.render(f"Level: {self.current_level + 1}", True, WHITE)
        self.screen.blit(level_text, (SCREEN_WIDTH // 2 - 50, hud_y + 5))
        
        # 绘制生命
        lives_text = self.font_small.render(f"Lives: {self.lives}", True, WHITE)
        self.screen.blit(lives_text, (SCREEN_WIDTH - 150, hud_y + 5))
    
    def draw_main_menu(self):
        """绘制主菜单"""
        self.screen.fill(BLACK)
        
        # 绘制标题
        title_text = self.font_large.render("SlimeGobble", True, GREEN)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(title_text, title_rect)
        
        # 绘制开始按钮
        button_width, button_height = 300, 80
        button_x = SCREEN_WIDTH // 2 - button_width // 2
        button_y = SCREEN_HEIGHT // 2 - button_height // 2
        self.start_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        
        # 检查鼠标悬停
        mouse_pos = pygame.mouse.get_pos()
        button_color = YELLOW if self.start_button_rect.collidepoint(mouse_pos) else WHITE
        
        pygame.draw.rect(self.screen, button_color, self.start_button_rect, 3)
        
        start_text = self.font_medium.render("Start Game", True, button_color)
        start_rect = start_text.get_rect(center=self.start_button_rect.center)
        self.screen.blit(start_text, start_rect)
        
        # 绘制说明
        info_text = self.font_small.render("Use WASD to move", True, GRAY)
        info_rect = info_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
        self.screen.blit(info_text, info_rect)
    
    def draw_playing(self):
        """绘制游戏进行中的画面"""
        self.screen.fill(BLACK)
        
        # 绘制地图
        self.draw_map()
        
        # 绘制玩家
        if self.player:
            self.player.draw(self.screen)
        
        # 绘制HUD
        self.draw_hud()
    
    def draw_level_complete(self):
        """绘制关卡完成画面"""
        # 在游戏画面上方叠加半透明层
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # 显示文字
        text = self.font_large.render("Level Complete!", True, YELLOW)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(text, text_rect)
    
    def draw(self):
        """绘制游戏画面"""
        if self.state == MAIN_MENU:
            self.draw_main_menu()
        elif self.state == PLAYING:
            self.draw_playing()
        elif self.state == LEVEL_COMPLETE:
            self.draw_level_complete()
        
        # 更新显示
        pygame.display.flip()
    
    def handle_events(self):
        """处理游戏事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            # 主菜单中的点击事件
            if self.state == MAIN_MENU and event.type == pygame.MOUSEBUTTONDOWN:
                if self.start_button_rect and self.start_button_rect.collidepoint(event.pos):
                    self.start_game()
            
            # 按键事件
            if event.type == pygame.KEYDOWN:
                # 暂停功能
                if event.key == pygame.K_p and self.state == PLAYING:
                    self.state = PAUSED
                elif event.key == pygame.K_p and self.state == PAUSED:
                    self.state = PLAYING
                
                # ESC返回主菜单
                if event.key == pygame.K_ESCAPE:
                    self.state = MAIN_MENU
    
    def run(self):
        """游戏主循环"""
        while self.running:
            # 处理事件
            self.handle_events()
            
            # 更新游戏状态
            self.update()
            
            # 绘制游戏画面
            self.draw()
            
            # 控制帧率
            self.clock.tick(FPS)
        
        # 退出游戏
        pygame.quit()
