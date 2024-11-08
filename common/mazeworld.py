if "__file__" in globals():
    import os, sys

    sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from typing import List, Tuple
import numpy as np
import common.mazeworld_render as render_helper

## TODO: 필요 없어진 경우 MazeWorld 기본값 제거할 것.
DEFAULT_START = (0, 2)
DEFAULT_GOAL = (3, 3)
DEFAULT_END = (2, 1)
DEFAULT_MAP = [
    [[1, 3], [2, 3], [1, 2, 3], [2]],
    [[0, 1], [3], [0, 2], [1]],
    [[0, 1, 3], [1, 2, 3], [1, 2, 3], [0, 1, 2]],
    [[0, 3], [0, 2, 3], [0, 2], [0]],
]


class MazeWorld:
    def __init__(
        self,
        start: Tuple[int] = DEFAULT_START,
        goal: Tuple[int] = DEFAULT_GOAL,
        end: Tuple[int] = DEFAULT_END,
        directions: List[List[int]] = DEFAULT_MAP,
    ):
        self.action_space = [0, 1, 2, 3]  # 행동 공간
        self.action_meaning = {  # 행동의 의미
            0: "UP",
            1: "DOWN",
            2: "LEFT",
            3: "RIGHT",
        }

        self.goal_state = goal  # 목표 상태
        self.end_state = end  # 도달 시 과제 실패
        self.start_state = start  # 시작 상태
        self.agent_state = self.start_state  # 에이전트 초기 상태

        # 미로의 두께가 없는 벽을 표현하기 위하여 각 상태에서 이동할 수 있는 방향을 명시
        self.possible_direction = np.array(directions, dtype=object)

    @property
    def height(self):  # 세로
        return len(self.possible_direction)

    @property
    def width(self):  # 가로
        return len(self.possible_direction[0])

    @property
    def shape(self):  # 세로, 가로
        return self.reward_map.shape

    def actions(self):  # 모든 행동 반환
        return self.action_space

    def states(self):  # 과제의 모든 상태 반환
        for h in range(self.height):
            for w in range(self.width):
                yield (h, w)

    def next_state(self, state, action):  # 현재 상태와 행동에 따른 다음 상태 반환
        action_move_map = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        if action in self.possible_direction[state]:
            move = action_move_map[action]
            next_state = (state[0] + move[0], state[1] + move[1])
        else:
            next_state = state

        return next_state

    def reward(
        self, state, action, next_state
    ):  # 현재 상태, 행동, 다음 상태에 따른 보상 반환
        if next_state == self.goal_state:
            reward = 10
        elif next_state == self.end_state:
            reward = -10
        else:
            reward = -1

        return reward

    def reset(self):  # 과제 종료시 에이전트 위치 초기화
        self.agent_state = self.start_state
        return self.agent_state

    def step(self, action):  # 행동 후 다음 상태, 보상과 과제 종료 여부 반환
        state = self.agent_state
        next_state = self.next_state(state, action)
        reward = self.reward(state, action, next_state)
        done = next_state == self.goal_state or next_state == self.end_state

        self.agent_state = next_state
        return next_state, reward, done

    def render_v(self, v=None, policy=None, print_value=True):  # V 값 시각화
        renderer = render_helper.Renderer(
            self.possible_direction, self.goal_state, self.end_state, self.start_state
        )
        renderer.render_v(v, policy, print_value)

    def render_q(self, q=None, print_value=True):  # Q 값 시각화
        renderer = render_helper.Renderer(
            self.possible_direction, self.goal_state, self.end_state, self.start_state
        )
        renderer.render_q(q, print_value)


if __name__ == "__main__":
    env = MazeWorld()

    V = {}
    for state in env.states():
        V[state] = np.random.randn()
    env.render_v(V)

    Q = {}
    for state in env.states():
        for action in env.actions():
            Q[state, action] = np.random.randn()
    env.render_q(Q)
