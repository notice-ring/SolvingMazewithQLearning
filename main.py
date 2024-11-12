from gui.main_window import MainWindow
from common.mazeworld import MazeWorld
from q_learning.q_learning import QLearningAgent


def on_maze_made(data):
    print("Start")

    maze_world = MazeWorld(**data)
    maze_agent = QLearningAgent()

    episodes = 1000
    for episode in range(episodes):
        state = maze_world.reset()

        while True:
            action = maze_agent.get_action(state)
            next_state, reward, done = maze_world.step(action)

            maze_agent.update(state, action, reward, next_state, done)

            if done:
                break

            state = next_state

    maze_world.render_q(maze_agent.Q)


if __name__ == "__main__":
    MainWindow(title="Maze World", size=700, on_finish=on_maze_made).show()
