# 模拟城堡游戏 - 资源管理与城市建设模拟器
# 这是一个使用tkinter构建的城堡模拟游戏，玩家需要管理资源、雇佣工人、建造建筑，
# 最终目标是建造研究中心完成游戏。
import tkinter as tk
from tkinter import ttk 
from tkinter import messagebox

class Tooltip:
    # 工具提示类，用于在鼠标悬停时显示提示信息
    # 属性:
    #   widget: 绑定提示的控件
    #   text: 提示文本内容 
    #   delay: 显示延迟(毫秒)
    #   tooltip: 提示窗口对象
    #   tooltip_id: 定时器ID
    
    def __init__(self, widget, text, delay=800):
        # 初始化工具提示
        # 参数:
        #   widget: 要绑定提示的控件
        #   text: 提示文本内容
        #   delay: 显示延迟(毫秒，默认800)
        self.widget = widget
        self.text = text
        self.delay =delay
        self.tooltip = None
        self.tooltip_id = None
        self.widget.bind("<Enter>", self.schedule_show)
        self.widget.bind("<Leave>", self.hide)

    def schedule_show(self, event=None):
        # 安排显示工具提示(鼠标进入时调用)
        # 参数:
        #   event: 鼠标事件(可选)
        self.tooltip_id = self.widget.after(self.delay, self.show)    

    def show(self):
        # 显示工具提示窗口
        # 计算位置并创建提示窗口
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        
        label = tk.Label(self.tooltip, text=self.text, background="#ffffe0", 
                        relief="solid", borderwidth=1, font=("隶书", 15))
        label.pack()

    def hide(self, event=None):
        # 隐藏工具提示(鼠标离开时调用)
        # 参数:
        #   event: 鼠标事件(可选)
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None
        if self.tooltip_id:
            self.widget.after_cancel(self.tooltip_id)
            self.tooltip_id = None


# 全局资源变量 - 存储游戏中的四种资源数量
resources = {
    "food": 150,
    "wood": 0,
    "stone": 0,
    "iron": 0
}

# 全局工人数量 - 存储五种工人的数量
workers = {
    "farmer": 0,
    "lumber": 0,
    "quarry": 0,
    "mine": 0,
    "builder": 0
}

def update_resources():
    # 更新资源数量(每秒调用一次)
    # 根据当前工人数量计算资源产量并更新UI显示
    # 农民生产
    food_produced = workers["farmer"] * 1  # 每个农民每秒生产1食物
    resources["food"] += food_produced
    
    # 伐木工生产
    if workers["lumber"] > 0:
        wood_produced = workers["lumber"] * 1
        resources["wood"] += wood_produced
            
    # 采石工生产
    if workers["quarry"] > 0:
        stone_produced = workers["quarry"] * 1
        resources["stone"] += stone_produced
            
    # 铁矿工生产
    if workers["mine"] > 0:
        iron_produced = workers["mine"] * 1
        resources["iron"] += iron_produced
        
    
    # 更新UI显示
    resource_labels["food"].config(text=f"食物: {resources['food']}")
    resource_labels["wood"].config(text=f"木头: {resources['wood']}")
    resource_labels["stone"].config(text=f"石头: {resources['stone']}")
    resource_labels["iron"].config(text=f"铁矿: {resources['iron']}")
    
    # 设置下一次更新
    root.after(1000, update_resources)

def start_new_game():
    # 开始新游戏
    # 初始化游戏界面，创建资源显示、工人管理、建筑管理等UI元素
    # 隐藏主菜单
    button_frame.pack_forget()
    
    # 创建游戏主界面
    game_frame = tk.Frame(root)                                                 
    game_frame.pack(expand=True, fill="both", padx=20, pady=20)                      
    
    # 创建信息显示容器
    info_container = tk.Frame(game_frame)
    info_container.pack(fill="x", pady=5)
    
    # 配置列权重
    info_container.grid_columnconfigure(0, weight=1)
    
    # 资源信息框
    resource_frame = tk.LabelFrame(info_container, text="资源信息", font=("隶书", 15))
    resource_frame.grid(row=0, column=0, padx=5, sticky="ew")
    
    global resource_labels                                         
    resource_labels = {
        "food": tk.Label(resource_frame, text="食物: 0", font=("隶书", 15)),   
        "wood": tk.Label(resource_frame, text="木头: 0", font=("隶书", 15)),
        "stone": tk.Label(resource_frame, text="石头: 0", font=("隶书", 15)),
        "iron": tk.Label(resource_frame, text="铁矿: 0", font=("隶书", 15))
    }
    resource_display_names = {                                                       
        "food": "食物",
        "wood": "木头", 
        "stone": "石头",
        "iron": "铁矿"
    }
    
    for label in resource_labels.values():                                          
        label.pack(anchor="w")
    
    # 启动资源更新循环
    update_resources()
    
    # 第二行容器
    row2_container = tk.Frame(info_container)
    row2_container.grid(row=1, column=0, sticky="ew")
    
    # 配置第二行列权重
    row2_container.grid_columnconfigure(0, weight=1,uniform="group1")
    row2_container.grid_columnconfigure(1, weight=1,uniform="group1")
    
    # 人口信息框
    population_frame = tk.LabelFrame(row2_container, text="人口信息", font=("隶书", 15))
    population_frame.grid(row=0, column=0, padx=5, sticky="nsew")
    
    # 初始建筑数量
    global farm_count, lumber_count, quarry_count, mine_count, worker_house_count
    global builder_count, builder_capacity, populations, buildings, population_capacities
    
    farm_count = 0
    lumber_count = 0
    quarry_count = 0
    mine_count = 0
    
    # 计算人口上限
    farmer_capacity = farm_count * 10           
    lumber_capacity = lumber_count * 10
    quarry_capacity = quarry_count * 10
    mine_capacity = mine_count * 10
    
    # 工人房数量
    worker_house_count = 0
    
    # 建筑工数量
    builder_count = 0
    builder_capacity = worker_house_count * 5
    
    # 人口信息
    populations = [
        ("农  民", farmer_capacity),
        ("伐木工", lumber_capacity),
        ("采石工", quarry_capacity),
        ("铁矿工", mine_capacity),
        ("建筑工", builder_capacity)
    ]
    
    # 建筑信息
    buildings = [
        ("农  屋", farm_count),
        ("伐木屋", lumber_count),
        ("采石屋", quarry_count),
        ("铁矿屋", mine_count),
        ("工人房", worker_house_count)
    ]
    
    # 存储容量信息
    population_capacities = {}
    
    for i, (name, capacity) in enumerate(populations):
        # 存储容量
        population_capacities[name] = capacity
        # 人口信息
        tk.Label(population_frame, 
                text=f"{name}: 0000/{capacity:04d}", 
                font=("隶书", 15)).grid(row=i, column=0, sticky="w", padx=5, pady=2)
        
        # 雇佣按钮
        btn = tk.Button(population_frame,
                       text=f"雇佣{name}",
                       width=15,
                       font=("隶书", 15))
        btn.grid(row=i, column=1, padx=5, pady=2)
            
        # 添加雇佣按钮提示
        if name == "农  民":
            Tooltip(btn, "需要20食物")
        elif name == "伐木工":
            Tooltip(btn, "需要50食物")
        elif name == "采石工":
            Tooltip(btn, "需要50木头")
        elif name == "铁矿工":
            Tooltip(btn, "需要50石头")
        elif name == "建筑工":
            Tooltip(btn, "需要50食物 + 50木头 + 50石头 + 50铁矿")
        
        # 为农民按钮绑定点击事件
        if name == "农  民":
            def hire_farmer(name, row):
                # 获取当前农民数量和容量
                capacity = population_capacities["农  民"]
                for widget in population_frame.grid_slaves(row=row, column=0):
                    if isinstance(widget, tk.Label):
                        current_text = widget.cget("text")
                        current_count = int(current_text.split(":")[1].split("/")[0])
                        
                        # 检查食物和居住空间
                        if current_count >= capacity:
                            messagebox.showwarning("居住空间不足", "没有足够的农屋来容纳更多农民")
                            return
                        if resources["food"] < 20:
                            messagebox.showwarning("食物不足", "需要20食物来雇佣农民")
                            return
                        
                            
                        # 执行雇佣
                        resources["food"] -= 20
                        workers["farmer"] += 1
                        resource_labels["food"].config(text=f"食物: {resources['food']}")
                        current_count += 1
                        widget.config(text=f"{name}: {current_count:04d}/{capacity:04d}")
            
            btn.config(command=lambda name=name, i=i: hire_farmer(name, i))

        # 为伐木工按钮绑定点击事件 
        if name == "伐木工":
            def hire_lumber(name, row):
                # 获取当前伐木工数量和容量
                capacity = population_capacities["伐木工"]
                for widget in population_frame.grid_slaves(row=row, column=0):
                    if isinstance(widget, tk.Label):
                        current_text = widget.cget("text")
                        current_count = int(current_text.split(":")[1].split("/")[0])
                        
                        # 检查食物和居住空间
                        if current_count >= capacity:
                            messagebox.showwarning("居住空间不足", "没有足够的伐木屋来容纳更多伐木工")
                            return
                        if resources["food"] < 50:
                            messagebox.showwarning("食物不足", "需要50食物来雇佣伐木工")
                            return
                        
                            
                        # 执行雇佣
                        resources["food"] -= 50
                        workers["lumber"] += 1
                        resource_labels["food"].config(text=f"食物: {resources['food']}")
                        current_count += 1
                        widget.config(text=f"{name}: {current_count:04d}/{capacity:04d}") 
            btn.config(command=lambda name=name, i=i: hire_lumber(name, i))
 
        # 为采石工按钮绑定点击事件
        if name ==  "采石工":
            def hire_quarry(name, row): 
                # 获取当前采石工数量和容量
                capacity = population_capacities["采石工"]
                for widget in population_frame.grid_slaves(row=row, column=0):
                    if isinstance(widget, tk.Label):
                        current_text = widget.cget("text")
                        current_count = int(current_text.split(":")[1].split("/")[0])
                        
                        # 检查石头和居住空间
                        if current_count >= capacity:
                            messagebox.showwarning("居住空间不足", "没有足够的采石屋来容纳更多采石工")
                            return
                        if resources["wood"] < 50:
                            messagebox.showwarning("木头不足", "需要50木头来雇佣采石工")
                            return
                        
                            
                        # 执行雇佣
                        resources["wood"] -= 50
                        workers["quarry"] += 1
                        resource_labels["wood"].config(text=f"木头: {resources['wood']}")
                        current_count += 1
                        widget.config(text=f"{name}: {current_count:04d}/{capacity:04d}")
            btn.config(command=lambda name=name, i=i: hire_quarry(name, i))

        # 为铁矿工按钮绑定点击事件
        if name == "铁矿工":
            def hire_mine(name, row):
                # 获取当前铁矿工数量和容量
                capacity = population_capacities["铁矿工"]
                for widget in population_frame.grid_slaves(row=row, column=0):
                    if isinstance(widget, tk.Label):
                        current_text = widget.cget("text")
                        current_count = int(current_text.split(":")[1].split("/")[0])
                        
                        # 检查铁矿和居住空间
                        if current_count >= capacity:
                            messagebox.showwarning("居住空间不足", "没有足够的铁矿屋来容纳更多铁矿工")
                            return
                        if resources["stone"] < 50:
                            messagebox.showwarning("石头不足", "需要50石头来雇佣铁矿工")
                            return
                        
                            
                        # 执行雇佣
                        resources["stone"] -= 50
                        workers["mine"] += 1
                        resource_labels["stone"].config(text=f"石头: {resources['stone']}")
                        current_count += 1
                        widget.config(text=f"{name}: {current_count:04d}/{capacity:04d}")
            btn.config(command=lambda name=name, i=i: hire_mine(name, i))            

        # 为建筑工按钮绑定点击事件
        if name ==  "建筑工":
            def hire_builder(name, row):
                # 获取当前建筑工数量和容量
                capacity = population_capacities["建筑工"]
                for widget in population_frame.grid_slaves(row=row, column=0):
                    if isinstance(widget, tk.Label):
                        current_text = widget.cget("text")
                        current_count = int(current_text.split(":")[1].split("/")[0])
                        
                        # 检查资源和居住空间
                        if current_count >= capacity:
                            messagebox.showwarning("居住空间不足", "没有足够的工人房来容纳更多建筑工")
                            return
                        if resources["food"] < 50:
                            messagebox.showwarning("食物不足", "需要50食物来雇佣建筑工")
                            return
                        if resources["wood"] < 50:
                            messagebox.showwarning("木头不足", "需要50木头来雇佣建筑工")
                            return
                        if resources["stone"] < 50:
                            messagebox.showwarning("石头不足", "需要50石头来雇佣建筑工")
                            return
                        if resources["iron"] < 50:
                            messagebox.showwarning("铁矿不足", "需要50铁矿来雇佣建筑工")
                            return
                        
                            
                        # 执行雇佣
                        resources["food"] -= 50
                        resources["wood"] -= 50
                        resources["stone"] -= 50
                        resources["iron"] -= 50
                        workers["builder"] += 1
                        resource_labels["food"].config(text=f"食物: {resources['food']}")
                        resource_labels["wood"].config(text=f"木头: {resources['wood']}")
                        resource_labels["stone"].config(text=f"石头: {resources['stone']}")
                        resource_labels["iron"].config(text=f"铁矿: {resources['iron']}")
                        current_count += 1
                        widget.config(text=f"{name}: {current_count:04d}/{capacity:04d}")
            btn.config(command=lambda name=name, i=i: hire_builder(name, i))

    # 建筑信息框
    building_frame = tk.LabelFrame(row2_container, text="建筑信息", font=("隶书", 15))
    building_frame.grid(row=0, column=1, padx=5, sticky="nsew")

    for i, (name, count) in enumerate(buildings):

        # 建筑信息标签
        tk.Label(building_frame, 
                text=f"{name}: {count:03d} ", 
                font=("隶书", 15)).grid(row=i, column=0, sticky="w", padx=5, pady=2)
        
        # 建造按钮
        btn = tk.Button(building_frame,
                       text=f"建造{name}",
                       width=15,
                       font=("隶书", 15))
        btn.grid(row=i, column=1, padx=5, pady=2)
        
        # 添加建造按钮提示
        if name == "农  屋":
            Tooltip(btn, "需要200食物")
        elif name == "伐木屋":
            Tooltip(btn, "需要200木头")
        elif name == "采石屋":
            Tooltip(btn, "需要200石头")
        elif name == "铁矿屋":
            Tooltip(btn, "需要200铁矿")
        elif name == "工人房":
            Tooltip(btn, "需要500食物 + 500木头 + 500石头 + 500铁矿")        
        
        # 为农屋按钮绑定点击事件
        if name == "农  屋":
            def build_farm():
                global farm_count, resource_labels, population_capacities, populations, buildings
                # 检查是否拥有农业社
                if not industry_built["农业社"]:
                    messagebox.showwarning("缺少农业社", "需要先建造农业社才能建造农屋")
                    return
                    
                # 检查食物是否足够
                if resources["food"] < 200:
                    messagebox.showwarning("食物不足", "需要200食物来建造农屋")
                    return
                
                # 扣除食物
                resources["food"] -= 200
                resource_labels["food"].config(text=f"食物: {resources['food']}")
                
                # 增加农屋数量
                farm_count += 1
                buildings[0] = ("农  屋", farm_count)
                
                # 更新农民容量
                farmer_capacity = farm_count * 10 + (1 if industry_built["农业社"] else 0) * 10
                population_capacities["农  民"] = farmer_capacity
                populations[0] = ("农  民", farmer_capacity)
                
                # 更新建筑信息显示
                for widget in building_frame.grid_slaves(row=0, column=0):
                    if isinstance(widget, tk.Label):
                        widget.config(text=f"农  屋: {farm_count:03d}")
                
                # 更新农民容量显示
                for widget in population_frame.grid_slaves(row=0, column=0):
                    if isinstance(widget, tk.Label):
                        current_text = widget.cget("text")
                        current_count = int(current_text.split(":")[1].split("/")[0])
                        widget.config(text=f"农  民: {current_count:04d}/{farmer_capacity:04d}")
                
                # 更新工人房信息
                for widget in building_frame.grid_slaves(row=4, column=0):
                    if isinstance(widget, tk.Label):
                        widget.config(text=f"工人房: {worker_house_count:03d}")
            
            btn.config(command=build_farm)
            
        # 为伐木屋按钮绑定点击事件
        elif name == "伐木屋":
            def build_lumber():
                global lumber_count, resource_labels, population_capacities, populations, buildings
                # 检查是否拥有林业社
                if not industry_built["林业社"]:
                    messagebox.showwarning("缺少林业社", "需要先建造林业社才能建造伐木屋")
                    return
                    
                # 检查木头是否足够
                if resources["wood"] < 200:
                    messagebox.showwarning("木头不足", "需要200木头来建造伐木屋")
                    return
                
                # 扣除木头
                resources["wood"] -= 200
                resource_labels["wood"].config(text=f"木头: {resources['wood']}")
                
                # 增加伐木屋数量
                lumber_count += 1
                buildings[1] = ("伐木屋", lumber_count)
                
                # 更新伐木工容量
                lumber_capacity = lumber_count * 10 + (1 if industry_built["林业社"] else 0) * 10
                population_capacities["伐木工"] = lumber_capacity
                populations[1] = ("伐木工", lumber_capacity)
                
                # 更新建筑信息显示
                for widget in building_frame.grid_slaves(row=1, column=0):
                    if isinstance(widget, tk.Label):
                        widget.config(text=f"伐木屋: {lumber_count:03d}")
                
                # 更新伐木工容量显示
                for widget in population_frame.grid_slaves(row=1, column=0):
                    if isinstance(widget, tk.Label):
                        current_text = widget.cget("text")
                        current_count = int(current_text.split(":")[1].split("/")[0])
                        widget.config(text=f"伐木工: {current_count:04d}/{lumber_capacity:04d}")
            
            btn.config(command=build_lumber)
            
        # 为采石屋按钮绑定点击事件
        elif name == "采石屋":
            def build_quarry_house():
                global quarry_count, resource_labels, population_capacities, populations, buildings
                # 检查是否拥有采石社
                if not industry_built["采石社"]:
                    messagebox.showwarning("缺少采石社", "需要先建造采石社才能建造采石屋")
                    return
                    
                # 检查石头是否足够
                if resources["stone"] < 200:
                    messagebox.showwarning("石头不足", "需要200石头来建造采石屋")
                    return
                
                # 扣除石头
                resources["stone"] -= 200
                resource_labels["stone"].config(text=f"石头: {resources['stone']}")
                
                # 增加采石屋数量
                quarry_count += 1
                buildings[2] = ("采石屋", quarry_count)
                
                # 更新采石工容量
                quarry_capacity = quarry_count * 10 + (1 if industry_built["采石社"] else 0) * 10
                population_capacities["采石工"] = quarry_capacity
                populations[2] = ("采石工", quarry_capacity)
                
                # 更新建筑信息显示
                for widget in building_frame.grid_slaves(row=2, column=0):
                    if isinstance(widget, tk.Label):
                        widget.config(text=f"采石屋: {quarry_count:03d}")
                
                # 更新采石工容量显示
                for widget in population_frame.grid_slaves(row=2, column=0):
                    if isinstance(widget, tk.Label):
                        current_text = widget.cget("text")
                        current_count = int(current_text.split(":")[1].split("/")[0])
                        widget.config(text=f"采石工: {current_count:04d}/{quarry_capacity:04d}")
            
            btn.config(command=build_quarry_house)
            
        # 为铁矿屋按钮绑定点击事件
        elif name == "铁矿屋":
            def build_mine_house():
                global mine_count, resource_labels, population_capacities, populations, buildings
                # 检查是否拥有铁矿社
                if not industry_built["铁矿社"]:
                    messagebox.showwarning("缺少铁矿社", "需要先建造铁矿社才能建造铁矿屋")
                    return
                    
                # 检查铁矿是否足够
                if resources["iron"] < 200:
                    messagebox.showwarning("铁矿不足", "需要200铁矿来建造铁矿屋")
                    return
                
                # 扣除铁矿
                resources["iron"] -= 200
                resource_labels["iron"].config(text=f"铁矿: {resources['iron']}")
                
                # 增加铁矿屋数量
                mine_count += 1
                buildings[3] = ("铁矿屋", mine_count)
                
                # 更新铁矿工容量
                mine_capacity = mine_count * 10 + (1 if industry_built["铁矿社"] else 0) * 10
                population_capacities["铁矿工"] = mine_capacity
                populations[3] = ("铁矿工", mine_capacity)
                
                # 更新建筑信息显示
                for widget in building_frame.grid_slaves(row=3, column=0):
                    if isinstance(widget, tk.Label):
                        widget.config(text=f"铁矿屋: {mine_count:03d}")
                
                # 更新铁矿工容量显示
                for widget in population_frame.grid_slaves(row=3, column=0):
                    if isinstance(widget, tk.Label):
                        current_text = widget.cget("text")
                        current_count = int(current_text.split(":")[1].split("/")[0])
                        widget.config(text=f"铁矿工: {current_count:04d}/{mine_capacity:04d}")
            
            btn.config(command=build_mine_house)
            
        # 为工人房按钮绑定点击事件
        elif name == "工人房":
            def build_worker_house():
                global worker_house_count, resource_labels, population_capacities, populations, buildings
                # 检查是否拥有建筑社
                if not industry_built["建筑社"]:
                    messagebox.showwarning("缺少建筑社", "需要先建造建筑社才能建造工人房")
                    return
                # 检查资源是否足够
                if resources["food"] < 1000:
                    messagebox.showwarning("食物不足", "需要1000食物来建造工人房")
                    return
                if resources["wood"] < 1000:
                    messagebox.showwarning("木头不足", "需要1000木头来建造工人房")
                    return
                if resources["stone"] < 500:
                    messagebox.showwarning("石头不足", "需要500石头来建造工人房")
                    return
                if resources["iron"] < 500:
                    messagebox.showwarning("铁矿不足", "需要500铁矿来建造工人房")
                    return
                
                # 扣除资源
                resources["food"] -= 1000
                resources["wood"] -= 1000
                resources["stone"] -= 500
                resources["iron"] -= 500
                resource_labels["food"].config(text=f"食物: {resources['food']}")
                resource_labels["wood"].config(text=f"木头: {resources['wood']}")
                resource_labels["stone"].config(text=f"石头: {resources['stone']}")
                resource_labels["iron"].config(text=f"铁矿: {resources['iron']}")
                
                # 增加工人房数量
                worker_house_count += 1
                buildings[4] = ("工人房", worker_house_count)
                
                # 更新建筑工容量
                builder_capacity = worker_house_count * 5 + (1 if industry_built["建筑社"] else 0) * 5
                population_capacities["建筑工"] = builder_capacity
                populations[4] = ("建筑工", builder_capacity)
                
                # 更新建筑信息显示
                for widget in building_frame.grid_slaves(row=4, column=0):
                    if isinstance(widget, tk.Label):
                        widget.config(text=f"工人房: {worker_house_count:03d}")
                
                # 更新建筑工容量显示
                for widget in population_frame.grid_slaves(row=4, column=0):
                    if isinstance(widget, tk.Label):
                        current_text = widget.cget("text")
                        current_count = int(current_text.split(":")[1].split("/")[0])
                        widget.config(text=f"建筑工: {current_count:04d}/{builder_capacity:04d}")
            
            btn.config(command=build_worker_house)

   
    
       
    # 行业建筑信息框
    industry_frame = tk.LabelFrame(info_container, text="行业建筑", font=("隶书", 15))     
    industry_frame.grid(row=3, column=0, columnspan=2, padx=5, pady=10, sticky="ew")               
    
    # 行业建筑标签
    industry_labels = [
        ("农业社", "gray"),
        ("林业社", "gray"), 
        ("采石社", "gray"),
        ("铁矿社", "gray"),
        ("建筑社", "gray")
    ]
    
    # 行业建筑状态
    industry_built = {
        "农业社": False,
        "林业社": False,
        "采石社": False,
        "铁矿社": False,
        "建筑社": False
    }

    def build_agriculture():                   
        if industry_built["农业社"]:
            messagebox.showinfo("提示", "已拥有农业社，不能再建造")
            return
            
        if resources["food"] < 120:
            messagebox.showwarning("食物不足", "需要120食物来建造农业社")
            return
            
        # 扣除食物
        resources["food"] -= 120
        resource_labels["food"].config(text=f"食物: {resources['food']}")
        
        # 更新状态
        industry_built["农业社"] = True
        agriculture_label.config(fg="green")
        
        # 增加农民居住上限
        farmer_capacity = farm_count * 5 + (1 if industry_built["农业社"] else 0) * 10
        population_capacities["农  民"] = farmer_capacity
        
        # 更新农民容量显示，数据格式04d表示4位整数，不足4位前面补0
        for widget in population_frame.grid_slaves(row=0, column=0):
            if isinstance(widget, tk.Label):
                current_text = widget.cget("text")
                current_count = int(current_text.split(":")[1].split("/")[0])
                widget.config(text=f"农  民: {current_count:04d}/{farmer_capacity:04d}")

    def build_forestry():
        if industry_built["林业社"]:
            messagebox.showinfo("提示", "已拥有林业社，不能再建造")
            return
            
        if resources["food"] < 500:
            messagebox.showwarning("食物不足", "需要500食物来建造林业社")
            return
            
        # 扣除食物
        resources["food"] -= 500
        resource_labels["food"].config(text=f"食物: {resources['food']}")
        
        # 更新状态
        industry_built["林业社"] = True
        forestry_label.config(fg="green")
        
        # 增加伐木工居住上限
        lumber_capacity = lumber_count * 5 + (1 if industry_built["林业社"] else 0) * 10
        population_capacities["伐木工"] = lumber_capacity
        
        # 更新伐木工容量显示
        for widget in population_frame.grid_slaves(row=1, column=0):
            if isinstance(widget, tk.Label):
                current_text = widget.cget("text")
                current_count = int(current_text.split(":")[1].split("/")[0])
                widget.config(text=f"伐木工: {current_count:04d}/{lumber_capacity:04d}")

    def build_quarry_society():
        if industry_built["采石社"]:
            messagebox.showinfo("提示", "已拥有采石社，不能再建造")
            return
            
        if resources["food"] < 500:
            messagebox.showwarning("食物不足", "需要500食物来建造采石社")
            return
            
        if resources["wood"] < 500:
            messagebox.showwarning("木头不足", "需要500木头来建造采石社")
            return
            
        # 扣除资源
        resources["food"] -= 500
        resources["wood"] -= 500
        resource_labels["food"].config(text=f"食物: {resources['food']}")
        resource_labels["wood"].config(text=f"木头: {resources['wood']}")
        
        # 更新状态
        industry_built["采石社"] = True
        quarry_label.config(fg="green")
        
        # 增加采石工居住上限
        quarry_capacity = quarry_count * 5 + (1 if industry_built["采石社"] else 0) * 10
        population_capacities["采石工"] = quarry_capacity
        
        # 更新采石工容量显示
        for widget in population_frame.grid_slaves(row=2, column=0):
            if isinstance(widget, tk.Label):
                current_text = widget.cget("text")
                current_count = int(current_text.split(":")[1].split("/")[0])
                widget.config(text=f"采石工: {current_count:04d}/{quarry_capacity:04d}")

    def build_mine_society():
        if industry_built["铁矿社"]:
            messagebox.showinfo("提示", "已拥有铁矿社，不能再建造")
            return
            
        if resources["food"] < 500:
            messagebox.showwarning("食物不足", "需要500食物来建造铁矿社")
            return
            
        if resources["wood"] < 500:
            messagebox.showwarning("木头不足", "需要500木头来建造铁矿社")
            return
            
        if resources["stone"] < 500:
            messagebox.showwarning("石头不足", "需要500石头来建造铁矿社")
            return
            
        # 扣除资源
        resources["food"] -= 500
        resources["wood"] -= 500
        resources["stone"] -= 500
        resource_labels["food"].config(text=f"食物: {resources['food']}")
        resource_labels["wood"].config(text=f"木头: {resources['wood']}")
        resource_labels["stone"].config(text=f"石头: {resources['stone']}")
        
        # 更新状态
        industry_built["铁矿社"] = True
        mine_label.config(fg="green")
        
        # 增加铁矿工居住上限
        mine_capacity = mine_count * 5 + (1 if industry_built["铁矿社"] else 0) * 10
        population_capacities["铁矿工"] = mine_capacity
        
        # 更新铁矿工容量显示
        for widget in population_frame.grid_slaves(row=3, column=0):
            if isinstance(widget, tk.Label):
                current_text = widget.cget("text")
                current_count = int(current_text.split(":")[1].split("/")[0])
                widget.config(text=f"铁矿工: {current_count:04d}/{mine_capacity:04d}")

    def build_architectural():
        if industry_built["建筑社"]:
            messagebox.showinfo("提示", "已拥有建筑社，不能再建造")
            return
        
        if resources["food"] < 2000:
            messagebox.showwarning("食物不足", "需要2000食物来建造建筑社")
            return
        if resources["wood"] < 2000:
            messagebox.showwarning("木头不足", "需要2000木头来建造建筑社")
            return
        if resources["stone"] < 1000:
            messagebox.showwarning("石头不足", "需要1000石头来建造建筑社")
            return
        if resources["iron"] < 1000:
            messagebox.showwarning("铁矿不足", "需要1000铁矿来建造建筑社")
            return
        
        # 扣除资源
        resources["food"] -= 2000
        resources["wood"] -= 2000
        resources["stone"] -= 1000
        resources["iron"] -= 1000
        resource_labels["food"].config(text=f"食物: {resources['food']}")
        resource_labels["wood"].config(text=f"木头: {resources['wood']}")
        resource_labels["stone"].config(text=f"石头: {resources['stone']}")
        resource_labels["iron"].config(text=f"铁矿: {resources['iron']}")

        # 更新状态
        industry_built["建筑社"] = True
        builder_label.config(fg="green")

        # 增加建筑工居住上限
        builder_capacity = worker_house_count * 5 + (1 if industry_built["建筑社"] else 0) * 5
        population_capacities["建筑工"] = builder_capacity
        
        #更新建筑工容量显示
        for widget in population_frame.grid_slaves(row=4, column=0):
            if isinstance(widget, tk.Label):
                current_text = widget.cget("text")
                current_count = int(current_text.split(":")[1].split("/")[0])
                widget.config(text=f"建筑工: {current_count:04d}/{builder_capacity:04d}")
                      
    for i, (name, color) in enumerate(industry_labels):
        label = tk.Label(industry_frame, 
                        text=name,
                        font=("隶书", 15),
                        fg=color)
        label.grid(row=0, column=i, sticky="w", padx=10, pady=5)
        
        # 添加行业建筑提示
        if name == "农业社":
            agriculture_label = label
            Tooltip(label, "需要120食物")
            label.bind("<Button-1>", lambda e: build_agriculture())
        elif name == "林业社":
            forestry_label = label
            Tooltip(label, "需要500食物")
            label.bind("<Button-1>", lambda e: build_forestry())
        elif name == "采石社":
            quarry_label = label
            Tooltip(label, "需要500食物 + 500木头")
            label.bind("<Button-1>", lambda e: build_quarry_society())
        elif name == "铁矿社":
            mine_label = label
            Tooltip(label, "需要500食物 + 500木头 + 500石头")
            label.bind("<Button-1>", lambda e: build_mine_society())
        elif name == "建筑社":
            builder_label = label
            Tooltip(label, "需要2000食物 + 2000木头 + 1000石头 + 1000铁矿")
            label.bind("<Button-1>", lambda e: build_architectural())
    
    # 在行业建筑框下方添加1行间隙
    tk.Frame(info_container, height=1).grid(row=4, column=0)

    # 在行业建筑框下方添加研究中心框
    research_center_frame = tk.LabelFrame(info_container, text="研究中心", font=("隶书", 15))
    research_center_frame.grid(row=4, column=0, padx=5, pady=5, sticky="ew")

    # 研究中心状态
    research_center = {
        "built": False,
        "building": False,
        "progress": 0,
        "required": 500
    }

    def update_research_progress():
        if research_center["building"]:
            # 每秒增加建筑工数量个建筑点
            research_center["progress"] += workers["builder"]
            if research_center["progress"] >= research_center["required"]:
                research_center["built"] = True
                research_center["building"] = False
                research_label.config(text="已完成",fg="green")
                progress_label.config(text=f"进度: {research_center['required']}/{research_center['required']}")
                messagebox.showinfo("提示", "研究中心建造完成！")
            else:
                # 更新进度显示
                progress_label.config(text=f"进度: {research_center['progress']}/{research_center['required']}")
                # 继续更新
                root.after(1000, update_research_progress)

    def build_research_center():
        if research_center["built"]:
            messagebox.showinfo("提示", "研究中心已建造完成")
            return
        if research_center["building"]:
            messagebox.showinfo("提示", "研究中心正在建造中")
            return
            
        # 检查资源
        if resources["food"] < 10000:
            messagebox.showwarning("食物不足", "需要10000食物")
            return
        if resources["wood"] < 10000:
            messagebox.showwarning("木头不足", "需要10000木头")
            return
        if resources["stone"] < 5000:
            messagebox.showwarning("石头不足", "需要5000石头")
            return
        if resources["iron"] < 5000:
            messagebox.showwarning("铁矿不足", "需要5000铁矿")
            return
            
        # 扣除资源
        resources["food"] -= 10000
        resources["wood"] -= 10000
        resources["stone"] -= 5000
        resources["iron"] -= 5000
        resource_labels["food"].config(text=f"食物: {resources['food']}")
        resource_labels["wood"].config(text=f"木头: {resources['wood']}")
        resource_labels["stone"].config(text=f"石头: {resources['stone']}")
        resource_labels["iron"].config(text=f"铁矿: {resources['iron']}")
        
        # 开始建造
        research_center["building"] = True
        research_label.config(text="建造中.",fg="orange")
        progress_label.config(text=f"进度: 0/{research_center['required']}")
        update_research_progress()

    # 研究中心开始建造标签  
    research_label = tk.Label(research_center_frame, text="开始建造", font=("隶书", 15), fg="gray")
    research_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)   
    Tooltip(research_label, "需要10000食物、10000木头、5000石头、5000铁矿")
    research_label.bind("<Button-1>", lambda e: build_research_center())
    
    # 进度标签
    progress_label = tk.Label(research_center_frame, text="", font=("隶书", 15))
    progress_label.grid(row=0, column=1, sticky="w", padx=10, pady=5)
   


 # 作弊函数
    def cheat_resources():   
        for key in resources:
            resources[key] += 1000
        for key in resource_labels:
            resource_labels[key].config(text=f"{resource_display_names[key]}: {resources[key]}")
            
    # 在行业建筑框下方添加1行间隙
    tk.Frame(info_container, height=1).grid(row=2, column=0)
        
    # 作弊按钮
    cheat_button = tk.Button(info_container, 
                           text="作弊", 
                           font=("隶书", 15),
                           bg="red",
                           fg="white",
                           command=cheat_resources )
    cheat_button.grid(row=5, column=0, sticky="sw", padx=5, pady=5)                

    # 添加作弊按钮提示
    Tooltip(cheat_button, "增加1000所有资源")
        

def continue_game():    
    # 继续游戏(暂未实现)
    print("加载游戏")



def exit_game():
    # 退出游戏
    root.destroy()

# 创建主窗口并设置居中显示
root = tk.Tk()
root.title("模拟城堡Demo")
window_width = 1024
window_height = 768
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

button_frame = tk.Frame(root)
button_frame.pack(expand=True)

start_button = tk.Button(button_frame, text="开始新游戏", command=start_new_game, width=20, 
                        font=("隶书", 15))
start_button.pack(pady=10)

continue_button = tk.Button(button_frame, text="加载游戏", command=continue_game, width=20,
                           font=("隶书", 15))
continue_button.pack(pady=10)

exit_button = tk.Button(button_frame, text="退出游戏", command=exit_game, width=20,
                       font=("隶书", 15))
exit_button.pack(pady=10)

root.mainloop()
