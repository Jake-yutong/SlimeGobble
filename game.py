"""
SlimeGobble - Game 类
游戏的核心逻辑：管理游戏状态、关卡、UI、碰撞检测等
"""

import pygame
import os
from config import *
from player import Player
from enemy import Enemy


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
        self.enemies = []  # 敌人列表
        
        # UI相关
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 36)
        
        # 加载资产
        self.load_assets()
        
        # 音效
        self.sounds = {}
        self.load_sounds()
        
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
        
    def load_sounds(self):
        """加载音效"""
        # 初始化mixer
        try:
            pygame.mixer.init()
        except:
            print("警告：无法初始化音效系统")
            return
        
        # 音效文件列表
        sound_files = {
            'coin': 'big coin.wav',  # 收集大金币音效
            'bgm': 'bgm.wav',        # 背景音乐
            'win': 'win.wav',        # 胜利音效
            'tap': 'tap.wav',        # UI点击音效
            'lose': 'lose.wav'       # 失败音效
        }
        
        for name, filename in sound_files.items():
            try:
                sound_path = os.path.join(ASSETS_PATH, filename)
                if name == 'bgm':
                    # 背景音乐使用music模块
                    pygame.mixer.music.load(sound_path)
                    print(f"成功加载背景音乐: {filename}")
                else:
                    # 音效使用Sound对象
                    self.sounds[name] = pygame.mixer.Sound(sound_path)
                    print(f"成功加载音效: {filename}")
            except Exception as e:
                print(f"警告：无法加载音效 {filename}: {e}")
    
    def play_sound(self, sound_name):
        """播放音效"""
        if sound_name in self.sounds:
            self.sounds[sound_name].play()
    
    def play_bgm(self):
        """播放背景音乐（循环）"""
        try:
            pygame.mixer.music.play(-1)  # -1表示无限循环
        except:
            pass
    
    def stop_bgm(self):
        """停止背景音乐"""
        try:
            pygame.mixer.music.stop()
        except:
            pass
    
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
        
        # 创建敌人
        self.enemies = []
        # 根据关卡确定AI模式和速度
        if level_index == 0:
            # 关卡1: 1个敌人, 随机移动
            ai_mode = 'random'
            speed = ENEMY_SPEED_LEVEL1
            num_enemies = min(1, len(self.enemy_spawns))  # 只使用第一个敌人出生点
        elif level_index == 1:
            # 关卡2: 2个敌人, 追逐模式
            ai_mode = 'chase'
            speed = ENEMY_SPEED_LEVEL2
            num_enemies = min(2, len(self.enemy_spawns))  # 使用前2个敌人出生点
        else:
            # 关卡3: 3个敌人, 快速追逐模式
            ai_mode = 'fast_chase'
            speed = ENEMY_SPEED_LEVEL3
            num_enemies = len(self.enemy_spawns)  # 使用所有敌人出生点
        
        # 创建指定数量的敌人
        for i in range(num_enemies):
            if i < len(self.enemy_spawns):
                spawn_x, spawn_y = self.enemy_spawns[i]
                enemy = Enemy(spawn_x, spawn_y, ai_mode, speed)
                self.enemies.append(enemy)
        
        print(f"\n=== 关卡 {level_index + 1} 加载完成 ===")
        print(f"  金币数量: {len(self.coins)}")
        print(f"  大金币数量: {len(self.big_coins)}")
        print(f"  敌人出生点总数: {len(self.enemy_spawns)}")
        print(f"  实际创建敌人数: {len(self.enemies)}")
        print(f"  敌人AI模式: {ai_mode}")
        print(f"  敌人速度: {speed}")
        print(f"=============================\n")
    
    def start_game(self):
        """开始游戏"""
        self.score = 0
        self.lives = PLAYER_LIVES
        self.current_level = 0
        self.load_level(0)
        self.state = PLAYING
        self.play_bgm()  # 开始播放背景音乐
        print("游戏开始！")
    
    def check_coin_collection(self):
        """检查玩家是否收集到金币"""
        # 使用玩家中心点来判定，更精确
        player_center_x = (self.player.x + TILE_SIZE // 2) // TILE_SIZE
        player_center_y = (self.player.y + TILE_SIZE // 2) // TILE_SIZE
        player_grid_pos = (player_center_x, player_center_y)
        
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
            self.play_sound('coin')  # 播放金币音效
            print(f"收集大金币！得分: {self.score}")
    
    def check_level_complete(self):
        """检查关卡是否完成（达到500分）"""
        if self.score >= LEVEL_UP_SCORE:
            self.state = LEVEL_COMPLETE
            self.play_sound('win')  # 播放胜利音效
            print(f"关卡 {self.current_level + 1} 完成！得分: {self.score}")
    
    def check_enemy_collision(self):
        """检查玩家与敌人的碰撞"""
        for enemy in self.enemies:
            if enemy.check_collision_with_player(self.player):
                # 玩家被敌人碰到
                self.lives -= 1
                print(f"被敌人碰到！剩余生命: {self.lives}")
                
                if self.lives <= 0:
                    # 游戏结束
                    self.state = GAME_OVER
                    self.stop_bgm()
                    self.play_sound('lose')
                    print("游戏结束！")
                else:
                    # 重置玩家和敌人位置
                    if self.player_spawn:
                        self.player.reset_position(self.player_spawn[0], self.player_spawn[1])
                    for enemy in self.enemies:
                        enemy.reset_position()
                
                break  # 一次只处理一个碰撞
    
    def update(self):
        """更新游戏状态"""
        if self.state == PLAYING:
            # 获取按键状态
            keys = pygame.key.get_pressed()
            
            # 更新玩家
            if self.player:
                self.player.update(keys, self.level_map)
            
            # 更新敌人
            for enemy in self.enemies:
                enemy.update(self.player, self.level_map)
            
            # 检查金币收集
            self.check_coin_collection()
            
            # 检查敌人碰撞
            self.check_enemy_collision()
            
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
        
        # 绘制标题（浅蓝色）
        title_text = self.font_large.render("SlimeGobble", True, LIGHT_BLUE)
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
        
        # 绘制敌人
        for enemy in self.enemies:
            enemy.draw(self.screen)
        
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
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(text, text_rect)
        
        # 显示提示
        if self.current_level < len(LEVELS) - 1:
            hint_text = self.font_small.render("Press SPACE to continue", True, WHITE)
        else:
            hint_text = self.font_small.render("Press SPACE for final level!", True, WHITE)
        hint_rect = hint_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        self.screen.blit(hint_text, hint_rect)
    
    def draw_game_over(self):
        """绘制游戏结束画面"""
        self.screen.fill(BLACK)
        
        # 显示Game Over
        title_text = self.font_large.render("GAME OVER", True, RED)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(title_text, title_rect)
        
        # 显示最终分数
        score_text = self.font_medium.render(f"Final Score: {self.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 250))
        self.screen.blit(score_text, score_rect)
        
        # 显示提示
        hint_text = self.font_small.render("Press R to Restart or ESC for Menu", True, GRAY)
        hint_rect = hint_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
        self.screen.blit(hint_text, hint_rect)
    
    def draw_victory(self):
        """绘制胜利画面"""
        self.screen.fill(BLACK)
        
        # 显示Victory
        title_text = self.font_large.render("VICTORY!", True, YELLOW)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(title_text, title_rect)
        
        # 显示最终分数
        score_text = self.font_medium.render(f"Final Score: {self.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 250))
        self.screen.blit(score_text, score_rect)
        
        # 显示祝贺
        congrats_text = self.font_small.render("Congratulations! You completed all levels!", True, GREEN)
        congrats_rect = congrats_text.get_rect(center=(SCREEN_WIDTH // 2, 350))
        self.screen.blit(congrats_text, congrats_rect)
        
        # 显示提示
        hint_text = self.font_small.render("Press R to Play Again or ESC for Menu", True, GRAY)
        hint_rect = hint_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
        self.screen.blit(hint_text, hint_rect)
    
    def draw(self):
        """绘制游戏画面"""
        if self.state == MAIN_MENU:
            self.draw_main_menu()
        elif self.state == PLAYING:
            self.draw_playing()
        elif self.state == LEVEL_COMPLETE:
            self.draw_level_complete()
        elif self.state == GAME_OVER:
            self.draw_game_over()
        elif self.state == VICTORY:
            self.draw_victory()
        
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
                    self.play_sound('tap')  # 播放点击音效
                    self.start_game()
            
            # 按键事件
            if event.type == pygame.KEYDOWN:
                # 暂停功能
                if event.key == pygame.K_p and self.state == PLAYING:
                    self.state = PAUSED
                elif event.key == pygame.K_p and self.state == PAUSED:
                    self.state = PLAYING
                
                # 关卡完成后按空格继续
                if event.key == pygame.K_SPACE and self.state == LEVEL_COMPLETE:
                    if self.current_level < len(LEVELS) - 1:
                        # 进入下一关 - 重置分数但保留生命值
                        self.current_level += 1
                        self.score = 0  # 重置分数，每关重新计算
                        self.load_level(self.current_level)
                        self.state = PLAYING
                        print(f"进入关卡 {self.current_level + 1}，分数重置为0")
                    else:
                        # 已完成所有关卡
                        self.state = VICTORY
                        self.stop_bgm()
                        self.play_sound('win')
                        print("恭喜通关！")
                
                # 重试功能
                if event.key == pygame.K_r and self.state in [GAME_OVER, VICTORY]:
                    self.start_game()
                
                # ESC返回主菜单
                if event.key == pygame.K_ESCAPE:
                    self.stop_bgm()
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
