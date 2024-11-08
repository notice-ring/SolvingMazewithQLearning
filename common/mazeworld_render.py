import numpy as np
import matplotlib
import matplotlib.pyplot as plt

class Renderer:
    def __init__(self, possible_direction, goal_state, end_state, start_state):
        self.possible_direction = possible_direction
        self.goal_state = goal_state
        self.end_state = end_state
        self.start_state = start_state
        self.ys = len(self.possible_direction)
        self.xs = len(self.possible_direction[0])

        # 입구와 출구 표시
        #self.possible_direction[self.start_state].append(0)
        #self.possible_direction[self.goal_state].append(1)
        
        self.ax = None
        self.fig = None
        self.first_flg = True

    # 그래프 기본 설정
    def set_figure(self, figsize=None):
        fig = plt.figure(figsize=figsize)
        self.ax = fig.add_subplot(111)
        ax = self.ax
        ax.clear()
        ax.tick_params(labelbottom=False, labelleft=False, labelright=False, labeltop=False)
        ax.set_xticks(range(self.xs+1))
        ax.set_yticks(range(self.ys+1))
        ax.set_xlim(0, self.xs)
        ax.set_xlim(0, self.ys)
        ax.grid(True)
    
    # 미로 표시
    def present_maze(self, ax):
        ys, xs = self.ys, self.xs
        direction_space = [0, 1, 2, 3]
        for y in range(ys):
            for x in range(xs):
                state = (y, x)
                
                tx, ty = x, ys-y-1
                direction_map = {
                        0: ((tx+1, ty+1), (tx, ty+1)),
                        1: ((tx, ty), (tx+1, ty)),
                        2: ((tx, ty), (tx, ty+1)),
                        3: ((tx+1, ty), (tx+1, ty+1)),
                    }
                
                for direction in direction_space:
                    if direction not in self.possible_direction[state]:
                        wall = plt.Polygon(direction_map[direction], edgecolor='b', lw=2)
                        ax.add_patch(wall)

    # 가치 함수 표현
    def render_v(self, v=None, policy=None, print_value=True):
        self.set_figure()
        
        ys, xs = self.ys, self.xs
        ax = self.ax

        if v is not None:
            color_list = ['red', 'white', 'green']
            cmap = matplotlib.colors.LinearSegmentedColormap.from_list(
                'colormap_name', color_list)
            
            v_dict = v
            v = np.zeros(self.possible_direction.shape)
            for state, value in v_dict.items():
                v[state] = value
            
            vmax, vmin = v.max(), v.min()
            vmax = max(vmax, abs(vmin))
            vmin = -1 * vmax
            vmax = 1 if vmax < 1 else vmax
            vmin = -1 if vmin > -1 else vmin

            ax.pcolormesh(np.flipud(v), cmap=cmap, vmin=vmin, vmax=vmax)

        for y in range(ys):
            for x in range(xs):
                state = (y, x)

                txt = ''
                if state == self.goal_state:
                    txt = 'R +10' + ' (GOAL)'
                elif state == self.end_state:
                    txt = 'R -10' + ' (END)'
                
                if txt:
                    ax.text(x+0.1, ys-y-0.9, txt)

                if v is not None:
                    if print_value:
                        offsets = [(0.4, -0.15), (-0.15, -0.3)]
                        key = 0
                        if v.shape[0] > 7: key = 1
                        offset = offsets[key]
                        ax.text(x+offset[0], ys-y+offset[1], "{:12.2f}".format(v[y, x]))

                # policy 출력
                if policy is not None:
                    actions = policy[state]
                    max_actions = [kv[0] for kv in actions.items() if kv[1] == max(actions.values())]

                    arrows = ["↑", "↓", "←", "→"]
                    offsets = [(0, 0.1), (0, -0.1), (-0.1, 0), (0.1, 0)]
                    for action in max_actions:
                        arrow = arrows[action]
                        offset = offsets[action]
                        if state == self.goal_state or state == self.end_state:
                            continue
                        ax.text(x+0.45+offset[0], ys-y-0.5+offset[1], arrow)
        
        self.present_maze(self.ax)
        plt.show()

    # 행동 가치 함수 표현
    def render_q(self, q, show_greedy_policy=True):
        self.set_figure()

        ys, xs = self.ys, self.xs
        ax = self.ax
        action_space = [0, 1, 2, 3]

        qmax, qmin = max(q.values()), min(q.values())
        qmax = max(qmax, abs(qmin))
        qmin = -1 * qmax
        qmax = 1 if qmax < 1 else qmax
        qmin = -1 if qmin > -1 else qmin

        color_list = ['red', 'white', 'green']
        cmap = matplotlib.colors.LinearSegmentedColormap.from_list(
            'colormap_name', color_list)
        
        for y in range(ys):
            for x in range(xs):
                for action in action_space:
                    state = (y, x)
                    
                    txt = ''
                    if state == self.goal_state:
                        txt = 'R +10' + ' (GOAL)'
                    elif state == self.end_state:
                        txt = 'R -10' + ' (END)'

                    if txt:
                        ax.text(x+0.05, ys-y-0.95, txt)

                    if state == self.goal_state or state == self.end_state:
                        continue

                    tx, ty = x, ys-y-1

                    action_map = {
                        0: ((0.5+tx, 0.5+ty), (tx+1, ty+1), (tx, ty+1)),
                        1: ((tx, ty), (tx+1, ty), (tx+0.5, ty+0.5)),
                        2: ((tx, ty), (tx+0.5, ty+0.5), (tx, ty+1)),
                        3: ((0.5+tx, 0.5+ty), (tx+1, ty), (tx+1, ty+1)),
                    }
                    offset_map = {
                        0: (0.1, 0.8),
                        1: (0.1, 0.1),
                        2: (-0.2, 0.4),
                        3: (0.4, 0.4),
                    }

                    if state == self.goal_state or state == self.end_state:
                        ax.add_patch(plt.Rectangle((tx, ty), 1, 1, fc=(0., 1., 0., 1.)))
                    else:
                        tq = q[(state, action)]
                        color_scale = 0.5 + (tq / qmax) / 2

                        poly = plt.Polygon(action_map[action], fc=cmap(color_scale))
                        ax.add_patch(poly)

                        offset = offset_map[action]
                        ax.text(tx+offset[0], ty+offset[1], "{:12.2f}".format(tq))

        self.present_maze(self.ax)
        plt.show()

        # 정책을 그리디하게 표현(render_v의 policy 출력 함수 이용)
        if show_greedy_policy:
            policy = {}
            for y in range(self.ys):
                for x in range(self.xs):
                    state = (y, x)
                    qs = [q[state, action] for action in action_space]
                    max_action = np.argmax(qs)
                    probs = {0:0.0, 1:0.0, 2:0.0, 3:0.0}
                    probs[max_action] = 1
                    policy[state] = probs

            self.render_v(None, policy)